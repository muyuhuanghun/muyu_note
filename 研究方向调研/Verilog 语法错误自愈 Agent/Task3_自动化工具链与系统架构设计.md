# Task 3: 自动化工具链与系统架构设计（Architecture Design）

> **目标**：设计 Verilog 语法错误自适应修复 Agent 的完整系统架构，给出可直接进入工程实现阶段的蓝图。
> **原则**：所有代码和数据结构必须达到生产环境标准，零省略。

---

## 1. 系统总体架构

### 1.1 模块划分

整个修复 Agent 由 5 个核心模块组成，形成一个闭环反馈回路：

```
┌─────────────────────────────────────────────────────────────────┐
│                     Verilog Self-Healing Agent                  │
│                                                                 │
│  ┌──────────┐    ┌──────────────┐    ┌───────────────────────┐  │
│  │  Source   │───>│  Compiler    │───>│   Error Parser &      │  │
│  │  Manager  │    │  Bridge      │    │   Feedback Extractor  │  │
│  │          │    │ (iverilog)   │    │                       │  │
│  └──────────┘    └──────────────┘    └───────────┬───────────┘  │
│       ^                                          │              │
│       │                                          v              │
│  ┌────┴─────────┐    ┌──────────────┐    ┌───────────────────┐  │
│  │  Patch       │<───│  LLM Agent   │<───│  Context Builder  │  │
│  │  Applicator  │    │  Controller  │    │  (Prompt Assembler)│  │
│  └──────────────┘    └──────────────┘    └───────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Simulation Runner (vvp)                      │   │
│  │    编译通过后执行 testbench，验证功能正确性                │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

| 模块 | 职责 | 核心技术 |
|:---|:---|:---|
| Source Manager | 管理原始 Verilog 代码、生成临时工作副本 | `tempfile`, `pathlib` |
| Compiler Bridge | 异步调用 iverilog 编译，捕获 stderr/stdout | `asyncio.subprocess` |
| Error Parser & Feedback Extractor | 解析编译/仿真错误，结构化为 JSON | 正则表达式, AST 解析 |
| Context Builder | 将历史轮次、错误信息、原始代码组装为 LLM prompt | JSON Schema 校验 |
| LLM Agent Controller | 调用 LLM API 获取修复建议，控制迭代上限 | OpenAI/Anthropic SDK |
| Patch Applicator | 将 LLM 返回的修复代码应用到源文件 | diff-match-patch |
| Simulation Runner | 编译通过后运行 vvp testbench，验证功能 | `asyncio.subprocess` |

### 1.2 迭代状态机

Agent 的生命周期由一个有限状态机驱动：

```
INIT --> COMPILE --> {PASS | FAIL}
                       |       |
                       v       v
                    SIMULATE  PARSE_ERROR
                       |       |
                  {PASS|FAIL}  v
                   |    |   BUILD_CONTEXT
                   v    v       |
                 DONE  DONE   CALL_LLM
                                 |
                                 v
                            APPLY_PATCH
                                 |
                                 v
                              COMPILE  (loop)
```

**终止条件**（满足任一即停止）：
1. 编译通过 且 testbench 仿真通过 -> `STATUS_SUCCESS`
2. 达到最大迭代轮数 `MAX_ITERATIONS`（默认 10）-> `STATUS_MAX_ITER`
3. LLM 连续 3 轮返回完全相同的修复 -> `STATUS_CONVERGED`
4. 单次编译/仿真超时超过 `TIMEOUT_SECONDS`（默认 60s）-> `STATUS_TIMEOUT`

---

## 2. Compiler Bridge：subprocess 异步调用 iverilog/vvp 的完整伪代码流

### 2.1 设计决策

| 决策点 | 选择 | 理由 |
|:---|:---|:---|
| 同步 vs 异步 | `asyncio.create_subprocess_exec` | 需要设置超时、非阻塞读取 stderr/stdout |
| shell=True vs False | `False` | 安全性：避免 shell injection；iverilog 参数由程序构造 |
| 输出捕获方式 | `PIPE` 重定向 | 必须完整捕获 stderr 用于错误解析 |
| 临时文件策略 | `tempfile.TemporaryDirectory` | 每次迭代独立目录，避免文件残留和竞态 |
| 编译与仿真分离 | 两阶段独立调用 | iverilog 生成 `.vvp` 中间产物，vvp 单独执行仿真 |

### 2.2 完整伪代码

```python
import asyncio
import json
import re
import hashlib
import time
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional
from enum import Enum


# ==========================================
# 数据结构定义
# ==========================================

class AgentStatus(Enum):
    """Agent 终止状态"""
    SUCCESS = "success"
    COMPILE_FAIL = "compile_fail"
    SIM_FAIL = "simulation_fail"
    MAX_ITER = "max_iterations_reached"
    CONVERGED = "converged_no_progress"
    TIMEOUT = "timeout"
    LLM_ERROR = "llm_api_error"


@dataclass
class CompileResult:
    """单次编译结果"""
    success: bool
    return_code: int
    stdout: str
    stderr: str
    elapsed_seconds: float
    output_vvp_path: Optional[str] = None


@dataclass
class SimulationResult:
    """单次仿真结果"""
    success: bool
    return_code: int
    stdout: str
    stderr: str
    elapsed_seconds: float
    testbench_passed: bool = False
    assertion_failures: list = field(default_factory=list)


@dataclass
class IterationRecord:
    """单轮迭代的完整记录"""
    iteration_index: int
    timestamp: str
    verilog_source_hash: str
    verilog_source_code: str
    compile_result: Optional[CompileResult] = None
    simulation_result: Optional[SimulationResult] = None
    llm_prompt_sent: Optional[str] = None
    llm_response_raw: Optional[str] = None
    patch_applied: bool = False
    error_category: Optional[str] = None


# ==========================================
# Compiler Bridge: iverilog 异步编译
# ==========================================

