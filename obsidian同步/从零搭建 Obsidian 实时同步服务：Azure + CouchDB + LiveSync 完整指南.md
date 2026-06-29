

> 本文完整记录了在 Azure 云服务器上自建 Obsidian LiveSync 实时同步服务的全过程，涵盖环境准备、CouchDB 部署、Nginx 反向代理、SSL 证书配置及客户端接入，包含完整的排错记录。

---

## 📖 目录

- [一、为什么选择自建同步？](#一为什么选择自建同步)
- [二、准备工作](#二准备工作)
- [三、Azure 环境配置](#三azure-环境配置)
- [四、服务器环境初始化](#四服务器环境初始化)
- [五、部署 CouchDB](#五部署-couchdb)
- [六、Nginx 反向代理与 SSL 证书](#六nginx-反向代理与-ssl-证书)
- [七、Obsidian 客户端配置](#七obsidian-客户端配置)
- [八、完整排错记录](#八完整排错记录)
- [九、运维建议](#九运维建议)
- [十、总结](#十总结)

---

## 一、为什么选择自建同步？

Obsidian 官方同步服务需要付费订阅，而 Git 方案存在以下痛点：

- **同步延迟**：分钟级同步，需要手动 commit/pull
- **操作繁琐**：容易遗忘推送或拉取
- **冲突风险**：多设备同时编辑时处理复杂
- **移动端体验差**：Git 操作在移动端不便

自建 CouchDB + LiveSync 方案的核心优势：

| 特性       | 说明                              |
| :------- | :------------------------------ |
| **实时同步** | 编辑完成后秒级推送到其他设备                  |
| **完全掌控** | 数据存储在自己服务器上，隐私无忧                |
| **多端支持** | Windows、macOS、iOS、Android 全平台覆盖 |
| **零月费**  | 一次投入（甚至无需金钱投入），长期使用             |

---

## 二、准备工作

### 2.1 硬件与云服务

| 项目    | 配置                                                                                 |
| :---- | :--------------------------------------------------------------------------------- |
| 云服务商  | Microsoft Azure（或其他云厂商）（学生认证后0成本，详见[zhihu](https://zhuanlan.zhihu.com/p/629609870) |
| 实例规格  | Standard_B1s（1核1GB，可调整）                                                            |
| 操作系统  | Ubuntu Server 22.04 LTS                                                            |
| 公网 IP | 静态公网 IP（如 `<your-ip>`）                                                             |
| 域名    | 已解析到公网 IP 的域名（如 `<your-domain>`）                                                   |

### 2.2 软件栈

- **Docker & Docker Compose**：容器化部署
- **CouchDB 3.3**：支持原生同步协议的 NoSQL 数据库
- **Nginx**：反向代理与 SSL 终止
- **Let's Encrypt**：免费 SSL 证书
- **Self-hosted LiveSync**：Obsidian 社区插件

---

## 三、Azure 环境配置

### 3.1 处理订阅区域限制

Azure 订阅可能有"允许区域"策略限制，部署前需确认可用区域：

```bash
# 查看区域策略
az policy assignment list --query "[?contains(displayName,'location')]" -o table
```

选择一个允许的区域（如 `eastasia`）创建资源组。

### 3.2 创建虚拟机

在 Azure 门户中创建 Ubuntu 22.04 LTS 虚拟机，配置如下：

| 配置项 | 值 |
|:---|:---|
| 资源组 | `<your-resource-group>`（如 `obsidian-sync-rg`） |
| 虚拟机名称 | `<your-vm-name>`（如 `obsidian-sync-vm`） |
| 区域 | 选择允许的区域 |
| 镜像 | Ubuntu Server 22.04 LTS |
| 规格 | Standard_B1s（可调整） |
| 认证方式 | SSH 公钥 |
| 用户名 | `<your-ssh-username>`（如 `azureuser`） |
| 开放端口 | SSH(22)、HTTP(80)、HTTPS(443) |

### 3.3 配置网络安全组（NSG）

> ⚠️ **关键提醒**：创建 VM 后务必检查 NSG 是否已关联到子网或网卡。这是导致后续 80/443 端口外部无法访问的根本原因。

添加入站规则：

| 优先级 | 端口 | 协议 | 源 | 操作 |
|:---|:---|:---|:---|:---|
| 310 | 80 | TCP | Any | 允许 |
| 320 | 443 | TCP | Any | 允许 |

---

## 四、服务器环境初始化

### 4.1 SSH 登录

```bash
# 设置密钥文件权限
chmod 400 ~/Downloads/<your-key>.pem

# SSH 登录
ssh -i ~/Downloads/<your-key>.pem <your-ssh-username>@<your-ip>
```

### 4.2 系统更新与基础工具

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git vim htop ufw
```

### 4.3 安装 Docker

```bash
# 安装 Docker（官方一键脚本）
curl -fsSL https://get.docker.com | sh

# 启动并设置开机自启
sudo systemctl start docker
sudo systemctl enable docker

# 将当前用户加入 docker 组
sudo usermod -aG docker $USER
```

安装 Docker Compose：

```bash
# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 验证安装
docker --version
docker-compose --version
```

> **注意**：执行 `usermod` 后需重新登录 SSH 才能生效。

### 4.4 配置 UFW 防火墙

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# 查看状态
sudo ufw status verbose
```

---

## 五、部署 CouchDB

### 5.1 创建项目目录

```bash
mkdir -p ~/obsidian-sync
cd ~/obsidian-sync
```

### 5.2 创建环境变量文件

> ⚠️ 避免从网页直接粘贴，防止引入不可见控制字符。

```bash
cat > .env << 'EOF'
COUCHDB_USER=admin
COUCHDB_PASSWORD=<your-strong-password>
COUCHDB_SECRET=<your-random-secret>
EOF
```

### 5.3 创建 docker-compose.yml

> ⚠️ 移除已废弃的 `version` 字段，否则会有警告。

```bash
cat > docker-compose.yml << 'EOF'
services:
  couchdb:
    image: couchdb:3.3
    container_name: obsidian-couchdb
    restart: unless-stopped
    ports:
      - "127.0.0.1:5984:5984"
    environment:
      - COUCHDB_USER=${COUCHDB_USER}
      - COUCHDB_PASSWORD=${COUCHDB_PASSWORD}
      - COUCHDB_SECRET=${COUCHDB_SECRET}
    volumes:
      - ./data:/opt/couchdb/data
      - ./config/local.ini:/opt/couchdb/etc/local.ini
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5984/_up"]
      interval: 30s
      timeout: 10s
      retries: 3
EOF
```

> ⚠️ **关键点**：卷挂载必须写成 `./config/local.ini:/opt/couchdb/etc/local.ini`（单个文件），不能写成 `./config:/opt/couchdb/etc`（整个目录），否则会覆盖容器内所有默认配置文件导致启动失败。

### 5.4 创建 CouchDB 配置文件

```bash
mkdir -p config
cat > config/local.ini << 'EOF'
[couchdb]
single_node = true
max_document_size = 50000000
q = 1
n = 1

[chttpd]
require_valid_user = true
enable_cors = true

[chttpd_auth]
require_valid_user = true

[httpd]
bind_address = 0.0.0.0
port = 5984

[cors]
origins = app://obsidian.md, capacitor://localhost, http://localhost, https://localhost
credentials = true
headers = accept, authorization, content-type, origin, referer
methods = GET, PUT, POST, HEAD, DELETE
max_age = 3600
EOF
```

### 5.5 启动 CouchDB

```bash
# 启动容器
docker-compose up -d

# 查看状态
docker-compose ps
# 应显示状态为 Up

# 查看日志（确认无错误）
docker-compose logs -f couchdb
# 按 Ctrl+C 退出
```

### 5.6 创建数据库

> ⚠️ 密码含 `!` 等特殊字符时，URL 必须用单引号包裹，否则 Bash 会报 `event not found`。

```bash
# 创建主数据库
curl -X PUT 'http://admin:<your-password>@localhost:5984/obsidian-vault'

# 创建配置数据库
curl -X PUT 'http://admin:<your-password>@localhost:5984/obsidian-vault-config'
```

验证数据库已创建：

```bash
curl 'http://admin:<your-password>@localhost:5984/_all_dbs'
# 应输出 ["obsidian-vault", "obsidian-vault-config"]
```

---

## 六、Nginx 反向代理与 SSL 证书

### 6.1 安装 Nginx

```bash
sudo apt install -y nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 6.2 配置 Nginx 虚拟主机

> ⚠️ 写入配置文件必须用 `sudo tee` 而非 `sudo cat >`，否则会因重定向权限不足而报错。

```bash
sudo tee /etc/nginx/sites-available/obsidian-sync > /dev/null << 'EOF'
server {
    listen 80;
    server_name <your-domain>;
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }
    location / {
        return 301 https://$server_name$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name <your-domain>;

    ssl_certificate /etc/letsencrypt/live/<your-domain>/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/<your-domain>/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://127.0.0.1:5984;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 300s;
        client_max_body_size 50M;
    }
}
EOF
```

### 6.3 启用站点

```bash
# 创建软链接
sudo ln -sf /etc/nginx/sites-available/obsidian-sync /etc/nginx/sites-enabled/

# 删除默认站点（避免 server_name 冲突）
sudo rm -f /etc/nginx/sites-enabled/default

# 测试配置
sudo nginx -t

# 重载 Nginx
sudo systemctl reload nginx
```

### 6.4 申请 SSL 证书

> ⚠️ 如遇到 80 端口外部不可达的问题，检查 Azure NSG 是否已正确关联到子网或网卡。

**方式一：webroot 模式**（推荐，无需停止 Nginx）

```bash
sudo mkdir -p /var/www/html
sudo certbot certonly --webroot -w /var/www/html -d <your-domain> --non-interactive --agree-tos -m <your-email>
```

**方式二：standalone 模式**（webroot 失败时使用）

```bash
sudo systemctl stop nginx
sudo certbot certonly --standalone -d <your-domain> --non-interactive --agree-tos -m <your-email>
sudo systemctl start nginx
```

成功输出示例：

```
Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/<your-domain>/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/<your-domain>/privkey.pem
This certificate expires on <expiry-date>.
These files will be updated when the certificate renews.
Certbot has set up a scheduled task to automatically renew this certificate in the background.
```

### 6.5 验证 HTTPS

```bash
# 检查 Nginx 是否监听 443
sudo ss -tlnp | grep :443
# 应显示 LISTEN 0.0.0.0:443

# 本地测试 HTTPS
curl -k https://localhost/_up
# 应返回 {"error":"unauthorized","reason":"Authentication required."}
```

**外部测试**（在本地电脑执行）：

```powershell
curl.exe https://<your-domain>/_up
# 应返回 {"error":"unauthorized","reason":"Authentication required."}
```

带认证测试：

```powershell
curl.exe -u admin:<your-password> https://<your-domain>/
# 应返回 CouchDB 欢迎信息
```

---

## 七、Obsidian 客户端配置

### 7.1 安装插件

1. 打开 Obsidian
2. 进入 **设置** → **第三方插件**
3. 关闭"安全模式"
4. 点击 **浏览**
5. 搜索 **Self-hosted LiveSync**
6. 点击 **安装**，安装完成后点击 **启用**

### 7.2 配置连接

进入插件设置界面，填写以下信息：

| 配置项 | 值 |
|:---|:---|
| Remote Database Server | `https://<your-domain>` |
| Username | `admin` |
| Password | `<your-password>` |
| Database Name | `obsidian-vault` |

> ✅ 使用 Let's Encrypt 正式证书，**无需**勾选"Ignore SSL certificate errors"。

### 7.3 同步策略推荐

| 配置项 | 推荐值 |
|:---|:---|
| Sync Mode | LiveSync |
| Enable Compression | 开启 |
| Conflict resolution | Newest wins |
| Ignore patterns | `.obsidian/workspace.json`<br>`.obsidian/graph.json`<br>`.git/`<br>`node_modules/` |

### 7.4 开始同步

1. 点击 **Test** 按钮，应显示连接成功
2. 点击 **Sync now** 开始首次同步
3. 观察状态栏，应变为绿色并显示"LiveSync connected"

---

## 八、完整排错记录

### 问题 1：`.env` 文件包含不可见控制字符

**现象**：
```
failed to read .env: line 1: unexpected character "\x1b" in variable name
```

**原因**：从网页复制粘贴时带入了 `\x1b[200~` 控制字符。

**解决**：

```bash
# 方式一：重新写入
cat > .env << 'EOF'
COUCHDB_USER=admin
COUCHDB_PASSWORD=<your-strong-password>
COUCHDB_SECRET=<your-random-secret>
EOF

# 方式二：清理控制字符
sed -i 's/\x1b\[[0-9;]*~//g' .env
```

---

### 问题 2：CouchDB 容器无限重启

**现象**：
```
touch: cannot touch '/opt/couchdb/etc/local.d/docker.ini': No such file or directory
Failed to open arguments file "/opt/couchdb/bin/../etc/vm.args"
```

**原因**：`volumes` 挂载了整个 `./config` 目录到 `/opt/couchdb/etc`，覆盖了容器内所有默认配置文件。

**解决**：改为挂载单个文件：

```yaml
volumes:
  - ./data:/opt/couchdb/data
  - ./config/local.ini:/opt/couchdb/etc/local.ini   # 只挂载这个文件
```

---

### 问题 3：curl 创建数据库报 `event not found`

**现象**：
```
-bash: !@localhost: event not found
```

**原因**：密码中的 `!` 被 Bash 解释为历史命令扩展。

**解决**：将整个 URL 用单引号包裹：

```bash
curl -X PUT 'http://admin:<your-password>@localhost:5984/obsidian-vault'
```

---

### 问题 4：外部无法访问 80/443 端口

**现象**：
```
curl: (7) Failed to connect to port 80/443 after timeout
```

**原因**：云服务商网络安全组未放行端口或未关联。

**解决**：
1. 进入虚拟网络 → 子网 → 关联 NSG
2. 添加入站规则放行 80 和 443 端口

---

### 问题 5：Nginx 未监听 443 端口

**现象**：
```bash
sudo ss -tlnp | grep :443
# 无任何输出
```

**原因**：配置文件中 `listen 443 ssl` 被注释或缺失。

**解决**：重新写入完整配置，确保包含 HTTPS server 块。

---

### 问题 6：Certbot webroot 超时

**现象**：
```
Detail: Timeout during connect (likely firewall problem)
```

**原因**：80 端口外部不可达（NSG 未放行）。

**解决**：
1. 先解决 NSG 问题
2. 或改用 DNS-01 挑战模式
3. 或改用 standalone 模式

---

### 问题 7：server_name 冲突警告

**现象**：
```
nginx: [warn] conflicting server name "<your-domain>" on 0.0.0.0:80
```

**原因**：默认站点 `default` 也监听了同一域名。

**解决**：

```bash
sudo rm -f /etc/nginx/sites-enabled/default
sudo systemctl reload nginx
```

---

### 问题 8：Nginx 配置文件写入权限不足

**现象**：
```
-bash: /etc/nginx/sites-available/obsidian-sync: Permission denied
```

**原因**：`sudo` 只作用于 `cat`，重定向 `>` 由当前 shell 执行。

**解决**：使用 `sudo tee`：

```bash
sudo tee /etc/nginx/sites-available/obsidian-sync > /dev/null << 'EOF'
...配置内容...
EOF
```

---

## 九、运维建议

### 9.1 自动备份

```bash
cat > ~/backup-couchdb.sh << 'EOF'
#!/bin/bash
BACKUP_DIR=~/obsidian-sync/backup
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# 备份 CouchDB 数据
docker exec obsidian-couchdb couchdb-backup.sh > $BACKUP_DIR/backup_$DATE.json

# 保留最近 7 天备份
find $BACKUP_DIR -name "backup_*.json" -mtime +7 -delete

echo "✅ 备份完成: backup_$DATE.json"
EOF

chmod +x ~/backup-couchdb.sh

# 添加定时任务（每天凌晨 3 点）
crontab -e
# 添加：0 3 * * * /home/<your-ssh-username>/backup-couchdb.sh
```

### 9.2 证书自动续期

Certbot 已自动配置定时任务，无需额外操作：

```bash
# 查看续期状态
sudo systemctl status certbot.timer

# 手动测试续期
sudo certbot renew --dry-run
```

### 9.3 服务状态检查

```bash
# 查看容器状态
docker-compose -f ~/obsidian-sync/docker-compose.yml ps

# 查看容器日志
docker-compose -f ~/obsidian-sync/docker-compose.yml logs -f --tail=50

# 查看 Nginx 状态
sudo systemctl status nginx

# 查看 Nginx 错误日志
sudo tail -30 /var/log/nginx/obsidian-sync-error.log
```

### 9.4 数据库维护

```bash
# 压缩数据库（释放空间）
curl -X POST 'http://admin:<your-password>@localhost:5984/obsidian-vault/_compact'

# 清理视图索引
curl -X POST 'http://admin:<your-password>@localhost:5984/obsidian-vault/_view_cleanup'
```

---

## 十、总结

### 10.1 部署检查清单

- [x] 云资源组已创建（在允许区域内）
- [x] 云 VM 已创建并获取公网 IP
- [x] 网络安全组已关联并放行 80、443 端口
- [x] 域名已解析到 VM 公网 IP
- [x] Docker + Docker Compose 已安装
- [x] CouchDB 容器运行正常
- [x] 数据库 `obsidian-vault` 已创建
- [x] Nginx 已配置并指向 CouchDB
- [x] SSL 证书已安装，HTTPS 访问正常
- [x] Obsidian LiveSync 插件可连接服务器

### 10.2 成果一览

| 阶段 | 关键产出 |
|:---|:---|
| 云环境 | VM + 安全组 + 公网 IP |
| CouchDB | Docker 容器 + obsidian-vault 数据库 |
| Nginx | 反向代理 + HTTPS |
| SSL 证书 | Let's Encrypt 正式证书（自动续期） |
| Obsidian | LiveSync 插件连接成功 |

### 10.3 成本分析（以 Azure B1s 为例）（学生实则可以做到0成本）

| 项目           | 月成本                              |
| :----------- | :------------------------------- |
| 云 VM (1核1GB) | ¥40-80（学生认证此部分成本为0）              |
| 域名           | ¥50-100/年（用cloudns或者qzz.io实现0成本） |
| SSL 证书       | 免费                               |
| **总计**       | **约 ¥50-100/月**                  |

### 10.4 最终效果

- ✅ 设备间同步延迟 **< 3 秒**
- ✅ 支持 **5+ 台设备**同时在线
- ✅ HTTPS 加密传输，安全可靠
- ✅ 数据完全自主掌控
- ✅ 无需支付 Obsidian Sync 订阅费
- ✅ 支持 Windows / macOS / iOS / Android 全平台

---

> 💡 **本文完整命令均可直接复制使用，注意将 `<your-domain>`、`<your-email>`、`<your-password>` 等替换为实际值。

---

## 🔗 相关资源

- [Obsidian LiveSync GitHub](https://github.com/vrtmrz/obsidian-livesync)
- [CouchDB 官方文档](https://docs.couchdb.org/)
- [Let's Encrypt 官方文档](https://letsencrypt.org/docs/)
- [Azure 虚拟机文档](https://docs.microsoft.com/azure/virtual-machines/)