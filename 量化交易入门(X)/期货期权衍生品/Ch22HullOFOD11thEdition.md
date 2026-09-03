# Ch22 VaR 与 Expected Shortfall

**相关笔记**: [[Ch21HullOFOD11thEdition|上一章：基础数值方法]] | [[Ch23HullOFOD11thEdition|下一章：波动率与相关性估计]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 22 Value at Risk and Expected Shortfall
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：理解风险价值、预期损失、历史模拟、模型法、压力测试和主成分分析。

💡 **核心理解**：VaR 关注分位点损失，ES 关注尾部平均损失；风险管理要看极端情形。

本章可以按下面的顺序阅读：
1. The Question Being Asked in VaR
2. VaR vs. Expected Shortfall（预期损失 ES）
3. VaR and ES
4. Historical Simulation to Calculate the One-Day VaR or ES
5. Historical Simulation continued
6. Example : Calculation of 1-day, 99% VaR or ES for a Portfolio on July 8, 2020 (Table 22.1)
7. Total Return Indices After Adjusting for Exchange Rates (Table 22.2)
8. Scenarios Generated (Table 22.3)
9. Ranked Losses (Table 22.4, page 499)
10. The N-day VaR or ES
11. Stressed VaR and Stressed ES
12. The Model-Building Approach
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **VaR**：在给定置信水平和期限内的分位数损失。
- **ES**：超过 VaR 后尾部损失的条件平均值。
- **波动率**：衡量价格变化不确定性的尺度，也是期权定价最关键输入之一。

---

## 三、逐页整理

### 2. The Question Being Asked in Va R

**原文要点**
- “What loss level is such that we are X% confident it will not be exceeded in N business days?”

📌 **中文解释**：这一页是“理解风险价值、预期损失、历史模拟、模型法、压力测试和主成分分析。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 3. Va R vs. Expected Shortfall（预期损失 ES）

**原文要点**
- VaR is the loss level that will not be exceeded with a specified probability
- Expected Shortfall (or C-VaR) is the expected loss given that the loss is greater than the VaR level
- Although expected shortfall is theoretically more appealing, it is VaR that is used by regulators in setting bank capital requirements

📌 **中文解释**：VaR 给出某个置信水平下的分位数损失，但不告诉超过分位点后会亏多少。ES 关注尾部平均损失，比 VaR 更能体现极端亏损严重程度。

---

### 4. Va R and ES

**原文要点**
- VaR captures an important aspect of risk
- in a single number
- It is easy to understand
- It asks the simple question: “How bad can things get?”
- ES answers the question: “If things do get bad, just how bad will they be”

📌 **中文解释**：VaR 给出某个置信水平下的分位数损失，但不告诉超过分位点后会亏多少。ES 关注尾部平均损失，比 VaR 更能体现极端亏损严重程度。

---

### 5. Historical Simulation to Calculate the One-Day Va R or ES

**原文要点**
- Create a database of the daily movements in all market variables.
- The first simulation trial assumes that the percentage changes in all market variables are as on the first day
- The second simulation trial assumes that the percentage changes in all market variables are as on the second day
- and so on

📌 **中文解释**：ES 关注尾部平均损失，比 VaR 更能体现极端亏损严重程度。

---

### 6. Historical Simulation continued

**原文要点**
- Suppose we use 501 days of historical data (Day 0 to Day 500)
- Let vi be the value of a variable on day i
- There are 500 simulation trials
- The ith trial assumes that the value of the market variable tomorrow is

📌 **中文解释**：这一页是“理解风险价值、预期损失、历史模拟、模型法、压力测试和主成分分析。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 7. Example : Calculation of 1-day, 99% Va R or ES for a Portfolio on July 8, 2020 (Table 22.1)

**原始表格 / 图示**
| Total Return Index | Value ($000s) |
|---|---|
| S&P 500 | 4,000 |
| FTSE 100 | 3,000 |
| CAC 40 | 1,000 |
| Nikkei 225 | 2,000 |

📌 **中文解释**：ES 关注尾部平均损失，比 VaR 更能体现极端亏损严重程度。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 8. Total Return Indices After Adjusting for Exchange Rates (Table 22.2)

**原始表格 / 图示**
| Day | Date | S&P 500 | FTSE 100 | CAC 40 | Nikkei 225 |
|---|---|---|---|---|---|
| 0 | May 9, 2018 | 5,292.90 | 8,830.23 | 16,910.33 | 322.40 |
| 1 | May 10, 2018 | 5,343.70 | 8,926.56 | 16,915.41 | 321.24 |
| 2 | May 11, 2018 | 5,354.69 | 8,982.76 | 17,065.64 | 326.20 |
| 3 | May 14, 2018 | 5,359.66 | 8,999.31 | 17,121.67 | 328.03 |
| … | …… | ….. | ….. | …… | …… |
| 499 | July 7, 2020 | 6,445.59 | 7,269.36 | 15,784.97 | 345.40 |
| 500 | July 8, 2020 | 6,496.14 | 7,255.04 | 15,540.44 | 342.01 |

📌 **中文解释**：这一页是“理解风险价值、预期损失、历史模拟、模型法、压力测试和主成分分析。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 9. Scenarios Generated (Table 22.3)

**原始表格 / 图示**
| Scenario | DJIA | FTSE 100 | CAC 40 | Nikkei 225 | Portfolio  Value ($000s) | Loss ($000s) |
|---|---|---|---|---|---|---|
| 1 | 6,558.49 | 7,334.19 | 15,545.12 | 340.79 | 10,064.257 | −64.257 |
| 2 | 6,509.50 | 7,300.72 | 15,678.46 | 347.28 | 10,066.822 | −66.822 |
| 3 | 6,502.17 | 7,268.41 | 15,591.47 | 343.93 | 10,023.722 | −23.722 |
| … | ……. | ……. | ……. | …….. | ……. | …….. |
| 499 | 6,425.90 | 7,293.40 | 15,543.89 | 341.21 | 9,968.126 | 31.874 |
| 500 | 6,547.09 | 7,240.75 | 15,299.71 | 338.66 | 9,990.361 | 9.639 |

📌 **中文解释**：这一页是“理解风险价值、预期损失、历史模拟、模型法、压力测试和主成分分析。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 10. Ranked Losses (Table 22.4, page 499)

**原文要点**
- 99% one-day VaR
- 99% one day ES is average of the five worst losses or $669,391

**原始表格 / 图示**
| Scenario Number | Loss ($000s) |
|---|---|
| 427 | 922.484 |
| 429 | 858.423 |
| 424 | 653.541 |
| 415 | 490.215 |
| 482 | 422.291 |
| 440 | 362.733 |
| 426 | 360.532 |

📌 **中文解释**：VaR 给出某个置信水平下的分位数损失，但不告诉超过分位点后会亏多少。ES 关注尾部平均损失，比 VaR 更能体现极端亏损严重程度。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 11. The N-day Va R or ES

📌 **中文解释**：ES 关注尾部平均损失，比 VaR 更能体现极端亏损严重程度。

---

### 12. Stressed Va R and Stressed ES

**原文要点**
- Stressed VaR and stressed ES calculations are based on historical data for a stressed period in the past (e.g. the year 2008) rather than on data from the most recent past (as in our example)

📌 **中文解释**：VaR 给出某个置信水平下的分位数损失，但不告诉超过分位点后会亏多少。ES 关注尾部平均损失，比 VaR 更能体现极端亏损严重程度。

---

### 13. The Model-Building Approach

**原文要点**
- The main alternative to historical simulation is to make assumptions about the probability distributions of the return on the market variables and calculate the probability distribution of the change in the value of the portfolio analytically
- This is known as the model building approach or the variance-covariance approach

📌 **中文解释**：这一页是“理解风险价值、预期损失、历史模拟、模型法、压力测试和主成分分析。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 14. Daily Volatilities

**原文要点**
- In option pricing we measure volatility “per year”
- In VaR and ES calculations we measure volatility “per day”

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 15. Daily Volatility continued（波动率）

**原文要点**
- Theoretically, sday is the standard deviation of the continuously compounded return in one day
- In practice we assume that it is the standard deviation of the percentage change in one day

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 16. Microsoft Example

**原文要点**
- We have a position worth $10 million in Microsoft shares
- The volatility of Microsoft is 2% per day (about 32% per year)
- We use N=10 and X=99

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 17. Microsoft Example continued

**原文要点**
- The standard deviation of the change in the portfolio in 1 day is $200,000
- Assume that the expected change is zero (OK for short time periods) and the probability distribution of the change is
- The 1-day 99% VaR is
- The 10-day 99% VaR is

📌 **中文解释**：VaR 给出某个置信水平下的分位数损失，但不告诉超过分位点后会亏多少。

---

### 18. AT&T Example

**原文要点**
- Consider a position of $5 million in AT&T
- The daily volatility of AT&T is 1% (approx 16% per year)
- The 10-day 99% VaR is

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。VaR 给出某个置信水平下的分位数损失，但不告诉超过分位点后会亏多少。

---

### 19. Portfolio

**原文要点**
- Now consider a portfolio consisting of both Microsoft and AT&T
- Assume that the returns of AT&T and Microsoft are bivariate normal
- Suppose that the correlation between the returns is 0.3

📌 **中文解释**：这一页是“理解风险价值、预期损失、历史模拟、模型法、压力测试和主成分分析。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 20. S.D. of Portfolio

**原文要点**
- A standard result in statistics states that
- In this case sX = 200,000 and sY = 50,000 and r = 0.3. The standard deviation of the change in the portfolio value in one day is therefore 220,200

📌 **中文解释**：这一页是“理解风险价值、预期损失、历史模拟、模型法、压力测试和主成分分析。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 21. Va R for Portfolio

**原文要点**
- The 10-day 99% VaR for the portfolio is
- The benefits of diversification are
- (1,471,300+367,800)–1,620,100=$219,00
- What is the incremental effect of the AT&T holding on VaR?

📌 **中文解释**：VaR 给出某个置信水平下的分位数损失，但不告诉超过分位点后会亏多少。

---

### 22. ES for the Model Building Approach (equation 22.1)

**原文要点**
- When the loss over the time horizon has a normal distribution with mean m and standard deviation s, the ES is
- where X is the confidence level and Y is the Xth percentile of a standard normal distribution
- For the Microsoft + AT&T portfolio, ES is $1,856,100

📌 **中文解释**：ES 关注尾部平均损失，比 VaR 更能体现极端亏损严重程度。

---

### 23. The Linear Model

**原文要点**
- This assumes
- The daily change in the value of a portfolio is linearly related to the daily returns from market variables
- The returns from the market variables are normally distributed

📌 **中文解释**：这一页是“理解风险价值、预期损失、历史模拟、模型法、压力测试和主成分分析。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 24. Markowitz Result for Variance of Return on Portfolio

📌 **中文解释**：这一页是“理解风险价值、预期损失、历史模拟、模型法、压力测试和主成分分析。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 25. Va R Result for Variance of Portfolio Value (ai = wi P) equation 22.3

📌 **中文解释**：这一页是“理解风险价值、预期损失、历史模拟、模型法、压力测试和主成分分析。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 26. Covariance Matrix (vari = covii)(Table 22.6)

**原文要点**
- covij = rij si sj where si and sj are the SDs of the daily returns of variables i and j, and rij is the correlation between them

📌 **中文解释**：这一页是“理解风险价值、预期损失、历史模拟、模型法、压力测试和主成分分析。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 27. Alternative Expressions for s P2(equation 22.4)

📌 **中文解释**：这一页是“理解风险价值、预期损失、历史模拟、模型法、压力测试和主成分分析。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 28. Alternatives for Handling Interest Rates（利率）

**原文要点**
- Duration approach: Linear relation between DP and Dy but assumes parallel shifts
- Cash flow mapping: Cash flows are mapped to standard maturities and variables are zero-coupon bond prices with the standard maturities
- Principal components analysis: 2 or 3 independent shifts with their own volatilities

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。零息利率用于直接折现单笔到期现金流，是构建收益率曲线的基础。

---

### 29. When Linear Model Can be Used

**原文要点**
- Portfolio of stocks
- Portfolio of bonds
- Forward contract on foreign currency
- Interest-rate swap

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 30. The Linear Model and Options（期权）

**原文要点**
- Consider a portfolio of options dependent on a single stock price, S. If d is the delta of the option, then it is approximately true that
- Define

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。Delta 衡量标的价格小幅变化对期权价值的影响，也是动态对冲的第一步。

---

### 31. Linear Model and Options continued（期权）

**原文要点**
- Then
- Similarly when there are many underlying market variables
- where di is the delta of the portfolio with respect to the ith asset

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。Delta 衡量标的价格小幅变化对期权价值的影响，也是动态对冲的第一步。

---

### 32. Example

**原文要点**
- Consider an investment in options on Microsoft and AT&T. Suppose the stock prices are 120 and 30 respectively and the deltas of the portfolio with respect to the two stock prices are 1,000 and 20,000 respectively
- As an approximation
- where Dx1 and Dx2 are the percentage changes in the two stock prices

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 33. But the distribution of the daily return on an option is not normal（期权）

**原文要点**
- The linear model fails to capture skewness in the probability distribution of the portfolio value.

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 34. Slide 34

**原文要点**
- Impact of gamma (Figure 22.3)
- Positive Gamma
- Negative Gamma

**原始表格 / 图示**
![[Ch22HullOFOD11thEdition/Ch22HullOFOD11thEdition_slide34_1.jpg]]
![[Ch22HullOFOD11thEdition/Ch22HullOFOD11thEdition_slide34_2.jpg]]
![[Ch22HullOFOD11thEdition/Ch22HullOFOD11thEdition_slide34_1.jpg]]
![[Ch22HullOFOD11thEdition/Ch22HullOFOD11thEdition_slide34_2.jpg]]

📌 **中文解释**：Gamma 衡量 Delta 的变化速度，Gamma 大时对冲需要更频繁调整。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 35. Slide 35

**原文要点**
- Translation of Asset Price Change to Price Change for Long Call (Figure 22.4)

**原始表格 / 图示**
![[Ch22HullOFOD11thEdition/Ch22HullOFOD11thEdition_slide35_1.jpg]]
![[Ch22HullOFOD11thEdition/Ch22HullOFOD11thEdition_slide35_2.jpg]]

📌 **中文解释**：这一页是“理解风险价值、预期损失、历史模拟、模型法、压力测试和主成分分析。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 36. Slide 36

**原文要点**
- Translation of Asset Price Change to Price Change for Short Call (Figure 22.5)

**原始表格 / 图示**
![[Ch22HullOFOD11thEdition/Ch22HullOFOD11thEdition_slide36_1.jpg]]
![[Ch22HullOFOD11thEdition/Ch22HullOFOD11thEdition_slide36_2.jpg]]

📌 **中文解释**：这一页是“理解风险价值、预期损失、历史模拟、模型法、压力测试和主成分分析。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 37. Quadratic Model (equation 22.7)

**原文要点**
- For a portfolio dependent on a single stock price it is approximately true that
- this becomes

📌 **中文解释**：这一页是“理解风险价值、预期损失、历史模拟、模型法、压力测试和主成分分析。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 38. Quadratic Model continued (equation 22.8)

**原文要点**
- With many market variables we get an expression of the form
- where
- But this is much more difficult to work with than the linear model

📌 **中文解释**：这一页是“理解风险价值、预期损失、历史模拟、模型法、压力测试和主成分分析。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 39. Monte Carlo Simulation（蒙特卡罗）

**原文要点**
- To calculate VaR using MC simulation we
- Value portfolio today
- Sample once from the multivariate distributions of the Dxi
- Use the Dxi to determine market variables at end of one day
- Revalue the portfolio at the end of day

📌 **中文解释**：VaR 给出某个置信水平下的分位数损失，但不告诉超过分位点后会亏多少。蒙特卡罗通过模拟大量路径估计期望，适合路径依赖或高维问题。

---

### 40. Monte Carlo Simulation continued（蒙特卡罗）

**原文要点**
- Calculate DP
- Repeat many times to build up a probability distribution for DP
- VaR is the appropriate fractile of the distribution times square root of N
- For example, with 1,000 trials the 1 percentile is the 10th worst case.

📌 **中文解释**：VaR 给出某个置信水平下的分位数损失，但不告诉超过分位点后会亏多少。蒙特卡罗通过模拟大量路径估计期望，适合路径依赖或高维问题。

---

### 41. Speeding up Calculations with the Partial Simulation Approach

**原文要点**
- Use the approximate delta/gamma relationship between DP and the Dxi to calculate the change in value of the portfolio
- This can also be used to speed up the historical simulation approach

📌 **中文解释**：Delta 衡量标的价格小幅变化对期权价值的影响，也是动态对冲的第一步。Gamma 衡量 Delta 的变化速度，Gamma 大时对冲需要更频繁调整。

---

### 42. Comparison of Approaches

**原文要点**
- Model building approach assumes normal distributions for market variables. It tends to give poor results for low delta portfolios
- Historical simulation lets historical data determine distributions, but is computationally slower

📌 **中文解释**：Delta 衡量标的价格小幅变化对期权价值的影响，也是动态对冲的第一步。

---

### 43. Back-Testing

**原文要点**
- Tests how well VaR estimates would have performed in the past
- We could ask the question: How often was the actual 1-day loss greater than the 99%/1- day VaR?

📌 **中文解释**：VaR 给出某个置信水平下的分位数损失，但不告诉超过分位点后会亏多少。

---

### 44. Principal Components Analysis for U.S. Treasury Rates

**原文要点**
- The first factor is a roughly parallel shift (87.3% of variance in data explained)
- The second factor is a twist (another 8.3% of variance explained)
- The third factor is a bowing (another 2.1% of variation explained)

📌 **中文解释**：这一页是“理解风险价值、预期损失、历史模拟、模型法、压力测试和主成分分析。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 45. Slide 45

**原文要点**
- The First Three Principal Components (Figure 22.6)

**原始表格 / 图示**
![[Ch22HullOFOD11thEdition/Ch22HullOFOD11thEdition_slide45_1.x-wmf]]

📌 **中文解释**：这一页是“理解风险价值、预期损失、历史模拟、模型法、压力测试和主成分分析。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 46. Standard Deviation of Factor Scores (bp) Table 22.10

**原始表格 / 图示**
| PC1 | PC2 | PC3 | PC4 | ….. |
|---|---|---|---|---|
| 11.54 | 3.55 | 1.78 | 1.25 | …. |

📌 **中文解释**：这一页是“理解风险价值、预期损失、历史模拟、模型法、压力测试和主成分分析。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 47. Using PCA to Calculate Va R (Table 22.11)

**原文要点**
- Example: Sensitivity of portfolio to 1 bp rate move ($m)
- Sensitivity to first factor is from factor loadings:
- 10×0.210 + 4×0.286 − 8×0.386 − 7 ×0.430 +2 ×0.428
- = −1.99
- Similarly sensitivity to second factor = − 3.06

**原始表格 / 图示**
| 1 yr | 2 yr | 3 yr | 4 yr | 5 yr |
|---|---|---|---|---|
| +10 | +4 | -8 | -7 | +2 |

📌 **中文解释**：这一页是“理解风险价值、预期损失、历史模拟、模型法、压力测试和主成分分析。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 48. Using PCA to calculate Va R continued

📌 **中文解释**：这一页是“理解风险价值、预期损失、历史模拟、模型法、压力测试和主成分分析。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
