# CCS 12 & CCS Theia & CCS 21.0.1 — 安装与配置教程

CCS12 是老版本（Eclipse 风格），CCS Theia 和 CCS 21.0.1 是新一代（VSCode 风格，跳过了 12~21 中间的版本号，直接编号为 21）。本质区别不大，但工程和缓存目录互不通用，混装会出各种诡异问题。

> [!warning] 2026-09-02 硬件型号更正
> 当前实际使用的板子是**老款 MSP-EXP430G2**，不是 MSP-EXP430G2ET。权威识别证据是 Windows 硬件 ID `USB\VID_0451&PID_F432&REV_0105`；TI 的硬件工具文档把 `0451:F432` 对应到老款 MSP-EXP430G2。它使用上一代 eZ430/TUSB3410 调试器，而 G2ET 使用更新的 eZ-FET。两者不能混为一谈，尤其是在驱动、固件和 USB 3.x 兼容性排障中。

---

# 一、版本选择与下载


## 版本对比

| 版本 | 风格 | 安装目录示例 | 推荐场景 |
| --- | --- | --- | --- |
| CCS 12.x | Eclipse 桌面 | `C:\ti\ccs1200` | 老教程、老工程、习惯 Eclipse |
| CCS Theia 1.5.x | VSCode 风格 | `C:\ti\ccstheia151` | 课程设计、新工程 |
| CCS 21.0.1 | VSCode 风格 | `C:\ti\ccs2100` | 想用最新版的可以试 |

💡 课程当前使用老款 MSP-EXP430G2 + MSP430G2553。CCS 能编译该工程，但截至 2026-09-02，F5 调试仍卡在板载调试器初始化阶段；详见本文第十一节。建议**只装一套**，避免下面"问题 4"里讲的混乱。

## 下载链接