class IverilogCompilerBridge:
    """
    异步调用 Icarus Verilog (iverilog) 进行编译。

    iverilog 命令行格式:
        iverilog -o <output.vvp> -g2012 <source.v> <testbench.v>

    关键参数说明:
        -o          指定输出文件（.vvp 中间格式）
        -g2012      启用 SystemVerilog 2012 特性支持
        -Wall       开启所有警告（警告也会被反馈给 LLM）
        -t null     仅做语法检查，不生成输出（快速验证模式）
    """

    def __init__(self, iverilog_path: str = "iverilog", default_timeout: int = 30):
        self.iverilog_path = iverilog_path
        self.default_timeout = default_timeout

    async def compile(
        self,
        source_files: list[str],
        output_path: str,
        include_dirs: list[str] = None,
        defines: dict[str, str] = None,
        timeout: int = None
    ) -> CompileResult:
        """
        异步编译 Verilog 源文件。

        Args:
            source_files: Verilog 源文件路径列表（含 testbench）
            output_path: 输出 .vvp 文件路径
            include_dirs: 额外的 include 搜索目录
            defines: 预定义宏，如 {"DATA_WIDTH": "16"}
            timeout: 超时秒数，None 则使用默认值

        Returns:
            CompileResult 数据类实例
        """
        timeout = timeout or self.default_timeout

        # 构造命令行参数
        cmd = [
            self.iverilog_path,
            "-o", output_path,
            "-g2012",
            "-Wall",
        ]

        # 添加 include 目录
        if include_dirs:
            for inc_dir in include_dirs:
                cmd.extend(["-I", inc_dir])

        # 添加预定义宏
        if defines:
            for macro_name, macro_value in defines.items():
                cmd.extend(["-D", f"{macro_name}={macro_value}"])

        # 添加源文件（必须在所有选项之后）
        cmd.extend(source_files)

        start_time = time.monotonic()

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            try:
                stdout_bytes, stderr_bytes = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                elapsed = time.monotonic() - start_time
                return CompileResult(
                    success=False,
                    return_code=-1,
                    stdout="",
                    stderr=f"[TIMEOUT] iverilog compilation exceeded {timeout}s limit",
                    elapsed_seconds=elapsed,
                )

            elapsed = time.monotonic() - start_time
            stdout_text = stdout_bytes.decode("utf-8", errors="replace")
            stderr_text = stderr_bytes.decode("utf-8", errors="replace")

            return CompileResult(
                success=(process.returncode == 0),
                return_code=process.returncode,
                stdout=stdout_text,
                stderr=stderr_text,
                elapsed_seconds=elapsed,
                output_vvp_path=output_path if process.returncode == 0 else None,
            )

        except FileNotFoundError:
            elapsed = time.monotonic() - start_time
            return CompileResult(
                success=False,
                return_code=-2,
                stdout="",
                stderr=f"[ERROR] iverilog executable not found at: {self.iverilog_path}",
                elapsed_seconds=elapsed,
            )

    async def syntax_check_only(
        self,
        source_file: str,
        timeout: int = None
    ) -> CompileResult:
        """
        仅做语法检查，不生成输出文件。
        使用 -t null target 快速验证语法正确性。
        """
        timeout = timeout or self.default_timeout
        cmd = [
            self.iverilog_path,
            "-t", "null",
            "-g2012",
            "-Wall",
            source_file,
        ]

        start_time = time.monotonic()
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout_bytes, stderr_bytes = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
            elapsed = time.monotonic() - start_time

            return CompileResult(
                success=(process.returncode == 0),
                return_code=process.returncode,
                stdout=stdout_bytes.decode("utf-8", errors="replace"),
                stderr=stderr_bytes.decode("utf-8", errors="replace"),
                elapsed_seconds=elapsed,
            )
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            elapsed = time.monotonic() - start_time
            return CompileResult(
                success=False,
                return_code=-1,
                stdout="",
                stderr=f"[TIMEOUT] syntax check exceeded {timeout}s",
                elapsed_seconds=elapsed,
            )


# ==========================================
# Simulation Runner: vvp 异步仿真
# ==========================================

class VvpSimulationRunner:
    """
    异步调用 vvp 执行编译后的 .vvp 仿真文件。

    vvp 命令行格式:
        vvp <input.vvp> [+TESTCASE=<name>]

    仿真结果判定逻辑:
        - returncode == 0 且 stdout 含 "PASS" -> 通过
        - returncode != 0 或 stdout 含 "FAIL" / "ERROR" -> 失败
        - testbench 中通过 $display("PASS") 或 $finish 信号判定
    """

    # 从 testbench stdout 中匹配结果的正则模式
    PASS_PATTERN = re.compile(
        r"(?i)\b(PASS|ALL\s+TESTS?\s+PASSED|SUCCESS)\b"
    )
    FAIL_PATTERN = re.compile(
        r"(?i)\b(FAIL|FAILED|ERROR|ASSERTION\s+FAILURE)\b"
    )
    ASSERTION_PATTERN = re.compile(
        r"(?i)assert(?:ion)?\s+(?:fail|error).*?(?:line\s+(\d+))?",
        re.MULTILINE
    )

    def __init__(self, vvp_path: str = "vvp", default_timeout: int = 60):
        self.vvp_path = vvp_path
        self.default_timeout = default_timeout

    async def simulate(
        self,
        vvp_file: str,
        plusargs: dict[str, str] = None,
        timeout: int = None
    ) -> SimulationResult:
        """
        异步执行 vvp 仿真。

        Args:
            vvp_file: iverilog 编译生成的 .vvp 文件路径
            plusargs: 仿真 plusargs 参数，如 {"TESTCASE": "test_reset"}
            timeout: 超时秒数

        Returns:
            SimulationResult 数据类实例
        """
        timeout = timeout or self.default_timeout

        cmd = [self.vvp_path, vvp_file]

        # 添加 plusargs（$plusargs 在 testbench 中读取）
        if plusargs:
            for key, value in plusargs.items():
                cmd.append(f"+{key}={value}")

        start_time = time.monotonic()

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            try:
                stdout_bytes, stderr_bytes = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                elapsed = time.monotonic() - start_time
                return SimulationResult(
                    success=False,
                    return_code=-1,
                    stdout="",
                    stderr=f"[TIMEOUT] vvp simulation exceeded {timeout}s limit",
                    elapsed_seconds=elapsed,
                    testbench_passed=False,
                )

            elapsed = time.monotonic() - start_time
            stdout_text = stdout_bytes.decode("utf-8", errors="replace")
            stderr_text = stderr_bytes.decode("utf-8", errors="replace")

            # 判定仿真是否通过
            pass_match = self.PASS_PATTERN.search(stdout_text)
            fail_match = self.FAIL_PATTERN.search(stdout_text)

            testbench_passed = False
            if process.returncode == 0 and pass_match and not fail_match:
                testbench_passed = True

            # 提取 assertion 失败详情
            assertion_failures = []
            for match in self.ASSERTION_PATTERN.finditer(stderr_text):
                line_num = match.group(1) if match.group(1) else "unknown"
                assertion_failures.append({
                    "line": line_num,
                    "message": match.group(0).strip(),
                })

            return SimulationResult(
                success=(process.returncode == 0),
                return_code=process.returncode,
                stdout=stdout_text,
                stderr=stderr_text,
                elapsed_seconds=elapsed,
                testbench_passed=testbench_passed,
                assertion_failures=assertion_failures,
            )

        except FileNotFoundError:
            elapsed = time.monotonic() - start_time
            return SimulationResult(
                success=False,
                return_code=-2,
                stdout="",
                stderr=f"[ERROR] vvp executable not found at: {self.vvp_path}",
                elapsed_seconds=elapsed,
                testbench_passed=False,
            )
```

### 2.3 关键工程细节说明

**为什么选择 `asyncio.create_subprocess_exec` 而非 `subprocess.run`？**

在闭环 Agent 中，我们需要在等待编译/仿真的同时做其他工作（例如准备下一轮的 prompt、更新 Pareto 记录、写日志）。`asyncio` 的协程模型允许我们在 `await process.communicate()` 期间挂起当前任务，让事件循环处理其他 IO 操作。此外，`asyncio.wait_for` 提供了原生的超时控制，比 `subprocess.run(timeout=...)` 更优雅——超时时我们可以先 kill 进程再做清理，而不是直接抛异常。

**为什么编译和仿真必须分离为两个阶段？**

iverilog 的 `-o` 参数生成的是 `.vvp` 中间字节码文件，这是一个独立的编译产物。分离的好处有三：(1) 编译失败时不需要浪费时间运行仿真；(2) 同一个 `.vvp` 文件可以用不同的 plusargs 参数运行多次仿真（例如不同 test case）；(3) 编译阶段的 stderr 包含的是语法/语义错误，仿真阶段的 stderr 包含的是运行时错误，两者的错误模式完全不同，需要不同的解析策略。

**Testbench 约定：如何让 Agent 自动判定仿真结果？**

Agent 无法理解波形或功能语义，因此必须通过 testbench 的文本输出来判定结果。我们约定以下规范：

```verilog
// testbench 必须在结尾输出 PASS 或 FAIL
initial begin
    // ... 测试逻辑 ...

    if (all_checks_passed) begin
        $display("[TB] ALL TESTS PASSED - PASS");
        $finish;
    end else begin
        $display("[TB] TEST FAILED - FAIL at check %0d", failed_check_id);
        $finish;
    end
