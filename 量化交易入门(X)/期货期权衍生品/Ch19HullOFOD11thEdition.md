# Ch19 希腊字母

**相关笔记**: [[Ch18HullOFOD11thEdition|上一章：期货期权与 Black 模型]] | [[Ch20HullOFOD11thEdition|下一章：波动率微笑与波动率曲面]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 19 The Greek Letters
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：系统整理 Delta、Gamma、Theta、Vega、Rho 及动态对冲。

💡 **核心理解**：希腊字母是期权组合对市场变量的局部敏感度，用来做风险分解和对冲。

本章可以按下面的顺序阅读：
1. Example
2. Naked & Covered Positions
3. Stop-Loss Strategy
4. Slide 5
5. Greek Letters（希腊字母）
6. Delta (See Figure 19.2)（Delta）
7. Hedge（套期保值）
8. Delta Hedging（套期保值）
9. Slide 10
10. Slide 11
11. The Costs in Delta Hedgingcontinued（套期保值）
12. First Scenario for the Example (Table 19.2)
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **Delta**：期权价格对标的价格的一阶敏感度。
- **Gamma**：Delta 对标的价格变化的敏感度。
- **Theta**：期权价值随时间流逝的变化率。
- **Vega**：期权价格对波动率变化的敏感度。
- **Rho**：期权价格对利率变化的敏感度。

---

## 三、逐页整理

### 2. Example

**原文要点**
- A bank has sold for $300,000 a European call option on 100,000 shares of a non-dividend paying stock
- S0 = 49, K = 50, r = 5%, s = 20%,
- T = 20 weeks, m = 13%
- The Black-Scholes-Merton value of the option is $240,000
- How does the bank hedge its risk to lock in a $60,000 profit?

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 3. Naked & Covered Positions

**原文要点**
- Naked position
- Take no action
- Covered position
- Buy 100,000 shares today
- What are the risks associated with these strategies?

📌 **中文解释**：这一页是“系统整理 Delta、Gamma、Theta、Vega、Rho 及动态对冲。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 4. Stop-Loss Strategy

**原文要点**
- This involves:
- Buying 100,000 shares as soon as price reaches $50
- Selling 100,000 shares as soon as price falls below $50

📌 **中文解释**：这一页是“系统整理 Delta、Gamma、Theta、Vega、Rho 及动态对冲。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 5. Slide 5

**原文要点**
- Stop-Loss Strategy continued (Figure 19.1)
- Ignoring discounting, the cost of writing and hedging the option appears to be max(*S*0−K, 0). What are we overlooking?

**原始表格 / 图示**
![[Ch19HullOFOD11thEdition/Ch19HullOFOD11thEdition_slide5_1.x-wmf]]

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 6. Greek Letters（希腊字母）

**原文要点**
- Greek letters are the partial derivatives with respect to the model parameters that are liable to change
- Usually traders use the Black-Scholes-Merton model when calculating partial derivatives
- The volatility parameter in BSM is set equal to the implied volatility when Greek letters are calculated. This is referred to as using the “practitioner Black-Scholes” model

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。

---

### 7. Delta (See Figure 19.2)（Delta）

**原文要点**
- Delta (D) is the rate of change of the option price with respect to the underlying asset price
- Call option price

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 8. Hedge（套期保值）

**原文要点**
- Trader would be hedged with the position:
- short 1000 options
- buy 600 shares
- Gain/loss on the option position is offset by loss/gain on stock position
- Delta changes as stock price changes and time passes
- Hedge position must therefore be rebalanced

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

### 9. Delta Hedging（套期保值）

**原文要点**
- This involves maintaining a delta neutral portfolio
- The delta of a European call on a non-dividend paying stock is N (d 1)
- The delta of a European put on the stock is
- N (d 1) – 1

📌 **中文解释**：套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。Delta 衡量标的价格小幅变化对期权价值的影响，也是动态对冲的第一步。

---

### 10. Slide 10

**原文要点**
- Delta of a Stock Option (K=50, r=0, s = 25%, T=2, Figure 19.3)
- Call
- Put

**原始表格 / 图示**
![[Ch19HullOFOD11thEdition/Ch19HullOFOD11thEdition_slide10_1.jpg]]
![[Ch19HullOFOD11thEdition/Ch19HullOFOD11thEdition_slide10_2.jpg]]
![[Ch19HullOFOD11thEdition/Ch19HullOFOD11thEdition_slide10_1.jpg]]
![[Ch19HullOFOD11thEdition/Ch19HullOFOD11thEdition_slide10_2.jpg]]

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。Delta 衡量标的价格小幅变化对期权价值的影响，也是动态对冲的第一步。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 11. Slide 11

**原文要点**
- Variation of Delta with Time to Maturity(S0=50, r=0, s=25%, Figure 19.4)

**原始表格 / 图示**
![[Ch19HullOFOD11thEdition/Ch19HullOFOD11thEdition_slide11_1.jpg]]

📌 **中文解释**：Delta 衡量标的价格小幅变化对期权价值的影响，也是动态对冲的第一步。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 12. The Costs in Delta Hedgingcontinued（套期保值）

**原文要点**
- Delta hedging a written option involves a “buy high, sell low” trading rule

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

### 13. First Scenario for the Example (Table 19.2)

**原始表格 / 图示**
| Week | Stock price | Delta | Shares purchased | Cost (‘$000) | Cumulative Cost ($000) | Interest |
|---|---|---|---|---|---|---|
| 0 | 49.00 | 0.522 | 52,200 | 2,557.8 | 2,557.8 | 2.5 |
| 1 | 48.12 | 0.458 | (6,400) | (308.0) | 2,252.3 | 2.2 |
| 2 | 47.37 | 0.400 | (5,800) | (274.7) | 1,979.8 | 1.9 |
| ....... | ....... | ....... | ....... | ....... | ....... | ....... |
| 19 | 55.87 | 1.000 | 1,000 | 55.9 | 5,258.2 | 5.1 |
| 20 | 57.25 | 1.000 | 0 | 0 | 5263.3 |  |

📌 **中文解释**：Delta 衡量标的价格小幅变化对期权价值的影响，也是动态对冲的第一步。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 14. Second Scenario for the Example (Table 19.3)

**原始表格 / 图示**
| Week | Stock price | Delta | Shares purchased | Cost (‘$000) | Cumulative Cost ($000) | Interest |
|---|---|---|---|---|---|---|
| 0 | 49.00 | 0.522 | 52,200 | 2,557.8 | 2,557.8 | 2.5 |
| 1 | 49.75 | 0.568 | 4,600 | 228.9 | 2,789.2 | 2.7 |
| 2 | 52.00 | 0.705 | 13,700 | 712.4 | 3,504.3 | 3.4 |
| ....... | ....... | ....... | ....... | ....... | ....... | ....... |
| 19 | 46.63 | 0.007 | (17,600) | (820.7) | 290.0 | 0.3 |
| 20 | 48.12 | 0.000 | (700) | (33.7) | 256.6 |  |

📌 **中文解释**：Delta 衡量标的价格小幅变化对期权价值的影响，也是动态对冲的第一步。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 15. Theta（Theta）

**原文要点**
- Theta (Q) of a derivative (or portfolio of derivatives) is the rate of change of the value with respect to the passage of time
- The theta of a call or put is usually negative. This means that, if time passes with the price of the underlying asset and its volatility remaining the same, the value of a long call or put option declines

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 16. Theta for Call Option (K=50, s = 25%, r = 0, T = 2, Figure 19.5)（期权）

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 17. Slide 17

**原文要点**
- Variation of Theta with Time to Maturity (S0=50, r=0, s=25%, Figure 19.6)

**原始表格 / 图示**
![[Ch19HullOFOD11thEdition/Ch19HullOFOD11thEdition_slide17_1.jpg]]

📌 **中文解释**：Theta 表示时间价值流逝，买期权通常承受时间损耗。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 18. Gamma（Gamma）

**原文要点**
- Gamma (G) is the rate of change of delta (D) with respect to the price of the underlying asset
- Gamma is greatest for options that are close to the money

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。Delta 衡量标的价格小幅变化对期权价值的影响，也是动态对冲的第一步。

---

### 19. Gamma Addresses Delta Hedging Errors Caused By Curvature (Figure 19.7)（套期保值）

**原文要点**
- S
- C
- Stock price
- S'
- Call
- price
- C''
- C'

📌 **中文解释**：套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。Delta 衡量标的价格小幅变化对期权价值的影响，也是动态对冲的第一步。

---

### 20. Interpretation of Gamma（Gamma）

**原文要点**
- For a delta neutral portfolio, DP » Q Dt + ½GDS 2

📌 **中文解释**：Delta 衡量标的价格小幅变化对期权价值的影响，也是动态对冲的第一步。Gamma 衡量 Delta 的变化速度，Gamma 大时对冲需要更频繁调整。

---

### 21. Slide 21

**原文要点**
- Gamma for Call or Put Option: (K=50, s = 25%, r = 0%, T = 2, Figure 19.9)

**原始表格 / 图示**
![[Ch19HullOFOD11thEdition/Ch19HullOFOD11thEdition_slide21_1.jpg]]

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看跌期权对应卖出权，常用于下行保护或表达下跌观点。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 22. Slide 22

**原文要点**
- Variation of Gamma with Time to Maturity (S0=50, r=0, s=25%, Figure 19.10)

**原始表格 / 图示**
![[Ch19HullOFOD11thEdition/Ch19HullOFOD11thEdition_slide22_1.jpg]]

📌 **中文解释**：Gamma 衡量 Delta 的变化速度，Gamma 大时对冲需要更频繁调整。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 23. Relationship Between Delta, Gamma, and Theta (equation 19.4)（Delta）

**原文要点**
- For a portfolio of derivatives on a stock paying a continuous dividend yield at rate *q *it follows from the Black-Scholes-Merton differential equation that

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。

---

### 24. Vega（Vega）

**原文要点**
- Vega (n) is the rate of change of the value of a derivatives portfolio with respect to volatility
- If vega is calculated for a portfolio as a weighted average of the vegas for the individual transactions comprising the portfolio, the result shows the effect of all implied volatilities changing by the same small amount

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。Vega 表示波动率风险，隐含波动率变化会显著影响期权组合。

---

### 25. Slide 25

**原文要点**
- Vega for Call or Put Option (K=50, s = 25%, r = 0, T = 2, Figure 19.11))

