# Ch21 基础数值方法

**相关笔记**: [[Ch20HullOFOD11thEdition|上一章：波动率微笑与波动率曲面]] | [[Ch22HullOFOD11thEdition|下一章：VaR 与 Expected Shortfall]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 21 Basic Numerical Procedures
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：整理二叉树、三叉树、有限差分和 Monte Carlo 等数值定价方法。

💡 **核心理解**：闭式解只覆盖少数产品，实际定价常靠数值方法处理路径依赖和复杂边界。

本章可以按下面的顺序阅读：
1. Approaches to Derivatives Valuation（衍生品）
2. Binomial Trees（二叉树）
3. Movements in Time Dt(Figure 21.1)
4. Tree Parameters for asset paying a dividend yield of q
5. Tree Parameters for asset paying a dividend yield of q(continued, equations 21.4 to 21.7)
6. The Complete Tree(Figure 21.2)
7. Backwards Induction
8. Example: Put Option(Example 21.1)（期权）
9. Slide 10
10. Calculation of Delta（Delta）
11. Calculation of Gamma（Gamma）
12. Calculation of Theta（Theta）
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **二叉树**：每一步价格只上/下两个状态的离散定价模型。
- **蒙特卡罗**：用大量随机路径估计衍生品期望价值。
- **期权**：买方支付权利金，获得未来按执行价买入或卖出标的的权利。

---

## 三、逐页整理

### 2. Approaches to Derivatives Valuation（衍生品）

**原文要点**
- Trees
- Monte Carlo simulation
- Finite difference methods

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 3. Binomial Trees（二叉树）

**原文要点**
- Binomial trees are frequently used to approximate the movements in the price of a stock or other asset
- In each small interval of time the stock price is assumed to move up by a proportional amount u or to move down by a proportional amount d

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 4. Movements in Time Dt(Figure 21.1)

📌 **中文解释**：这一页是“整理二叉树、三叉树、有限差分和 Monte Carlo 等数值定价方法。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 5. Tree Parameters for asset paying a dividend yield of q

**原文要点**
- Parameters p, u, and d are chosen so that the tree gives correct values for the mean & variance of the stock price changes in a risk-neutral world
- Mean: e(r−q)Dt = pu + (1– p )d
- Variance: s2Dt = pu2 + (1– p )d 2 – e2(r−q)Dt
- A further condition often imposed is u = 1/ d

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 6. Tree Parameters for asset paying a dividend yield of q(continued, equations 21.4 to 21.7)

**原文要点**
- When Dt is small a solution to the equations is

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 7. The Complete Tree(Figure 21.2)

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 8. Backwards Induction

**原文要点**
- We know the value of the option at the final nodes
- We work back through the tree using risk-neutral valuation to calculate the value of the option at each node, testing for early exercise when appropriate

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 9. Example: Put Option(Example 21.1)（期权）

**原文要点**
- S0 = 50; K = 50; r =10%; s = 40%;
- T = 5 months = 0.4167; Dt = 1 month = 0.0833
- In this case

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看跌期权对应卖出权，常用于下行保护或表达下跌观点。

---

### 10. Slide 10

**原文要点**
- Example (continued; Figure 21.3)

**原始表格 / 图示**
![[Ch21HullOFOD11thEdition/Ch21HullOFOD11thEdition_slide10_1.x-wmf]]

📌 **中文解释**：这一页是“整理二叉树、三叉树、有限差分和 Monte Carlo 等数值定价方法。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 11. Calculation of Delta（Delta）

**原文要点**
- Delta is calculated from the nodes at time Dt

📌 **中文解释**：Delta 衡量标的价格小幅变化对期权价值的影响，也是动态对冲的第一步。

---

### 12. Calculation of Gamma（Gamma）

**原文要点**
- Gamma is calculated from the nodes at time 2Dt
- =0.5(62.99+50)−0.5(50+39.69)

📌 **中文解释**：Gamma 衡量 Delta 的变化速度，Gamma 大时对冲需要更频繁调整。

---

### 13. Calculation of Theta（Theta）

**原文要点**
- Theta is calculated from the central nodes at times 0 and 2Dt

📌 **中文解释**：Theta 表示时间价值流逝，买期权通常承受时间损耗。

---

### 14. Calculation of Vega（Vega）

**原文要点**
- We can proceed as follows
- Construct a new tree with a volatility of 41% instead of 40%.
- Value of option is 4.62
- Vega is

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 15. Trees for Options on Indices, Currencies and Futures Contracts（期货合约）

**原文要点**
- As with Black-Scholes-Merton:
- For options on stock indices, q equals the dividend yield on the index
- For options on a foreign currency, q equals the foreign risk-free rate
- For options on futures contracts q = r

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 16. Binomial Tree for Stock Paying Known Dividends（二叉树）

**原文要点**
- Procedure:
- Construct a tree for the stock price less the present value of the dividends
- Create a new tree by adding the present value of the dividends at each node
- This ensures that the tree recombines and makes assumptions similar to those when the Black-Scholes-Merton model is used for European options

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 17. Control Variate Technique

**原文要点**
- Value American option, fA
- Value European option using same tree, fE
- Value European option using Black-Scholes –Merton, fBS
- Option price =fA+(fBS – fE)

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 18. Alternative Binomial Tree（二叉树）

**原文要点**
- Instead of setting u = 1/d we can set each of the 2 probabilities to 0.5 and

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 19. Trinomial Tree

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 20. Time Dependent Parameters in a Binomial Tree（二叉树）

**原文要点**
- Making r or q a function of time does not affect the geometry of the tree. The probabilities on the tree become functions of time.
- We can make s a function of time by making the lengths of the time steps inversely proportional to the variance rate.

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 21. Slide 21

**原文要点**
- Monte Carlo Simulation and p (Figure 21.13)
- How could you calculate p by randomly sampling points in the square?

**原始表格 / 图示**
![[Ch21HullOFOD11thEdition/Ch21HullOFOD11thEdition_slide21_1.x-wmf]]

📌 **中文解释**：蒙特卡罗通过模拟大量路径估计期望，适合路径依赖或高维问题。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 22. Monte Carlo Simulation and Options（期权）

**原文要点**
- When used to value European stock options, Monte Carlo simulation involves the following steps:
- 1. Simulate 1 path for the stock price in a risk neutral world
- 2. Calculate the payoff from the stock option
- 3. Repeat steps 1 and 2 many times to get many sample payoffs
- 4. Calculate mean payoff
- 5. Discount mean payoff at risk free rate to get an estimate of the value of the option

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。蒙特卡罗通过模拟大量路径估计期望，适合路径依赖或高维问题。

---

### 23. Sampling Stock Price Movements

**原文要点**
- In a risk neutral world the process for a stock price is
- where is the risk-neutral return
- We can simulate a path by choosing time steps of length Dt and using the discrete version of this
- where e is a random sample from f(0,1)

📌 **中文解释**：这一页是“整理二叉树、三叉树、有限差分和 Monte Carlo 等数值定价方法。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 24. A More Accurate Approach(Equation 21.17)

📌 **中文解释**：这一页是“整理二叉树、三叉树、有限差分和 Monte Carlo 等数值定价方法。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 25. Extensions

**原文要点**
- When a derivative depends on several underlying variables we can simulate paths for each of them in a risk-neutral world to calculate the values for the derivative

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。

---

### 26. Sampling from Normal Distribution

**原文要点**
- In Excel =NORMSINV(RAND()) gives a random sample from f(0,1)

📌 **中文解释**：这一页是“整理二叉树、三叉树、有限差分和 Monte Carlo 等数值定价方法。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 27. To Obtain 2 Correlated Normal Samples

**原文要点**
- Obtain independent normal samples x1 and x2 and set
- Use a procedure known as Cholesky’s decomposition when samples are required from more than two normal variables

📌 **中文解释**：这一页是“整理二叉树、三叉树、有限差分和 Monte Carlo 等数值定价方法。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 28. Standard Errors in Monte Carlo Simulation（蒙特卡罗）

**原文要点**
- The standard error of the estimate of the option price is the standard deviation of the discounted payoffs given by the simulation trials divided by the square root of the number of observations.

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。蒙特卡罗通过模拟大量路径估计期望，适合路径依赖或高维问题。

---

### 29. Application of Monte Carlo Simulation（蒙特卡罗）

**原文要点**
- Monte Carlo simulation can deal with path dependent options, options dependent on several underlying state variables, and options with complex payoffs
- It cannot easily deal with American-style options

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。蒙特卡罗通过模拟大量路径估计期望，适合路径依赖或高维问题。

---

### 30. Determining Greek Letters（希腊字母）

**原文要点**
- For D:
- 1. Make a small change to asset price
- 2. Carry out the simulation again using the same random number streams
- 3. Estimate D as the change in the option price divided by the change in the asset price
- Proceed in a similar manner for other Greek letters

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 31. Variance Reduction Techniques

**原文要点**
- Antithetic variable technique
- Control variate technique
- Importance sampling
- Stratified sampling
- Moment matching
- Using quasi-random sequences

📌 **中文解释**：这一页是“整理二叉树、三叉树、有限差分和 Monte Carlo 等数值定价方法。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 32. Sampling Through the Tree

**原文要点**
- Instead of sampling from the stochastic process we can sample paths randomly through a binomial or trinomial tree to value a derivative
- At each node that is reached we sample a random number between 0 and 1. If it is between 0 and p, we take the up branch; if it is between p and 1, we take the down branch

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 33. Finite Difference Methods

**原文要点**
- Finite difference methods aim to represent the differential equation in the form of a difference equation
- We form a grid by considering equally spaced time values and stock price values
- Define ƒi,j as the value of ƒ at time iDt when the stock price is jDS

📌 **中文解释**：这一页是“整理二叉树、三叉树、有限差分和 Monte Carlo 等数值定价方法。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 34. The Grid (Figure 21.5)

📌 **中文解释**：这一页是“整理二叉树、三叉树、有限差分和 Monte Carlo 等数值定价方法。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 35. Finite Difference Methods(continued, equations 21.24 and 21.26)

📌 **中文解释**：这一页是“整理二叉树、三叉树、有限差分和 Monte Carlo 等数值定价方法。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 36. Implicit Finite Difference Method

📌 **中文解释**：这一页是“整理二叉树、三叉树、有限差分和 Monte Carlo 等数值定价方法。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 37. Explicit Finite Difference Method

📌 **中文解释**：这一页是“整理二叉树、三叉树、有限差分和 Monte Carlo 等数值定价方法。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 38. Implicit vs Explicit Finite Difference Method

**原文要点**
- The explicit finite difference method is equivalent to the trinomial tree approach
- The implicit finite difference method is equivalent to a multinomial tree approach

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 39. Implicit vs Explicit Finite Difference Methods (Figure 21.16)

📌 **中文解释**：这一页是“整理二叉树、三叉树、有限差分和 Monte Carlo 等数值定价方法。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 40. Other Points on Finite Difference Methods

**原文要点**
- It is better to have ln S rather than S as the underlying variable
- Improvements over the basic implicit and explicit methods:
- Hopscotch method
- Crank-Nicolson method

📌 **中文解释**：这一页是“整理二叉树、三叉树、有限差分和 Monte Carlo 等数值定价方法。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