end
```

这个约定使得 `VvpSimulationRunner` 只需通过正则匹配 stdout 中的 `PASS` / `FAIL` 关键字即可判定结果，无需理解具体的硬件功能。

---

## 3. Error Parser & Feedback Extractor

### 3.1 iverilog stderr 错误分类器

iverilog 的 stderr 输出具有高度结构化的格式，典型模式为：

```
source.v:42: error: Syntax error in assignment target.
source.v:55: warning: Implicit declaration of signal 'data_out'.
source.v:63: error: Unable to elaborate port connections.
```

每条错误都遵循 `<文件名>:<行号>: <级别>: <消息>` 的格式。我们利用这个规律构建分类器：

```python
class IverilogErrorParser:
    """
    解析 iverilog stderr 输出，提取结构化错误信息。

    iverilog 的错误输出格式:
        <filename>:<line>: <severity>: <message>
        <filename>:<line>:<column>: <severity>: <message>

    支持的 severity 级别:
        error   - 编译必须失败
        warning - 编译可继续但需要关注
        sorry   - iverilog 不支持的特性
        note    - 辅助信息
    """

    # 匹配 iverilog 错误/警告行的正则表达式
    # 支持两种格式：有列号和无列号
    ERROR_LINE_PATTERN = re.compile(
        r"^(?P<filename>.+?):(?P<line>\d+)(?::(?P<col>\d+))?:\s*"
        r"(?P<severity>error|warning|sorry|note):\s*"
        r"(?P<message>.+)$",
        re.MULTILINE
    )

    # 特定错误类型的细分模式
    ERROR_SUBCATEGORY_PATTERNS = {
        "syntax_error": re.compile(
            r"(?i)syntax\s+error|unexpected\s+token|parse\s+error"
        ),
        "undefined_signal": re.compile(
            r"(?i)undefined\s+(?:signal|name|identifier)|not\s+declared"
        ),
        "implicit_decl": re.compile(
            r"(?i)implicit\s+declaration"
        ),
        "port_mismatch": re.compile(
            r"(?i)port\s+(?:connection|mismatch|width)|unable\s+to\s+elaborate\s+port"
        ),
        "multi_driver": re.compile(
            r"(?i)multiple\s+(?:drivers?|driver)|procedural\s+and\s+continuous"
        ),
        "latch_inference": re.compile(
            r"(?i)latch|incomplete\s+(?:case|if)|missing\s+(?:else|default)"
        ),
        "width_mismatch": re.compile(
            r"(?i)(?:width|truncat|extend|bit\s+width)|\d+\s*(?:bits?|to)\s*\d+"
        ),
        "type_error": re.compile(
            r"(?i)type\s+mismatch|incompatible\s+type|cannot\s+assign"
        ),
        "module_not_found": re.compile(
            r"(?i)unknown\s+module|module\s+\S+\s+not\s+found|cannot\s+find\s+module"
        ),
        "always_comb_blocking": re.compile(
            r"(?i)blocking\s+assignment\s+in\s+(?:combinational|always_comb)"
        ),
    }

    def parse(self, stderr_text: str, source_filename: str = None) -> dict:
        """
        解析 iverilog stderr，返回结构化错误报告。

        Args:
            stderr_text: iverilog 的 stderr 输出
            source_filename: 源文件名（用于过滤和匹配）

        Returns:
            结构化错误报告字典
        """
        errors = []
        warnings = []

        for match in self.ERROR_LINE_PATTERN.finditer(stderr_text):
            entry = {
                "file": match.group("filename"),
                "line": int(match.group("line")),
                "column": int(match.group("col")) if match.group("col") else None,
                "severity": match.group("severity"),
                "message": match.group("message").strip(),
                "subcategory": self._classify_error(match.group("message")),
            }

            if entry["severity"] == "error":
                errors.append(entry)
            elif entry["severity"] == "warning":
                warnings.append(entry)

        # 按行号排序，便于 LLM 定位
        errors.sort(key=lambda e: e["line"])
        warnings.sort(key=lambda w: w["line"])

        # 提取错误上下文（出错行附近的源代码行号）
        error_lines = sorted(set(e["line"] for e in errors))

        return {
            "total_errors": len(errors),
            "total_warnings": len(warnings),
            "errors": errors,
            "warnings": warnings,
            "error_line_numbers": error_lines,
            "primary_error_category": self._determine_primary_category(errors),
            "raw_stderr": stderr_text,
        }

    def _classify_error(self, message: str) -> str:
        """将错误消息归类到细分类型"""
        for category, pattern in self.ERROR_SUBCATEGORY_PATTERNS.items():
            if pattern.search(message):
                return category
        return "unknown"

    def _determine_primary_category(self, errors: list) -> str:
        """
        确定本轮的主要错误类别。
        选择策略：出现频率最高的 subcategory，用于指导 LLM 的修复方向。
        """
        if not errors:
            return "none"

        category_counts = {}
        for error in errors:
            cat = error["subcategory"]
            category_counts[cat] = category_counts.get(cat, 0) + 1

        return max(category_counts, key=category_counts.get)
```

### 3.2 vvp 仿真错误解析器

```python
class VvpErrorParser:
    """
    解析 vvp 仿真运行时的 stderr 和 stdout 输出。

    vvp 的错误类型与编译错误完全不同，主要包括:
        - $finish 信号（正常结束）
        - $fatal 信号（致命错误）
        - Assertion failure（断言失败）
        - Infinite loop detection（死循环）
        - Segfault / memory error（vvp 内部错误）
    """

    FINISH_PATTERN = re.compile(r"\$finish\s+at\s+time\s+(\d+)")
    FATAL_PATTERN = re.compile(r"\$fatal\s+(\d+)?\s*,?\s*(.*)")
    ASSERTION_PATTERN = re.compile(
        r"(?i)assert(?:ion)?\s+failure.*?(?:at\s+)?(\S+\.v)?(?:\s*:\s*(\d+))?",
        re.MULTILINE
    )

    def parse(self, stdout_text: str, stderr_text: str) -> dict:
        """解析仿真输出，返回结构化报告"""
        runtime_errors = []

        # 检查 $fatal
        for match in self.FATAL_PATTERN.finditer(stdout_text):
            runtime_errors.append({
                "type": "fatal",
                "finish_code": int(match.group(1)) if match.group(1) else 1,
                "message": match.group(2).strip() if match.group(2) else "$fatal triggered",
            })

        # 检查 assertion failure
        for match in self.ASSERTION_PATTERN.finditer(stderr_text):
            runtime_errors.append({
                "type": "assertion_failure",
                "file": match.group(1) if match.group(1) else "unknown",
                "line": int(match.group(2)) if match.group(2) else -1,
                "message": match.group(0).strip(),
            })

        # 检查 stderr 中的运行时错误
        if stderr_text.strip():
            runtime_errors.append({
                "type": "runtime_error",
                "file": "N/A",
                "line": -1,
                "message": stderr_text.strip()[:500],
            })

        return {
            "runtime_error_count": len(runtime_errors),
            "runtime_errors": runtime_errors,
            "raw_stdout": stdout_text,
            "raw_stderr": stderr_text,
        }