**原始表格 / 图示**
![[Ch19HullOFOD11thEdition/Ch19HullOFOD11thEdition_slide25_1.jpg]]

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看跌期权对应卖出权，常用于下行保护或表达下跌观点。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 26. Taylor Series Expansion (Appendix to Chapter 19)

**原文要点**
- The value of a portfolio of derivatives dependent on an asset is a function of of the asset price S, its volatility s, and time t

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 27. Managing Delta, Gamma, & Vega（Delta）

**原文要点**
- Delta can be changed by taking a position in the underlying asset
- To adjust gamma and vega it is necessary to take a position in an option or other derivative

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 28. Example 19.5

**原文要点**
- What position in option 1 and the underlying asset will make the portfolio delta and gamma neutral? Answer: Long 10,000 options, short 6000 of the asset
- What position in option 1 and the underlying asset will make the portfolio delta and vega neutral? Answer: Long 4000 options, short 2400 of the asset

**原始表格 / 图示**
|  | Delta | Gamma | Vega |
|---|---|---|---|
| Portfolio | 0 | −5000 | −8000 |
| Option 1 | 0.6 | 0.5 | 2.0 |
| Option 2 | 0.5 | 0.8 | 1.2 |

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。Delta 衡量标的价格小幅变化对期权价值的影响，也是动态对冲的第一步。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 29. Example 19.5 continued