- **CCS Theia**: [CCSTUDIO-THEIA IDE、配置、编译器或调试器 | TI.com.cn](https://www.ti.com.cn/tool/cn/download/CCSTUDIO-THEIA/1.1.0)
- **CCS 21.0.1**: [CCSTUDIO IDE, configuration, compiler or debugger | TI.com](https://www.ti.com/tool/download/CCSTUDIO/21.0.1)
- **CCS 12**: 在 TI 官网搜索 `CCSTUDIO` 找历史版本

📌 下载前要登录 TI 账号，注册免费但需要邮箱验证。

---


# 二、安装流程（以 CCS Theia 为例）


## 2.1 安装器选组件

```
# ==========================================
# MSP430 开发必须勾选的组件
# ==========================================

✅ MSP430 Ultra Low Power MCUs    # MSP430 编译器 + 调试支持
✅ TI MSP430 Debug Stack          # eZ-FET / FET430 驱动栈
✅ CCS Theia IDE                  # 1.5.x 主体
✅ TI Arm Debug Stack             # 如果未来要用 Tiva / C2000 可以勾上
✅ TI C28xx Debug Stack
```

⚠️ **不要**只勾 IDE 不勾调试栈——这是后面"识别不到板子"的常见原因之一。

## 2.2 安装路径

默认路径就是 `C:\ti\ccstheia151`，**别改**：

```text
C:\ti\ccstheia151\
├── ccs\                  # IDE 主体
├── ccs\ccs_base\         # 目标数据库、驱动
├── tools\compiler\       # MSP430 编译器
├── xnucleo\              # MSP Debug Stack
└── .theia\               # 用户配置（注意这个名字，VSCode 是 .vscode）
```

⚠️ 改路径会出现"能找到 IDE 但找不到编译器"的报错，而且错误信息非常迷惑。

---

# 三、首次启动 + 驱动验证

## 3.1 插入 MSP-EXP430G2（老款）

把板子插入 USB，**先不要急着打开 IDE**，先确认设备管理器：

```
# ==========================================
# 设备管理器应该看到（按硬件 ID 排序）
# ==========================================

通用串行总线设备
  └── HID-compliant device              # 调试接口（被 HID 驱动接管，正常的！）
端口 (COM 和 LPT)
  └── MSP430 Application UART (COMx)    # 回传串口，x 可能是 3、5、9...
```

📌 关键认知：**COM 口 ≠ 调试接口**。COM 口是给串口调试工具（SSCOM、PuTTY）用的，调试接口走的是 Spy-Bi-Wire，对 Windows 表现为 HID。

💡 端口号会变。每次重新插板或重启电脑，COM 编号都可能换。程序里不要硬编码 `COM9`，每次用设备管理器看一眼。

## 3.2 不要混淆 G2 与 G2ET 的驱动

⚠️ 当前老款 MSP-EXP430G2 的 USB ID 是 `0451:F432`，UART 接口应绑定 TI 的 `430CDC.inf`；本机当前安装的是 CCS 自带的 `1.5.0.0`（2016-10-27），文件哈希与 CCS 安装目录中的版本完全一致。不要把 `usbuart3410.inf` 强塞给当前已经正常枚举的复合设备，也不要照着 G2ET/eZ-FET 的教程替换驱动。

新版 MSP-EXP430G2ET 使用另一代 eZ-FET 和不同的 USB 标识。看到设备管理器里有 UART 与 HID，只能证明 USB 枚举成功，不能证明调试器协议握手一定成功。

---

# 四、工程打开的正确姿势

## 4.1 工作区根目录要固定

CCS Theia 把工作区信息存在 `.theia/launch.json`。**外层目录和内层工程目录各有一份**的时候，IDE 会用错的那份。

```
# ==========================================
# 错误示范：嵌套目录导致两份 launch.json
# ==========================================

D:\课程\实验1\
└── msp430g2xx3_uscia0_uart_01_115k\        # ← 打开这个
    └── msp430g2xx3_uscia0_uart_01_115k\    # ← 打开这个也会成功，但 launch.json 是另一份
        └── .ccsproject
```

📌 **规则**：要么只打开外层，要么只打开工程根目录。混着开就会出现 `targetConfigs` 找不到、调试探针选错、报错 `MSP-FET430UIF on COM port`（但实际并不是 COM 口问题）。

## 4.2 三件配置必须对上号

打开工程后，确认下面这三件东西指向同一个芯片：

```c
// 1. .ccsproject 里写的器件
//    <com.ti.ccstudio.apps.modelProjectModel
//        deviceId="MSP430G2553"

// 2. targetConfigs/MSP430G2553.ccxml
//    <connection value="TI MSP430 USB1"/>

// 3. .theia/launch.json 里的 configName
//    "configName": "MSP430G2553.ccxml"
```

任何一个对不上都会出现"找不到器件"或"找不到调试探针"。

---

# 五、Debug 流程

## 5.1 第一次 Debug

1. CCS 里点 **Debug Project**（不是 Run，是 Debug）
2. Output 面板会显示：
   ```
   Configuring Debugger...
   Initializing: MSP430
   Initializing: MSP430G2553
   Loading: <程序名>.out
   ```
3. 停在 `main()` 第一行 → F8 继续运行

💡 第一次启动可能要 1~3 分钟，那是工具链在解析 `targetdb` 的 XML、初始化调试栈。**别拔 USB、别关 CCS**。

## 5.2 报错的处理顺序

⚠️ 报错了**不要立刻清缓存**，按下面的顺序来：

```
# ==========================================
# CCS 报错时的标准排查流程
# ==========================================

[1] 看 CCS 弹的提示
    "Please unplug and re-plug the USB connection"
       → 直接拔插 USB，重试 Debug，别动文件

    "Could not find MSP-FET430UIF on specified COM port"
       → 99% 是误导性文本，先按上一条处理

[2] Terminate 当前 Debug 会话（不是 Disconnect）
    → 等调用栈从 Debug 视图消失

[3] 拔 USB，等 3~5 秒，重插
    → 等设备管理器把 Application UART 和 HID 都枚举成 OK

[4] 在 CCS 里直接重试 Debug，不要重开 CCS
    → 第一次成功过的工程，配置没问题
```

📌 CCS 自己提示"unplug and re-plug"时，**就按它说的做**，不要自作主张去删 `.lock`、清 `.theia`、清 `ccs2100` 工作区——那些是过头动作。

什么时候才需要清缓存：

```c
// 只有在下面三种情况之一，才考虑清缓存
if (Output 日志明确出现缓存路径错误) {
    // 清 .lock
} else if (连续两次拔插 USB 都报同一错) {
    // 清 .theia + .lock
} else if (Initializing 阶段就卡死、不进入 MSP430) {
    // 清整个工作区
}
```

---

# 六、拔 USB 的正确姿势


⚠️ **永远不要在活动调试会话中拔 USB**。MSP Debug Stack 官方文档明确警告过：可能让目标 MCU 处于未知状态、让 IDE 工作区状态损坏。

```
# ==========================================
# 标准拔线顺序
# ==========================================

1. CCS Debug 视图 → 点 Terminate
2. 等调用栈和调试会话从界面消失
3. 退出 CCS（或不退出，反正别再 Debug）
4. 再拔 USB
```

只是改代码后重新烧录？**不需要拔 USB**。结束旧会话、重新构建、启动 Debug 就行。

---


# 七、串口调试配合（SSCOM / PuTTY）


回显 UART 用 SSCOM 验证：

```
# ==========================================
# SSCOM 配置
# ==========================================

端口: COMx (看设备管理器，MSP430 Application UART 那行)
波特率: 9600 (MSP430G2553 例程默认)
数据位: 8
停止位: 1
校验位: None
流控: None
```

打开串口 → 板子周期打印 `HELLO!\r\n` → 在发送框输 `A` → 收到 `A` 回显 → 说明 UART 收发都通了。

💡 程序里 `HELLO!` 能收到但 `A` 发出去没回显？**99% 是漏了 `__enable_interrupt()`**。见 [[踩坑总结_2026#问题 6]]。

---

# 八、UART 中断最小代码模板


MSP430 的中断要"两层都开"——外设允许 + CPU 全局允许。下面是验证过能跑通的最小模板：

```c
#include <msp430g2553.h>

// 初始化 UART
void UART_Init(void) {
    P1SEL  |= BIT1 + BIT2;     // P1.1 = RX, P1.2 = TX
    P1SEL2 |= BIT1 + BIT2;
    UCA0CTL1 |= UCSSEL_2;      // SMCLK
    UCA0BR0 = 104;             // 1MHz / 9600 ≈ 104
    UCA0BR1 = 0;
    UCA0MCTL = UCBRS0;         // 调制
    UCA0CTL1 &= ~UCSWRST;      // 启动 UART
}

// 接收中断：把收到的字节原样发回去
#pragma vector=USCIAB0RX_VECTOR
__interrupt void USCI0RX_ISR(void) {
    while (!(IFG2 & UCA0TXIFG));   // 等发送缓冲区空
    UCA0TXBUF = UCA0RXBUF;         // 回显
}

int main(void) {
    WDTCTL = WDTPW + WDTHOLD;   // 关看门狗
    UART_Init();

    IE2 |= UCA0RXIE;            // 📌 外设允许接收中断
    __enable_interrupt();       // 📌 CPU 打开全局中断 GIE

    // 周期发 HELLO!
    while (1) {
        volatile unsigned int i;
        for (i = 0; i < 50000; i++);
        while (!(IFG2 & UCA0TXIFG));
        UCA0TXBUF = 'H';
        // ... 后面继续发 E L L O ! \r \n
    }
}
```

⚠️ 两个 `📌` 行缺一个都不行：
- 只开外设 (`IE2 |= UCA0RXIE`)，收不到中断
- 只开 GIE，没外设允许，也进不了中断向量

很多 TI 低功耗例程用 `__bis_SR_register(LPM0_bits + GIE)` 一行同时进低功耗和开中断，改成普通循环时要把 GIE 单独补回来。

---

# 九、装了两套 CCS 怎么办

💡 **别慌着卸载**。两套 CCS 的工程和缓存目录是分开的（`ccstheia151` vs `ccs2100`），不会直接冲突。但**打开工程时用了不同安装目录**会让 CCS 选错编译器版本、目标数据库版本。

排查步骤：

```text
1. 看 UART 工程编译产物的路径
   build.log 里应该写 "C:/ti/ccstheia151/..."
   如果看到 "C:/ti/ccs2100/..."，说明混了

2. 决定保留哪一套
   - 课程只用 MSP430G2553 → 任意一套都行
   - 用了多个 CCS 版本专属功能 → 看哪个工程依赖哪套

3. 卸载另一套（确认没有依赖后再卸）
   Windows 控制面板 → 卸载 TI 那套 → 勾选清除工作区
```

📌 卸完之后记得检查 `C:\ti\` 下面有没有残留目录，否则下次装新版会出现奇怪的版本冲突。

---

# 十、文件路径同步

课程文件搬了位置？用全盘搜索按文件名找：

```powershell
# PowerShell：按文件名找 .ccsproject
Get-ChildItem -Path C:\Users\muyuhuanghun -Recurse -Filter "*.ccsproject" -ErrorAction SilentlyContinue
```

📌 课程总 README 里只写相对路径，别写 `C:\Users\muyuhuanghun\Desktop\lesson_design\...` 这种绝对路径。换台电脑就全失效。

---

# 附：常见问题速查

| 现象 | 大概率原因 | 处理 |
| --- | --- | --- |
| `No compatible board detected` | USB 没插稳 / CCS 装得太早没驱动栈 | 重插 USB，重装 CCS 勾上 Debug Stack |
| `MSP-FET430UIF on COM port` | 通用的调试器初始化错误，可能是 USB 控制器、驱动、占用、固件或硬件 | 先做一次规范拔插；若稳定复现，查看 Debug Server 日志，不要反复清缓存 |
| `HELLO!` 有，单字符发出去没回显 | 漏 `__enable_interrupt()` | 见第八节最小模板 |
| `Initializing: MSP430` 卡 5 分钟 | 第一次扫描 + Defender | 等。Defender 排除项**不要**默认加 |
| `Could not find launch configuration` | 工作区打开了错的层级 | 固定工程根目录，看 `.theia/launch.json` 的 `resourceId` |
| 拔 USB 后 GUI 报错 | 没先结束调试会话 | 见第六节标准拔线顺序 |
| 装两套 CCS 报错混用 | 用错了安装目录的工具链 | 见第九节 |

---

# 十一、2026-09-02 当前故障状态：F5 无法初始化板载调试器

> [!summary] 当前结论
> 故障**尚未修复**。当前概率最高的原因是老款 MSP-EXP430G2 板载 eZ430 调试器与本机 AMD USB 3.x/xHCI 路径存在兼容问题，但这仍是待验证假设，不是已经闭环的结论。正在等待联想 `BY01-2.0` 真 USB 2.0 Hub 到货，进行只改变 USB 路径的 A/B 测试。

## 11.1 当前环境

| 项目 | 当前事实 |
| --- | --- |
| IDE | CCS Theia 1.5.1，安装于 `C:\ti\ccstheia151` |
| 命令行调试器 | DSLite 12.8.0.3529 |
| MSP430 Debug Stack | `msp430.dll` 3.15.1.1，SHA-256 `BEDDC082B17ED12CA9E61C9AF0824B4ABDD35D4C1D2B3983CF4AB2918E257288` |
| 开发板 | **老款 MSP-EXP430G2**，USB ID `0451:F432`，设备修订 `0105` |
| 目标芯片 | MSP430G2553 |
| UART | `MSP430 Application UART (COM9)`，状态 OK |
| 调试接口 | `MSP430 Debug-Interface` / HID，状态 OK |
| 当前 USB 主机路径 | AMD USB 3.10 xHCI，`PCI\VEN_1022&DEV_15B7` |
| CCS 目标配置 | `TI MSP430 USB1` + `MSP430G2553.ccxml` |

## 11.2 现象

工程可以正常编译，但按 F5 启动 Debug 时出现：

```text
MSP430G2553 Unable to connect to MSP430G2553.
Please unplug and re-plug the USB connection and try again.

TI MSP430 USB1/MSP430
Error initializing emulator:
Could not find MSP-FET430UIF on specified COM port
```

这个错误发生在程序下载之前，因此不能用用户程序是否打开全局中断来解释。

## 11.3 最关键的直接证据

使用 DSLite 对复位向量 `0xFFFE` 做 2 字节只读测试，没有擦除、下载或写 Flash。重启电脑并让板子断电静置一夜后，测试仍在约 96.83 秒后失败：

```text
MSP430_GetNumberOfUsbIfs(...) = 1
MSP430_GetNameOfUsbIf(...) = HID0015:COM9
MSP430_SetTargetArchitecture(0) = 0
MSP430_Initialize(HID0015:COM9, ...) = -1    # 约 95 秒后
MSP430_Error_Number() = 57
MSP430_Error_String(57) = Could not find MSP-FET430UIF on specified COM port
MSP430_Close(FALSE) = 0
```

日志里只加载了 `MSP430_OpenDevice` 函数地址，**没有实际调用 `MSP430_OpenDevice()`**。这说明失败点位于“PC 上的 MSP430.dll 与板载 eZ430 调试器初始化”阶段，还没有打开目标 MSP430G2553。

最新只读测试证据：

```text
C:\Users\muyuhuanghun\Desktop\lesson_design\artifacts\board-connect-20260902-080119\dslite-memory.log
```

此前完全断电再插回后的同类证据：

```text
C:\Users\muyuhuanghun\Desktop\lesson_design\artifacts\board-connect-20260902-000601\dslite-memory.log
```

## 11.4 已验证排除或明显降级的方向

| 方向 | 证据与结论 |
| --- | --- |
| 忘记打开全局中断 | 与 F5 连接错误无关；连接失败发生在目标程序运行之前。源码中也已经有 `IE2 |= UCA0RXIE;` 和 `__enable_interrupt();`。GIE 只影响 UART 接收中断/回显。 |
| CCS 工程或 `launch.json` | 使用同一份 `MSP430G2553.ccxml` 的 DSLite 命令行能独立复现，因此 GUI 启动配置不是当前主因。 |
| COM9 被占用 | .NET SerialPort 独占打开测试成功；微软 Sysinternals Handle 审计也没有发现 COM9 句柄。 |
| HID 接口被占用 | Handle 对 `VID_0451&PID_F432` 返回 `No matching handles found`；HIDClass 没有 UpperFilters/LowerFilters。 |
| 驱动文件错误 | 已安装 `oem132.inf`，原始文件 `430CDC.inf`，TI 1.5.0.0；其 SHA-256 与 CCS 自带版本完全一致。 |
| USB 省电 | 设备级 `EnhancedPowerManagementEnabled=0`、`AllowIdleIrpInD3=0`、`SelectiveSuspendOn=0`；当前电源方案的 USB 3 Link Power Management 交流/直流均为 Off。重启后设置仍保持。 |
| 只是 eZ430 没有彻底复位 | 电脑已重启，板子完全断电并静置一夜，故障仍稳定复现。 |
| 只有新版 CCS/MSP430.dll 有问题 | 2011 年旧版 TI MSP430Flasher + 旧 DLL 也在初始化 TIUSB 时失败，约 35 秒后返回 `ERROR 1014`。 |
| 自动枚举选错 COM | 旧版 Flasher 明确指定 `-i COM9` 仍在约 2.1 秒后返回同一个 `ERROR 1014`。 |
| 固件被程序偷偷更新 | 日志中只解析了固件更新函数地址，没有调用固件更新；当前排障也没有执行任何 FET 固件写入。 |

现场人工确认过：使用原装线、主机 USB 口、SSCOM 已关闭、没有额外外围连线，J101/SBW 跳线已压紧。这些属于人工检查结果，不等同于示波器级信号完整性验证。

## 11.5 为什么当前优先怀疑 USB 3.x/xHCI

当前设备拓扑显示，板子直接挂在：

```text
USB\ROOT_HUB30\5&6148D45&0&0
└── AMD USB 3.10 eXtensible Host Controller
    └── PCI\VEN_1022&DEV_15B7
```

这台 ROG Strix G16 的外部 USB-A 口属于 USB 3.x 控制器。机器虽然还有一个 AMD USB 2.0 控制器 `DEV_15B8`，但当前只连接内置摄像头，没有暴露为可直接使用的外部 USB-A 口。

TI 支持论坛存在同款老 MSP-EXP430G2、同类 error 57 的历史案例：TI 工程师在 USB 2.0 口测试成功，并把 USB 3.0/xHCI 列为重点嫌疑；另有用户更换 USB 主机控制器后恢复稳定连接。这证明“老 eZ430 与某些 USB 3.x/xHCI 路径不兼容”不是凭空猜测。

但 error 57 本身只是通用初始化错误，不能单靠错误文本确认根因。因此当前只能写成：

> USB 3.x/xHCI 兼容问题是**概率最高、已有历史案例支持、尚待本机 A/B 验证**的假设。

## 11.6 已做的系统修改及备份

为了排除电源管理，已针对当前 eZ430 HID 接口关闭相关省电，并关闭当前电源方案的 USB 3 链路省电。修改前的注册表和电源设置已备份：

```text
C:\Users\muyuhuanghun\Desktop\lesson_design\artifacts\usb-power-backup-20260902-001059
```

这些修改重启后仍然生效，但没有消除 error 57，因此“Windows 省电是主因”的假设已经被显著削弱。该备份可用于后续回滚。

## 11.7 下一步：联想 BY01-2.0 A/B 测试

已选择联想 `BY01-2.0`，它是 USB-A 上行、4 个 USB-A 下行的真正 USB 2.0 Hub。推荐 0.25 米短线版。

连接方式：

```text
笔记本右侧 USB-A
        ↓
联想 BY01-2.0（USB 2.0 Hub）
        ↓
MSP-EXP430G2
```

首次验证时，Hub 上只接 LaunchPad，不接鼠标、U 盘或其他设备。验证顺序必须固定：

1. 关闭 CCS 和串口助手。
2. 通过 BY01-2.0 插入板子。
3. 用 Windows PnP 信息确认设备拓扑中确实多出一层 USB 2.0 Hub，而不是仍然直连根集线器。
4. 用 DSLite 只读 `0xFFFE,2`，不烧写。
5. 连续做两次只读连接，排除“偶然成功一次”。
6. 打开 CCS，正常 Build 后按 F5。
7. 正常 Terminate，再次 F5，验证会话释放后的第二次连接。

判定规则：

- 如果经过 Hub 后连接从约 95 秒超时变成几秒内成功，连续只读与两次 F5 都成功，可以基本确认根因是老 eZ430 与当前 AMD USB 3.x/xHCI 路径的兼容性。
- 如果经过 Hub 后仍稳定停在 `MSP430_Initialize` 并报 error 57，不能继续把问题都归因于 USB 3.0；下一步应在另一台电脑上交叉验证，再考虑官方老 LaunchPad 固件恢复工具或板载 eZ430/TUSB3410 硬件故障。

## 11.8 当前状态用语

截至 2026-09-02，准确状态是：

> CCS 编译正常；Windows 能枚举 UART 与 HID；PC 到板载 eZ430 的初始化稳定失败；用户程序与全局中断不是本次 F5 错误的原因；USB 3.x/xHCI 是最高概率但尚未验证闭环的根因；等待 BY01-2.0 到货完成决定性测试。

---

## 相关文档

- [[踩坑总结_2026]]：本次踩坑的完整时间线和证据分级
- [MSP-EXP430G2 用户指南（SLAU318）](https://www.ti.com/lit/pdf/slau318)：当前老款板子的 TUSB3410/eZ430、电路图、Spy-Bi-Wire 与回传 UART
- [MSP430 Hardware Tools 用户指南](https://www.ti.com/lit/ug/slau278y/slau278y.pdf)：不同 MSP430 调试工具的 USB VID/PID 对照
- [TI：相同 error 57 与 USB 3.0/xHCI 的历史案例](https://e2e.ti.com/support/microcontrollers/msp-low-power-microcontrollers-group/msp430/f/msp-low-power-microcontroller-forum/497398/msp430g2-launchpad-error-could-not-find-msp-fet430uif-on-specified-com-port)
- [CCS Theia 1.5 调试文档](https://software-dl.ti.com/ccs/esd/documents/users_guide_ccs_theia/ccs_debug-main.html)：`.ccxml`、`launch.json` 和 GUI 启动过程
- [TI MSP Debug Stack 页面](https://www.ti.com/tool/MSPDS)：IDE 所带低层驱动说明，以及不要在活动调试中拔线

---

## 一句话总结

💡 装好一套 CCS、固定一个工作区根目录、Debug 前别随意清缓存、拔 USB 前先 Terminate，是正常工作流；但老款 MSP-EXP430G2 还要额外关注 eZ430 与现代 USB 3.x/xHCI 的兼容性。当前故障尚待 BY01-2.0 A/B 测试闭环。
