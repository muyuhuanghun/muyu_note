# Ch13 二叉树

**相关笔记**: [[Ch12HullOFOD11thEdition|上一章：期权交易策略]] | [[Ch14HullOFOD11thEdition|下一章：维纳过程与伊藤引理]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 13 Binomial Trees
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：用离散树模型理解风险中性定价、复制组合和美式期权回溯定价。

💡 **核心理解**：二叉树是把连续的不确定性拆成一格一格的路径，再从到期收益向前折现。

本章可以按下面的顺序阅读：
1. A Simple Binomial Model（二叉树）
2. A Call Option (Figure 13.1)（期权）
3. Setting Up a Riskless Portfolio
4. Valuing the Portfolio(Risk-Free Rate is 4%)
5. Valuing the Option（期权）
6. Generalization (Figure 13.2)
7. Generalization (continued)
8. Generalization (continued)
9. Generalization continued (equation 13.2 and 13.3)
10. p as a Probability
11. Risk-Neutral Valuation（风险中性测度）
12. Original Example Revisited
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **二叉树**：每一步价格只上/下两个状态的离散定价模型。
- **期权**：买方支付权利金，获得未来按执行价买入或卖出标的的权利。
- **风险中性测度**：定价时可用无风险利率折现期望收益的概率测度。

---

## 三、逐页整理

### 2. A Simple Binomial Model（二叉树）

**原文要点**
- A stock price is currently $20
- In 3 months it will be either $22 or $18

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 3. A Call Option (Figure 13.1)（期权）

**原文要点**
- A 3-month call option on the stock has a strike price of 21.
- Stock Price = $18
- Option Payoff = $0

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 4. Setting Up a Riskless Portfolio

**原文要点**
- For a portfolio that is long D shares and a short 1 call option values are
- Portfolio is riskless when 22D – 1 = 18D or D = 0.25

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 5. Valuing the Portfolio(Risk-Free Rate is 4%)

**原文要点**
- The riskless portfolio is:
- long 0.25 shares
- short 1 call option
- The value of the portfolio in 3 months is
- 22 ×0.25 – 1 = 4.50
- The value of the portfolio today is
- 4.5e–0.04×0.25 = 4.455

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 6. Valuing the Option（期权）

**原文要点**
- The portfolio that is
- long 0.25 shares
- short 1 option
- is worth 4.455
- The value of the shares is 5.000 (= 0.25 × 20 )
- The value of the option is therefore
- 5.000 – 4.455 = 0.545

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 7. Generalization (Figure 13.2)

**原文要点**
- A derivative lasts for time T and is dependent on a stock

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。

---

### 8. Generalization (continued)

**原文要点**
- Value of a portfolio that is long D shares and short 1 derivative:
- The portfolio is riskless when S0uD – ƒu = S0dD – ƒd or
- S0uD – ƒu
- S0dD – ƒd

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。

---

### 9. Generalization (continued)

**原文要点**
- Value of the portfolio at time T is S0uD – ƒu
- Value of the portfolio today is (S0uD – ƒu)e–rT
- Another expression for the portfolio value today is S0D – f
- Hence
- ƒ = S0D – (S0uD – ƒu )e–rT

📌 **中文解释**：这一页是“用离散树模型理解风险中性定价、复制组合和美式期权回溯定价。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 10. Generalization continued (equation 13.2 and 13.3)

**原文要点**
- Substituting for D we obtain
- ƒ = [ pƒu + (1 – p)ƒd ]e–rT
- where

📌 **中文解释**：这一页是“用离散树模型理解风险中性定价、复制组合和美式期权回溯定价。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 11. p as a Probability

**原文要点**
- It is natural to interpret p and 1-p as probabilities of up and down movements
- The value of a derivative is then its expected payoff in a risk-neutral world discounted at the risk-free rate

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。

---

### 12. Risk-Neutral Valuation（风险中性测度）

**原文要点**
- When the probability of an up and down movements are p and 1-p the expected stock price at time T is S0erT
- This shows that the stock price earns the risk-free rate
- Binomial trees illustrate the general result that to value a derivative we can assume that the expected return on the underlying asset is the risk-free rate and discount at the risk-free rate
- This is known as using risk-neutral valuation

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 13. Original Example Revisited

**原文要点**
- p is the probability that gives a return on the stock equal to the risk-free rate:
- 20e 0.04 ×0.25 = 22p + 18(1 – p ) so that p = 0.5503
- Alternatively:

📌 **中文解释**：这一页是“用离散树模型理解风险中性定价、复制组合和美式期权回溯定价。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 14. Valuing the Option Using Risk-Neutral Valuation（期权）

**原文要点**
- The value of the option is
- e–0.04×0.25 (0.5503 ×1 + 0.4497×0)
- = 0.545

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 15. Irrelevance of Stock’s Expected Return

**原文要点**
- When we are valuing an option in terms of the price of the underlying asset, the probability of up and down movements in the real world are irrelevant
- This is an example of a more general result stating that the expected return on the underlying asset in the real world is irrelevant

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 16. A Two-Step Example Figure 13.3

**原文要点**
- K=21, r = 4%
- Each time step is 3 months

📌 **中文解释**：这一页是“用离散树模型理解风险中性定价、复制组合和美式期权回溯定价。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 17. Valuing a Call Option Figure 13.4（期权）

**原文要点**
- Value at node B
- = e–0.04×0.25(0.5503×3.2 + 0.4497×0) = 1.7433
- Value at node A
- = e–0.04×0.25(0.5503×1.7433 + 0.4497×0) = 0.9497

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 18. A Put Option Example Figure 13.7（期权）

**原文要点**
- K = 52, time step =1yr
- r = 5%, u =1.2, d = 0.8, p = 0.6282

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看跌期权对应卖出权，常用于下行保护或表达下跌观点。

---

### 19. What Happens When the Put Option is American (Figure 13.8)（期权）

**原文要点**
- The American feature increases the value at node C from 9.4636 to 12.0000.
- This increases the value of the option from 4.1923 to 5.0894.

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看跌期权对应卖出权，常用于下行保护或表达下跌观点。

---

### 20. Delta（Delta）

**原文要点**
- Delta (D) is the ratio of the change in the price of a stock option to the change in the price of the underlying stock
- The value of D varies from node to node

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。Delta 衡量标的价格小幅变化对期权价值的影响，也是动态对冲的第一步。

---

### 21. Choosing u and d (equations 13.15 and 13.16)

**原文要点**
- One way of matching the volatility is to set
- where s is the volatility and Dt is the length of the time step. This is the approach used by Cox, Ross, and Rubinstein

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 22. Girsanov’s Theorem

**原文要点**
- Volatility is the same in the real world and the risk-neutral world
- We can therefore measure volatility in the real world and use it to build a tree for the an asset in the risk-neutral world

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 23. Assets Other than Non-Dividend Paying Stocks

**原文要点**
- For options on stock indices, currencies and futures the basic procedure for constructing the tree is the same except for the calculation of p

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 24. The Probability of an Up Move

📌 **中文解释**：这一页是“用离散树模型理解风险中性定价、复制组合和美式期权回溯定价。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 25. Proving Black-Scholes-Merton from Binomial Trees (Appendix to Chapter 13)（Black-Scholes-Merton 模型）

**原文要点**
- Option is in the money when j > a where
- so that

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 26. Proving Black-Scholes-Merton from Binomial Trees continued（Black-Scholes-Merton 模型）

**原文要点**
- The expression for U1 can be written
- where
- Both U1 and U2 can now be evaluated in terms of the cumulative binomial distribution
- We now let the number of time steps tend to infinity and use the result that a binomial distribution tends to a normal distribution

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
