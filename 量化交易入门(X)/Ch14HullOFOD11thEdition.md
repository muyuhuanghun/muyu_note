# Ch14 维纳过程与伊藤引理

**相关笔记**: [[Ch13HullOFOD11thEdition|上一章：二叉树]] | [[Ch15HullOFOD11thEdition|下一章：Black-Scholes-Merton 模型]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 14 Wiener Processes and Itô’s Lemma
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：理解随机过程、布朗运动、几何布朗运动和伊藤引理。

💡 **核心理解**：这一章是从离散树走向连续时间模型的数学桥梁。

本章可以按下面的顺序阅读：
1. Stochastic Processes
2. Example 1
3. Example 2
4. Markov Processes
5. Weak-Form Market Efficiency
6. Example
7. Questions
8. Variances & Standard Deviations
9. Variances & Standard Deviations (continued)
10. A Wiener Process (equation 14.1)（维纳过程）
11. Properties of a Wiener Process（维纳过程）
12. Generalized Wiener Processes（维纳过程）
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **维纳过程**：连续时间随机运动的基础模型。
- **伊藤引理**：处理随机过程函数微分的核心工具。

---

## 三、逐页整理

### 2. Stochastic Processes

**原文要点**
- Describes the way in which a variable such as a stock price, exchange rate or interest rate changes through time
- Incorporates uncertainties

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。

---

### 3. Example 1

**原文要点**
- Each day a stock price
- increases by $1 with probability 30%
- stays the same with probability 50%
- reduces by $1 with probability 20%

📌 **中文解释**：这一页是“理解随机过程、布朗运动、几何布朗运动和伊藤引理。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 4. Example 2

**原文要点**
- Each day a stock price change is drawn from a normal distribution with mean $0.2 and standard deviation $1

📌 **中文解释**：这一页是“理解随机过程、布朗运动、几何布朗运动和伊藤引理。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 5. Markov Processes

**原文要点**
- In a Markov process future movements in a variable depend only on where we are, not the history of how we got to where we are
- Is the process followed by the temperature at a certain place Markov?
- We assume that stock prices follow Markov processes

📌 **中文解释**：这一页是“理解随机过程、布朗运动、几何布朗运动和伊藤引理。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 6. Weak-Form Market Efficiency

**原文要点**
- This asserts that it is impossible to produce consistently superior returns with a trading rule based on the past history of stock prices. In other words technical analysis does not work.
- A Markov process for stock prices is consistent with weak-form market efficiency

📌 **中文解释**：这一页是“理解随机过程、布朗运动、几何布朗运动和伊藤引理。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 7. Example

**原文要点**
- A variable is currently 40
- It follows a Markov process
- Process is stationary (i.e. the parameters of the process do not change as we move through time)
- At the end of 1 year the variable will have a normal probability distribution with mean 40 and standard deviation 10

📌 **中文解释**：这一页是“理解随机过程、布朗运动、几何布朗运动和伊藤引理。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 8. Questions

**原文要点**
- What is the probability distribution of the stock price at the end of 2 years?
- ½ years?
- ¼ years?
- Dt years?
- Taking limits we have defined a continuous stochastic process

📌 **中文解释**：这一页是“理解随机过程、布朗运动、几何布朗运动和伊藤引理。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 9. Variances & Standard Deviations

**原文要点**
- In Markov processes changes in successive periods of time are independent
- This means that variances are additive
- Standard deviations are not additive

📌 **中文解释**：这一页是“理解随机过程、布朗运动、几何布朗运动和伊藤引理。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 10. Variances & Standard Deviations (continued)

**原文要点**
- In our example it is correct to say that the variance is 100 per year.
- It is strictly speaking not correct to say that the standard deviation is 10 per year.

📌 **中文解释**：这一页是“理解随机过程、布朗运动、几何布朗运动和伊藤引理。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 11. A Wiener Process (equation 14.1)（维纳过程）

**原文要点**
- Define f(m,v) as a normal distribution with mean m and variance v
- A variable z follows a Wiener process if
- The change in z in a small interval of time Dt is Dz
- The values of Dz for any 2 different (non-overlapping) periods of time are independent

📌 **中文解释**：维纳过程是连续时间随机波动的基本构件，后续 BSM 和利率模型都会用到。

---

### 12. Properties of a Wiener Process（维纳过程）

**原文要点**
- Mean of [z (T ) – z (0)] is 0
- Variance of [z (T ) – z (0)] is T
- Standard deviation of [z (T ) – z (0)] is

📌 **中文解释**：维纳过程是连续时间随机波动的基本构件，后续 BSM 和利率模型都会用到。

---

### 13. Generalized Wiener Processes（维纳过程）

**原文要点**
- A Wiener process has a drift rate (i.e. average change per unit time) of 0 and a variance rate of 1
- In a generalized Wiener process the drift rate and the variance rate can be set equal to any chosen constants

📌 **中文解释**：维纳过程是连续时间随机波动的基本构件，后续 BSM 和利率模型都会用到。

---

### 14. Generalized Wiener Processes(continued)（维纳过程）

**原文要点**
- Mean change in x per unit time is a
- Variance of change in x per unit time is b2

📌 **中文解释**：维纳过程是连续时间随机波动的基本构件，后续 BSM 和利率模型都会用到。

---

### 15. Taking Limits . . .

**原文要点**
- What does an expression involving dz and dt mean?
- It should be interpreted as meaning that the corresponding expression involving Dz and Dt is true in the limit as Dt tends to zero
- In this respect, stochastic calculus is analogous to ordinary calculus

📌 **中文解释**：这一页是“理解随机过程、布朗运动、几何布朗运动和伊藤引理。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 16. The Example Revisited

**原文要点**
- A stock price starts at 40 and has a probability distribution of f(40,100) at the end of the year
- If we assume the stochastic process is Markov with no drift then the process is
- dS = 10dz
- If the stock price were expected to grow by $8 on average during the year, so that the year-end distribution is f(48,100), the process would be
- dS = 8dt + 10dz

📌 **中文解释**：这一页是“理解随机过程、布朗运动、几何布朗运动和伊藤引理。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 17. Itô Process (equation 14.4)（伊藤）

**原文要点**
- In an Itô process the drift rate and the variance rate are functions of time
- dx=a(x,t) dt+b(x,t) dz
- The discrete time equivalent
- is true in the limit as Dt tends to
- zero

📌 **中文解释**：伊藤引理用于给随机过程的函数做微分，是推导 BSM 方程的数学工具。

---

### 18. Why a Generalized Wiener Process Is Not Appropriate for Stocks（维纳过程）

**原文要点**
- For a stock price we can conjecture that its expected percentage change in a short period of time remains constant (not its expected actual change)
- We can also conjecture that our uncertainty as to the size of future stock price movements is proportional to the level of the stock price

📌 **中文解释**：维纳过程是连续时间随机波动的基本构件，后续 BSM 和利率模型都会用到。

---

### 19. An Ito Process for Stock Prices(equation 14.6 and 14.7)（伊藤引理）

**原文要点**
- where m is the expected return s is the volatility.
- The discrete time equivalent is
- The process is known as geometric Brownian motion

📌 **中文解释**：维纳过程是连续时间随机波动的基本构件，后续 BSM 和利率模型都会用到。伊藤引理用于给随机过程的函数做微分，是推导 BSM 方程的数学工具。

---

### 20. Interest Rates（利率）

**原文要点**
- What would be a reasonable stochastic process to assume for the short-term interest rate?

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。

---

### 21. Monte Carlo Simulation（蒙特卡罗）

**原文要点**
- We can sample random paths for the stock price by sampling values for e
- Suppose m= 0.15, s= 0.30, and Dt = 1 week (=1/52 or 0.0192 years), then

📌 **中文解释**：蒙特卡罗通过模拟大量路径估计期望，适合路径依赖或高维问题。

---

### 22. Monte Carlo Simulation – Sampling one Path (See Table 14.1)（蒙特卡罗）

📌 **中文解释**：蒙特卡罗通过模拟大量路径估计期望，适合路径依赖或高维问题。

---

### 23. Correlated Processes

**原文要点**
- Suppose dz1 and dz2 are Wiener processes with correlation r
- Then

📌 **中文解释**：维纳过程是连续时间随机波动的基本构件，后续 BSM 和利率模型都会用到。

---

### 24. Itô’s Lemma (See equation 14.12)（伊藤）

**原文要点**
- If we know the stochastic process followed by x, Itô’s lemma tells us the stochastic process followed by some function G (x, t ). When dx=a(x,t) dt+b(x,t) dz then
- Since a derivative is a function of the price of the underlying asset and time, Itô’s lemma plays an important part in the analysis of derivatives

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。伊藤引理用于给随机过程的函数做微分，是推导 BSM 方程的数学工具。

---

### 25. Indication of Why Itô’s Lemma is True (Appendix to Chapter 14)（伊藤）

**原文要点**
- A Taylor’s series expansion of G(x, t) gives

📌 **中文解释**：伊藤引理用于给随机过程的函数做微分，是推导 BSM 方程的数学工具。

---

### 26. Ignoring Terms of Higher Order Than Dt

📌 **中文解释**：这一页是“理解随机过程、布朗运动、几何布朗运动和伊藤引理。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 27. Substituting for Dx

📌 **中文解释**：这一页是“理解随机过程、布朗运动、几何布朗运动和伊藤引理。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 28. The e2Dt Term

📌 **中文解释**：这一页是“理解随机过程、布朗运动、几何布朗运动和伊藤引理。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 29. Taking Limits

📌 **中文解释**：这一页是“理解随机过程、布朗运动、几何布朗运动和伊藤引理。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 30. Application of Itô’s Lemmato a Stock Price Process（伊藤）

📌 **中文解释**：伊藤引理用于给随机过程的函数做微分，是推导 BSM 方程的数学工具。

---

### 31. Examples

📌 **中文解释**：这一页是“理解随机过程、布朗运动、几何布朗运动和伊藤引理。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 32. Fractional Brownian Motion

📌 **中文解释**：维纳过程是连续时间随机波动的基本构件，后续 BSM 和利率模型都会用到。

---

### 33. Fractional Brownian Motion

**原文要点**
- When H > 0.5, changes in successive periods are positively correlated
- When H = 0.5, fractional Brownian motion becomes regular Brownian motion where changes in successive periods are uncorrelated
- When H < 0.5, changes in successive periods are negatively correlated

📌 **中文解释**：维纳过程是连续时间随机波动的基本构件，后续 BSM 和利率模型都会用到。

---

### 34. Slide 34

**原文要点**
- H=0.9 (time step =0.01)

**原始表格 / 图示**
![[Ch14HullOFOD11thEdition/Ch14HullOFOD11thEdition_slide34_1.x-wmf]]

📌 **中文解释**：这一页是“理解随机过程、布朗运动、几何布朗运动和伊藤引理。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 35. Slide 35

**原文要点**
- H=0.5 (time step =0.01

**原始表格 / 图示**
![[Ch14HullOFOD11thEdition/Ch14HullOFOD11thEdition_slide35_1.x-wmf]]

📌 **中文解释**：这一页是“理解随机过程、布朗运动、几何布朗运动和伊藤引理。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 36. Slide 36

**原文要点**
- H=0.1 (time step =0.01

**原始表格 / 图示**
![[Ch14HullOFOD11thEdition/Ch14HullOFOD11thEdition_slide36_1.x-wmf]]

📌 **中文解释**：这一页是“理解随机过程、布朗运动、几何布朗运动和伊藤引理。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