```

---

## 4. Context Builder 与完整 JSON 数据交互流

这是整个架构中最关键的部分——如何将所有信息打包为一个结构化的 JSON，投喂给 LLM 进行修复。

### 4.1 JSON Schema 定义

以下是一个完整的 LLM 输入 JSON 示例，对应第一轮迭代（编译失败场景）。这个 JSON 同时也是 `ContextBuilder` 模块的输出格式：

```json
{
  "agent_metadata": {
    "agent_id": "verilog-heal-fir-001",
    "experiment_tag": "exp_baseline_20260614",
    "current_iteration": 3,
    "max_iterations": 10,
    "total_elapsed_seconds": 47.3,
    "status": "compile_fail"
  },
  "task_description": {
    "instruction": "Fix the Verilog syntax/semantic errors in the provided source code so that it compiles cleanly with iverilog -g2012 and passes the given testbench.",
    "target_simulator": "iverilog",
    "verilog_standard": "IEEE 1800-2017 (SystemVerilog subset supported by iverilog)",
    "constraints": [
      "Do NOT change the module port interface (module name, port names, port directions)",
      "Do NOT change the functional intent of the design",
      "Prefer minimal changes: fix only what is broken",
      "If a latch is inferred, add explicit default assignments instead of removing the always block"
    ]
  },
  "source_code": {
    "design_unit": {
      "filename": "fir_filter.v",
      "content": "module fir_filter #(\n  parameter DATA_WIDTH = 16,\n  parameter TAP_COUNT  = 8\n) (\n  input  wire                    clk,\n  input  wire                    rst_n,\n  input  wire signed [DATA_WIDTH-1:0] data_in,\n  output reg  signed [DATA_WIDTH-1:0] data_out\n);\n\n  reg signed [DATA_WIDTH-1:0] shift_reg [0:TAP_COUNT-1];\n  reg signed [DATA_WIDTH-1:0] coeff      [0:TAP_COUNT-1];\n  integer i;\n  reg signed [2*DATA_WIDTH-1:0] acc;\n\n  // 初始化系数\n  initial begin\n    coeff[0] = 16'h0002;\n    coeff[1] = 16'h0005;\n    coeff[2] = 16'h000A;\n    coeff[3] = 16'h000F;\n    coeff[4] = 16'h000F;\n    coeff[5] = 16'h000A;\n    coeff[6] = 16'h0005;\n    coeff[7] = 16'h0002;\n  end\n\n  always @(posedge clk or negedge rst_n) begin\n    if (!rst_n) begin\n      for (i = 0; i < TAP_COUNT; i = i + 1)\n        shift_reg[i] <= 0;\n      data_out <= 0;\n    end else begin\n      // 移位寄存器更新\n      shift_reg[0] <= data_in;\n      for (i = 1; i < TAP_COUNT; i = i + 1)\n        shift_reg[i] <= shift_reg[i-1];\n\n      // MAC 累加\n      acc = 0;  // BUG: 阻塞赋值在时序逻辑中\n      for (i = 0; i < TAP_COUNT; i = i + 1)\n        acc = acc + shift_reg[i] * coeff[i];  // BUG: 位宽截断\n      data_out <= acc[DATA_WIDTH-1:0];\n    end\n  end\nendmodule",
      "line_count": 45,
      "hash_sha256": "a3f2b8c1d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1"
    },
    "testbench": {
      "filename": "fir_filter_tb.v",
      "content": "module fir_filter_tb;\n  parameter DATA_WIDTH = 16;\n  reg                    clk;\n  reg                    rst_n;\n  reg  signed [DATA_WIDTH-1:0] data_in;\n  wire signed [DATA_WIDTH-1:0] data_out;\n\n  fir_filter #(\n    .DATA_WIDTH(DATA_WIDTH),\n    .TAP_COUNT(8)\n  ) uut (\n    .clk(clk),\n    .rst_n(rst_n),\n    .data_in(data_in),\n    .data_out(data_out)\n  );\n\n  initial clk = 0;\n  always #5 clk = ~clk;\n\n  integer pass_count;\n  integer fail_count;\n\n  initial begin\n    pass_count = 0;\n    fail_count = 0;\n    rst_n = 0;\n    data_in = 0;\n    #20;\n    rst_n = 1;\n    #10;\n\n    // Test 1: impulse response\n    data_in = 16'sd100;\n    #10;\n    data_in = 0;\n    #(10 * 8);  // wait for pipeline flush\n\n    if (data_out !== 16'sbx) begin\n      pass_count = pass_count + 1;\n    end else begin\n      fail_count = fail_count + 1;\n      $display(\"[FAIL] Test 1: output is X after impulse\");\n    end\n\n    if (fail_count == 0)\n      $display(\"[TB] ALL TESTS PASSED - PASS\");\n    else\n      $display(\"[TB] %0d TESTS FAILED - FAIL\", fail_count);\n    $finish;\n  end\nendmodule",
      "line_count": 52,
      "hash_sha256": "b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3"
    }
  },
  "compilation_feedback": {
    "attempt_number": 3,
    "iverilog_command": "iverilog -o fir_filter.vvp -g2012 -Wall fir_filter.v fir_filter_tb.v",
    "return_code": 2,
    "success": false,
    "elapsed_seconds": 0.34,
    "parsed_errors": {
      "total_errors": 2,
      "total_warnings": 1,
      "primary_error_category": "width_mismatch",
      "errors": [
        {
          "file": "fir_filter.v",
          "line": 35,
          "column": 7,
          "severity": "error",
          "message": "Assignment to 'acc' from non-blocking assignment in sequential block. Use blocking assignment (=) only in combinational always blocks.",
          "subcategory": "always_comb_blocking",
          "context_source_lines": {
            "33": "      // MAC 累加",
            "34": "      acc = 0;",
            "35": "      for (i = 0; i < TAP_COUNT; i = i + 1)",
            "36": "        acc = acc + shift_reg[i] * coeff[i];",
            "37": "      data_out <= acc[DATA_WIDTH-1:0];"
          }
        },
        {
          "file": "fir_filter.v",
          "line": 36,
          "column": 41,
          "severity": "error",
          "message": "Width mismatch: expression 'shift_reg[i] * coeff[i]' is 32 bits, but target 'acc' requires explicit truncation or extension.",
          "subcategory": "width_mismatch",
          "context_source_lines": {
            "34": "      acc = 0;",
            "35": "      for (i = 0; i < TAP_COUNT; i = i + 1)",
            "36": "        acc = acc + shift_reg[i] * coeff[i];",
            "37": "      data_out <= acc[DATA_WIDTH-1:0];"
          }
        }
      ],
      "warnings": [
        {
          "file": "fir_filter.v",
          "line": 14,
          "column": null,
          "severity": "warning",
          "message": "Implicit declaration of variable 'i' in for-loop. Consider declaring it explicitly.",
          "subcategory": "implicit_decl"
        }
      ],
      "error_line_numbers": [35, 36],
      "raw_stderr": "fir_filter.v:35: error: Assignment to 'acc' requires blocking (=) in combinational context.\nfir_filter.v:36: error: Width mismatch: 32-bit expression assigned to 2*DATA_WIDTH-bit target.\nfir_filter.v:14: warning: Implicit loop variable 'i'.\n"
    }
  },
  "simulation_feedback": {
    "attempt_number": null,
    "vvp_command": null,
    "return_code": null,
    "success": null,
    "testbench_passed": null,
    "runtime_errors": [],
    "raw_stdout": null,
    "raw_stderr": null,
    "note": "Simulation was not attempted because compilation failed."
  },
  "iteration_history": [
    {
      "iteration_index": 1,
      "status": "compile_fail",
      "error_category": "syntax_error",
      "error_count": 5,
      "summary": "Missing semicolons on lines 20, 21; undeclared variable 'temp_reg' on line 28.",
      "source_hash": "f1e2d3c4b5a6f7e8d9c0b1a2f3e4d5c6b7a8f9e0d1c2b3a4f5e6d7c8b9a0f1e2"
    },
    {
      "iteration_index": 2,
      "status": "compile_fail",
      "error_category": "latch_inference",
      "error_count": 3,
      "summary": "Fixed syntax errors but introduced incomplete case statement causing latch inference on line 30.",
      "source_hash": "c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3"
    }
  ],
  "diagnosis_hints": {
    "likely_root_cause": "Mixing blocking and non-blocking assignments in the same sequential always block. The 'acc' accumulator should either be declared as combinational (use always @* with blocking) or converted to non-blocking assignment pattern.",
    "suggested_fix_strategy": "Option A: Extract the MAC computation into a separate always @* combinational block using blocking assignments, then assign the result with <= in the sequential block. Option B: Convert acc to use <= throughout and adjust the pipeline latency accordingly.",
    "resource_constraint": "This is a pipelined FIR filter. Ensure the fix maintains the single-cycle MAC throughput if possible."
  },
  "llm_output_contract": {
    "expected_format": "You must return the COMPLETE corrected Verilog source code for the design unit (fir_filter.v). Do NOT return partial code, diffs, or explanations outside the code block.",
    "output_template": "```verilog\n<complete corrected fir_filter.v here>\n```",
    "additional_instructions": [
      "Wrap the code in a single markdown code block with language tag 'verilog'.",
      "Include all module declarations, parameters, port lists, and endmodule.",
      "If you need to change the testbench as well, provide it in a separate code block tagged 'verilog-tb'.",
      "After the code block, provide a one-line summary of changes made, prefixed with 'CHANGES:'."
    ]
  }
}
```

### 4.2 JSON Schema 的设计哲学

上述 JSON 并非随意堆砌字段，每个 section 的存在都有明确的工程目的：

| Section | 为什么存在 | 如果缺失会导致什么问题 |
|:---|:---|:---|
| `agent_metadata` | 让 LLM 知道当前是第几轮，还剩多少轮预算 | LLM 可能在第 1 轮就做出过于激进的修改，浪费迭代预算 |
| `task_description.constraints` | 硬约束端口不变，避免 LLM "修好语法但改了接口" | 修复后的代码虽然编译通过，但与 testbench 的端口连接又会失败 |
| `source_code` | 提供完整的源代码（含 testbench），而非片段 | LLM 缺乏上下文，可能做出局部正确但全局错误的修复 |
| `compilation_feedback.parsed_errors` | 结构化错误而非原始 stderr | LLM 需要在大量文本中自己提取行号和错误类型，增加 token 消耗和出错概率 |
| `compilation_feedback.context_source_lines` | 出错行周围的 ±2 行代码 | LLM 可能需要看到上下文才能理解错误的根因（例如某个变量在上面几行被错误声明） |
| `iteration_history` | 避免 LLM 重复前几轮已经尝试过的失败修复 | LLM 可能陷入循环，反复提出相同的修复方案 |
| `diagnosis_hints` | 前几轮的错误分析积累 | 纯靠 LLM 自行分析可能导致每轮都从零开始，收敛缓慢 |
| `llm_output_contract` | 约束 LLM 输出格式，便于程序化解析 | LLM 返回自然语言解释而非代码，Agent 无法自动应用修复 |

### 4.3 Context Builder 实现

```python
import json
import hashlib
from datetime import datetime, timezone
from typing import Optional


