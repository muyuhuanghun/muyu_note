# Ch02 期货市场与中央对手方

**相关笔记**: [[Ch01HullOFOD11thEdition|上一章：衍生品导论]] | [[Ch03HullOFOD11thEdition|下一章：期货套期保值策略]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 2 Futures Markets and Central Counterparties
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：理解期货合约、保证金、每日结算、交易所和中央对手方如何降低违约风险。

💡 **核心理解**：期货市场的核心不是预测价格，而是用制度设计把信用风险拆成每日现金流。

本章可以按下面的顺序阅读：
1. Futures Contracts（期货合约）
2. Convergence of Futures to Spot (Figure 2.1)（期货）
3. Margins（保证金）
4. Margin Cash Flows（保证金）
5. Example of a Futures Trade（期货）
6. A Possible Outcome (Table 2.1)
7. Margin Cash Flows When Futures Price Increases（期货）
8. Margin Cash Flows When Futures Price Decreases（期货）
9. Some Terminology
10. Key Points About Futures（期货）
11. Crude Oil Trading on May 21, 2020 (Table 2.2)
12. Delivery
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **期货**：交易所标准化合约，每日盯市结算，由保证金制度控制违约风险。
- **保证金**：为覆盖潜在亏损而存入的履约资金。
- **中央对手方**：站在交易双方中间清算，降低双边信用风险。

---

## 三、逐页整理

### 2. Futures Contracts（期货合约）

**原文要点**
- Available on a wide range of assets
- Exchange traded
- Specifications need to be defined:
- What can be delivered,
- Where it can be delivered, &
- When it can be delivered
- Settled daily

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。

---

### 3. Convergence of Futures to Spot (Figure 2.1)（期货）

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。

---

### 4. Margins（保证金）

**原文要点**
- A margin is cash or marketable securities deposited by an investor with his or her broker
- The balance in the margin account is adjusted to reflect daily settlement
- Margins minimize the possibility of a loss through a default on a contract

📌 **中文解释**：保证金机制把潜在违约损失提前现金化，是清算体系控制风险的重要手段。信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 5. Margin Cash Flows（保证金）

**原文要点**
- A retail trader has to bring the balance in the margin account up to the initial margin when it falls below the maintenance margin level
- A member of the exchange clearing house only has an initial margin and is required to maintain the balance in its account at that level every day.
- These daily margin cash flows are referred to as variation margin
- A member of the exchange is also required to contribute to a default fund

📌 **中文解释**：保证金机制把潜在违约损失提前现金化，是清算体系控制风险的重要手段。信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 6. Example of a Futures Trade（期货）

**原文要点**
- A retail trader takes a long position in 2 December gold futures contracts on June 5
- contract size is 100 oz.
- futures price is US$1,750
- initial margin requirement is US$6,000/contract (US$12,000 in total)
- maintenance margin is US$4,500/contract (US$9,000 in total)

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。保证金机制把潜在违约损失提前现金化，是清算体系控制风险的重要手段。

---

### 7. A Possible Outcome (Table 2.1)

**原始表格 / 图示**
| Day | Trade Price ($) | Settle Price ($) | Daily Gain ($) | Cumul. Gain ($) | Margin Balance ($) | Margin Call ($) |
|---|---|---|---|---|---|---|
| 1 | 1,750.00 |  |  |  | 12,000 |  |
| 1 |  | 1,741.00 | −1,800 | − 1,800 | 10,200 |  |
| 2 |  | 1,738.30 | −540 | −2,340 | 9,660 |  |
| ….. |  | ….. | ….. | ….. | …… |  |
| 6 |  | 1,736.20 | −780 | −2,760 | 9,240 |  |
| 7 |  | 1,729.90 | −1,260 | −4,020 | 7,980 | 4,020 |
| 8 |  | 1,730.80 | 180 | −3,840 | 12,180 |  |
| ….. |  | ….. | ….. | ….. | …… |  |
| 16 | 1,726.90 |  | 780 | −4,620 | 15,180 |  |

📌 **中文解释**：保证金机制把潜在违约损失提前现金化，是清算体系控制风险的重要手段。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 8. Margin Cash Flows When Futures Price Increases（期货）

**原文要点**
- Short Trader

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。保证金机制把潜在违约损失提前现金化，是清算体系控制风险的重要手段。

---

### 9. Margin Cash Flows When Futures Price Decreases（期货）

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。保证金机制把潜在违约损失提前现金化，是清算体系控制风险的重要手段。

---

### 10. Some Terminology

**原文要点**
- Open interest: the total number of contracts outstanding
- equal to number of long positions or number of short positions
- Settlement price: the price just before the final bell each day
- used for the daily settlement process
- Volume of trading: the number of trades in one day

📌 **中文解释**：这一页是“理解期货合约、保证金、每日结算、交易所和中央对手方如何降低违约风险。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 11. Key Points About Futures（期货）

**原文要点**
- They are settled daily
- Closing out a futures position involves entering into an offsetting trade
- Most contracts are closed out before maturity

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。

---

### 12. Crude Oil Trading on May 21, 2020 (Table 2.2)

**原始表格 / 图示**
|  | Open | High | Low | Prior Settle | Last Trade | Change | Volume |
|---|---|---|---|---|---|---|---|
| Jul 2020 | 33.53 | 34.66 | 33.26 | 33.49 | 33.96 | +0.47 | 356,081 |
| Aug 2020 | 33.93 | 35.05 | 33.78 | 33.94 | 34.40 | +0.46 | 118,534 |
| Dec 2020 | 35.18 | 36.08 | 35.06 | 35.23 | 35.76 | +0.53 | 78,825 |
| Dec 2021 | 37.87 | 38.49 | 37.78 | 37.91 | 38.15 | +0.24 | 22,542 |
| Dec 2022 | 40.30 | 40.74 | 39.92 | 40.27 | 40.24 | −0.03 | 3,732 |

📌 **中文解释**：这一页是“理解期货合约、保证金、每日结算、交易所和中央对手方如何降低违约风险。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 13. Delivery

**原文要点**
- If a futures contract is not closed out before maturity, it is usually settled by delivering the assets underlying the contract. When there are alternatives about what is delivered, where it is delivered, and when it is delivered, the party with the short position chooses.
- A few contracts (for example, those on stock indices and Eurodollars) are settled in cash

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。

---

### 14. Questions

**原文要点**
- When a new trade is completed what are the possible effects on the open interest?
- Can the volume of trading in a day be greater than the open interest?

📌 **中文解释**：这一页是“理解期货合约、保证金、每日结算、交易所和中央对手方如何降低违约风险。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 15. Types of Orders

**原文要点**
- Limit
- Stop-loss
- Stop-limit
- Market-if touched
- Discretionary
- Time of day
- Open
- Fill or kill

📌 **中文解释**：这一页是“理解期货合约、保证金、每日结算、交易所和中央对手方如何降低违约风险。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 16. Regulation of Futures（期货）

**原文要点**
- In the US, the regulation of futures markets is primarily the responsibility of the Commodity Futures and Trading Commission (CFTC)
- Regulators try to protect the public interest and prevent questionable trading practices

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。商品衍生品定价要考虑储存、运输、库存和便利收益，不能完全套用金融资产逻辑。

---

### 17. Accounting & Tax

**原文要点**
- Ideally hedging profits (losses) should be recognized at the same time as the losses (profits) on the item being hedged
- Ideally profits and losses from speculation should be recognized on a mark-to-market basis
- Roughly speaking, this is what the accounting and tax treatment of futures in the U.S. and many other countries attempt to achieve

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

### 18. Forward Contracts vs Futures Contracts (Table 2.3)（期货合约）

**原文要点**
- Contract usually closed out

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 19. Foreign Exchange Quotes

**原文要点**
- Futures exchange rates are quoted as the number of USD per unit of the foreign currency
- Forward exchange rates are quoted in the same way as spot exchange rates. This means that GBP, EUR, AUD, and NZD are quoted as USD per unit of foreign currency. Other currencies (e.g., CAD and JPY) are quoted as units of the foreign currency per USD.

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 20. Slide 20

**原文要点**
- OTC Derivatives Transactions: Bilateral Clearing vs Central Clearing

**原始表格 / 图示**
![[Ch02HullOFOD11thEdition/Ch02HullOFOD11thEdition_slide20_1.jpg]]

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。场外交易条款灵活，但必须额外管理交易对手信用、清算和监管报告。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 21. Bilaterally Cleared Derivatives Transactions（衍生品）

**原文要点**
- Usually governed by an ISDA Master agreement with a credit support annex (CSA)
- The agreement explains the rights of one party if the other party defaults
- The CSA defines the collateral which must be posted
- If one party defaults, the other party is entitled to keep any collateral that has been posted up to what is necessary to settle its claims
- Traditionally CSAs have required variation margin but not initial margin (e.g., LTCM in Business Snapshot 2.2)

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。保证金机制把潜在违约损失提前现金化，是清算体系控制风险的重要手段。

---

### 22. Post-Crisis Regulations 1

**原文要点**
- Standard transactions between financial institutions must be cleared through CCPs
- Non-standard transactions can be cleared bilaterally
- A transaction with a non-financial corporation can be cleared bilaterally

📌 **中文解释**：中央对手方通过保证金、盯市和清算会员制度降低双边违约风险。

---

### 23. Post-Crisis Regulations 2

**原文要点**
- New regulations for non-standard trades between financial institutions that are not cleared centrally require the financial institutions to have CSAs where both initial margin and variation margin are posted
- The initial margin is posted with a third party

📌 **中文解释**：保证金机制把潜在违约损失提前现金化，是清算体系控制风险的重要手段。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