**原文要点**
- We solve
- −5000+0.5w1 +0.8w2 =0
- −8000+2.0w1 +1.2w2 =0
- to get *w*1* *= 400 and *w**2** *= 6000. We require long positions of 400 and 6000 in option 1 and option 2. A short position of 3240 in the asset is then required to make the portfolio delta neutral

**原始表格 / 图示**
|  | Delta | Gamma | Vega |
|---|---|---|---|
| Portfolio | 0 | −5000 | −8000 |
| Option 1 | 0.6 | 0.5 | 2.0 |
| Option 2 | 0.5 | 0.8 | 1.2 |

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。Delta 衡量标的价格小幅变化对期权价值的影响，也是动态对冲的第一步。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 30. Rho（Rho）

**原文要点**
- Rho is the rate of change of the value of a derivative with respect to the interest rate

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 31. Hedging in Practice（套期保值）

**原文要点**
- Traders usually ensure that their portfolios are delta-neutral at least once a day
- Whenever the opportunity arises, they improve gamma and vega
- There are economies of scale
- As portfolio becomes larger hedging becomes less expensive per option in the portfolio

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

### 32. Scenario Analysis

**原文要点**
- A scenario analysis involves testing the effect on the value of a portfolio of different assumptions concerning asset prices and their volatilities

📌 **中文解释**：这一页是“系统整理 Delta、Gamma、Theta、Vega、Rho 及动态对冲。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 33. Greek Letters for European Options on an Asset that Provides a Yield at Rate q (Table 19.6)（希腊字母）

**原文要点**
- In practice, the volatility, s, is usually set equal to the implied volatility

**原始表格 / 图示**
| Greek Letter | Call Option | Put Option |
|---|---|---|
| Delta |  |  |
| Gamma |  |  |
| Theta |  |  |
| Vega |  |  |
| Rho |  |  |

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 34. Futures Contract Can Be Used for Hedging（套期保值）

**原文要点**
- The delta of a futures contract on an asset paying a yield at rate q is e(r−q)T times the delta of a spot contract
- The position required in futures for delta hedging is therefore e−(r−q)T times the position required in the corresponding spot contract

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

### 35. Hedging vs Creation of an Option Synthetically（套期保值）

**原文要点**
- When we are hedging we take positions that offset delta, gamma, vega, etc
- When we create an option synthetically we take positions that matchdelta, gamma, vega, etc

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

### 36. Portfolio Insurance

**原文要点**
- In October of 1987 many portfolio managers attempted to create a put option on a portfolio synthetically
- This involves initially selling enough of the portfolio (or of index futures) to match the D of the put option

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 37. Portfolio Insurancecontinued

**原文要点**
- As the value of the portfolio increases, the D of the put becomes less negative and some of the original portfolio is repurchased
- As the value of the portfolio decreases, the D of the put becomes more negative and more of the portfolio must be sold

📌 **中文解释**：这一页是“系统整理 Delta、Gamma、Theta、Vega、Rho 及动态对冲。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 38. Portfolio Insurancecontinued

**原文要点**
- The strategy did not work well on October 19, 1987...

📌 **中文解释**：这一页是“系统整理 Delta、Gamma、Theta、Vega、Rho 及动态对冲。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
