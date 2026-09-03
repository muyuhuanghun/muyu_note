# Ch05 远期和期货价格的确定

**相关笔记**: [[Ch04HullOFOD11thEdition|上一章：利率基础]] | [[Ch06HullOFOD11thEdition|下一章：利率期货]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 5 Determination of Forward and Futures Prices
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：用无套利思想推导远期/期货价格，区分投资资产、消费资产、持有成本和便利收益。

💡 **核心理解**：定价时始终比较两条路径：现在买入并持有，还是签订远期到期交割。

本章可以按下面的顺序阅读：
1. Consumption vs Investment Assets
2. Short Selling
3. Short Selling (continued)
4. Example
5. Notation for Valuing Futures and Forward Contracts（远期合约）
6. An Arbitrage Opportunity?
7. Another Arbitrage Opportunity?
8. The Forward Price (equation 5.1)（远期）
9. If Short Sales Are Not Possible..
10. When an Investment Asset Provides a Known Income (equation 5.2)
11. When an Investment Asset Provides a Known Yield (equation 5.3)
12. Valuing a Forward Contract（远期）
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **远期**：场外定制合约，到期按约定价格买卖标的，信用风险通常更集中。
- **期货**：交易所标准化合约，每日盯市结算，由保证金制度控制违约风险。
- **利率**：衍生品定价中的折现基础，也是重要的可交易风险因子。
- **商品衍生品**：标的为能源、金属、农产品等实物商品的衍生品。
- **便利收益**：持有实物商品带来的非现金收益。

---

## 三、逐页整理

### 2. Consumption vs Investment Assets

**原文要点**
- Investment assets are assets held by significant numbers of people purely for investment purposes (Examples: gold, silver)
- Consumption assets are assets held primarily for consumption (Examples: copper, oil)

📌 **中文解释**：这一页是“用无套利思想推导远期/期货价格，区分投资资产、消费资产、持有成本和便利收益。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 3. Short Selling

**原文要点**
- Short selling involves selling securities you do not own
- Your broker borrows the securities from another client and sells them in the market in the usual way

📌 **中文解释**：这一页是“用无套利思想推导远期/期货价格，区分投资资产、消费资产、持有成本和便利收益。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 4. Short Selling (continued)

**原文要点**
- At some stage you must buy the securities so they can be replaced in the account of the client
- You must pay dividends and other benefits the owner of the securities receives
- There may be a small fee for borrowing the securities

📌 **中文解释**：这一页是“用无套利思想推导远期/期货价格，区分投资资产、消费资产、持有成本和便利收益。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 5. Example

**原文要点**
- You short 100 shares when the price is $100 and close out the short position three months later when the price is $90
- During the three months a dividend of $3 per share is paid
- What is your profit?
- What would be your loss if you had bought 100 shares?

📌 **中文解释**：这一页是“用无套利思想推导远期/期货价格，区分投资资产、消费资产、持有成本和便利收益。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 6. Notation for Valuing Futures and Forward Contracts（远期合约）

**原始表格 / 图示**
| S0: | Spot price today |
|---|---|
| F0: | Futures or forward price today |
| T: | Time until delivery date |
| r: | Risk-free interest rate for maturity T |

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 7. An Arbitrage Opportunity?

**原文要点**
- Suppose that:
- The spot price of a non-dividend-paying stock is $40
- The 3-month forward price is $43
- The 3-month US$ interest rate is 5% per annum
- Is there an arbitrage opportunity?

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 8. Another Arbitrage Opportunity?

**原文要点**
- Suppose that:
- The spot price of non-dividend-paying stock is $40
- The 3-month forward price is US$39
- The 1-year US$ interest rate is 5% per annum (continuously compounded)
- Is there an arbitrage opportunity?

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 9. The Forward Price (equation 5.1)（远期）

**原文要点**
- If the spot price of an investment asset that provides no income is S0 and the futures price for a contract deliverable in T years is F0, then
- F0 = S0erT
- where r is the T-year risk-free rate of interest.
- In our examples, S0 =40, T=0.25, and r=0.05 so that
- F0 = 40e0.05×0.25 = 40.50

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 10. If Short Sales Are Not Possible..

**原文要点**
- Formula still works for an investment asset because investors who hold the asset will sell it and buy forward contracts when the forward price is too low

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 11. When an Investment Asset Provides a Known Income (equation 5.2)

**原文要点**
- F0 = (S0 – I )erT
- where I is the present value of the income during life of forward contract

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 12. When an Investment Asset Provides a Known Yield (equation 5.3)

**原文要点**
- F0 = S0 e(r–q )T
- where q is the average yield during the life of the contract (expressed with continuous compounding)

📌 **中文解释**：这一页是“用无套利思想推导远期/期货价格，区分投资资产、消费资产、持有成本和便利收益。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 13. Valuing a Forward Contract（远期）

**原文要点**
- A forward contract is worth zero (except for bid-offer spread effects) when it is first negotiated
- Later it may have a positive or negative value
- Suppose that K is the delivery price and F0 is the forward price for a contract that would be negotiated today

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 14. Valuing a Forward Contract(equation 5.4)（远期）

**原文要点**
- By considering the difference between a contract with delivery price K and a contract with delivery price F0 we can deduce that:
- the value of a long forward contract is (F0 – K )e–rT
- the value of a short forward contract is
- (K – F0 )e–rT

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 15. Forward vs Futures Prices（期货）

**原文要点**
- When the maturity and asset price are the same, forward and futures prices are usually assumed to be equal. (Eurodollar futures are an exception)
- In theory, when interest rates are uncertain, they are slightly different:
- A strong positive correlation between interest rates and the asset price implies the futures price is slightly higher than the forward price
- A strong negative correlation implies the reverse

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 16. Stock Index (equation 5.8)

**原文要点**
- Can be viewed as an investment asset paying a dividend yield
- The futures price and spot price relationship is therefore
- F0 = S0 e(r–q )T
- where q is the average dividend yield on the portfolio represented by the index during life of contract

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。

---

### 17. Stock Index (continued)

**原文要点**
- For the formula to be true it is important that the index represent an investment asset
- In other words, changes in the index must correspond to changes in the value of a tradable portfolio
- The Nikkei index viewed as a dollar number does not represent an investment asset (See Business Snapshot 5.3)

📌 **中文解释**：这一页是“用无套利思想推导远期/期货价格，区分投资资产、消费资产、持有成本和便利收益。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 18. Index Arbitrage

**原文要点**
- When F0 > S0e(r-q)T an arbitrageur buys the stocks underlying the index and sells futures
- When F0 < S0e(r-q)T an arbitrageur buys futures and shorts or sells the stocks underlying the index

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。

---

### 19. Index Arbitrage(continued)

**原文要点**
- Index arbitrage involves simultaneous trades in futures and many different stocks
- Very often a computer is used to generate the trades
- Occasionally simultaneous trades are not possible and the theoretical no-arbitrage relationship between F0 and S0 does not hold (see Business Snapshot 5.4)

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。

---

### 20. Futures and Forwards on Currencies (equation 5.9)（期货）

**原文要点**
- A foreign currency is analogous to a security providing a yield
- The yield is the foreign risk-free interest rate
- It follows that if rf is the foreign risk-free interest rate

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 21. Explanation of the Relationship Between Spot and Forward (Figure 5.1)（远期）

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 22. Consumption Assets: Storage is Negative Income (equations 5.11 and 5.12)

**原文要点**
- F0  S0 e(r+u )T
- where u is the storage cost per unit time as a percent of the asset value.
- Alternatively,
- F0  (S0+U )erT
- where U is the present value of the storage costs.

📌 **中文解释**：这一页是“用无套利思想推导远期/期货价格，区分投资资产、消费资产、持有成本和便利收益。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 23. The Cost of Carry (equation 5.19)

**原文要点**
- The cost of carry, c, is the storage cost plus the interest costs less the income earned
- For an investment asset F0 = S0ecT
- For a consumption asset F0  S0ecT
- The convenience yield on the consumption asset, y, is defined so that F0 = S0 e(c–y )T

📌 **中文解释**：商品衍生品定价要考虑储存、运输、库存和便利收益，不能完全套用金融资产逻辑。

---

### 24. Futures Prices & Expected Future Spot Prices (equation 5.20)（期货）

**原文要点**
- Suppose k is the expected return required by investors in an asset
- We can invest F0e–r T at the risk-free rate and enter into a long futures contract to create a cash inflow of ST at maturity
- This shows that

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。

---

### 25. Futures Prices & Future Spot Prices (continued)（期货）

**原文要点**
- Positive systematic risk: stock indices
- Negative systematic risk: gold (at least for some periods)

**原始表格 / 图示**
| No Systematic Risk | k = r | F0 = E(ST) |
|---|---|---|
| Positive Systematic Risk | k > r | F0 < E(ST) |
| Negative Systematic Risk | k < r | F0 > E(ST) |

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
