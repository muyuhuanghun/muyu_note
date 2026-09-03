# Ch37 衍生品事故与教训

**相关笔记**: [[Ch36HullOFOD11thEdition|上一章：实物期权]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 37 Derivatives Mishaps and What We Can Learn From Them
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：复盘典型衍生品亏损事件，总结风控、模型、授权和流动性教训。

💡 **核心理解**：事故通常不是某个公式错了，而是杠杆、模型误用、监督缺位和流动性同时失控。

本章可以按下面的顺序阅读：
1. Big Losses by Financial Institutions
2. Big Losses by Non-Financial Corporations
3. Lessons for All Users of Derivatives（衍生品）
4. Lessons for Financial Institutions
5. Lessons for Financial Institutions continued
6. Lessons for Non-Financial Corporations

---

## 二、核心概念速记

- **衍生品**：价值依赖股票、利率、汇率、商品等标的资产的金融合约。
- **信用风险**：债务人或交易对手不履约导致损失的风险。
- **VaR**：在给定置信水平和期限内的分位数损失。

---

## 三、逐页整理

### 2. Big Losses by Financial Institutions

**原文要点**
- Allied Irish Bank ($700 million)
- Amaranth ($6 billion)
- Barings ($1 billion)
- Enron Counterparties (Several over $1 billion)
- Kidder Peabody ($350 million)
- LTCM ($4 billion)
- Midland Bank ($500 million)
- Société Générale ($7 billion)
- Subprime Mortgages (many billions)
- UBS ($2.3 billion)

📌 **中文解释**：这一页是“复盘典型衍生品亏损事件，总结风控、模型、授权和流动性教训。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 3. Big Losses by Non-Financial Corporations

**原文要点**
- Allied Lyons ($150 million)
- Gibsons Greetings ($20 million)
- Hammersmith and Fulham ($600 million)
- Metallgesellschaft ($1.8 billion)
- Orange County ($2 billion)
- Procter and Gamble ($90 million)
- Shell ($1 billion)
- Sumitomo ($2 billion)

📌 **中文解释**：这一页是“复盘典型衍生品亏损事件，总结风控、模型、授权和流动性教训。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 4. Lessons for All Users of Derivatives（衍生品）

**原文要点**
- Risk must be quantified and risk limits defined
- Exceeding risk limits not acceptable even when profits result
- Do not assume that a trader with a good track record will always be right
- Be diversified
- Scenario analysis and stress testing is important

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。

---

### 5. Lessons for Financial Institutions

**原文要点**
- Do not give too much independence to star traders
- Separate the front middle and back office
- Models can be wrong
- Be conservative in recognizing inception profits
- Do not sell clients inappropriate products
- Beware of easy profits
- Liquidity risk is important
- There are dangers when many are following the same strategy

📌 **中文解释**：这一页是“复盘典型衍生品亏损事件，总结风控、模型、授权和流动性教训。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 6. Lessons for Financial Institutions continued

**原文要点**
- Beware of potential liquidity problems when long-term funding requirements are financed with short-term liabilities
- Market transparency is important
- Manage incentives
- Never ignore risk management, even when times are good

📌 **中文解释**：这一页是“复盘典型衍生品亏损事件，总结风控、模型、授权和流动性教训。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 7. Lessons for Non-Financial Corporations

**原文要点**
- It is important to fully understand the products you trade
- Beware of hedgers becoming speculators
- It can be dangerous to make the Treasurer’s department a profit center

📌 **中文解释**：这一页是“复盘典型衍生品亏损事件，总结风控、模型、授权和流动性教训。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
