# Ch30 凸性、时机与 Quanto 调整

**相关笔记**: [[Ch29HullOFOD11thEdition|上一章：利率衍生品：标准市场模型]] | [[Ch31HullOFOD11thEdition|下一章：短利率均衡模型]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 30 Convexity, Timing, and Timing, and Quanto Adjustments
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：理解 convexity adjustment、timing adjustment 和 quanto adjustment。

💡 **核心理解**：这些调整处理的是现金流时点、标的计价货币和非线性收益带来的偏差。

本章可以按下面的顺序阅读：
1. Forward Yields and Forward Prices（远期）
2. Relationship Between Bond Yields and Prices (Figure 30.1)
3. Convexity Adjustment for Bond Yields (equation 30.1)（凸性）
4. Convexity Adjustment for Swap Rate（互换）
5. Example 30.1
6. Timing Adjustments (Equation 30.3)
7. Example 30.2
8. Quantos (Section 30.3)
9. Diff Swap（互换）
10. Quanto Adjustment (equation 30.5)
11. Example 30.3
12. Quantos continued
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **凸性**：债券价格对利率变化的二阶敏感度。
- **利率**：衍生品定价中的折现基础，也是重要的可交易风险因子。

---

## 三、逐页整理

### 2. Forward Yields and Forward Prices（远期）

**原文要点**
- We define the forward yield on a bond as the yield calculated from the forward bond price
- There is a non-linear relation between bond yields and bond prices
- It follows that when the forward bond price equals the expected future bond price, the forward yield does not necessarily equal the expected future yield

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 3. Relationship Between Bond Yields and Prices (Figure 30.1)

📌 **中文解释**：这一页是“理解 convexity adjustment、timing adjustment 和 quanto adjustment。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 4. Convexity Adjustment for Bond Yields (equation 30.1)（凸性）

**原文要点**
- Suppose a derivative provides a payoff at time T dependent on a bond yield, yT observed at time T. Define:
- G(yT) : price of the bond as a function of its yield
- yF : forward bond yield at time zero
- sy : forward yield volatility
- The expected bond price in a world defined by numeraire P(0,T) is the forward bond price
- The expected bond yield in a world defined by numeraire P(0,T) is (approximately)

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 5. Convexity Adjustment for Swap Rate（互换）

**原文要点**
- The expected value of the swap rate for the period T to T+t in a world defined by numeraire P(0,T) is (approximately)
- where G(y) defines the relationship between price and yield for a bond lasting between T and T+t that pays a coupon equal to the forward swap rate

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 6. Example 30.1

**原文要点**
- An instrument provides a payoff in 3 years = to the 3-year swap rate multiplied by $100
- Payments are made annually on the swap
- All swap rates are 6%; volatility is 22%
- Risk-free zero curve is flat at 5% (with annual compounding)
- The convexity adjustment is 9.7 bps so that the value of the instrument is 6.097/1.053 = 5.27

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。凸性描述非线性利率风险，利率变化较大时只看久期会低估误差。

---

### 7. Timing Adjustments (Equation 30.3)

**原文要点**
- The expected value of a variable, V, in a world that is defined by numeraire P(0,T) is the expected value of the variable in a world defined by numeraire P(0,T) multiplied by
- where RF is the forward interest rate between T and T expressed with a compounding frequency of m, sR is the volatility of RF, sV is the volatility of V, and r is the correlation between RF and V

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 8. Example 30.2

**原文要点**
- A derivative provides a payoff 6 years equal to the value of a stock index in 5 years. The interest rate is 8% with annual compounding
- 1200 is the 5-year forward value of the stock index
- This is the expected value in a world defined by numeraire P(0,5)
- To get the value in a world defined by numeraire P(0,6) we multiply by 1.00535
- The value of the derivative is 1200×1.00535/(1.086) or 760.26

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 9. Quantos (Section 30.3)

**原文要点**
- Quantos are derivatives where the payoff is defined using variables measured in one currency and paid in another currency
- Example: contract providing a payoff of
- ST – K dollars ($) where S is the Nikkei stock index (a yen number)

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。鞅和测度转换用于把定价问题改写成可折现的期望问题。

---

### 10. Diff Swap（互换）

**原文要点**
- Diff swaps are a type of quanto
- A floating rate is observed in one currency and applied to a principal in another currency

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 11. Quanto Adjustment (equation 30.5)

**原文要点**
- The expected value of a variable, V, in a world that is defined by numeraire PX(0,T) is its expected value in a world that is defined by numeraire PY(0,T) multiplied by exp(rVWsVsWT)
- W is the forward exchange rate (units of Y per unit of X) and rVW is the correlation between V and W.

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 12. Example 30.3

**原文要点**
- Current value of Nikkei index is 15,000
- This gives one-year forward as 15,150.75
- Suppose the volatility of the Nikkei is 20%, the volatility of the dollar-yen exchange rate is 12% and the correlation between the two is 0.3
- The one-year forward value of the Nikkei for a contract settled in dollars is 15,150.75e0.3 ×0.2×0.12×1 or 15,260.23

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 13. Quantos continued

**原文要点**
- When we move from the traditional risk neutral world in currency Y to the tradional risk neutral world in currency X, the growth rate of a variable V increases by
- rsV sS
- where sV is the volatility of V, sS is the volatility of the exchange rate (units of Y per unit of X) and r is the correlation between the two
- rsV sS

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 14. Siegel’s Paradox

📌 **中文解释**：这一页是“理解 convexity adjustment、timing adjustment 和 quanto adjustment。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 15. When is a Convexity, Timing, or Quanto Adjustment Necessary: Summary（凸性）

**原文要点**
- A convexity or timing adjustment is necessary when interest rates are used in a nonstandard or unnatural way for the purposes of defining a payoff
- No adjustment is necessary for a vanilla swap, a cap, or a swap option

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
