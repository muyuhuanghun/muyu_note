# Linux 基础命令速查

> 📌 本文整理 Linux 常用命令，涵盖文件操作、用户管理、网络、进程管理等核心知识点。
> 适用于 CentOS (yum) 和 Ubuntu (apt) 环境。

---

## 🖥️ 系统基础

### 获取 IP 与快照

```bash
# 进入终端，获取 IP 地址
ifconfig          # Ubuntu 需先安装 net-tools：sudo apt install net-tools
# IP 存在于 ens33 的 inet 字段

# 💡 特殊 IP 地址
# 127.0.0.1 — 本机回环地址
# 0.0.0.0   — 特殊地址，代指本机；端口绑定中表示绑定所有 IP
```

### 主机名管理

```bash
hostname                        # 查看主机名
sudo hostnamectl set-hostname 新名字   # root 下修改主机名
```

---

## 📂 文件与目录操作

### 基本命令

| 命令 | 功能 | 常用参数 |
|:---|:---|:---|
| `ls` | 列出目录内容 | `-a` 显示隐藏文件，`-h` 人性化文件大小，`-l` 详细信息 |
| `cd` | 切换目录 | `/` 根目录，`..` 上一级，`~` home 目录 |
| `pwd` | 显示当前工作目录 | — |
| `mkdir` | 新建文件夹 | — |
| `touch` | 新建空文件 | — |
| `cat` | 读取文件内容（一次性输出） | — |
| `more` | 读取文件（可翻页） | — |
| `cp` | 复制文件/文件夹 | `-r` 递归复制文件夹 |
| `mv` | 移动/重命名文件 | — |
| `rm` | 删除文件/文件夹 | `-r` 递归删除，`-f` 强制删除 |

### 通配符

```bash
*a      # 以 a 结尾的文件
a*      # 以 a 开头的文件
*a*     # 包含 a 的文件
```

### 查找与过滤

```bash
# find — 在文件系统中查找文件
find / -name "****"           # 按名称查找
find / -size -10k             # 按大小查找（小于 10KB）

# grep — 在文件内容中过滤行
grep -n "xu" test.txt         # -n 显示行号

# which — 查找命令的可执行文件路径
which python3

# wc — 统计文件信息
wc -c test.txt    # bytes 数量
wc -m test.txt    # 字符数量
wc -l test.txt    # 行数
wc -w test.txt    # 单词数
```

---

## ✍️ Vi/Vim 文本编辑器

📌 Vim 是 Vi 的加强版，支持 shell 程序编辑，可用不同颜色标识语法。

### 三种模式

| 模式 | 说明 | 进入方式 |
|:---|:---|:---|
| **命令模式** (Command) | 按键均为命令，执行不同功能 | 启动默认进入，或按 `Esc` |
| **输入模式** (Insert) | 编辑文本内容 | 命令模式下按 `i` |
| **底线模式** (Last Line) | 保存、退出等操作 | 命令模式下按 `:` |

### 常用快捷键

```bash
# ⚠️ 任何情况下按 Esc 都能回到命令模式

# 命令模式操作
dd        # 删除光标所在行
yy        # 复制光标所在行
p         # 粘贴

# 搜索（命令模式下）
/关键词    # 进入搜索模式
n         # 向下继续搜索
N         # 向上继续搜索

# 底线模式操作
:w        # 保存
:q        # 退出
:wq       # 保存并退出
:q!       # 强制退出不保存
```

---

## 👤 用户与权限管理

### 用户切换

```bash
su - root       # 切换到 root 用户（- 加载环境变量）
exit            # 退回普通用户
sudo 命令        # 临时赋予 root 权限
```

📌 **为普通用户配置 sudo 免密认证**：
1. 切换到 root 用户
2. 执行 `visudo`
3. 按 `o` 进入编辑，添加：`用户名 ALL=(ALL) NOPASSWD:ALL`
4. `wq` 保存退出

### 用户组管理（root 下执行）

```bash
# 用户组
groupadd 组名           # 创建用户组
groupdel 组名           # 删除用户组

# 用户
useradd -g 组名 用户名    # 创建用户并指定用户组（不指定则默认创建同名组）
useradd -d /path 用户名   # 指定 home 目录路径
userdel -r 用户名         # 删除用户及其 home 目录

# 查看信息
id 用户名               # 查看用户信息
getent passwd           # 查看系统所有用户
getent group            # 查看系统所有用户组

# 用户组操作
usermod -aG 用户组 用户名   # 将用户加入指定用户组
```

### 文件权限

```bash
# 修改权限
chmod [-R] 权限 文件或文件夹
chmod u=rwx,g=rx,o=x 文件夹
chmod -R u=rwx,g=rx,o=x 文件夹    # -R 递归处理

# 💡 权限缩写对照表
# u (user) 所属用户 | g (group) 用户组 | o (other) 其他用户
# r=4 读 | w=2 写 | x=1 执行 | -=0 无权限
#
# 0 ---    1 --x    2 -w-    3 -wx
# 4 r--    5 r-x    6 rw-    7 rwx

# 示例
chmod 751 文件夹    # 等价于 chmod u=rwx,g=rx,o=x 文件夹

# 修改所属用户/用户组（仅 root）
chown root 文件名       # 修改所属用户
chown :root 文件名      # 修改所属用户组
chown -R :root 文件夹   # 递归修改
```

---

## ⌨️ 终端快捷键

