#!/usr/bin/env python3
"""
实验数据处理 Pipeline
📌 CSV/JSON 数据 → 清洗 → 统计分析 → 可视化画图 → 导出报告
⚠️ 需要安装: pip install pandas matplotlib seaborn
"""

import argparse
import json
import sys
from pathlib import Path

# Windows 终端 UTF-8 输出
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use("Agg")  # 无 GUI 后端
except ImportError:
    print("❌ 需要安装依赖: pip install pandas matplotlib seaborn")
    sys.exit(1)


def load_data(filepath: str) -> pd.DataFrame:
    """加载 CSV 或 JSON 数据"""
    path = Path(filepath)
    if path.suffix == ".csv":
        return pd.read_csv(filepath)
    elif path.suffix == ".json":
        return pd.read_json(filepath)
    elif path.suffix in (".xlsx", ".xls"):
        return pd.read_excel(filepath)
    else:
        print(f"❌ 不支持的文件格式: {path.suffix}")
        sys.exit(1)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """数据清洗"""
    print(f"  原始数据: {len(df)} 行 × {len(df.columns)} 列")

    # 去除完全重复行
    before = len(df)
    df = df.drop_duplicates()
    if before > len(df):
        print(f"  去重: 删除 {before - len(df)} 行")

    # 去除全空行
    df = df.dropna(how="all")

    # 数值列填充中位数
    numeric_cols = df.select_dtypes(include=["number"]).columns
    for col in numeric_cols:
        null_count = df[col].isnull().sum()
        if null_count > 0:
            median = df[col].median()
            df[col] = df[col].fillna(median)
            print(f"  填充 {col}: {null_count} 个空值 → 中位数 {median:.4f}")

    print(f"  清洗后: {len(df)} 行 × {len(df.columns)} 列")
    return df


def analyze_data(df: pd.DataFrame) -> dict:
    """统计分析"""
    stats = {}

    # 基本统计
    stats["shape"] = df.shape
    stats["describe"] = df.describe().to_string()

    # 各列信息
    stats["columns"] = {}
    for col in df.columns:
        col_info = {
            "dtype": str(df[col].dtype),
            "null": int(df[col].isnull().sum()),
            "unique": int(df[col].nunique()),
        }
        if df[col].dtype in ("int64", "float64"):
            col_info["mean"] = float(df[col].mean())
            col_info["std"] = float(df[col].std())
            col_info["min"] = float(df[col].min())
            col_info["max"] = float(df[col].max())
        stats["columns"][col] = col_info

    return stats


def plot_data(df: pd.DataFrame, output_dir: str, style: str = "default"):
    """生成可视化图表"""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    try:
        plt.style.use(style)
    except Exception:
        pass

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    if not numeric_cols:
        print("  ⚠️ 没有数值列，跳过画图")
        return

    # 1. 数值列分布直方图
    fig, axes = plt.subplots(
        nrows=(len(numeric_cols) + 2) // 3,
        ncols=min(3, len(numeric_cols)),
        figsize=(5 * min(3, len(numeric_cols)), 4 * ((len(numeric_cols) + 2) // 3)),
    )
    if len(numeric_cols) == 1:
        axes = [axes]
    else:
        axes = axes.flatten()

    for i, col in enumerate(numeric_cols):
        axes[i].hist(df[col].dropna(), bins=30, edgecolor="black", alpha=0.7)
        axes[i].set_title(f"{col} 分布")
        axes[i].set_xlabel(col)
        axes[i].set_ylabel("频次")

    # 隐藏多余子图
    for j in range(len(numeric_cols), len(axes)):
        axes[j].set_visible(False)

    plt.tight_layout()
    hist_path = out / "distributions.png"
    plt.savefig(hist_path, dpi=150)
    plt.close()
    print(f"  📊 分布图: {hist_path}")

    # 2. 相关性热力图（至少 2 个数值列）
    if len(numeric_cols) >= 2:
        try:
            import seaborn as sns
            fig, ax = plt.subplots(figsize=(8, 6))
            corr = df[numeric_cols].corr()
            sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
            ax.set_title("特征相关性矩阵")
            plt.tight_layout()
            corr_path = out / "correlation.png"
            plt.savefig(corr_path, dpi=150)
            plt.close()
            print(f"  📊 相关性: {corr_path}")
        except ImportError:
            print("  ⚠️ 未安装 seaborn，跳过相关性热力图")

    # 3. 箱线图
    fig, axes = plt.subplots(1, len(numeric_cols), figsize=(4 * len(numeric_cols), 5))
    if len(numeric_cols) == 1:
        axes = [axes]
    for i, col in enumerate(numeric_cols):
        axes[i].boxplot(df[col].dropna())
        axes[i].set_title(col)
    plt.tight_layout()
    box_path = out / "boxplots.png"
    plt.savefig(box_path, dpi=150)
    plt.close()
    print(f"  📊 箱线图: {box_path}")


def generate_report(stats: dict, output_path: str):
    """生成 Markdown 分析报告"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 实验数据分析报告\n\n")
        f.write(f"## 数据概览\n\n")
        f.write(f"- 数据维度: {stats['shape'][0]} 行 × {stats['shape'][1]} 列\n\n")
        f.write(f"## 描述性统计\n\n```\n{stats['describe']}\n```\n\n")
        f.write(f"## 各列信息\n\n")
        f.write(f"| 列名 | 类型 | 空值 | 唯一值 | 均值 | 标准差 |\n")
        f.write(f"|------|------|------|--------|------|--------|\n")
        for col, info in stats["columns"].items():
            mean = f"{info.get('mean', '-'):.4f}" if "mean" in info else "-"
            std = f"{info.get('std', '-'):.4f}" if "std" in info else "-"
            f.write(f"| {col} | {info['dtype']} | {info['null']} | {info['unique']} | {mean} | {std} |\n")

    print(f"  📄 报告: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="实验数据处理 Pipeline")
    parser.add_argument("input", help="输入数据文件（CSV/JSON/Excel）")
    parser.add_argument("--output", "-o", default="results", help="输出目录")
    parser.add_argument("--step", choices=["all", "clean", "analyze", "plot"],
                        default="all", help="执行步骤")
    parser.add_argument("--plot-style", default="default", help="Matplotlib 画图风格")

    args = parser.parse_args()

    print(f"📂 加载数据: {args.input}")
    df = load_data(args.input)

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    if args.step in ("all", "clean"):
        print("\n🧹 数据清洗:")
        df = clean_data(df)
        cleaned_path = out / "cleaned.csv"
        df.to_csv(cleaned_path, index=False)
        print(f"  💾 已保存: {cleaned_path}")

    if args.step in ("all", "analyze"):
        print("\n📊 统计分析:")
        stats = analyze_data(df)
        print(stats["describe"])
        report_path = out / "report.md"
        generate_report(stats, str(report_path))

    if args.step in ("all", "plot"):
        print("\n🎨 可视化画图:")
        plot_data(df, str(out), args.plot_style)

    print("\n✅ Pipeline 完成！")


if __name__ == "__main__":
    main()
