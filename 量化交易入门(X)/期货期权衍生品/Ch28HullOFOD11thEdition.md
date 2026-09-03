# Ch28 鞅与测度

**相关笔记**: [[Ch27HullOFOD11thEdition|上一章：模型与数值方法进阶]] | [[Ch29HullOFOD11thEdition|下一章：利率衍生品：标准市场模型]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 28 Martingales and Measures
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：理解鞅、计价单位、风险中性测度和远期测度。

💡 **核心理解**：换测度的目的，是把复杂随机折现问题改写成更好计算的期望。

本章可以按下面的顺序阅读：
1. Derivatives Dependent on a Single Underlying Variable (equations 28.1 to 28.3)（衍生品）
2. Forming a Riskless Portfolio (equations 28.4 and 28.5)
3. Market Price of Risk (equation 28.6)
4. Extension of the Analysisto Several Underlying Variables(Equations 28.12 and 28.13)
5. Martingales（鞅）
6. Alternative Worlds
7. The Equivalent Martingale Measure Result（鞅）
8. Numeraire
9. Alternative Choices for the Numeraire Security g
10. Money Market Accountas the Numeraire
11. Money Market Accountcontinued
12. Zero-Coupon Bond Maturing at time T as Numeraire
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **鞅**：在某个测度下，未来条件期望等于当前值的随机过程。
- **风险中性测度**：定价时可用无风险利率折现期望收益的概率测度。

---

## 三、逐页整理

### 2. Derivatives Dependent on a Single Underlying Variable (equations 28.1 to 28.3)（衍生品）

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。

---

### 3. Forming a Riskless Portfolio (equations 28.4 and 28.5)

📌 **中文解释**：这一页是“理解鞅、计价单位、风险中性测度和远期测度。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 4. Market Price of Risk (equation 28.6)

**原文要点**
- This shows that (m – r )/s is the same for all derivatives dependent on the same underlying variable, q
- We refer to (m – r )/s as the market price of risk for q and denote it by l

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。

---

### 5. Extension of the Analysisto Several Underlying Variables(Equations 28.12 and 28.13)

📌 **中文解释**：这一页是“理解鞅、计价单位、风险中性测度和远期测度。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 6. Martingales（鞅）

**原文要点**
- A martingale is a stochastic process with zero drift
- A variable following a martingale has the property that its expected future value equals its value today

📌 **中文解释**：鞅和测度转换用于把定价问题改写成可折现的期望问题。

---

### 7. Alternative Worlds

📌 **中文解释**：这一页是“理解鞅、计价单位、风险中性测度和远期测度。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 8. The Equivalent Martingale Measure Result（鞅）

📌 **中文解释**：鞅和测度转换用于把定价问题改写成可折现的期望问题。

---

### 9. Numeraire

**原文要点**
- We will refer to a world where the market price of risk is the volatility of g as “a world defined by numeraire g”
- If Eg denotes expectations in a world defined by numeraire g

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 10. Alternative Choices for the Numeraire Security g

**原文要点**
- Money Market Account
- Zero-coupon bond price
- Annuity factor

📌 **中文解释**：零息利率用于直接折现单笔到期现金流，是构建收益率曲线的基础。

---

### 11. Money Market Accountas the Numeraire

**原文要点**
- The money market account is an account that starts at $1 and is always invested at the short-term risk-free interest rate
- The process for the value of the account is
- dg = rg dt
- This has zero volatility. Using the money market account as the numeraire leads to the traditional risk-neutral world where l=0

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 12. Money Market Accountcontinued

📌 **中文解释**：这一页是“理解鞅、计价单位、风险中性测度和远期测度。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 13. Zero-Coupon Bond Maturing at time T as Numeraire

📌 **中文解释**：零息利率用于直接折现单笔到期现金流，是构建收益率曲线的基础。

---

### 14. Forward Prices（远期）

**原文要点**
- In a world defined by numeraire P(0,T), the expected value of a security at time T is its forward price

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 15. Interest Rates（利率）

**原文要点**
- In a world defined by numeraire P(0,T2), the expected value of an interest rate lasting between times T1 and T2 is the forward interest rate

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 16. Annuity Factor as the Numeraire

📌 **中文解释**：这一页是“理解鞅、计价单位、风险中性测度和远期测度。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 17. Annuity Factors and Swap Rates（互换）

**原文要点**
- Suppose that s(t) is the swap rate corresponding to the annuity factor A.
- Then:
- s(t)=EA[s(T)]

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 18. Extension to Several Independent Factors

📌 **中文解释**：这一页是“理解鞅、计价单位、风险中性测度和远期测度。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 19. Extension to Several Independent Factors continued

📌 **中文解释**：这一页是“理解鞅、计价单位、风险中性测度和远期测度。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 20. Applications

**原文要点**
- Extension of Black’s model to case where interest rates are stochastic
- Valuation of an option to exchange one asset for another

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 21. Black’s Model (equations 28.28 and 28.29)

**原文要点**
- By working in a world defined by numeraire P(0,T), it can be seen that Black’s model is true when interest rates are stochastic providing the forward price of the underlying asset is has a constant volatility
- c = P(0,T)[F0N(d1)−KN(d2)]
- p = P(0,T)[KN(−d2) − F0N(−d1)]

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 22. Option to exchange an asset worth U for one worth V (Section 28.7)（期权）

**原文要点**
- This can be valued by working in a world defined by numeraire U
- Value is

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 23. Change of Numeraire(Section 28.8)

📌 **中文解释**：这一页是“理解鞅、计价单位、风险中性测度和远期测度。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
