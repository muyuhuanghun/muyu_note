# 13.自动化与通知

📌 定时任务、消息通知、自动化工作流工具。

# ==========================================
# 📁 脚本列表
# ==========================================

| 脚本 | 功能 | 适用场景 |
|------|------|----------|
| `cron_helper.py` | 定时任务管理助手 | 生成 cron/Task Scheduler 配置 |
| `notification_sender.py` | 多渠道消息通知 | 训练完成提醒、错误告警 |
| `workflow_builder.py` | 简易工作流编排 | 多步骤任务串行/并行执行 |

# ==========================================
# 🚀 使用示例
# ==========================================

## cron_helper.py — 定时任务

```bash
# 生成每小时执行一次的 cron 表达式
python cron_helper.py --every 1h --command "python backup.py"

# 生成每天凌晨 2 点执行的 cron
python cron_helper.py --daily 02:00 --command "python cleanup.py"

# 生成每周一执行的 cron
python cron_helper.py --weekly mon --command "python report.py"

# 生成 Windows Task Scheduler XML
python cron_helper.py --daily 02:00 --command "python cleanup.py" --format xml

# 列出当前用户的 cron 任务
python cron_helper.py --list
```

## notification_sender.py — 消息通知

```bash
# 发送桌面通知
python notification_sender.py --title "训练完成" --body "模型准确率 95.2%"

# 发送邮件通知（需配置 SMTP）
python notification_sender.py --email --to "you@example.com" --subject "实验结果"

# 发送到 Webhook（企业微信/钉钉/Slack）
python notification_sender.py --webhook "https://hooks.example.com/xxx" --text "任务完成"

# 作为训练脚本的回调
python train.py && python notification_sender.py --title "✅ 训练完成" --body "查看结果"
```

## workflow_builder.py — 工作流编排

```bash
# 从 YAML 文件加载并执行工作流
python workflow_builder.py workflow.yaml

# 生成示例工作流文件
python workflow_builder.py --init > my_workflow.yaml
```

工作流 YAML 格式：
```yaml
name: 数据处理流水线
steps:
  - name: 清洗数据
    command: python clean.py
  - name: 训练模型
    command: python train.py
    depends_on: [清洗数据]
  - name: 生成报告
    command: python report.py
    depends_on: [训练模型]
```

# ==========================================
# 💡 Tips
# ==========================================

- `cron_helper.py` 同时支持 Linux cron 和 Windows Task Scheduler
- `notification_sender.py` 可以作为任何长时间运行脚本的结尾回调
- `workflow_builder.py` 支持依赖关系，自动决定执行顺序
