# Ch20 波动率微笑与波动率曲面

**相关笔记**: [[Ch19HullOFOD11thEdition|上一章：希腊字母]] | [[Ch21HullOFOD11thEdition|下一章：基础数值方法]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 20 Volatility Smiles and Volatility Surfaces
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：理解隐含波动率为何随执行价和期限变化，以及波动率曲面的使用。

💡 **核心理解**：市场用不同隐含波动率修正 BSM 的常数波动率假设。

本章可以按下面的顺序阅读：
1. What is a Volatility Smile?（波动率）
2. Why the Volatility Smile is the Same for European Calls and Put（波动率）
3. The Volatility Smile for Foreign Currency Options (Figure 20.1)（波动率）
4. Slide 5
5. Properties of Implied Distribution for Foreign Currency Options（期权）
6. Possible Causes of Volatility Smile for Foreign Currencies（波动率）
7. Historical Analysis of Exchange Rate Changes (Table 20.1)
8. The Volatility Smile for Equity Options (Figure 20.3)（波动率）
9. Slide 10
10. Properties of Implied Distribution for Equity Options（期权）
11. Reasons for Smile in Equity Options（期权）
12. Other Volatility Smiles?（波动率）
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **波动率**：衡量价格变化不确定性的尺度，也是期权定价最关键输入之一。
- **波动率微笑**：不同执行价对应不同隐含波动率的现象。
- **Black-Scholes 模型**：经典欧式期权定价模型。

---

## 三、逐页整理

### 2. What is a Volatility Smile?（波动率）

**原文要点**
- It is the relationship between implied volatility and strike price for options with a certain maturity
- The volatility smile for European call options should be exactly the same as that for European put options
- The same is at least approximately true for American options

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 3. Why the Volatility Smile is the Same for European Calls and Put（波动率）

**原文要点**
- Put-call parity p + S0e−qT = c +K e–rT holds for market prices (pmkt and cmkt) and for Black-Scholes-Merton prices (pbs and cbs)
- As a result, pmkt− pbs=cmkt− cbs
- When pbs = pmkt, it must be true that cbs = cmkt
- It follows that the implied volatility calculated from a European call option should be the same as that calculated from a European put option when both have the same strike price and maturity

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 4. The Volatility Smile for Foreign Currency Options (Figure 20.1)（波动率）

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 5. Slide 5

**原文要点**
- Implied Distribution for Foreign Currency Options (Figure 20.2)

**原始表格 / 图示**
![[Ch20HullOFOD11thEdition/Ch20HullOFOD11thEdition_slide5_1.x-wmf]]

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 6. Properties of Implied Distribution for Foreign Currency Options（期权）

**原文要点**
- Both tails are heavier than the lognormal distribution
- It is also “more peaked” than the lognormal distribution

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 7. Possible Causes of Volatility Smile for Foreign Currencies（波动率）

**原文要点**
- Exchange rate exhibits jumps rather than continuous changes
- Volatility of exchange rate is stochastic

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。波动率微笑/曲面说明市场不完全相信常数波动率和对数正态分布假设。

---

### 8. Historical Analysis of Exchange Rate Changes (Table 20.1)

**原始表格 / 图示**
|  | Real World (%) | Normal Model (%) |
|---|---|---|
| >1 SD | 23.32 | 31.73 |
| >2SD | 4.67 | 4.55 |
| >3SD | 1.30 | 0.27 |
| >4SD | 0.49 | 0.01 |
| >5SD | 0.24 | 0.00 |
| >6SD | 0.13 | 0.00 |

📌 **中文解释**：这一页是“理解隐含波动率为何随执行价和期限变化，以及波动率曲面的使用。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 9. The Volatility Smile for Equity Options (Figure 20.3)（波动率）

**原文要点**
- Implied
- Volatility
- K/S0

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 10. Slide 10

**原文要点**
- Implied Distribution for Equity Options (Figure 20.4)

**原始表格 / 图示**
![[Ch20HullOFOD11thEdition/Ch20HullOFOD11thEdition_slide10_1.x-wmf]]

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 11. Properties of Implied Distribution for Equity Options（期权）

**原文要点**
- The left tail is heavier than the lognormal distribution
- The right tail is less heavy than the lognormal distribution

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 12. Reasons for Smile in Equity Options（期权）

**原文要点**
- There is a negative correlation between equity prices and volatility. Possible reasons:
- Leverage
- Volatility feedback
- Crashophobia
- When the price decreases (increases), volatility tends to increase (decrease) making further decreases (increases) more (less) likely

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 13. Other Volatility Smiles?（波动率）

**原文要点**
- What is the volatility smile if
- True distribution has a less heavy left tail and heavier right tail
- True distribution has both a less heavy left tail and a less heavy right tail

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。波动率微笑/曲面说明市场不完全相信常数波动率和对数正态分布假设。

---

### 14. Ways of Characterizing the Volatility Smiles（波动率）

**原文要点**
- Plot implied volatility against
- Plot implied volatility against
- Note: traders frequently define an option as at-the-money when K equals the forward price, F0, not when it equals the spot price S0
- Plot implied volatility against delta of the option
- Note: traders sometimes define at-the money as a call with a delta of 0.5 or a put with a delta of −0.5. These are referred to as “50-delta options”

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 15. Volatility Term Structure（波动率）

**原文要点**
- In addition to calculating a volatility smile, traders also calculate a volatility term structure
- This shows the variation of implied volatility with the time to maturity of the option
- The volatility term structure tends to be downward sloping when volatility is high and upward sloping when it is low

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 16. Volatility Surface（波动率）

**原文要点**
- The implied volatility as a function of the strike price and time to maturity is known as a volatility surface

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。波动率微笑/曲面说明市场不完全相信常数波动率和对数正态分布假设。

---

### 17. Example of a Volatility Surface(Table 20.2)（波动率）

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。波动率微笑/曲面说明市场不完全相信常数波动率和对数正态分布假设。

---

### 18. Minimum Variance Delta（Delta）

📌 **中文解释**：Delta 衡量标的价格小幅变化对期权价值的影响，也是动态对冲的第一步。

---

### 19. Minimum Variance Delta continued（Delta）

**原文要点**
- In practice the volatility smile tends to move down when the stock price increases (negative correlation)
- The net result of the two effects is that the minimum variance delta is less than the Black-Scholes-Merton delta

📌 **中文解释**：Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。Delta 衡量标的价格小幅变化对期权价值的影响，也是动态对冲的第一步。

---

### 20. Volatility Smiles When a Large Jump is Expected（波动率）

**原文要点**
- At the money implied volatilities are higher that in-the-money or out-of-the-money options (so that the smile is a frown!)

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 21. Determining the Implied Distribution for S (Appendix to Chapter 20)

📌 **中文解释**：这一页是“理解隐含波动率为何随执行价和期限变化，以及波动率曲面的使用。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 22. Slide 22

**原文要点**
- A Geometric Interpretation (Figure 20A.1)
- Assuming that density is g(K) from K−d to K+d, c1 +c3 −c2 = e−rT d2 g(K)

**原始表格 / 图示**
![[Ch20HullOFOD11thEdition/Ch20HullOFOD11thEdition_slide22_1.x-wmf]]

📌 **中文解释**：这一页是“理解隐含波动率为何随执行价和期限变化，以及波动率曲面的使用。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