| 快捷键 | 功能 |
|:---|:---|
| `Ctrl + C` | 强制停止当前程序 / 命令输入错误时退出 |
| `Ctrl + D` | 退出登录 / 退出特定程序（如 python）⚠️ 不能退出 vi/vim |
| `Ctrl + R` | 搜索历史命令 |
| `Ctrl + A` | 跳转至命令开头 |
| `Ctrl + E` | 跳转至命令结尾 |
| `Ctrl + ←` | 向左跳一个单词 |
| `Ctrl + →` | 向右跳一个单词 |
| `Ctrl + L` | 清屏（等同 `clear`） |

```bash
history           # 查看历史命令
```

---

## 📦 软件包管理

### CentOS — yum

```bash
# 🚀 rpm 包软件管理器，自动化安装配置，自动解决依赖
sudo yum -y install 软件名    # 安装
sudo yum -y remove 软件名     # 卸载
sudo yum search 关键词        # 搜索
```

### Ubuntu — apt

```bash
# 语法和 yum 一致
sudo apt install 软件名
sudo apt remove 软件名
sudo apt search 关键词
```

### 服务管理 — systemctl

```bash
systemctl start 服务名     # 启动
systemctl stop 服务名      # 停止
systemctl status 服务名    # 查看状态
systemctl enable 服务名    # 开机自启
systemctl disable 服务名   # 取消开机自启
```

---

## 🔗 软链接（快捷方式）

```bash
ln -s 参数1 参数2
# -s 创建软链接
# 参数1 — 被链接的文件/目录
# 参数2 — 链接目的地

# 示例
ln -s /home/muyu/test/xzx.txt ~/muyu
```

---

## 🌐 网络命令

### 连通性测试

```bash
ping -c 5 ip或主机名    # -c 指定检查次数
```

### 文件下载

```bash
# wget — 后台下载
wget -b url
# -b 后台下载，通过 tail -f 文件名 监控下载进度

# curl — 发送网络请求 / 下载文件
curl -O url             # -O 下载文件并保存
curl cip.cc             # 获取本机公网 IP
```

### 端口扫描

```bash
nmap 127.0.0.1    # 查看本机对外暴露的端口
```

💡 **端口分类**：

| 范围 | 类型 | 说明 |
|:---|:---|:---|
| 1 ~ 1023 | 公认端口 | 系统服务使用 |
| 1024 ~ 49151 | 注册端口 | 一般程序/服务松散绑定 |
| 49152 ~ 65535 | 动态端口 | 程序对外连接临时使用 |

---

## 📊 进程管理

### 进程查看

```bash
ps -ef              # 查看全部进程（完全格式化）

# 输出字段说明
# UID   — 进程所属用户 ID
# PID   — 进程 ID
# PPID  — 父进程 ID
# C     — CPU 占用率
# STIME — 启动时间
# TTY   — 终端序列号
# TIME  — CPU 占用时间

ps -ef | grep tail    # 管道过滤，查找含 tail 的进程
```

### 进程控制

```bash
kill -9 进程ID        # 强制关闭进程
```

### 系统监控

```bash
# top — 任务管理器
top                   # 实时监控
top -p 进程ID         # 监控特定进程
top -d 2              # 设置刷新间隔（秒）
top -c                # 显示完整命令

# 磁盘
df -h                 # 查看硬盘使用情况（-h 人性化单位）

# CPU/磁盘 I/O
iostat                # 查看 CPU、磁盘占用
iostat -x             # 更详细信息

# 网络
sar -n DEV 1 5        # 查看网络统计（1秒刷新，共5次）
```

---

## 🌍 环境变量

```bash
env                           # 查看所有环境变量
echo $PATH                    # 获取 PATH 环境变量

# 临时设置（当前会话有效）
export 变量名=变量值

# 永久生效
# 针对当前用户：~/.bashrc 文件中添加 export
# 针对全部用户：/etc/profile 文件中添加 export

# 修改后需手动生效
source ~/.bashrc
source /etc/profile

# 🌟 自定义 PATH（追加新路径到 PATH）
export PATH=$PATH:/home/xxx/custom_path
```

---

## 📁 压缩与解压

### tar 归档

```bash
# .tar — 归档文件（简单封装）
# .gz  — gzip 压缩格式

# 常用参数
# -c 创建压缩  -v 显示过程  -x 解压模式
# -f 指定文件（必须放最后）  -z gzip 模式  -C 指定解压目的地

# 压缩
tar -zcvf 归档名.tar.gz 要压缩的文件或目录

# 解压
tar -zxvf 归档名.tar.gz -C 目标目录
```

### zip 压缩

```bash
# 压缩
zip -r 压缩包名.zip 要压缩的文件或目录

# 解压（-d 指定解压目的地）
unzip -d 目标目录 压缩包名.zip
```

---

## 📎 文件上传下载

```bash
# ⚠️ 需要终端工具支持（如 Xshell、SecureCRT 等）
rz      # 从本地上传文件到服务器
sz 文件名 # 从服务器下载文件到本地
```

---

## 📅 系统时间

```bash
date                   # 查看系统时间
date +"%Y-%m-%d %H:%M:%S"    # 格式化输出

# 格式符
# %Y 完整年份  %y 年份后两位  %M 月份  %d 日
# %H 时  %M 分  %S 秒  %s 时间戳（起始 1970.01.01）
```

---

> 💡 **相关笔记**：[[服务器与VPS]] | [[VPN BASE SET]]
