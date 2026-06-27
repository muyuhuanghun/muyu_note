# 03.科研工具

📌 研究生阶段高频工具，覆盖论文阅读→实验→写作全流程。

# ==========================================
# 📁 脚本列表
# ==========================================

| 脚本 | 功能 | 适用场景 |
|------|------|----------|
| `paper_manager.py` | 论文下载、重命名、归档 | 文献管理 |
| `experiment_data_pipeline.py` | 实验数据清洗→分析→画图→导出 | 数据处理 pipeline |
| `bibtex_manager.py` | BibTeX 参考文献管理 | 论文写作 |
| `arxiv_daily.py` | arXiv 每日论文推送 | 追踪前沿研究 |

# ==========================================
# 🚀 使用示例
# ==========================================

## paper_manager.py — 论文管理

```bash
# 根据 arXiv ID 下载论文并重命名
python paper_manager.py download 2301.07041 --dir ./papers/

# 批量重命名已有 PDF（根据 DOI 或文件名解析）
python paper_manager.py rename ./papers/ --format "{author}_{year}_{title}.pdf"

# 列出所有论文
python paper_manager.py list ./papers/
```

## experiment_data_pipeline.py — 数据处理

```bash
# 完整 pipeline：读取 → 清洗 → 统计 → 画图 → 导出
python experiment_data_pipeline.py data.csv --output results/

# 只做数据清洗
python experiment_data_pipeline.py data.csv --step clean --output cleaned.csv

# 自定义画图样式
python experiment_data_pipeline.py data.csv --plot-style seaborn --output results/
```

⚠️ 需要安装：`pip install pandas matplotlib seaborn`

## bibtex_manager.py — 参考文献

```bash
# 从 DOI 获取 BibTeX 条目
python bibtex_manager.py fetch 10.1109/TPAMI.2023.1234567

# 检查 .bib 文件中的重复条目
python bibtex_manager.py check refs.bib --dedup

# 按作者/年份排序
python bibtex_manager.py sort refs.bib --by year -o sorted.bib
```

## arxiv_daily.py — 每日论文推送

```bash
# 获取今日 cs.CV 类别的论文
python arxiv_daily.py --category cs.CV

# 自定义关键词过滤
python arxiv_daily.py --category cs.AI --keywords "transformer,LLM,agent"

# 输出为 Markdown 格式
python arxiv_daily.py --category cs.AR --format md -o 今日论文.md
```

# ==========================================
# 💡 进阶建议
# ==========================================

- 搭配 Zotero 使用：`paper_manager.py` 管理文件，Zotero 管理元数据
- 实验数据 pipeline 可以封装成 Makefile 或 Snakemake 流程
- arXiv 推送可以配合 cron/Task Scheduler 实现每日自动运行
