# Git 基础操作

> 📌 Git 版本控制完整操作指南，涵盖从环境搭建到分支管理的全流程。
> 基于 Linux (Ubuntu) 环境，使用阿里云 Codeup 作为远端仓库。

---

## 🚀 前期准备

### 安装 Git 环境

```bash
sudo apt install git -y
git --version    # 查看版本（6.3.3 / 6.4.2）
```

### 配置全局用户信息

```bash
git config --global user.name "<muyu>"
git config --global user.email "<940>"
```

### 安装 Python3 与虚拟环境

```bash
sudo apt install python3 -y
sudo apt install python3-venv
```

### 创建并激活虚拟环境

```bash
python3 -m venv exp_venv          # 创建虚拟环境目录
source exp_venv/bin/activate       # 激活环境
```

### 安装依赖

```bash
# 创建 requirement.txt
touch requirement.txt
# 内容：sanic, requests, pymssql

pip install -r requirement.txt     # 安装第三方库
```

---

## 🔑 SSH 密钥配置

### 生成密钥对

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -C "<添加注释>"
# -t 指定密钥类型（ed25519 或 rsa）
# -f 指定私钥文件路径（默认 ~/.ssh/id_rsa）
# -C 注释内容，用于标识公钥
```

### 查看与配置公钥

```bash
ls ~/.ssh/                         # 查看生成的密钥文件
cat ~/.ssh/id_ed25519.pub          # 查看公钥内容
```

📌 在 Codeup 页面：个人设置 → SSH 公钥 → 粘贴公钥

---

## 📦 远端仓库操作

### 克隆仓库

```bash
# 在 Codeup 仓库首页复制 SSH URL
git clone <url>
```

### 基本推送流程

```bash
touch README.md
git add README.md
git status
git pull
git commit -m "docs: 创建README.md"
git push origin master
```

---

## 📝 代码托管流程

### 创建文件并同步到远端

```bash
echo "import json" > test.py       # 创建代码文件
git add test.py                     # 暂存（纳入跟踪）
git status                          # 状态：被跟踪、已暂存、等待提交
git commit -m "feat(test.py): 引入json"
git push origin master
```

### 修改文件并同步

```bash
echo "import random" > test.py     # 修改代码
git status                          # 状态：被跟踪、修改未暂存
git add test.py
echo "import re" >> test.py        # 再次修改
git commit -a -m "feat(test.py): 引入random, re"   # -a 自动暂存已跟踪文件
git push                            # 等价于 git push origin master
```

### 查看提交历史与差异

```bash
git log                             # 查看所有提交（最近在上）
git log -p -1                       # 查看最近一次提交的详细差异
git diff <版本号> test.py            # 比较指定版本与当前的差异
```

💡 `commit` 后紧跟的 SHA-1 哈希值即为版本号

---

## ↩️ 撤销操作

### 撤销暂存

```bash
git restore --staged test.py        # 将 HEAD 版本复制回暂存区
# 或
git reset HEAD <file>               # 较危险操作
```

### 撤销提交

```bash
git reset HEAD~                     # HEAD~ 指向最后一次提交的前一次
```

### 撤销推送

```bash
git reset HEAD~                     # 本地强制回滚
git push -f origin master           # 强制推送至远端
```

---

## 🗑️ 文件删除与恢复

### 保留文件，取消跟踪

```bash
git rm --cached test.py             # 取消跟踪
git add test.py                     # 恢复跟踪
```

### 从暂存区恢复文件

```bash
rm test.py                          # 本地删除
git restore test.py                 # 从暂存区恢复
```

### 从本地仓库恢复文件

```bash
git rm test.py
git rm -f test.py
git status                          # 文件标注为 deleted

# ⚠️ 此时不能直接 restore 恢复，需要两步：
git restore --staged test.py        # 先从提交区恢复到暂存区
git restore test.py                 # 再从暂存区恢复到工作目录
```

### 从远端仓库恢复

```bash
git pull                            # 抓取远端分支所有工作融合至当前分支
```

---

## 🌿 分支管理

### 创建与切换分支

```bash
git branch develop                  # 创建新分支（本质上是创建新指针）
git switch develop                  # 切换到 develop 分支

# 或一步完成
git checkout -b <branch>
```

### 分支开发实践示例

在 `develop` 分支下开发，使用 `.gitignore` 忽略本地配置：

```bash
# config.json（本地测试配置，不提交）
{
    "dev_sn": "68h89asd79fxfa",
    "dev_pwd": "hda89dsa0sa9dha"
}

# test.py（业务逻辑代码，需要托管）
import json

def get_config(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)

if __name__ == '__main__':
    config = get_config("./config.json")
    print(f"dev_sn:{config['dev_sn']}")
    print(f"dev_pwd:{config['dev_pwd']}")
```

```bash
python3 test.py                     # 本地测试

# 配置忽略
echo "config.json" >> .gitignore

# 提交推送
git add test.py .gitignore
git commit -m "feat(test.py): 添加读取config.json并打印sn,pwd;
docs(.gitignore): 添加config.json"
git push origin develop
```

---

> 📎 **相关笔记**：[[GitHub学生认证]] | [[GitHub Recovery Codes]] | [[COLPILOT]] | [[Github Base Info]]
