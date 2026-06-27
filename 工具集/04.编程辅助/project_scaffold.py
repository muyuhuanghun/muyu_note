#!/usr/bin/env python3
"""
项目脚手架生成器
📌 快速生成标准化的项目目录结构
📌 支持 Python、C++ CMake、PyTorch 深度学习项目
"""

import argparse
import os
import sys
from pathlib import Path

# Windows 终端 UTF-8 输出
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


SCAFFOLDS = {
    "python": {
        "description": "Python 标准项目",
        "files": {
            "main.py": '''#!/usr/bin/env python3
"""主程序入口"""

def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
''',
            "requirements.txt": "# 项目依赖\n",
            "README.md": "# {project_name}\n\n项目描述\n",
            ".gitignore": '''__pycache__/
*.pyc
.env
venv/
*.egg-info/
dist/
build/
''',
            "src/__init__.py": "",
            "tests/__init__.py": "",
            "tests/test_main.py": '''import unittest

class TestMain(unittest.TestCase):
    def test_placeholder(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
''',
        },
    },
    "cpp-cmake": {
        "description": "C++ CMake 项目",
        "files": {
            "CMakeLists.txt": '''cmake_minimum_required(VERSION 3.10)
project({project_name})

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(${PROJECT_NAME} src/main.cpp)
''',
            "src/main.cpp": '''#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
''',
            "include/.gitkeep": "",
            "README.md": "# {project_name}\n\n项目描述\n",
            ".gitignore": '''build/
cmake-build-*/
*.o
*.exe
.vscode/
''',
            "tests/CMakeLists.txt": '''# 测试配置
enable_testing()
# add_test(NAME test_xxx COMMAND test_xxx)
''',
        },
    },
    "pytorch": {
        "description": "PyTorch 深度学习项目",
        "files": {
            "train.py": '''#!/usr/bin/env python3
"""模型训练脚本"""
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

def train():
    # 🚀 设备配置
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🖥️ 使用设备: {device}")

    # 📌 在这里构建模型、数据集、优化器
    # model = YourModel().to(device)
    # dataset = YourDataset(...)
    # dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    # optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    # criterion = nn.CrossEntropyLoss()

    # 🌟 训练循环
    # for epoch in range(num_epochs):
    #     for batch in dataloader:
    #         ...
    pass

if __name__ == "__main__":
    train()
''',
            "model.py": '''#!/usr/bin/env python3
"""模型定义"""
import torch
import torch.nn as nn

class YourModel(nn.Module):
    """📌 在这里定义你的模型结构"""
    def __init__(self):
        super().__init__()
        # self.layer = nn.Linear(...)

    def forward(self, x):
        # return self.layer(x)
        return x
''',
            "dataset.py": '''#!/usr/bin/env python3
"""数据集定义"""
from torch.utils.data import Dataset

class YourDataset(Dataset):
    """📌 在这里定义数据加载逻辑"""
    def __init__(self, data_path, transform=None):
        self.data = []
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sample = self.data[idx]
        if self.transform:
            sample = self.transform(sample)
        return sample
''',
            "config.py": '''#!/usr/bin/env python3
"""训练配置"""
# 📌 所有超参数集中管理

class Config:
    # 数据
    data_path = "./data"
    batch_size = 32
    num_workers = 4

    # 模型
    input_dim = 128
    hidden_dim = 256
    output_dim = 10

    # 训练
    epochs = 100
    lr = 1e-3
    weight_decay = 1e-4

    # 保存
    checkpoint_dir = "./checkpoints"
    log_dir = "./logs"
''',
            "utils.py": '''#!/usr/bin/env python3
"""工具函数"""
import torch
import os

def save_checkpoint(model, optimizer, epoch, path):
    """保存训练检查点"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    torch.save({
        "epoch": epoch,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
    }, path)
    print(f"💾 检查点已保存: {path}")

def load_checkpoint(model, optimizer, path):
    """加载训练检查点"""
    checkpoint = torch.load(path)
    model.load_state_dict(checkpoint["model_state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
    return checkpoint["epoch"]
''',
            "requirements.txt": '''torch>=2.0
torchvision>=0.15
numpy
matplotlib
tqdm
''',
            "README.md": "# {project_name}\n\n深度学习项目\n\n## 使用\n\n```bash\npython train.py\n```\n",
            ".gitignore": '''__pycache__/
*.pyc
checkpoints/
logs/
data/
*.pth
.env
venv/
''',
            "data/.gitkeep": "",
            "checkpoints/.gitkeep": "",
            "logs/.gitkeep": "",
        },
    },
}


def create_scaffold(project_name: str, scaffold_type: str):
    """生成项目脚手架"""
    if scaffold_type not in SCAFFOLDS:
        print(f"❌ 未知项目类型: {scaffold_type}")
        print(f"   可用类型: {', '.join(SCAFFOLDS.keys())}")
        sys.exit(1)

    scaffold = SCAFFOLDS[scaffold_type]
    project_dir = Path(project_name)

    if project_dir.exists():
        print(f"❌ 目录已存在: {project_name}")
        sys.exit(1)

    print(f"📁 创建项目: {project_name}")
    print(f"📋 类型: {scaffold['description']}")
    print("-" * 60)

    for filepath, content in scaffold["files"].items():
        full_path = project_dir / filepath
        full_path.parent.mkdir(parents=True, exist_ok=True)

        # 替换占位符
        formatted = content.replace("{project_name}", project_name)
        full_path.write_text(formatted, encoding="utf-8")
        print(f"  ✅ {filepath}")

    print("-" * 60)
    print(f"🎉 项目创建完成！")
    print(f"\n💡 下一步:")
    print(f"   cd {project_name}")


def main():
    parser = argparse.ArgumentParser(
        description="项目脚手架生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python project_scaffold.py my_project --type python
  python project_scaffold.py my_cpp --type cpp-cmake
  python project_scaffold.py my_dl --type pytorch
        """,
    )
    parser.add_argument("name", help="项目名称（也是目录名）")
    parser.add_argument("--type", required=True, choices=list(SCAFFOLDS.keys()),
                        help="项目类型")

    args = parser.parse_args()
    create_scaffold(args.name, args.type)


if __name__ == "__main__":
    main()