class ContextBuilder:
    """
    将 Agent 的内部状态组装为 LLM 输入 JSON。

    核心职责:
    1. 管理迭代历史记录
    2. 提取源代码上下文窗口（出错行 ±N 行）
    3. 生成 diagnosis hints（跨轮次错误模式分析）
    4. 控制 JSON 总 token 量（避免超出 LLM context window）
    """

    # 出错行周围提取的上下文行数
    CONTEXT_WINDOW = 3

    # JSON 各部分的 token 预算上限（近似值，1 token ≈ 4 字符英文 / 1.5 字符中文）
    MAX_SOURCE_TOKENS = 8000
    MAX_HISTORY_TOKENS = 2000
    MAX_RAW_STDERR_TOKENS = 2000

    def __init__(
        self,
        agent_id: str,
        max_iterations: int = 10,
        experiment_tag: str = "default",
    ):
        self.agent_id = agent_id
        self.max_iterations = max_iterations
        self.experiment_tag = experiment_tag
        self.iteration_history: list[dict] = []
        self.start_time = time.monotonic()

    def build_context(
        self,
        current_iteration: int,
        design_filename: str,
        design_source: str,
        tb_filename: str,
        tb_source: str,
        compile_result: Optional[CompileResult] = None,
        simulation_result: Optional[SimulationResult] = None,
        error_report: Optional[dict] = None,
        diagnosis_hints: Optional[dict] = None,
    ) -> dict:
        """
        构建完整的 LLM 上下文 JSON。

        这是 ContextBuilder 的核心方法，每次迭代调用一次。
        """
        # 计算源代码 hash 用于去重检测
        source_hash = hashlib.sha256(design_source.encode("utf-8")).hexdigest()

        # 确定当前状态
        if compile_result and not compile_result.success:
            status = "compile_fail"
        elif simulation_result and not simulation_result.testbench_passed:
            status = "simulation_fail"
        elif compile_result and compile_result.success and (
            simulation_result is None or simulation_result.testbench_passed
        ):
            status = "success"
        else:
            status = "unknown"

        # 构建编译反馈 section
        compilation_feedback = self._build_compile_feedback(
            current_iteration, compile_result, error_report, design_source
        )

        # 构建仿真反馈 section
        simulation_feedback = self._build_simulation_feedback(
            simulation_result
        )

        # 构建最终 JSON
        context = {
            "agent_metadata": {
                "agent_id": self.agent_id,
                "experiment_tag": self.experiment_tag,
                "current_iteration": current_iteration,
                "max_iterations": self.max_iterations,
                "total_elapsed_seconds": round(
                    time.monotonic() - self.start_time, 2
                ),
                "status": status,
            },
            "task_description": {
                "instruction": (
                    "Fix the Verilog syntax/semantic errors in the provided source "
                    "code so that it compiles cleanly with iverilog -g2012 and "
                    "passes the given testbench."
                ),
                "target_simulator": "iverilog",
                "verilog_standard": "IEEE 1800-2017 (SystemVerilog subset supported by iverilog)",
                "constraints": [
                    "Do NOT change the module port interface (module name, port names, port directions)",
                    "Do NOT change the functional intent of the design",
                    "Prefer minimal changes: fix only what is broken",
                    "If a latch is inferred, add explicit default assignments instead of removing the always block",
                ],
            },
            "source_code": {
                "design_unit": {
                    "filename": design_filename,
                    "content": design_source,
                    "line_count": design_source.count("\n") + 1,
                    "hash_sha256": source_hash,
                },
                "testbench": {
                    "filename": tb_filename,
                    "content": tb_source,
                    "line_count": tb_source.count("\n") + 1,
                    "hash_sha256": hashlib.sha256(
                        tb_source.encode("utf-8")
                    ).hexdigest(),
                },
            },
            "compilation_feedback": compilation_feedback,
            "simulation_feedback": simulation_feedback,
            "iteration_history": self._truncate_history(
                self.iteration_history
            ),
            "diagnosis_hints": diagnosis_hints or {
                "likely_root_cause": "Unknown - first iteration or no prior analysis available.",
                "suggested_fix_strategy": "Analyze the errors from top to bottom. Fix syntax errors first, then semantic errors.",
                "resource_constraint": None,
            },
            "llm_output_contract": {
                "expected_format": (
                    "You must return the COMPLETE corrected Verilog source code "
                    "for the design unit. Do NOT return partial code, diffs, or "
                    "explanations outside the code block."
                ),
                "output_template": f"```verilog\n<complete corrected {design_filename} here>\n```",
                "additional_instructions": [
                    "Wrap the code in a single markdown code block with language tag 'verilog'.",
                    "Include all module declarations, parameters, port lists, and endmodule.",
                    "If you need to change the testbench as well, provide it in a separate code block tagged 'verilog-tb'.",
                    "After the code block, provide a one-line summary of changes made, prefixed with 'CHANGES:'.",
                ],
            },
        }

        # 记录到历史
        self.iteration_history.append({
            "iteration_index": current_iteration,
            "status": status,
            "error_category": (
                error_report.get("primary_error_category", "unknown")
                if error_report
                else "unknown"
            ),
            "error_count": (
                error_report.get("total_errors", 0) if error_report else 0
            ),
            "summary": self._generate_iteration_summary(
                compile_result, simulation_result, error_report
            ),
            "source_hash": source_hash,
        })

        return context

    def _build_compile_feedback(
        self,
        iteration: int,
        compile_result: Optional[CompileResult],
        error_report: Optional[dict],
        source_code: str,
    ) -> dict:
        """构建编译反馈 section，包含上下文行窗口"""
        if compile_result is None:
            return {
                "attempt_number": None,
                "iverilog_command": None,
                "return_code": None,
                "success": None,
                "elapsed_seconds": None,
                "parsed_errors": None,
                "note": "No compilation attempted yet.",
            }

        # 为每个 error 附加上下文行
        enriched_errors = []
        if error_report and "errors" in error_report:
            source_lines = source_code.split("\n")
            for error in error_report["errors"]:
                enriched_error = dict(error)
                enriched_error["context_source_lines"] = (
                    self._extract_context_window(
                        source_lines, error["line"]
                    )
                )
                enriched_errors.append(enriched_error)

        enriched_warnings = []
        if error_report and "warnings" in error_report:
            source_lines = source_code.split("\n")
            for warning in error_report["warnings"]:
                enriched_warning = dict(warning)
                enriched_warning["context_source_lines"] = (
                    self._extract_context_window(
                        source_lines, warning["line"]
                    )
                )
                enriched_warnings.append(enriched_warning)

        return {
            "attempt_number": iteration,
            "iverilog_command": (
                f"iverilog -o <output>.vvp -g2012 -Wall "
                f"<design>.v <testbench>.v"
            ),
            "return_code": compile_result.return_code,
            "success": compile_result.success,
            "elapsed_seconds": round(compile_result.elapsed_seconds, 3),
            "parsed_errors": {
                "total_errors": (
                    error_report.get("total_errors", 0) if error_report else 0
                ),
                "total_warnings": (
                    error_report.get("total_warnings", 0) if error_report else 0
                ),
                "primary_error_category": (
                    error_report.get("primary_error_category", "unknown")
                    if error_report
                    else "unknown"
                ),
                "errors": enriched_errors,
                "warnings": enriched_warnings,
                "error_line_numbers": (
                    error_report.get("error_line_numbers", [])
                    if error_report
                    else []
                ),
                "raw_stderr": self._truncate_text(
                    compile_result.stderr, self.MAX_RAW_STDERR_TOKENS
                ),
            },
        }

    def _build_simulation_feedback(
        self, sim_result: Optional[SimulationResult]
    ) -> dict:
        """构建仿真反馈 section"""
        if sim_result is None:
            return {
                "attempt_number": None,
                "vvp_command": None,
                "return_code": None,
                "success": None,
                "testbench_passed": None,
                "runtime_errors": [],
                "raw_stdout": None,
                "raw_stderr": None,
                "note": "Simulation was not attempted because compilation failed.",
            }

        return {
            "attempt_number": 1,
            "vvp_command": "vvp <output>.vvp",
            "return_code": sim_result.return_code,
            "success": sim_result.success,
            "testbench_passed": sim_result.testbench_passed,
            "runtime_errors": sim_result.assertion_failures,
            "raw_stdout": self._truncate_text(sim_result.stdout, 1000),
            "raw_stderr": self._truncate_text(sim_result.stderr, 1000),
        }

    def _extract_context_window(
        self, source_lines: list[str], error_line: int, window: int = None
    ) -> dict:
        """
        提取出错行周围的 ±window 行代码。
        行号从 1 开始（与 iverilog 输出一致），列表索引从 0 开始。
        """
        window = window or self.CONTEXT_WINDOW
        start = max(0, error_line - 1 - window)
        end = min(len(source_lines), error_line + window)

        context = {}
        for idx in range(start, end):
            context[str(idx + 1)] = source_lines[idx]
        return context

    def _truncate_history(self, history: list[dict]) -> list[dict]:
        """
        截断迭代历史，保留最近的记录以控制 token 量。
        策略：保留前 2 轮 + 最近 3 轮，中间的只保留摘要。
        """
        if len(history) <= 5:
            return history

        preserved = history[:2]
        preserved.append({
            "iteration_index": "...",
            "status": "omitted_for_brevity",
            "summary": f"({len(history) - 5} iterations omitted)",
        })
        preserved.extend(history[-3:])
        return preserved

    def _truncate_text(self, text: str, max_tokens: int) -> str:
        """截断文本到近似 token 上限"""
        max_chars = max_tokens * 4  # 粗略估计
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "\n... [TRUNCATED]"

    def _generate_iteration_summary(
        self,
        compile_result: Optional[CompileResult],
        simulation_result: Optional[SimulationResult],
        error_report: Optional[dict],
    ) -> str:
        """生成人类可读的单轮迭代摘要"""
        if compile_result and not compile_result.success:
            error_count = (
                error_report.get("total_errors", 0) if error_report else 0
            )
            category = (
                error_report.get("primary_error_category", "unknown")
                if error_report
                else "unknown"
            )
            return f"Compilation failed with {error_count} error(s). Primary category: {category}."

        if simulation_result and not simulation_result.testbench_passed:
            return "Compilation passed but testbench simulation failed."

        if compile_result and compile_result.success:
            if simulation_result is None:
                return "Compilation passed. Simulation not yet attempted."
            if simulation_result.testbench_passed:
                return "Compilation and simulation both passed."

        return "Status unknown."
