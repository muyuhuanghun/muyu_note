# Ch03 期货套期保值策略

**相关笔记**: [[Ch02HullOFOD11thEdition|上一章：期货市场与中央对手方]] | [[Ch04HullOFOD11thEdition|下一章：利率基础]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 3 Hedging Strategies Using Futures
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：学习用期货管理价格风险，包括基差风险、交叉套保和最优套保比率。

💡 **核心理解**：套保的目标是降低不确定性，不是保证盈利；剩余风险主要来自基差和合约不匹配。

本章可以按下面的顺序阅读：
1. Long & Short Hedges（套期保值）
2. Arguments in Favor of Hedging（套期保值）
3. Arguments against Hedging（套期保值）
4. Basis Risk（基差）
5. Long Hedge for Purchase of an Asset（套期保值）
6. Short Hedge for Sale of an Asset（套期保值）
7. Choice of Contract
8. Optimal Hedge Ratio (equation 3.1)（套期保值）
9. Optimal Number of Contracts (equation 3.2)
10. Example (Example 3.3)
11. Example continued
12. Optimal Number of Contracts When Contract Is Settled Daily
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **套期保值**：用衍生品抵消现货或投资组合的价格风险。
- **基差**：现货价格与期货价格之差，是套保残余风险来源。
- **期货**：交易所标准化合约，每日盯市结算，由保证金制度控制违约风险。

---

## 三、逐页整理

### 2. Long & Short Hedges（套期保值）

**原文要点**
- A long futures hedge is appropriate when you know you will purchase an asset in the future and want to lock in the price
- A short futures hedge is appropriate when you know you will sell an asset in the future and want to lock in the price

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

### 3. Arguments in Favor of Hedging（套期保值）

**原文要点**
- Companies should focus on the main business they are in and take steps to minimize risks arising from interest rates, exchange rates, and other market variables

📌 **中文解释**：套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 4. Arguments against Hedging（套期保值）

**原文要点**
- Shareholders are usually well diversified and can make their own hedging decisions
- It may increase risk to hedge when competitors do not
- Explaining a situation where there is a loss on the hedge and a gain on the underlying can be difficult

📌 **中文解释**：套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

### 5. Basis Risk（基差）

**原文要点**
- Basis is usually defined as the spot price minus the futures price
- Basis risk arises because of the uncertainty about the basis when the hedge is closed out

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

### 6. Long Hedge for Purchase of an Asset（套期保值）

**原文要点**
- Define
- F1 : Futures price at time hedge is set up
- F2 : Futures price at time asset is purchased
- S2 : Asset price at time of purchase
- b2 : Basis at time of purchase

**原始表格 / 图示**
| Cost of asset | S2 |
|---|---|
| Gain on Futures | F2 −F1 |
| Net  amount paid | S2  −  (F2 −F1) =F1 + b2 |

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 7. Short Hedge for Sale of an Asset（套期保值）

**原文要点**
- Define
- F1 : Futures price at time hedge is set up
- F2 : Futures price at time asset is sold
- S2 : Asset price at time of sale
- b2 : Basis at time of sale

**原始表格 / 图示**
| Price of asset | S2 |
|---|---|
| Gain on Futures | F1 −F2 |
| Net amount received | S2  +  (F1 −F2) =F1 + b2 |

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 8. Choice of Contract

**原文要点**
- Choose a delivery month that is as close as possible to, but later than, the end of the life of the hedge
- When there is no futures contract on the asset being hedged, choose the contract whose futures price is most highly correlated with the asset price. This is known as cross hedging.

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

### 9. Optimal Hedge Ratio (equation 3.1)（套期保值）

**原文要点**
- Ignoring daily settlement of futures (or assuming forwards are used) , the proportion of the exposure that should optimally be hedged is
- where
- sS is the standard deviation of DS, the change in the spot price during the hedging period,
- sF is the standard deviation of DF, the change in the futures price during the hedging period
- r is the coefficient of correlation between DS and DF.

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 10. Optimal Number of Contracts (equation 3.2)

📌 **中文解释**：这一页是“学习用期货管理价格风险，包括基差风险、交叉套保和最优套保比率。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 11. Example (Example 3.3)

**原文要点**
- Airline will purchase 2 million gallons of jet fuel in one month and hedges using heating oil futures
- From historical data sF =0.0313, sS =0.0263, and r= 0.928

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。

---

### 12. Example continued

**原文要点**
- The size of one heating oil contract is 42,000 gallons
- Optimal number of contracts is
- which rounds to 37

📌 **中文解释**：这一页是“学习用期货管理价格风险，包括基差风险、交叉套保和最优套保比率。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 13. Optimal Number of Contracts When Contract Is Settled Daily

**原始表格 / 图示**
|  | Correlation between percentage daily changes for spot and futures |
|---|---|
|  | SD of percentage daily changes in spot |
|  | SD of percentage daily changes in futures |

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 14. An Alternative Expression for N when there is daily settlement (equation 3.3)

📌 **中文解释**：这一页是“学习用期货管理价格风险，包括基差风险、交叉套保和最优套保比率。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 15. Daily Settlement

**原文要点**
- Day to day changes in N are small and often ignored
- Tailing the hedge involves dividing N by one plus the amount of interest that will be earned over the remaining life of the hedge

📌 **中文解释**：套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

### 16. Hedging Using Index Futures(equation 3.4)（套期保值）

**原文要点**
- To hedge the risk in a portfolio the number of contracts that should be shorted is
- where VA is the value of the portfolio, b is its beta, and VF is the value of one futures contract

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

### 17. Example

**原文要点**
- Index futures price is 1,000
- Value of Portfolio is $5 million
- Beta of portfolio is 1.5
- What position in futures contracts on the index is necessary to hedge the portfolio?

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

### 18. Changing Beta

**原文要点**
- What position is necessary to reduce the beta of the portfolio to 0.75?
- What position is necessary to increase the beta of the portfolio to 2.0?

📌 **中文解释**：这一页是“学习用期货管理价格风险，包括基差风险、交叉套保和最优套保比率。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 19. Why Hedge Equity Returns（套期保值）

**原文要点**
- May want to be out of the market for a while. Hedging avoids the costs of selling and repurchasing the portfolio
- Suppose stocks in your portfolio have an average beta of 1.0, but you feel they have been chosen well and will outperform the market in both good and bad times. Hedging ensures that the return you earn is the risk-free return plus the excess return of your portfolio over the market.

📌 **中文解释**：套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

### 20. Stack and Roll

**原文要点**
- We can roll futures contracts forward to hedge future exposures
- Initially we enter into futures contracts to hedge exposures up to a time horizon
- Just before maturity we close them out an replace them with new contract reflect the new exposure
- etc

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 21. Liquidity Issues (Business Snapshot 3.2)

**原文要点**
- In any hedging situation there is a danger that losses will be realized on the hedge while the gains on the underlying exposure are unrealized
- This can create liquidity problems
- One example is Metallgesellschaft which sold long term fixed-price contracts on heating oil and gasoline and hedged using stack and roll
- The price of oil fell.....

📌 **中文解释**：套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
