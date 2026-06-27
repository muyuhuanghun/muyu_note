#!/usr/bin/env python3
"""
多渠道消息通知工具
📌 支持桌面通知、邮件、Webhook（企业微信/钉钉/Slack）
📌 适合作为长时间运行脚本的结尾回调
"""

import argparse
import json
import sys
import urllib.request

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def send_desktop(title: str, body: str):
    """发送桌面通知"""
    if sys.platform == "win32":
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(title, body, duration=5)
            print(f"✅ 桌面通知已发送: {title}")
            return
        except ImportError:
            pass

        # 备用方案：PowerShell
        import subprocess
        ps_cmd = f'''
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        $template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
        $template.GetElementsByTagName("text")[0].AppendChild($template.CreateTextNode("{title}"))
        $template.GetElementsByTagName("text")[1].AppendChild($template.CreateTextNode("{body}"))
        $toast = [Windows.UI.Notifications.ToastNotification]::new($template)
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Script").Show($toast)
        '''
        try:
            subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True)
            print(f"✅ 桌面通知已发送: {title}")
        except Exception as e:
            print(f"❌ 通知失败: {e}")

    elif sys.platform == "darwin":
        import subprocess
        subprocess.run([
            "osascript", "-e",
            f'display notification "{body}" with title "{title}"'
        ])
        print(f"✅ 桌面通知已发送: {title}")

    else:
        # Linux: notify-send
        import subprocess
        try:
            subprocess.run(["notify-send", title, body])
            print(f"✅ 桌面通知已发送: {title}")
        except FileNotFoundError:
            print(f"⚠️ 不支持桌面通知（需要 notify-send）")


def send_email(
    to: str,
    subject: str,
    body: str,
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 587,
    username: str = None,
    password: str = None,
):
    """发送邮件通知"""
    import smtplib
    from email.mime.text import MIMEText

    if not username or not password:
        print("❌ 邮件发送需要 SMTP 认证信息（--smtp-user / --smtp-pass）")
        return

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = username
    msg["To"] = to

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
        print(f"✅ 邮件已发送: {subject} → {to}")
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")


def send_webhook(url: str, text: str, title: str = None):
    """发送 Webhook 通知（支持企业微信/钉钉/Slack）"""
    # 自动检测 Webhook 类型
    if "qyapi.weixin" in url or "weixin" in url:
        # 企业微信
        payload = {"msgtype": "text", "text": {"content": f"{title + ': ' if title else ''}{text}"}}
    elif "dingtalk" in url or "oapi.dingtalk" in url:
        # 钉钉
        payload = {"msgtype": "text", "text": {"content": f"{title + ': ' if title else ''}{text}"}}
    elif "hooks.slack" in url:
        # Slack
        payload = {"text": f"*{title}*\n{text}" if title else text}
    else:
        # 通用 JSON
        payload = {"title": title, "text": text}

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = resp.read().decode("utf-8")
            print(f"✅ Webhook 已发送: {result[:100]}")
    except Exception as e:
        print(f"❌ Webhook 发送失败: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="多渠道消息通知工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python notification_sender.py --title "训练完成" --body "准确率 95.2%"
  python notification_sender.py --email --to "you@example.com" --subject "实验结果"
  python notification_sender.py --webhook "https://hooks.xxx" --text "任务完成"

  作为回调使用:
  python train.py && python notification_sender.py --title "✅ 完成" --body "查看结果"
        """,
    )
    parser.add_argument("--title", default="通知", help="通知标题")
    parser.add_argument("--body", default="", help="通知内容")
    parser.add_argument("--desktop", action="store_true", default=True, help="桌面通知（默认）")
    parser.add_argument("--email", action="store_true", help="发送邮件")
    parser.add_argument("--to", help="收件人邮箱")
    parser.add_argument("--subject", help="邮件主题")
    parser.add_argument("--smtp-server", default="smtp.gmail.com")
    parser.add_argument("--smtp-port", type=int, default=587)
    parser.add_argument("--smtp-user", help="SMTP 用户名")
    parser.add_argument("--smtp-pass", help="SMTP 密码")
    parser.add_argument("--webhook", help="Webhook URL")
    parser.add_argument("--text", help="Webhook 消息文本")

    args = parser.parse_args()

    if args.email:
        send_email(
            to=args.to, subject=args.subject or args.title,
            body=args.body, smtp_server=args.smtp_server,
            smtp_port=args.smtp_port, username=args.smtp_user,
            password=args.smtp_pass,
        )
    elif args.webhook:
        send_webhook(args.webhook, args.text or args.body, args.title)
    else:
        send_desktop(args.title, args.body)


if __name__ == "__main__":
    main()