```

---

## 5. LLM Agent Controller 与主循环

将所有模块组装为完整的闭环 Agent：

```python
import re
import json


class LLMAgentController:
    """
    自适应修复 Agent 主控制器。

    驱动整个 LLM -> Compile -> Parse -> Feedback -> LLM 闭环。
    """

    # 从 LLM 响应中提取 Verilog 代码块的正则
    VERILOG_BLOCK_PATTERN = re.compile(
        r"```verilog\s*\n(.*?)```",
        re.DOTALL
    )
    VERILOG_TB_BLOCK_PATTERN = re.compile(
        r"```verilog-tb\s*\n(.*?)```",
        re.DOTALL
    )
    CHANGES_SUMMARY_PATTERN = re.compile(
        r"^CHANGES:\s*(.+)$",
        re.MULTILINE
    )

    def __init__(
        self,
        compiler: IverilogCompilerBridge,
        simulator: VvpSimulationRunner,
        error_parser: IverilogErrorParser,
        sim_error_parser: VvpErrorParser,
        context_builder: ContextBuilder,
        llm_client=None,
        max_iterations: int = 10,
        convergence_window: int = 3,
    ):
        self.compiler = compiler
        self.simulator = simulator
        self.error_parser = error_parser
        self.sim_error_parser = sim_error_parser
        self.context_builder = context_builder
        self.llm_client = llm_client
        self.max_iterations = max_iterations
        self.convergence_window = convergence_window

    async def run(
        self,
        design_filename: str,
        design_source: str,
        tb_filename: str,
        tb_source: str,
        work_dir: str,
    ) -> dict:
        """
        执行完整的修复闭环。

        Args:
            design_filename: 设计文件名（如 "fir_filter.v"）
            design_source: 原始含 bug 的 Verilog 源代码
            tb_filename: testbench 文件名
            tb_source: testbench 源代码
            work_dir: 工作目录路径

        Returns:
            最终结果字典，包含修复后的代码和迭代日志
        """
        import tempfile
        from pathlib import Path

        current_source = design_source
        recent_source_hashes = []

        for iteration in range(1, self.max_iterations + 1):
            iteration_dir = Path(work_dir) / f"iter_{iteration:03d}"
            iteration_dir.mkdir(parents=True, exist_ok=True)

            # 写入当前版本的源文件
            design_path = iteration_dir / design_filename
            tb_path = iteration_dir / tb_filename
            design_path.write_text(current_source, encoding="utf-8")
            tb_path.write_text(tb_source, encoding="utf-8")

            vvp_path = str(iteration_dir / "output.vvp")

            # ---- 阶段 1: 编译 ----
            compile_result = await self.compiler.compile(
                source_files=[str(design_path), str(tb_path)],
                output_path=vvp_path,
            )

            # ---- 阶段 2: 解析编译错误 ----
            error_report = None
            if not compile_result.success:
                error_report = self.error_parser.parse(
                    compile_result.stderr, design_filename
                )

            # ---- 阶段 3: 仿真（仅编译通过时） ----
            sim_result = None
            if compile_result.success:
                sim_result = await self.simulator.simulate(vvp_path)

                if not sim_result.testbench_passed:
                    sim_error_report = self.sim_error_parser.parse(
                        sim_result.stdout, sim_result.stderr
                    )
                    # 将仿真错误合并到 error_report
                    if error_report is None:
                        error_report = {
                            "total_errors": sim_error_report["runtime_error_count"],
                            "total_warnings": 0,
                            "errors": [
                                {
                                    "file": design_filename,
                                    "line": -1,
                                    "column": None,
                                    "severity": "error",
                                    "message": err["message"],
                                    "subcategory": err["type"],
                                }
                                for err in sim_error_report["runtime_errors"]
                            ],
                            "warnings": [],
                            "error_line_numbers": [],
                            "primary_error_category": "simulation_failure",
                        }

            # ---- 阶段 4: 检查终止条件 ----
            if compile_result.success and (
                sim_result is None or sim_result.testbench_passed
            ):
                return {
                    "status": AgentStatus.SUCCESS.value,
                    "final_source": current_source,
                    "total_iterations": iteration,
                    "history": self.context_builder.iteration_history,
                }

            # ---- 阶段 5: 构建 LLM 上下文 ----
            context = self.context_builder.build_context(
                current_iteration=iteration,
                design_filename=design_filename,
                design_source=current_source,
                tb_filename=tb_filename,
                tb_source=tb_source,
                compile_result=compile_result,
                simulation_result=sim_result,
                error_report=error_report,
            )

            # ---- 阶段 6: 调用 LLM ----
            llm_response = await self._call_llm(context)

            # ---- 阶段 7: 提取修复代码 ----
            patched_source = self._extract_verilog_code(
                llm_response, design_filename
            )

            if patched_source is None:
                # LLM 未能返回有效代码，重试
                continue

            # ---- 阶段 8: 收敛检测 ----
            patch_hash = hashlib.sha256(
                patched_source.encode("utf-8")
            ).hexdigest()
            recent_source_hashes.append(patch_hash)

            if len(recent_source_hashes) >= self.convergence_window:
                if len(set(recent_source_hashes[-self.convergence_window:])) == 1:
                    return {
                        "status": AgentStatus.CONVERGED.value,
                        "final_source": current_source,
                        "total_iterations": iteration,
                        "history": self.context_builder.iteration_history,
                    }

            current_source = patched_source

        # 达到最大迭代次数
        return {
            "status": AgentStatus.MAX_ITER.value,
            "final_source": current_source,
            "total_iterations": self.max_iterations,
            "history": self.context_builder.iteration_history,
        }

    async def _call_llm(self, context: dict) -> str:
        """
        调用 LLM API，返回原始响应文本。

        实际实现中需要根据使用的 API 进行适配:
        - OpenAI: openai.ChatCompletion.create(...)
        - Anthropic: anthropic.Anthropic().messages.create(...)
        - 本地模型: requests.post("http://localhost:8080/v1/chat/completions", ...)
        """
        prompt_text = json.dumps(context, ensure_ascii=False, indent=2)

        # 此处为接口占位，实际实现需替换为具体 SDK 调用
        response = await self.llm_client.chat(
            system_prompt=(
                "You are an expert Verilog debugging agent. "
                "You receive a buggy Verilog module, its testbench, "
                "and structured error reports from iverilog/vvp. "
                "Your task is to return the COMPLETE corrected Verilog "
                "source code. Output ONLY the code in a markdown code block."
            ),
            user_message=prompt_text,
        )

        return response

    def _extract_verilog_code(
        self, llm_response: str, expected_filename: str
    ) -> Optional[str]:
        """
        从 LLM 响应中提取 Verilog 代码。

        解析策略（按优先级）:
        1. 查找 ```verilog ... ``` 代码块
        2. 查找 ``` ... ``` 通用代码块（fallback）
        3. 如果整个响应看起来就是纯代码（没有 markdown 标记），直接使用

        返回 None 表示提取失败。
        """
        # 策略 1: 精确匹配 verilog 代码块
        match = self.VERILOG_BLOCK_PATTERN.search(llm_response)
        if match:
            code = match.group(1).strip()
            if self._validate_verilog_skeleton(code):
                return code

        # 策略 2: 通用代码块 fallback
        generic_block_pattern = re.compile(
            r"```\w*\s*\n(.*?)```", re.DOTALL
        )
        generic_match = generic_block_pattern.search(llm_response)
        if generic_match:
            code = generic_match.group(1).strip()
            if self._validate_verilog_skeleton(code):
                return code

        # 策略 3: 整个响应就是代码
        stripped = llm_response.strip()
        if stripped.startswith("module ") and "endmodule" in stripped:
            return stripped

        return None

    def _validate_verilog_skeleton(self, code: str) -> bool:
        """
        快速验证提取的代码是否具有基本的 Verilog 骨架结构。
        不做语义分析，仅检查结构性标记。
        """
        has_module = "module " in code
        has_endmodule = "endmodule" in code
        return has_module and has_endmodule
