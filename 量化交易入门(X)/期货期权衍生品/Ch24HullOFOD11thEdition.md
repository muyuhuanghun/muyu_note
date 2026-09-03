# Ch24 信用风险

**相关笔记**: [[Ch23HullOFOD11thEdition|上一章：波动率与相关性估计]] | [[Ch25HullOFOD11thEdition|下一章：信用衍生品]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 24 Credit Risk
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：理解违约概率、回收率、信用评级迁移、信用 VaR 和交易对手风险。

💡 **核心理解**：信用风险定价的关键变量是违约概率、违约损失和风险暴露。

本章可以按下面的顺序阅读：
1. Credit Ratings
2. Estimating Default Probabilities
3. Historical Data
4. Cumulative Ave Default Rates (%) (1970-2019, S&P, Table 24.1)
5. Interpretation
6. Do Default Probabilities Increase with Time?
7. Conditional vs Unconditional Default Probabilities
8. Hazard Rate
9. Recovery Rate
10. Using Credit Spreads (Equation 24.2)
11. Explanation
12. Matching Bond Prices
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **信用风险**：债务人或交易对手不履约导致损失的风险。
- **VaR**：在给定置信水平和期限内的分位数损失。

---

## 三、逐页整理

### 2. Credit Ratings

**原文要点**
- In the S&P rating system, AAA is the best rating. After that comes AA, A, BBB, BB, B, CCC, CC, and C
- The corresponding Moody’s ratings are Aaa, Aa, A, Baa, Ba, B,Caa, Ca, and C
- Bonds with ratings of BBB (or Baa) and above are considered to be “investment grade”

📌 **中文解释**：这一页是“理解违约概率、回收率、信用评级迁移、信用 VaR 和交易对手风险。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 3. Estimating Default Probabilities

**原文要点**
- Alternatives:
- use historical data
- use credit spreads
- use Merton’s model

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 4. Historical Data

**原文要点**
- Historical data provided by rating agencies are also used to estimate the probability of default

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 5. Cumulative Ave Default Rates (%) (1970-2019, S&P, Table 24.1)

**原始表格 / 图示**
|  | 1yr | 2yr | 3yr | 4yr | 5yr | 7yr | 10yr | 15yr |
|---|---|---|---|---|---|---|---|---|
| AAA | 0.00 | 0.03 | 0.13 | 0.24 | 0.35 | 0.51 | 0.70 | 0.91 |
| AA | 0.02 | 0.06 | 0.12 | 0.21 | 0.31 | 0.50 | 0.72 | 1.02 |
| A | 0.05 | 0.14 | 0.23 | 0.35 | 0.47 | 0.79 | 1.24 | 1.89 |
| BBB | 0.16 | 0.45 | 0.78 | 1.17 | 1.58 | 2.33 | 3.32 | 4.69 |
| BB | 0.61 | 1.92 | 3.48 | 5.05 | 6.52 | 9.01 | 11.78 | 14.67 |
| B | 3.33 | 7.71 | 11.55 | 14.58 | 16.93 | 20.36 | 23.74 | 27.12 |
| CCC/C | 27.08 | 36.64 | 41.41 | 44.10 | 46.19 | 48.26 | 50.38 | 52.59 |

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 6. Interpretation

**原文要点**
- The table shows the probability of default for companies starting with a particular credit rating
- A company with an initial credit rating of BBB has a probability of 0.16% of defaulting by the end of the first year, 0.45% by the end of the second year, and so on

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 7. Do Default Probabilities Increase with Time?

**原文要点**
- For a company that starts with a good credit rating default probabilities tend to increase with time
- For a company that starts with a poor credit rating default probabilities tend to decrease with time

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 8. Conditional vs Unconditional Default Probabilities

**原文要点**
- Probability of a CCC bond defaulting during the third year is 41.41− 36.64 = 4.77%
- This is an unconditional probability (as seen at time zero)
- Probability of a CCC bond defaulting during the third year conditional on no earlier default is 0.0477/0.6336 or 7.53%

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 9. Hazard Rate

**原文要点**
- The hazard rate (also called default density), l(t), at time t is defined so that l(t)Dt is the conditional default probability for a short period between t and t+Dt
- If V(t) is the probability of a company surviving to time t

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 10. Recovery Rate

**原文要点**
- The recovery rate for a bond is usually defined as the price of the bond immediately after default as a percent of its face value
- Recovery rates tend to decrease as default rates increase

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 11. Using Credit Spreads (Equation 24.2)

**原文要点**
- Suppose s(T) is the credit spread for maturity T
- Average hazard rate between time zero and time T is approximately
- where R is the recovery rate
- This estimate is very accurate in most situations

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 12. Explanation

**原文要点**
- Loss rate at time t is l(t)(1−R)
- If the credit spread is compensation for this loss rate it should approximately equal

📌 **中文解释**：这一页是“理解违约概率、回收率、信用评级迁移、信用 VaR 和交易对手风险。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 13. Matching Bond Prices

**原文要点**
- For more accuracy we can work forward in time choosing hazard rates that match bond prices
- This is another application of the bootstrap method

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 14. Real World vs Risk-Neutral Default Probabilities（风险中性测度）

**原文要点**
- The default probabilities backed out of bond prices or credit default swap spreads are risk-neutral default probabilities
- The default probabilities backed out of historical data are real-world default probabilities

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 15. A Comparison

**原文要点**
- Calculate 7-year default intensities from the historical default probabilities
- Estimate default intensities from the credit spreads given by bond yields

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 16. Results published in 2005(Table 24.2)

**原文要点**
- 1 Calculated as−[ln(1-d)]/7 where d is the historical 7 yr default rate.
- 2 Calculated as s/(1-R) where s is the bond yield spread and R is the recovery rate (assumed to be 40%).

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 17. Average Risk Premiums Earned By Bond Traders (Table 24.3)

**原文要点**
- 1 Equals average spread of bond yield over benchmark risk-free rate (e.g. OIS rate, not theTreasury rate)
- 2 Equals historical hazard rate times (1-R) where R is the recovery rate.

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 18. Possible Reasons for the Extra Risk Premium (The third reason is the most important)

**原文要点**
- Corporate bonds are relatively illiquid
- The subjective default probabilities of bond traders may be much higher than the estimates from Moody’s historical data
- Bonds do not default independently of each other. This leads to systematic risk that cannot be diversified away.
- Bond returns are highly skewed with limited upside. The non-systematic risk is difficult to diversify away and may be priced by the market

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 19. Which World Should We Use?

**原文要点**
- We should use risk-neutral estimates for valuing credit derivatives and estimating the present value of the cost of default
- We should use real world estimates for calculating credit VaR and scenario analysis

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 20. Using Equity Prices: Merton’s Model

**原文要点**
- Merton’s model regards the equity as an option on the assets of the firm
- In a simple situation the equity value is
- max(VT −D, 0)
- where VT is the value of the firm and D is the debt repayment required

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 21. Equity vs. Assets

**原文要点**
- The Black-Scholes-Merton option pricing model enables the value of the firm’s equity today, E0, to be related to the value of its assets today, V0, and the volatility of its assets, sV

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。

---

### 22. Volatilities

**原文要点**
- This equation together with the option pricing relationship enables V0 and sV to be determined from E0 and sE

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 23. Example

**原文要点**
- A company’s equity is $3 million and the volatility of the equity is 80%
- The risk-free rate is 5%, the debt is $10 million and time to debt maturity is 1 year
- Solving the two equations yields V0=12.40 and sv=21.23%
- The probability of default is N(−d2) or 12.7%

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 24. The Implementation of Merton’s Model

**原文要点**
- Choose time horizon
- Calculate cumulative obligations to time horizon. This is termed by KMV the “default point”. We denote it by D
- Use Merton’s model to calculate a theoretical probability of default
- Use historical data or bond data to develop a one-to-one mapping of theoretical probability into either real-world or risk-neutral probability of default.

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 25. CVA（信用估值调整）

**原文要点**
- Credit value adjustment (CVA) is the amount by which a dealer must reduce the total value of transactions with a counterparty because of counterparty default risk

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。CVA 把交易对手可能违约造成的损失反映到估值里，是无风险价格到真实交易价格的桥梁。

---

### 26. The CVA Calculation（信用估值调整）

**原文要点**
- Time
- 0
- t1
- t2
- t3
- t4
- tn=T
- Default probability
- for counterparty
- q1
- q2
- q3
- q4
- ………………
- ………………
- qn
- PV of expected loss
- given default
- v1
- v2
- v3
- v4
- vn
- ………………

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。CVA 把交易对手可能违约造成的损失反映到估值里，是无风险价格到真实交易价格的桥梁。

---

### 27. Calculation of qi’s

**原文要点**
- Default probabilities are calculated from credit spreads

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 28. Calculation of vi’s

**原文要点**
- The vi are calculated by simulating the market variables underlying the portfolio in a risk-neutral world
- If no collateral is posted the loss on a particular simulation trial during the ith interval is the PV of (1-R)max(Vi, 0) where Vi is the value of the portfolio at the mid point of the interval
- vi is the average of the losses across all simulation trials

📌 **中文解释**：这一页是“理解违约概率、回收率、信用评级迁移、信用 VaR 和交易对手风险。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 29. Collateral

**原文要点**
- It is usually assumed that the collateral is posted as agreed, and returned as agreed, until N days before a default. The N days are referred to as the “cure period” or “margin period at risk.” Usually N is 10 or 20.
- Suppose that that a portfolio is fully collateralized with no initial margin and its value moves in favor of the dealer during the cure period. Then vi is positive because
- If the portfolio has a positive value to the dealer at the default time, collateral posted by the counterparty is insufficient
- If the portfolio has a negative value to the dealer at the default time, excess collateral posted by the dealer will not be returned

📌 **中文解释**：保证金机制把潜在违约损失提前现金化，是清算体系控制风险的重要手段。信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 30. Incremental CVA（信用估值调整）

**原文要点**
- Results from Monte Carlo are stored so that the incremental impact of a new trade can be calculated without simulating all the other trades.

📌 **中文解释**：CVA 把交易对手可能违约造成的损失反映到估值里，是无风险价格到真实交易价格的桥梁。蒙特卡罗通过模拟大量路径估计期望，适合路径依赖或高维问题。

---

### 31. CVA Risk（信用估值调整）

**原文要点**
- The CVA for a counterparty can be regarded as a complex derivative
- Increasingly, dealers are managing it like any other derivative
- Two sources of risk:
- Changes in counterparty spreads
- Changes in market variables underlying the portfolio

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。CVA 把交易对手可能违约造成的损失反映到估值里，是无风险价格到真实交易价格的桥梁。

---

### 32. Wrong Way/Right Way Risk

**原文要点**
- Simplest assumption is that probability of default qi is independent of net exposure vi.
- Wrong-way risk occurs when qi is positively dependent on vi
- Right-way risk occurs when qi is negatively dependent on vi

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 33. DVA（债务估值调整）

**原文要点**
- Debit (or debt) value adjustment (DVA) is an estimate of the cost to the counterparty of a default by the dealer
- Same formulas apply except that v is counterparty’s loss given a dealer default and q is dealer’s probability of default
- Value of transactions with counterparty = No default value – CVA + DVA

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。CVA 把交易对手可能违约造成的损失反映到估值里，是无风险价格到真实交易价格的桥梁。

---

### 34. DVA continued（债务估值调整）

**原文要点**
- What happens to the reported value of transactions as dealer’s credit spread increases?

📌 **中文解释**：XVA 说明真实交易价格还要考虑信用、融资、保证金和资本占用。

---

### 35. Credit Risk Mitigation（信用风险）

**原文要点**
- Netting
- Collateralization
- Downgrade triggers

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 36. Simple Situation

**原文要点**
- Suppose portfolio with a counterparty consists of a single uncollateralized transaction that always has a positive value to the dealer and provides a payoff at time T
- The CVA adjustment has the effect of multiplying the value of the transaction by e-s(T)T where s(T) is the counterparty’s credit spread for maturity T

📌 **中文解释**：CVA 把交易对手可能违约造成的损失反映到估值里，是无风险价格到真实交易价格的桥梁。

---

### 37. Example 24.5

**原文要点**
- A 2-year uncollateralized option sold by a new counterparty to the dealer has a Black-Scholes-Merton value of $3
- Assume a 2 year zero coupon bond issued by the counterparty has a yield of 1.5% greater than the risk free rate
- If there is no collateral and there are no other transactions between the parties, value of option is 3e-0.015×2=2.91

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。

---

### 38. Uncollateralized Long Forward with Counterparty（远期）

**原文要点**
- For a long forward contract that matures at time T the expected exposure at time t is
- where F0 is the forward price today, K is the delivery price, s is the volatility of the forward price, T is the time to maturity of the forward contract, and r is the risk-free rate

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 39. Example 24.6

**原文要点**
- 2 year forward. Current forward price is $1,600 per ounce. Two one-year intervals
- K = 1,500, s = 20%, R = 0.3, r = 5%
- t1 =0.5, t2=1.5
- Suppose q1 =0.02 and q2=0.03
- v1 = 92.67 and v2 = 130.65
- CVA=0.02×92.67+0.03×130.65 = 5.77
- Value after CVA =
- (1600−1500)e-0.05×2 − 5.77 = 84.71

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。CVA 把交易对手可能违约造成的损失反映到估值里，是无风险价格到真实交易价格的桥梁。

---

### 40. Default Correlation

**原文要点**
- The credit default correlation between two companies is a measure of their tendency to default at about the same time
- Default correlation is important in risk management when analyzing the benefits of credit risk diversification
- It is also important in the valuation of some credit derivatives, eg a first-to-default CDS and CDO tranches.

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。证券化把资产池现金流重新分层出售，关键风险在资产相关性和分层吸收损失的顺序。

---

### 41. Measurement

**原文要点**
- There is no generally accepted measure of default correlation
- Default correlation is a more complex phenomenon than the correlation between two random variables

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。鞅和测度转换用于把定价问题改写成可折现的期望问题。

---

### 42. Survival Time Correlation

**原文要点**
- Define ti as the time to default for company i and Qi(ti) as the cumulative probability distribution for ti
- The default correlation between companies i and j can be defined as the correlation between ti and tj
- But this does not uniquely define the joint probability distribution of default times

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 43. The Gaussian Copula Model

**原文要点**
- 0.2
- 0
- 0.2
- 0.4
- 0.6
- 0.8
- 1
- 1.2
- 0.2
- 0
- 0.2
- 0.4
- 0.6
- 0.8
- 1
- 1.2
- V
- 1
- V
- 2
- 6
- 4
- 2
- 0
- 2
- 4
- 6
- 2
- 4
- 6
- 6
- 4
- 2
- 0
- 2
- 4
- 6
- U
- 1
- U
- 2
- One
- to
- one
- mappings
- Correlation
- Assumption

📌 **中文解释**：这一页是“理解违约概率、回收率、信用评级迁移、信用 VaR 和交易对手风险。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 44. Gaussian Copula Model continued

**原文要点**
- Define a one-to-one correspondence between the time to default, ti, of company i and a variable xi by
- Qi(ti ) = N(xi ) or xi = N-1[Q(ti)]
- where N is the cumulative normal distribution function.
- This is a “percentile to percentile” transformation. The p percentile point of the Qi distribution is transformed to the p percentile point of the xi distribution. xi has a standard normal distribution
- We assume that the xi are multivariate normal. The default correlation measure, rij between companies i and j is the correlation between xi and xj

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。鞅和测度转换用于把定价问题改写成可折现的期望问题。

---

### 45. Example of Use of Gaussian Copula (Example 24.7)

**原文要点**
- Suppose that we wish to simulate the defaults for n companies . For each company the cumulative probabilities of default during the next 1, 2, 3, 4, and 5 years are 1%, 3%, 6%, 10%, and 15%, respectively

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 46. Use of Gaussian Copula continued

**原文要点**
- We sample from a multivariate normal distribution (with appropriate correlations) to get the xi
- Critical values of xi are
- N -1(0.01) = -2.33, N -1(0.03) = -1.88,
- N -1(0.06) = -1.55, N -1(0.10) = -1.28,
- N -1(0.15) = -1.04

📌 **中文解释**：这一页是“理解违约概率、回收率、信用评级迁移、信用 VaR 和交易对手风险。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 47. Use of Gaussian Copula continued

**原文要点**
- When sample for a company is less than
- 2.33, the company defaults in the first year
- When sample is between -2.33 and -1.88, the company defaults in the second year
- When sample is between -1.88 and -1.55, the company defaults in the third year
- When sample is between -1,55 and -1.28, the company defaults in the fourth year
- When sample is between -1.28 and -1.04, the company defaults during the fifth year
- When sample is greater than -1.04, there is no default during the first five years

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 48. A One-Factor Model for the Correlation Structure

**原文要点**
- The correlation between xi and xj is aiaj
- The ith company defaults by time T when xi < N-1[Qi(T)] or
- Conditional on F the probability of this is

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 49. Credit Va R

**原文要点**
- Can be defined analogously to Market Risk VaR
- A T-year credit VaR with an X% confidence is the loss level that we are X% confident will not be exceeded over T years

📌 **中文解释**：VaR 给出某个置信水平下的分位数损失，但不告诉超过分位点后会亏多少。

---

### 50. Calculation from a Factor-Based Gaussian Copula Model (equation 24.10)

**原文要点**
- Consider a large portfolio of loans, each of which has a probability of Q(T) of defaulting by time T. Suppose that all pairwise copula correlations are r so that all ai’s are
- We are X% certain that F is less than
- N−1(1−X) = −N−1(X)
- It follows that the VaR is

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。VaR 给出某个置信水平下的分位数损失，但不告诉超过分位点后会亏多少。

---

### 51. Example 24.8

**原文要点**
- A bank has $100 million of retail exposures
- 1-year probability of default averages 2% and the recovery rate averages 60%
- The copula correlation parameter is 0.1
- 99.9% worst case default rate is
- The one-year 99.9% credit VaR is therefore 100×0.128×(1-0.6) or $5.13 million

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。VaR 给出某个置信水平下的分位数损失，但不告诉超过分位点后会亏多少。

---

### 52. Credit Metrics

**原文要点**
- Calculates credit VaR by considering possible rating transitions
- A Gaussian copula model is used to define the correlation between the ratings transitions of different companies

📌 **中文解释**：VaR 给出某个置信水平下的分位数损失，但不告诉超过分位点后会亏多少。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
