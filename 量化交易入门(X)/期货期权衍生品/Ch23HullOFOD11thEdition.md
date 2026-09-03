# Ch23 波动率与相关性估计

**相关笔记**: [[Ch22HullOFOD11thEdition|上一章：VaR 与 Expected Shortfall]] | [[Ch24HullOFOD11thEdition|下一章：信用风险]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 23 Estimating Volatilities and Correlations
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：学习历史波动率、EWMA、GARCH、相关性和最大似然估计。

💡 **核心理解**：模型输入的波动率和相关性会直接决定风险和价格，估计方法本身就是风险来源。

本章可以按下面的顺序阅读：
1. Standard Approach to Estimating Volatility (equation 23.1)（波动率）
2. Simplifications Usually Made in Risk Management (equations 23.2 and 23.3)
3. Weighting Scheme (equation 23.4)
4. ARCH(m) Model (equation 23.5)
5. EWMA Model (equation 23.7)（EWMA）
6. To Show that Weights Decline Exponentially
7. Attractions of EWMA（EWMA）
8. GARCH (1,1) equation 23.8（GARCH）
9. GARCH (1,1) continued; equation 23.9（GARCH）
10. Example (Example 23.2)
11. Example continued
12. GARCH (p,q)（GARCH）
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **波动率**：衡量价格变化不确定性的尺度，也是期权定价最关键输入之一。
- **EWMA**：指数加权移动平均，用近期数据更高权重估计波动率。
- **GARCH**：刻画波动率聚集效应的时间序列模型。

---

## 三、逐页整理

### 2. Standard Approach to Estimating Volatility (equation 23.1)（波动率）

**原文要点**
- Define sn as the volatility per day between day n-1 and day n, as estimated at end of day n-1
- Define Si as the value of market variable at end of day i
- Define ui= ln(Si/Si-1)

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 3. Simplifications Usually Made in Risk Management (equations 23.2 and 23.3)

**原文要点**
- Set ui = (Si −Si-1)/Si-1
- Assume that the mean value of ui is zero
- Replace m−1 by m
- This gives

📌 **中文解释**：这一页是“学习历史波动率、EWMA、GARCH、相关性和最大似然估计。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 4. Weighting Scheme (equation 23.4)

**原文要点**
- Instead of assigning equal weights to the observations we can set

📌 **中文解释**：这一页是“学习历史波动率、EWMA、GARCH、相关性和最大似然估计。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 5. ARCH(m) Model (equation 23.5)

**原文要点**
- In an ARCH(m) model we also assign some weight to the long-run variance rate, VL:

📌 **中文解释**：这一页是“学习历史波动率、EWMA、GARCH、相关性和最大似然估计。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 6. EWMA Model (equation 23.7)（EWMA）

**原文要点**
- In an exponentially weighted moving average model, the weights assigned to the u2 decline exponentially as we move back through time
- This leads to

📌 **中文解释**：EWMA/GARCH 用历史收益率估计随时间变化的波动率，重点是波动率聚集。

---

### 7. To Show that Weights Decline Exponentially

📌 **中文解释**：这一页是“学习历史波动率、EWMA、GARCH、相关性和最大似然估计。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 8. Attractions of EWMA（EWMA）

**原文要点**
- Relatively little data needs to be stored
- We need only remember the current estimate of the variance rate and the most recent observation on the market variable
- Tracks volatility changes
- 0.94 is a popular choice for l

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。EWMA/GARCH 用历史收益率估计随时间变化的波动率，重点是波动率聚集。

---

### 9. GARCH (1,1) equation 23.8（GARCH）

**原文要点**
- In GARCH (1,1) we assign some weight to the long-run average variance rate
- Since weights must sum to 1
- g + a + b =1

📌 **中文解释**：EWMA/GARCH 用历史收益率估计随时间变化的波动率，重点是波动率聚集。

---

### 10. GARCH (1,1) continued; equation 23.9（GARCH）

**原文要点**
- Setting w = gV the GARCH (1,1) model is
- and

📌 **中文解释**：EWMA/GARCH 用历史收益率估计随时间变化的波动率，重点是波动率聚集。

---

### 11. Example (Example 23.2)

**原文要点**
- Suppose
- The long-run variance rate is 0.0002 so that the long-run volatility per day is 1.4%

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 12. Example continued

**原文要点**
- Suppose that the current estimate of the volatility is 1.6% per day and the most recent percentage change in the market variable is 1%.
- The new variance rate is
- The new volatility is 1.53% per day

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 13. GARCH (p,q)（GARCH）

📌 **中文解释**：EWMA/GARCH 用历史收益率估计随时间变化的波动率，重点是波动率聚集。

---

### 14. Maximum Likelihood Methods

**原文要点**
- In maximum likelihood methods we choose parameters that maximize the likelihood of the observations occurring

📌 **中文解释**：这一页是“学习历史波动率、EWMA、GARCH、相关性和最大似然估计。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 15. Example 1

**原文要点**
- We observe that a certain event happens one time in ten trials. What is our estimate of the proportion of the time, p, that it happens?
- The probability of the event happening on one particular trial and not on the others is
- We maximize this to obtain a maximum likelihood estimate. Result: p = 0.1 (as expected)

📌 **中文解释**：这一页是“学习历史波动率、EWMA、GARCH、相关性和最大似然估计。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 16. Example 2

**原文要点**
- Estimate the variance of observations from a normal distribution with mean zero

📌 **中文解释**：这一页是“学习历史波动率、EWMA、GARCH、相关性和最大似然估计。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 17. Application to GARCH（GARCH）

**原文要点**
- We choose parameters that maximize

📌 **中文解释**：EWMA/GARCH 用历史收益率估计随时间变化的波动率，重点是波动率聚集。

---

### 18. S&P 500 Excel Application

**原文要点**
- Start with trial values of w, a, and b
- Update variances
- Calculate
- Use solver to search for values of w, a, and b that maximize this objective function
- For efficient operation of Solver: set up spreadsheet so that three numbers that are the same order of magnitude are being searched for

📌 **中文解释**：这一页是“学习历史波动率、EWMA、GARCH、相关性和最大似然估计。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 19. S&P 500 Excel Application (Table 23.1)

**原始表格 / 图示**
| Date | Day | Si | ui=(Si−Si-1)/Si-1 | vi =si2 | −ln(vi ) −ui2 /vi |
|---|---|---|---|---|---|
| 10-Jul-2015 | 1 | 2076.62 |  |  |  |
| 13-Jul-2015 | 2 | 2099.60 | 0.011066 |  |  |
| 14-Jul-2015 | 3 | 2108.95 | 0.004453 | 0.00012246 | 8.8458 |
| 15-Jul-2015 | 4 | 2107.40 | −0.000735 | 0.00009997 | 9.2053 |
| ……. | ….. | ……. | ……….. | …………. | ………… |
| 9-Jul-2020 | 1259 | 3152.05 | −0.005644 | 0.00014276 | 8.6313 |
| Total |  |  |  |  | 10,837.4227 |

📌 **中文解释**：这一页是“学习历史波动率、EWMA、GARCH、相关性和最大似然估计。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 20. Slide 20

**原文要点**
- Estimated Volatility per day (Figure 23.2)

**原始表格 / 图示**
![[Ch23HullOFOD11thEdition/Ch23HullOFOD11thEdition_slide20_1.x-wmf]]

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 21. Variance Targeting

**原文要点**
- One way of implementing GARCH(1,1) that increases stability is by using variance targeting
- We set the long-run average volatility equal to the sample variance
- Only two other parameters then have to be estimated

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。EWMA/GARCH 用历史收益率估计随时间变化的波动率，重点是波动率聚集。

---

### 22. How Good is the Model?

**原文要点**
- The Ljung-Box statistic tests for autocorrelation
- We compare the autocorrelation of the
- ui2 with the autocorrelation of the ui2/si2

📌 **中文解释**：这一页是“学习历史波动率、EWMA、GARCH、相关性和最大似然估计。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 23. Forecasting Future Volatility (equation 23.13)（波动率）

**原文要点**
- A few lines of algebra shows that
- The variance rate for an option expiring on day m is

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 24. Forecasting Future Volatility continued (equation 23.14)（波动率）

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 25. S&P Example

**原始表格 / 图示**
| Option Life (days) | 10 | 30 | 50 | 100 | 500 |
|---|---|---|---|---|---|
| Volatility (% per annum) | 26.5 | 24.9 | 23.8 | 22.0 | 19.5 |

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 26. Volatility Term Structures（波动率）

**原文要点**
- GARCH (1,1) suggests that, when calculating vega, we should shift the long maturity volatilities less than the short maturity volatilities
- When instantaneous volatility changes by Ds(0), volatility for T-day option changes by

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。Vega 表示波动率风险，隐含波动率变化会显著影响期权组合。

---

### 27. Results for S&P 500 (Table 23.4)

**原文要点**
- When instantaneous volatility changes by 1%

**原始表格 / 图示**
| Option Life (days) | 10 | 30 | 50 | 100 | 500 |
|---|---|---|---|---|---|
| Volatility increase (%) | 0.90 | 0.74 | 0.61 | 0.41 | 0.10 |

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 28. Correlations and Covariances

**原文要点**
- Define xi=(Xi−Xi-1)/Xi-1 and yi=(Yi−Yi-1)/Yi-1
- Also
- sx,n: daily vol of X calculated on day n−1
- sy,n: daily vol of Y calculated on day n−1
- covn: covariance calculated on day n−1
- The correlation is covn/(sx,n sy,n)

📌 **中文解释**：这一页是“学习历史波动率、EWMA、GARCH、相关性和最大似然估计。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 29. Updating Correlations

**原文要点**
- We can use similar models to those for volatilities
- Under EWMA
- covn = l covn-1+(1-l)xn-1yn-1

📌 **中文解释**：EWMA/GARCH 用历史收益率估计随时间变化的波动率，重点是波动率聚集。

---

### 30. Positive Finite Definite Condition

**原文要点**
- A variance-covariance matrix, W, is internally consistent if the positive semi-definite condition
- for all vectors w

📌 **中文解释**：这一页是“学习历史波动率、EWMA、GARCH、相关性和最大似然估计。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 31. Example

**原文要点**
- The variance-covariance matrix
- is not internally consistent

📌 **中文解释**：这一页是“学习历史波动率、EWMA、GARCH、相关性和最大似然估计。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
