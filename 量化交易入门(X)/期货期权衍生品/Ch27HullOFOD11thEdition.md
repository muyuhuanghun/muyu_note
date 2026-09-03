# Ch27 模型与数值方法进阶

**相关笔记**: [[Ch26HullOFOD11thEdition|上一章：奇异期权]] | [[Ch28HullOFOD11thEdition|下一章：鞅与测度]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 27 More on Models and Numerical Procedures
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：学习更复杂的树、Monte Carlo 技巧、跳跃扩散和随机波动率模型。

💡 **核心理解**：模型越贴近市场现象，校准和计算成本通常越高。

本章可以按下面的顺序阅读：
1. Time Varying Volatility（波动率）
2. Three Alternatives to Geometric Brownian Motion
3. CEV Model
4. CEV Models Implied Volatilities
5. Mixed Jump Diffusion Model
6. Simulating a Jump Process
7. Jumps and the Smile
8. The Variance-Gamma Model（Gamma）
9. Understanding the Variance-Gamma Model（Gamma）
10. Stochastic Volatility Models (equations 27.2 and 27.3)（波动率）
11. Stochastic Volatility Models continued（波动率）
12. SABR Model
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **蒙特卡罗**：用大量随机路径估计衍生品期望价值。
- **期权**：买方支付权利金，获得未来按执行价买入或卖出标的的权利。
- **波动率**：衡量价格变化不确定性的尺度，也是期权定价最关键输入之一。

---

## 三、逐页整理

### 2. Time Varying Volatility（波动率）

**原文要点**
- The variance rate substituted into BSM should be the average variance rate
- Suppose the volatility is s1 for the first year and s2 for the second and third
- Total accumulated variance at the end of three years is s12 + 2s22
- The 3-year average volatility is given by

📌 **中文解释**：Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 3. Three Alternatives to Geometric Brownian Motion

**原文要点**
- Constant elasticity of variance (CEV)
- Mixed Jump diffusion
- Variance Gamma

📌 **中文解释**：维纳过程是连续时间随机波动的基本构件，后续 BSM 和利率模型都会用到。Gamma 衡量 Delta 的变化速度，Gamma 大时对冲需要更频繁调整。

---

### 4. CEV Model

📌 **中文解释**：这一页是“学习更复杂的树、Monte Carlo 技巧、跳跃扩散和随机波动率模型。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 5. CEV Models Implied Volatilities

**原文要点**
- K

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 6. Mixed Jump Diffusion Model

**原文要点**
- Merton produced a pricing formula when the asset price follows a diffusion process overlaid with random jumps
- dp is the random jump
- k is the expected size of the jump
- l dt is the probability that a jump occurs in the next interval of length dt
- lk is the expected return from jumps

📌 **中文解释**：这一页是“学习更复杂的树、Monte Carlo 技巧、跳跃扩散和随机波动率模型。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 7. Simulating a Jump Process

**原文要点**
- In each time step
- Sample from a binomial distribution to determine the number of jumps
- Sample to determine the size of each jump

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 8. Jumps and the Smile

**原文要点**
- Jumps have a big effect on the implied volatility of short term options
- They have a much smaller effect on the implied volatility of long term options

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 9. The Variance-Gamma Model（Gamma）

**原文要点**
- Define g as change over time T in a variable that follows a gamma process. This is a process where small jumps occur frequently and there are occasional large jumps
- Conditional on g, ln ST is normal. Its variance proportional to g
- There are 3 parameters
- v, the variance rate of the gamma process
- s2, the average variance rate of ln S per unit time
- q, a parameter defining skewness

📌 **中文解释**：Gamma 衡量 Delta 的变化速度，Gamma 大时对冲需要更频繁调整。

---

### 10. Understanding the Variance-Gamma Model（Gamma）

**原文要点**
- g defines the rate at which information arrives during time T (g is sometimes referred to as measuring economic time)
- If g is large the change in ln S has a relatively large mean and variance
- If g is small relatively little information arrives and the change in ln S has a relatively small mean and variance

📌 **中文解释**：Gamma 衡量 Delta 的变化速度，Gamma 大时对冲需要更频繁调整。

---

### 11. Stochastic Volatility Models (equations 27.2 and 27.3)（波动率）

**原文要点**
- When V and S are uncorrelated a European option price is the Black-Scholes-Merton price integrated over the distribution of the average variance rate

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。

---

### 12. Stochastic Volatility Models continued（波动率）

**原文要点**
- When V and S are negatively correlated we obtain a downward sloping volatility skew similar to that observed in the market for equities
- When V and S are positively correlated the skew is upward sloping. (This pattern is sometimes observed for commodities)

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 13. SABR Model

**原文要点**
- Typically practitioners estimate parameters for each maturity.
- There are good analytic approximations for the implied volatility
- Can match many different volatility smiles

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。波动率微笑/曲面说明市场不完全相信常数波动率和对数正态分布假设。

---

### 14. Rough Volatility Model（波动率）

**原文要点**
- The variance rate is assumed to follow fractional Brownian motion with a Hurst exponent less than 0.5
- This fits the observed behavior of stock indices fairly well
- It also can be fitted better than some other stochastic volatility models to the volatility surfaces that are observed in practice

📌 **中文解释**：维纳过程是连续时间随机波动的基本构件，后续 BSM 和利率模型都会用到。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 15. The IVF Model

📌 **中文解释**：这一页是“学习更复杂的树、Monte Carlo 技巧、跳跃扩散和随机波动率模型。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 16. The Volatility Function (equation 27.4)（波动率）

**原文要点**
- The volatility function that leads to the model matching all European option prices is

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 17. Strengths and Weaknesses of the IVF Model

**原文要点**
- The model matches the probability distribution of asset prices assumed by the market at each future time
- The models does not necessarily give reasonable values for the joint probability distribution of asset prices at two or more times

📌 **中文解释**：这一页是“学习更复杂的树、Monte Carlo 技巧、跳跃扩散和随机波动率模型。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 18. Convertible Bonds (Section 27.4)

**原文要点**
- Often valued with a tree where during a time interval Dt there is
- a probability pu of an up movement
- A probability pd of a down movement
- A probability 1-exp(-lt) that there will be a default (l is the hazard rate)
- In the event of a default the stock price falls to zero and there is a recovery on the bond

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 19. The Probabilities

📌 **中文解释**：这一页是“学习更复杂的树、Monte Carlo 技巧、跳跃扩散和随机波动率模型。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 20. Node Calculations

**原文要点**
- Define:
- Q1: value of bond if neither converted nor called
- Q2: value of bond if called
- Q3: value of bond if converted
- Bond is called if Q2<Q1
- Bond is converted if Q3>min(Q1,Q2)

📌 **中文解释**：这一页是“学习更复杂的树、Monte Carlo 技巧、跳跃扩散和随机波动率模型。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 21. Example 27.1

**原文要点**
- 9-month zero-coupon bond with face value of $100
- Convertible into 2 shares
- Callable for $113 at any time
- Initial stock price = $50,
- volatility = 30%,
- no dividends
- Risk-free rates all 5%
- Default intensity, l, is 1%
- Recovery rate=40%

📌 **中文解释**：零息利率用于直接折现单笔到期现金流，是构建收益率曲线的基础。信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 22. The Tree (Figure 27.2)

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 23. Numerical Procedures

**原文要点**
- Topics:
- Path dependent options using tree
- Barrier options
- Options where there are two stochastic variables
- American options using Monte Carlo

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 24. Path Dependence: The Traditional View

**原文要点**
- Trees work well for American options. They cannot be used for path-dependent options
- Monte Carlo simulation works well for path-dependent options; it cannot be used for American options

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 25. Extending the Use of Trees

**原文要点**
- Backwards induction can be used for some path-dependent options
- We will first illustrate the methodology using lookback options and then show how it can be used for Asian options

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 26. Lookback Example

**原文要点**
- Consider an American lookback put on a stock where
- S = 50, s = 40%, r = 10%, Dt = 1 month & the life of the option is 3 months
- Payoff is Smax-ST
- We can value the deal by considering all possible values of the maximum stock price at each node
- (This example is presented to illustrate the methodology. It is not the most efficient way of handling American lookbacks (See Technical Note 13)

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 27. Example: An American Lookback Put Option（期权）

**原文要点**
- S0 = 50, s = 40%, r = 10%, Dt = 1 month,
- Top number is stock price
- Middle numbers are alternative maximum stock prices
- Lower numbers are option prices

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看跌期权对应卖出权，常用于下行保护或表达下跌观点。

---

### 28. Why the Approach Works

**原文要点**
- This approach works for lookback options because
- The payoff depends on just 1 function of the path followed by the stock price. (We will refer to this as a “path function”)
- The value of the path function at a node can be calculated from the stock price at the node and from the value of the function at the immediately preceding node
- The number of different values of the path function at a node does not grow too fast as we increase the number of time steps on the tree

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 29. Extensions of the Approach

**原文要点**
- The approach can be extended so that there are no limits on the number of alternative values of the path function at a node
- The basic idea is that it is not necessary to consider every possible value of the path function
- It is sufficient to consider a relatively small number of representative values of the function at each node

📌 **中文解释**：这一页是“学习更复杂的树、Monte Carlo 技巧、跳跃扩散和随机波动率模型。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 30. Working Forward（远期）

**原文要点**
- First work forward through the tree calculating the max and min values of the “path function” at each node
- Next choose representative values of the path function that span the range between the min and the max
- Simplest approach: choose the min, the max, and N equally spaced values between the min and max

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 31. Backwards Induction

**原文要点**
- We work backwards through the tree in the usual way carrying out calculations for each of the alternative values of the path function that are considered at a node
- When we require the value of the derivative at a node for a value of the path function that is not explicitly considered at that node, we use linear or quadratic interpolation

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 32. Part of Tree to Calculate Value of an Option on the Arithmetic Average(Figure 27.3)（期权）

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 33. Part of Tree to Calculate Value of an Option on the Arithmetic Average (continued)（期权）

**原文要点**
- Consider Node X when the average of 5 observations is 51.44
- Node Y: If this is reached, the average becomes 51.98. The option price is interpolated as 8.247
- Node Z: If this is reached, the average becomes 50.49. The option price is interpolated as 4.182
- Node X: value is
- (0.5056×8.247 + 0.4944×4.182)e–0.1×0.05 = 6.206

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 34. Using Trees with Barriers(Section 27.6)（障碍期权）

**原文要点**
- When trees are used to value options with barriers, convergence tends to be slow
- The slow convergence arises from the fact that the barrier is inaccurately specified by the tree

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 35. True Barrier vs Tree Barrier for a Knockout Option: The Binomial Tree Case（期权）

**原文要点**
- Tree Barrier
- True Barrier

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 36. Inner and Outer Barriers for Trinomial Trees (Figure 27.4)（障碍期权）

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 37. Alternative Solutions to Valuing Barrier Options（期权）

**原文要点**
- Interpolate between value when inner barrier is assumed and value when outer barrier is assumed
- Ensure that nodes always lie on the barriers
- Use adaptive mesh methodology
- In all cases a trinomial tree is preferable to a binomial tree

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 38. Modeling Two Correlated Variables Using a 3-Dimensional Tree (Section 27.7)

**原文要点**
- Approaches
- Transform variables so that they are not correlated and build the tree in the transformed variables
- Take the correlation into account by adjusting the position of the nodes
- Take the correlation into account by adjusting the probabilities

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 39. Monte Carlo Simulation and American Options（期权）

**原文要点**
- Two approaches:
- The least squares approach
- The exercise boundary parameterization approach
- Consider a 3-year put option where the initial asset price is 1.00, the strike price is 1.10, the risk-free rate is 6%, and there is no income

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看跌期权对应卖出权，常用于下行保护或表达下跌观点。

---

### 40. Sampled Paths (Table 27.4)

**原始表格 / 图示**
| Path | t = 0 | t =1 | t =2 | t =3 |
|---|---|---|---|---|
| 1 | 1.00 | 1.09 | 1.08 | 1.34 |
| 2 | 1.00 | 1.16 | 1.26 | 1.54 |
| 3 | 1.00 | 1.22 | 1.07 | 1.03 |
| 4 | 1.00 | 0.93 | 0.97 | 0.92 |
| 5 | 1.00 | 1.11 | 1.56 | 1.52 |
| 6 | 1.00 | 0.76 | 0.77 | 0.90 |
| 7 | 1.00 | 0.92 | 0.84 | 1.01 |
| 8 | 1.00 | 0.88 | 1.22 | 1.34 |

📌 **中文解释**：这一页是“学习更复杂的树、Monte Carlo 技巧、跳跃扩散和随机波动率模型。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 41. The Least Squares Approach

**原文要点**
- We work back from the end using a least squares approach to calculate the continuation value at each time
- Consider year 2. The option is in the money for five paths. These give observations on S of 1.08, 1.07, 0.97, 0.77, and 0.84. The continuation values are 0.00, 0.07e-0.06, 0.18e-0.06, 0.20e-0.06, and 0.09e-0.06

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 42. The Least Squares Approach continued

**原文要点**
- Fitting a model of the form V=a+bS+cS2 we get a best fit relation
- V=-1.070+2.983S-1.813S2
- for the continuation value V
- This defines the early exercise decision at
- t =2. We carry out a similar analysis at t=1

📌 **中文解释**：这一页是“学习更复杂的树、Monte Carlo 技巧、跳跃扩散和随机波动率模型。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 43. The Least Squares Approach continued

**原文要点**
- In practice more complex functional forms can be used for the continuation value and many more paths are sampled

📌 **中文解释**：这一页是“学习更复杂的树、Monte Carlo 技巧、跳跃扩散和随机波动率模型。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 44. The Early Exercise Boundary Parametrization Approach

**原文要点**
- We assume that the early exercise boundary can be parameterized in some way
- We carry out a first Monte Carlo simulation and work back from the end calculating the optimal parameter values
- We then discard the paths from the first Monte Carlo simulation and carry out a new Monte Carlo simulation using the early exercise boundary defined by the parameter values.

📌 **中文解释**：蒙特卡罗通过模拟大量路径估计期望，适合路径依赖或高维问题。

---

### 45. Application to Example

**原文要点**
- We parameterize the early exercise boundary by specifying a critical asset price, S, below which the option is exercised.
- At t =1 the optimal S for the eight paths is 0.88. At t =2 the optimal S is 0.84
- In practice we would use many more paths to calculate the S

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