```

---

## 6. 端到端调用示例

```python
async def main():
    """完整的端到端调用流程"""

    # 初始化所有组件
    compiler = IverilogCompilerBridge(iverilog_path="iverilog")
    simulator = VvpSimulationRunner(vvp_path="vvp")
    error_parser = IverilogErrorParser()
    sim_error_parser = VvpErrorParser()
    context_builder = ContextBuilder(
        agent_id="verilog-heal-fir-001",
        max_iterations=10,
        experiment_tag="exp_baseline_20260614",
    )

    # 实际使用时替换为真实的 LLM client
    # llm_client = OpenAIClient(api_key="sk-...")
    llm_client = None  # 开发阶段占位

    agent = LLMAgentController(
        compiler=compiler,
        simulator=simulator,
        error_parser=error_parser,
        sim_error_parser=sim_error_parser,
        context_builder=context_builder,
        llm_client=llm_client,
        max_iterations=10,
    )

    # 含 bug 的 Verilog 源代码
    buggy_source = """module fir_filter #(
  parameter DATA_WIDTH = 16,
  parameter TAP_COUNT  = 8
) (
  input  wire                    clk,
  input  wire                    rst_n,
  input  wire signed [DATA_WIDTH-1:0] data_in,
  output reg  signed [DATA_WIDTH-1:0] data_out
);

  reg signed [DATA_WIDTH-1:0] shift_reg [0:TAP_COUNT-1];
  reg signed [DATA_WIDTH-1:0] coeff      [0:TAP_COUNT-1];
  integer i;
  reg signed [2*DATA_WIDTH-1:0] acc;

  initial begin
    coeff[0] = 16'h0002;
    coeff[1] = 16'h0005;
    coeff[2] = 16'h000A;
    coeff[3] = 16'h000F;
    coeff[4] = 16'h000F;
    coeff[5] = 16'h000A;
    coeff[6] = 16'h0005;
    coeff[7] = 16'h0002;
  end

  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      for (i = 0; i < TAP_COUNT; i = i + 1)
        shift_reg[i] <= 0;
      data_out <= 0;
    end else begin
      shift_reg[0] <= data_in;
      for (i = 1; i < TAP_COUNT; i = i + 1)
        shift_reg[i] <= shift_reg[i-1];
      acc = 0;
      for (i = 0; i < TAP_COUNT; i = i + 1)
        acc = acc + shift_reg[i] * coeff[i];
      data_out <= acc[DATA_WIDTH-1:0];
    end
  end
endmodule"""

    tb_source = """module fir_filter_tb;
  parameter DATA_WIDTH = 16;
  reg                    clk;
  reg                    rst_n;
  reg  signed [DATA_WIDTH-1:0] data_in;
  wire signed [DATA_WIDTH-1:0] data_out;

  fir_filter #(.DATA_WIDTH(DATA_WIDTH), .TAP_COUNT(8)) uut (
    .clk(clk), .rst_n(rst_n), .data_in(data_in), .data_out(data_out)
  );

  initial clk = 0;
  always #5 clk = ~clk;

  integer fail_count;

  initial begin
    fail_count = 0;
    rst_n = 0; data_in = 0;
    #20; rst_n = 1; #10;
    data_in = 16'sd100; #10; data_in = 0;
    #(10 * 8);
    if (data_out === 16'sbx) begin
      fail_count = fail_count + 1;
      $display("[FAIL] Output is X after impulse");
    end
    if (fail_count == 0)
      $display("[TB] ALL TESTS PASSED - PASS");
    else
      $display("[TB] %0d TESTS FAILED - FAIL", fail_count);
    $finish;
  end
endmodule"""

    # 运行修复闭环
    import tempfile
    with tempfile.TemporaryDirectory(prefix="verilog_heal_") as work_dir:
        result = await agent.run(
            design_filename="fir_filter.v",
            design_source=buggy_source,
            tb_filename="fir_filter_tb.v",
            tb_source=tb_source,
            work_dir=work_dir,
        )

    # 输出结果
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 7. 架构设计总结

