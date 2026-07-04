# Ch15 Black-Scholes-Merton 模型

**相关笔记**: [[Ch14HullOFOD11thEdition|上一章：维纳过程与伊藤引理]] | [[Ch16HullOFOD11thEdition|下一章：员工股票期权]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 15 The Black-Scholes-Merton Model
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：掌握 BSM 假设、公式、风险中性定价和隐含波动率。

💡 **核心理解**：BSM 的核心是动态复制：用股票和无风险资产复制期权现金流。

本章可以按下面的顺序阅读：
1. The Stock Price Assumption
2. The Lognormal Property(Equations 15.2 and 15.3)
3. The Lognormal Distribution
4. Continuously Compounded Return (Equations 15.6 and 15.7)
5. The Expected Return
6. m and m −s 2/2
7. Mutual Fund Returns (See Business Snapshot 15.1)
8. The Volatility（波动率）
9. Estimating Volatility from Historical Data（波动率）
10. Nature of Volatility (Business Snapshot 15.2)（波动率）
11. Example
12. The Concepts Underlying Black-Scholes-Merton（Black-Scholes-Merton 模型）
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **Black-Scholes 模型**：经典欧式期权定价模型。
- **风险中性测度**：定价时可用无风险利率折现期望收益的概率测度。
- **波动率**：衡量价格变化不确定性的尺度，也是期权定价最关键输入之一。

---

## 三、逐页整理

### 2. The Stock Price Assumption

**原文要点**
- Consider a stock whose price is S
- In a short period of time of length Dt, the return on the stock is normally distributed:
- where m is expected return and s is volatility

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 3. The Lognormal Property(Equations 15.2 and 15.3)

**原文要点**
- It follows from this assumption that
- Since the logarithm of ST is normal, ST is lognormally distributed

📌 **中文解释**：这一页是“掌握 BSM 假设、公式、风险中性定价和隐含波动率。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 4. The Lognormal Distribution

📌 **中文解释**：这一页是“掌握 BSM 假设、公式、风险中性定价和隐含波动率。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 5. Continuously Compounded Return (Equations 15.6 and 15.7)

**原文要点**
- If x is the realized continuously compounded return

📌 **中文解释**：这一页是“掌握 BSM 假设、公式、风险中性定价和隐含波动率。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 6. The Expected Return

**原文要点**
- The expected value of the stock price is S0emT
- The expected return on the stock is
- m – s 2/2 not m
- This is because
- are not the same

📌 **中文解释**：这一页是“掌握 BSM 假设、公式、风险中性定价和隐含波动率。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 7. m and m −s 2/2

**原文要点**
- m is the expected return in a very short time, Dt, expressed with a compounding frequency of Dt
- m −s2/2 is the expected return in a long period of time expressed with continuous compounding (or, to a good approximation, with a compounding frequency of Dt)

📌 **中文解释**：这一页是“掌握 BSM 假设、公式、风险中性定价和隐含波动率。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 8. Mutual Fund Returns (See Business Snapshot 15.1)

**原文要点**
- Suppose that returns in successive years are 15%, 20%, 30%, −20% and 25% (ann. comp.)
- The arithmetic mean of the returns is 14%
- The returned that would actually be earned over the five years (the geometric mean) is 12.4% (ann. comp.)
- The arithmetic mean of 14% is analogous to m
- The geometric mean of 12.4% is analogous to m−s2/2

📌 **中文解释**：这一页是“掌握 BSM 假设、公式、风险中性定价和隐含波动率。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 9. The Volatility（波动率）

**原文要点**
- The volatility is the standard deviation of the continuously compounded rate of return in 1 year
- The standard deviation of the return in a short time period time Dt is approximately
- If a stock price is $50 and its volatility is 25% per year what is the standard deviation of the price change in one day?

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 10. Estimating Volatility from Historical Data（波动率）

**原文要点**
- Take observations S0, S1, . . . , Sn at intervals of t years (e.g. for weekly data t = 1/52)
- Calculate the continuously compounded return in each interval as:
- Calculate the standard deviation, s , of the ui´s
- The historical volatility estimate is:

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 11. Nature of Volatility (Business Snapshot 15.2)（波动率）

**原文要点**
- Volatility is usually much greater when the market is open (i.e. the asset is trading) than when it is closed
- For this reason time is usually measured in “trading days” not calendar days when options are valued
- It is assumed that there are 252 trading days in one year for most assets

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 12. Example

**原文要点**
- Suppose it is April 1 and an option lasts to April 30 so that the number of days remaining is 30 calendar days or 22 trading days
- The time to maturity would be assumed to be 22/252 = 0.0873 years

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 13. The Concepts Underlying Black-Scholes-Merton（Black-Scholes-Merton 模型）

**原文要点**
- The option price and the stock price depend on the same underlying source of uncertainty
- We can form a portfolio consisting of the stock and the option which eliminates this source of uncertainty
- The portfolio is instantaneously riskless and must instantaneously earn the risk-free rate
- This leads to the Black-Scholes-Merton differential equation

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。

---

### 14. The Derivation of the Black-Scholes-Merton Differential Equation (equation 15.10 and 15.11)（Black-Scholes-Merton 模型）

📌 **中文解释**：Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。

---

### 15. The Derivation of the Black-Scholes-Merton Differential Equation continued (equation 15.12 and 15.13)（Black-Scholes-Merton 模型）

📌 **中文解释**：Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。

---

### 16. The Derivation of the Black-Scholes-Merton Differential Equation continued (equation 15.15 and 5.16)（Black-Scholes-Merton 模型）

📌 **中文解释**：Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。

---

### 17. The Differential Equation

**原文要点**
- Any security whose price is dependent on the stock price satisfies the differential equation
- The particular security being valued is determined by the boundary conditions of the differential equation
- In a forward contract the boundary condition is ƒ = S – K when t =T
- The solution to the equation is
- ƒ = S – K e–r (T – t )

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 18. Perpetual Derivative (equation 15.17)（衍生品）

**原文要点**
- For a perpetual derivative there is no dependence on time and the differential equation becomes
- A derivative that pays off Q when S = H is worth QS/H when S<H and when S>H. (These values satisfy the differential equation and the boundary conditions)

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。

---

### 19. The Black-Scholes-Merton Formulas for Options (equations 15.20 and 15.21))（Black-Scholes-Merton 模型）

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。

---

### 20. Slide 20

**原文要点**
- The N(x) Function
- N(x) is the probability that a normally distributed variable with a mean of zero and a standard deviation of 1 is less than x
- See tables at the end of the book

**原始表格 / 图示**
![[Ch15HullOFOD11thEdition/Ch15HullOFOD11thEdition_slide20_1.x-wmf]]

📌 **中文解释**：这一页是“掌握 BSM 假设、公式、风险中性定价和隐含波动率。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 21. Properties of Black-Scholes Formula（Black-Scholes 模型）

**原文要点**
- As S0 becomes very large c tends to S0 – Ke-rT and p tends to zero
- As S0 becomes very small c tends to zero and p tends to Ke-rT – S0
- What happens as s becomes very large?
- What happens as T becomes very large?

📌 **中文解释**：Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。

---

### 22. Understanding Black-Scholes（Black-Scholes 模型）

📌 **中文解释**：Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。

---

### 23. Risk-Neutral Valuation（风险中性测度）

**原文要点**
- The variable m does not appear in the Black-Scholes-Merton differential equation
- The equation is independent of all variables affected by risk preference
- The solution to the differential equation is therefore the same in a risk-free world as it is in the real world
- This leads to the principle of risk-neutral valuation

📌 **中文解释**：Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。

---

### 24. Applying Risk-Neutral Valuation（风险中性测度）

**原文要点**
- 1. Assume that the expected return from the stock price is the risk-free rate
- 2. Calculate the expected payoff from the option
- 3. Discount at the risk-free rate

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 25. Valuing a Forward Contract with Risk-Neutral Valuation（远期）

**原文要点**
- Payoff is ST – K
- Expected payoff in a risk-neutral world is S0erT – K
- Present value of expected payoff is
- e-rT[S0erT – K] = S0 – Ke-rT

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 26. Proving Black-Scholes-Merton Using Risk-Neutral Valuation (Appendix to Chapter 15)（Black-Scholes-Merton 模型）

**原文要点**
- where g(ST) is the probability density function for the lognormal distribution of ST in a risk-neutral world. ln ST is j(m, s2) where
- We substitute
- so that
- where h is the probability density function for a standard normal. Evaluating the integral leads to the BSM result.

📌 **中文解释**：Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。

---

### 27. Implied Volatility（波动率）

**原文要点**
- The implied volatility of an option is the volatility for which the Black-Scholes-Merton price equals the market price
- There is a one-to-one correspondence between prices and implied volatilities
- Traders and brokers often quote implied volatilities rather than dollar prices

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。

---

### 28. Slide 28

**原文要点**
- The VIX S&P500 Volatility Index (Figure 15.4)
- Chapter 26 explains how the index is calculated

**原始表格 / 图示**
![[Ch15HullOFOD11thEdition/Ch15HullOFOD11thEdition_slide28_1.x-wmf]]

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 29. An Issue of Warrants & Executive Stock Options（期权）

**原文要点**
- When a regular call option is exercised the stock that is delivered must be purchased in the open market
- When a warrant or executive stock option is exercised new Treasury stock is issued by the company
- If little or no benefits are foreseen by the market, the stock price will reduce at the time the issue is announced.
- There is no further dilution (See Business Snapshot 15.3.)

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 30. The Impact of Dilution

**原文要点**
- After the options have been issued it is not necessary to take account of dilution when they are valued
- Before they are issued we can calculate the cost of each option as N/(N+M) times the price of a regular option with the same terms where N is the number of existing shares and M is the number of new shares that will be created if exercise takes place

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 31. Dividends

**原文要点**
- European options on dividend-paying stocks are valued by substituting the stock price less the present value of dividends into Black-Scholes
- Only dividends with ex-dividend dates during life of option should be included
- The “dividend” should be the expected reduction in the stock price expected

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。

---

### 32. American Calls（看涨期权）

**原文要点**
- An American call on a non-dividend-paying stock should never be exercised early
- An American call on a dividend-paying stock should only ever be exercised immediately prior to an ex-dividend date
- Suppose dividend dates are at times t1, t2, …tn. Early exercise is sometimes optimal at time ti if the dividend at that time is greater than

📌 **中文解释**：看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 33. Black’s Approximation for Dealing with Dividends in American Call Options（期权）

**原文要点**
- Set the American price equal to the maximum of two European prices:
- 1. The 1st European price is for an option maturing at the same time as the American option
- 2. The 2nd European price is for an option maturing just before the final ex-dividend date

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
