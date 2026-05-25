# 一.前置概念

## 1.为什么要自建节点

- 商业机场的隐私风险：流量审计、日志记录、节点共享
- 自建节点的优势：独享IP、可控延迟、不会被机场跑路影响
- 自建节点的劣势：需要维护、单个IP有被封风险

## 2.常见协议选择

| 协议 | 特点 | 推荐场景 |
|------|------|----------|
| Shadowsocks-rust | 轻量、抗检测较弱 | 低风险环境、低配VPS |
| Xray + VLESS + XTLS | 抗检测强、性能好 | **当前首选方案** |
| Xray + VMess + WS + TLS | 套CDN、伪装强 | 高墙环境 |
| Hysteria2 | 基于QUIC、速度极快 | 需要高速传输 |
| WireGuard | 标准VPN协议、全流量代理 | 回国/办公场景 |

# 二.VPS选购

## 1.选择要点

- **地理位置**：延迟越低越好，亚洲优化线路（CN2 GIA / 9929 / CMI）
- **带宽**：至少 500GB/月流量，带宽 ≥ 1Gbps
- **线路**：对大陆优化线路 > 普通国际线路
- **价格**：年付 $15-$50 为合理区间

## 2.常见VPS商家

- [BandwagonHost (搬瓦工)](https://bandwagonhost.com)：CN2 GIA线路，稳定但贵
- [RackNerd](https://racknerd.com)：性价比高，黑五促销时年付$10起
- [Vultr](https://www.vultr.com)：按小时计费，可随时销毁换IP
- [CloudCone](https://cloudcone.com)：便宜，线路一般
- [Akile](https://akile.io)：适合日本/新加坡节点
- [DigitalOcean](https://www.digitalocean.com)：适合学习，有GitHub学生包免费额度[[Github Base Info]]

## 3.购买后确认信息

- VPS IP地址
- root 密码（或 SSH Key）
- SSH 端口（默认22）

# 三.服务器初始化

## 1.SSH连接

```bash
ssh root@你的VPS_IP -p 端口号
```

常见默认端口：22

首次登录后建议修改root密码：

```bash
passwd
```

## 2.基础环境配置

```bash
# 更新系统
apt update && apt upgrade -y   # Debian/Ubuntu
yum update -y                   # CentOS

# 安装必备工具
apt install -y curl wget vim git ufw
```

## 3.开启BBR加速

BBR是Google开发的TCP拥塞控制算法，能显著提升网络吞吐量：

```bash
# 检查内核版本
uname -r

# 开启BBR（内核 ≥ 4.9）
echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
sysctl -p

# 验证是否生效
sysctl net.ipv4.tcp_congestion_control
# 输出应为: net.ipv4.tcp_congestion_control = bbr
```

## 4.防火墙设置

```bash
# 开启防火墙
ufw allow 22/tcp        # SSH
ufw allow 你的代理端口/tcp
ufw enable
```

# 四.搭建代理服务

## 方案一：Xray + VLESS + XTLS（推荐）

使用官方一键脚本 [Xray-install](https://github.com/XTLS/Xray-install)：

```bash
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install
```

配置文件位置：`/usr/local/etc/xray/config.json`

参考配置模板（VLESS + XTLS）：

```json
{
  "inbounds": [{
    "port": 443,
    "protocol": "vless",
    "settings": {
      "clients": [{
        "id": "你的UUID",
        "flow": "xtls-rprx-vision"
      }],
      "decryption": "none"
    },
    "streamSettings": {
      "network": "tcp",
      "security": "reality",
      "realitySettings": {
        "dest": "www.microsoft.com:443",
        "serverNames": ["www.microsoft.com"],
        "privateKey": "你的私钥",
        "shortIds": ["6ba85179e30d4fc2"]
      }
    }
  }],
  "outbounds": [{
    "protocol": "freedom"
  }]
}
```

生成UUID和密钥：

```bash
# 生成UUID
xray uuid

# 生成reality密钥对
xray x25519
```

启动服务：

```bash
systemctl enable xray
systemctl start xray
systemctl status xray
```

## 方案二：Hysteria2（高速版）

```bash
bash <(curl -fsSL https://get.hy2.sh/)
```

配置示例 `/etc/hysteria/config.yaml`：

```yaml
listen: :443
tls:
  cert: /etc/hysteria/cert.crt
  key: /etc/hysteria/cert.key
auth:
  type: password
  password: 你的密码
masquerade:
  type: proxy
  proxy:
    url: https://www.bing.com
    rewriteHost: true
```

启动：

```bash
systemctl enable hysteria-server
systemctl start hysteria-server
```

## 方案三：Shadowsocks-rust（轻量级）

```bash
# 使用ss-install脚本
bash <(curl -sL https://raw.githubusercontent.com/iAmGz/shadowsocks-rust-install/main/install.sh)
```

按提示设置端口、密码、加密方式（推荐 `2022-blake3-aes-128-gcm`）。

# 五.客户端配置

## 1.Windows / macOS / Linux

| 客户端 | 适用协议 | 推荐度 |
|--------|----------|--------|
| [v2rayN](https://github.com/2dust/v2rayN) | Xray/V2Ray全系列 | Windows首选 |
| [Clash Verge Rev](https://github.com/clash-verge-rev/clash-verge-rev) | 通用订阅客户端 | 全平台 |
| [Sing-box](https://github.com/SagerNet/sing-box) | 通用内核 | 高级用户 |
| [Shadowsocks](https://shadowsocks.org) | SS/SSR | 仅SS用户 |

- **v2rayN 配置**：复制服务器配置JSON → 在v2rayN中选择"服务器"→"添加服务器"→ 粘贴配置
- **Clash Verge Rev**：编写订阅配置文件或直接导入节点

## 2.Android

- [v2rayNG](https://github.com/2dust/v2rayNG)
- [Clash Meta for Android](https://github.com/MetaCubeX/ClashMetaForAndroid)
- [Sing-box](https://play.google.com/store/apps/details?id=com.sagernet.singbox)

## 3.iOS

- Shadowrocket（App Store付费）
- Streisand
- Sing-box

# 六.CDN加速与伪装

## 1.套Cloudflare CDN

适用场景：IP被墙或需要隐藏真实IP

- 在Cloudflare中添加域名，将A记录指向VPS IP
- 开启CDN代理（橙色云朵）
- 使用 Xray + VMess + WebSocket + TLS 配置
- 使用Nginx/Caddy做前置反代

## 2.推荐伪装站点

使用 `www.microsoft.com`、`www.bing.com`、`www.apple.com` 等大型站点作为XTLS reality的fallback目标。

# 七.优化与维护

## 1.优化内核参数

```bash
cat >> /etc/sysctl.conf << EOF
net.ipv4.tcp_slow_start_after_idle=0
net.ipv4.tcp_notsent_lowat=16384
net.ipv4.tcp_mtu_probing=1
EOF
sysctl -p
```

## 2.定时更新

```bash
# Xray更新
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install

# 一般VPS系统更新
apt update && apt upgrade -y
```

## 3.流量监控

```bash
# 使用vnstat监控流量
apt install -y vnstat
vnstat -m   # 按月查看
vnstat -d   # 按日查看
```

## 4.IP被墙应对

- 客观检查：[IPCheck](https://ipcheck.need.sh/)
- Vultr等支持销毁重建 → 换IP
- 固定IP的VPS → 套Cloudflare CDN
- 保留备用节点

# 八.常见问题

- **连接超时**：检查防火墙端口是否开放、VPS是否正常运行
- **速度慢**：尝试开启BBR、检查本地网络到VPS的延迟、换协议
- **证书错误**：检查系统时间 `date`，确保时间同步 `ntpdate -u pool.ntp.org`
- **CPU占用高**：Xray reality的dest目标可能响应慢，换一个目标站

---

- 当你不再需要魔法上网的时候，你也就不再需要魔法上网了