### 7.1 与现有项目的关系

本 Verilog 自愈 Agent 的架构设计直接复用了 `cpp to verilog` 项目中已验证的工程模式：

| 复用的设计模式 | 来源 | 本项目中的对应 |
|:---|:---|:---|
| JSON Schema 约束 LLM 输出 | `0.3_执行路线与风险清单.md` 中的 Pragma JSON Schema | `llm_output_contract` section |
| Feedback Extractor 模块 | `00_GPT5.5改进意见/04_新框架与研究再定位.md` 中六模块架构 | `Error Parser & Feedback Extractor` |
| Mock-first 策略 | `0.3` 中 Mock HLS Simulator 设计 | 可用 iverilog 替代 Vitis HLS 做 mock |
| 迭代预算控制 | `0.3` 中 20 synthesis budget per kernel | `MAX_ITERATIONS = 10` |
| 结构化诊断反馈 | `0.3` 中 Feedback prompt 设计 | `diagnosis_hints` section |
| Pragma-to-Tcl 转换原型 | `pragma_converter_prototype.py` | 同样是 JSON -> 工具命令的转换范式 |

### 7.2 可扩展性设计

当前架构为未来扩展预留了以下接口：

1. **多 testbench 支持**：`VvpSimulationRunner.simulate()` 接受 `plusargs` 参数，可以对同一个 `.vvp` 文件运行多个 test case
2. **Verilator 后端**：`IverilogCompilerBridge` 和 `VvpSimulationRunner` 都是独立类，可以新增 `VerilatorCompilerBridge` 实现相同接口
3. **增量修复**：`ContextBuilder` 的 `iteration_history` 支持 delta 分析，可以只向 LLM 发送变化部分
4. **Pareto 记录**：当 Agent 修复了语法错误后，可以继续进入面积/时序优化阶段，复用 `cpp to verilog` 项目的 Pareto 维护逻辑

### 7.3 关键工程风险与缓解

| 风险 | 概率 | 缓解 |
|:---|:---|:---|
| LLM 返回的代码无法被正则提取 | 中 | 三级 fallback 策略（精确匹配 -> 通用代码块 -> 纯代码检测） |
| iverilog 版本差异导致错误格式不同 | 低 | 正则模式设计为宽匹配，使用 `(?i)` 忽略大小写 |
| 收敛到局部最优（语法正确但功能错误） | 高 | testbench 仿真验证 + 收敛检测 + 最大迭代限制 |
| LLM context window 超限 | 中 | `MAX_SOURCE_TOKENS` / `MAX_HISTORY_TOKENS` 截断 + 历史压缩 |
| 编译超时（复杂设计） | 低 | 可配置 timeout + kill 机制 |
