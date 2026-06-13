# PyMS 网页爬虫控制台

一个基于 Python 的网页爬虫控制台系统。通过浏览器提交 URL，系统自动抓取网页、清洗数据、生成词云图、展示结果。

## 功能

- 输入 URL 创建爬取任务（支持 limit/depth/关键字/任务名称）
- 命令行式控制台（开始/暂停/继续/停止/清洗/删除/词云图）
- 实时事件流（SSE）显示爬取进度
- 数据清洗：去 HTML 标签、日期规范化、去重
- 关键字过滤：支持多个关键字逗号分隔，不区分大小写
- 结果导出为 JSON 或 CSV
- 词云图生成：基于 jieba 分词和 wordcloud 生成文本词云

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动服务
python main.py

# 3. 打开浏览器
# 访问 http://127.0.0.1:8000
```

## 项目结构

```
pyms/
├── main.py                 # 入口文件
├── requirements.txt        # 依赖（7个包）
├── app/
│   ├── server.py           # Web 路由（FastAPI）
│   ├── config.py           # 配置读取
│   ├── db.py               # SQLite 数据库
│   ├── service.py          # 任务管理
│   ├── command_engine.py   # 命令解析
│   ├── worker.py           # 爬虫 Worker
│   ├── cleaning.py         # 数据清洗与词云图
│   ├── security.py         # URL 安全校验（防 SSRF）
│   ├── state_machine.py    # 任务状态机（6种状态）
│   ├── errors.py           # 错误码
│   └── static/
│       ├── index.html      # 前端页面
│       ├── styles.css      # 深色主题样式
│       └── app.js          # 前端逻辑（SSE/词云图）
└── tests/                  # 测试（8个模块 37个用例）
    ├── test_day1_day2.py   # 状态机、URL校验、任务创建
    ├── test_day3_day4.py   # 命令引擎、API端点
    ├── test_day5_day6.py   # 爬虫Worker、队列消费
    ├── test_day7_day8.py   # 数据清洗、结果查询
    ├── test_day9.py        # SSE事件流
    ├── test_day10.py       # JSON/CSV导出
    ├── test_keyword.py     # 关键字过滤
    └── test_wordcloud.py   # 词云图生成
```

## 支持的命令

| 命令 | 说明 |
|------|------|
| `help` | 显示帮助 |
| `crawl start url=<...> limit=<1-1000> depth=<1-5> [task_name=<...>] [keyword=<...>]` | 创建并启动任务 |
| `crawl pause task_id=<...>` | 暂停任务 |
| `crawl resume task_id=<...>` | 继续任务 |
| `crawl stop task_id=<...>` | 停止任务 |
| `task status task_id=<...>` | 查看任务状态 |
| `task delete task_id=<...>` | 删除任务 |
| `queue list task_id=<...> [state=<...>]` | 查看队列 |
| `clean run task_id=<...>` | 执行数据清洗 |
| `wordcloud run task_id=<...>` | 生成词云图 |

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/v1/crawl/submit` | 创建爬取任务（url, limit, depth, task_name, keyword） |
| POST | `/v1/command` | 执行命令（command, request_id） |
| GET | `/v1/tasks` | 任务列表 |
| GET | `/v1/tasks/{id}` | 任务详情 |
| DELETE | `/v1/tasks/{id}` | 删除已结束的任务 |
| GET | `/v1/tasks/{id}/queue` | 队列列表（state过滤, 分页） |
| GET | `/v1/tasks/{id}/results` | 结果查询（view=raw/clean, 分页, 搜索） |
| POST | `/v1/tasks/{id}/export` | 导出结果（json/csv） |
| GET | `/v1/tasks/{id}/wordcloud` | 生成词云图(PNG) |
| GET | `/v1/events/stream` | 实时事件流(SSE, task_id, after_id) |
| GET | `/v1/health` | 健康检查 |

## 数据库表

| 表名 | 用途 |
|------|------|
| `tasks` | 任务表（task_id, root_url, keyword, status, limit, depth, 进度统计） |
| `queue_items` | 队列表（url, state, hop_count, retry_count, UNIQUE(task_id,url)） |
| `event_logs` | 事件日志表（event_type, payload_json） |
| `command_logs` | 命令日志表（request_id, command, result_code） |
| `raw_items` | 原始数据表（news_id, news_title, news_content, source_url） |
| `clean_items` | 清洗结果表（dedup_key, clean_status, UNIQUE(task_id,dedup_key)） |

## 任务状态

```
pending → running → success
                 → failed
                 → paused → running
                          → stopped
```

## 运行测试

```bash
python -m pytest tests/ -v
```

## 环境变量（可选）

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `PYMS_HOST` | `127.0.0.1` | 监听地址 |
| `PYMS_PORT` | `8000` | 监听端口 |
| `PYMS_DB_PATH` | `data/app.db` | 数据库路径 |
| `PYMS_API_KEY` | （空） | API Key（设置后启用鉴权） |
