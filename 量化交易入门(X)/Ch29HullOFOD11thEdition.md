# Ch29 利率衍生品：标准市场模型

**相关笔记**: [[Ch28HullOFOD11thEdition|上一章：鞅与测度]] | [[Ch30HullOFOD11thEdition|下一章：凸性、时机与 Quanto 调整]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 29 Interest Rate Derivatives: The Standard Market Models
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：整理债券期权、利率上限/下限、互换期权和市场 Black 模型。

💡 **核心理解**：市场模型通常直接建模可交易利率或远期利率，便于和报价校准。

本章可以按下面的顺序阅读：
1. The Complications in Valuing Interest Rate Derivatives（衍生品）
2. Approaches to Pricing Interest Rate Options（期权）
3. Black’s Model
4. Black’s Model for European Bond Options (Equations 29.1 and 29.2)（期权）
5. Forward Bond and Forward Yield（远期）
6. Yield Vols vs Price Vols (Equation 29.4)
7. Theoretical Justification for Bond Option Model（期权）
8. Caps and Floors
9. Caplets
10. Black’s Model for Caps (equations 29.7 and 29.8)
11. When Applying Black’s Model To Caps We Must ...
12. Theoretical Justification for Cap Model
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **利率**：衍生品定价中的折现基础，也是重要的可交易风险因子。
- **期权**：买方支付权利金，获得未来按执行价买入或卖出标的的权利。
- **互换**：双方按约定规则交换未来现金流，可看成一组远期合约。
- **Black-Scholes 模型**：经典欧式期权定价模型。

---

## 三、逐页整理

### 2. The Complications in Valuing Interest Rate Derivatives（衍生品）

**原文要点**
- We need a whole term structure to define the level of interest rates at any time
- The stochastic process for an interest rate is more complicated than that for a stock price
- Volatilities of different points on the term structure are different
- Interest rates are used for discounting the payoff as well as for defining the payoff.

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 3. Approaches to Pricing Interest Rate Options（期权）

**原文要点**
- Use a variant of Black’s model
- Use a no-arbitrage (yield curve based) model

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 4. Black’s Model

**原文要点**
- Similar to the model proposed by Fischer Black for valuing options on futures in 1976
- Assumes that the value of an interest rate, a bond price, or some other variable at a particular time T in the future has a lognormal distribution

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 5. Black’s Model for European Bond Options (Equations 29.1 and 29.2)（期权）

**原文要点**
- Assume that the future bond price is lognormal
- Both the bond price and the strike price should be cash prices not quoted prices

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。

---

### 6. Forward Bond and Forward Yield（远期）

**原文要点**
- Approximate duration relation between forward bond price, FB, and forward bond yield, yF
- where D is the (modified) duration of the forward bond at option maturity

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 7. Yield Vols vs Price Vols (Equation 29.4)

**原文要点**
- This relationship implies the following approximation
- where sy is the forward yield volatility, sB is the forward price volatility, and y0 is today’s forward yield
- Often sy is quoted with the understanding that this relationship will be used to calculate sB

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 8. Theoretical Justification for Bond Option Model（期权）

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 9. Caps and Floors

**原文要点**
- A cap is a portfolio of call options on interest rates. It has the effect of guaranteeing that the interest rate in each of a number of future periods will not rise above a certain level
- Payoff at time tk+1 is Ldk max(Rk−RK, 0) where L is the principal, dk =tk+1 − tk , RK is the cap rate, and Rk is the rate at time tk for the period between tk and tk+1
- A floor is similarly a portfolio of put options on interest rates. Payoff at time tk+1 is
- Ldk max(RK − Rk , 0)

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 10. Caplets

**原文要点**
- A cap is a portfolio of “caplets”
- Each caplet is a call option on a future interest rate with the payoff occurring in arrears
- When using Black’s model we assume that the interest rate underlying each caplet is lognormal

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 11. Black’s Model for Caps (equations 29.7 and 29.8)

**原文要点**
- The value of a caplet, for period (tk, tk+1) is
- The value of a floorlet is

📌 **中文解释**：Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。

---

### 12. When Applying Black’s Model To Caps We Must ...

**原文要点**
- EITHER
- Use spot volatilities
- Volatility different for each caplet
- OR
- Use flat volatilities
- Volatility same for each caplet within a particular cap but varies according to life of cap

📌 **中文解释**：Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 13. Theoretical Justification for Cap Model

📌 **中文解释**：这一页是“整理债券期权、利率上限/下限、互换期权和市场 Black 模型。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 14. Negative Rates

**原文要点**
- Can use a shifted lognormal model where Fk is replaced by Fk +a and RK is replaced by RK+a in Black’s model
- Alternatively, the forward rate can be assumed to follow an arithmetic (normal) process:
- This leads to the price of the caplet being
- and the price of a floorlet being

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。远期利率表示今天市场隐含的未来利率，是远期利率协议和利率模型的核心输入。

---

### 15. Swaptions（互换）

**原文要点**
- A swaption or swap option gives the holder the right to enter into an interest rate swap in the future
- Two kinds
- The right to pay a specified fixed rate and receive floating
- The right to receive a specified fixed rate and pay floating

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 16. Black’s Model for European Swaptions（互换）

**原文要点**
- When valuing European swap options it is usual to assume that the swap rate is lognormal
- Consider a swaption which gives the right to pay sK on an n -year swap starting at time T. The payoff on each swap payment date is
- where L is principal, m is payment frequency and sT is market swap rate at time T

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 17. Black’s Model for European Swaptions continued (equations 29.10 and 29.11)（互换）

**原文要点**
- The value of the swaption where holder has right to pay sK is LA[sFN(d1)−sK N(d2)]
- The value of a swaption where the hold has the right to receive sK is LA[sKN(−d2)−sF N(−d1)]
- sF is the forward swap rate; s is the forward swap rate volatility; ti is the time from today until the ith swap payment.

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 18. Black’s Model and OIS Discounting（隔夜指数互换）

**原文要点**
- A is defined by the OIS zero curve
- sF is defined by forward rates

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 19. Theoretical Justification for Swap Option Model（互换）

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 20. Relationship Between Swaptions and Bond Options（期权）

**原文要点**
- An interest rate swap can be regarded as the exchange of a fixed-rate bond for a floating-rate bond
- A swaption or swap option is therefore an option to exchange a fixed-rate bond for a floating-rate bond

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 21. Relationship Between Swaptions and Bond Options (continued)（期权）

**原文要点**
- At the start of the swap the floating-rate bond is worth par so that the swaption can be viewed as an option to exchange a fixed-rate bond for par
- An option on a swap where fixed is paid and floating is received is a put option on the bond with a strike price of par
- When floating is paid and fixed is received, it is a call option on the bond with a strike price of par

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 22. Negative Rates

**原文要点**
- Can use a shifted lognormal model where sF is replaced by sF +a and RK is replaced by RK+a in Black’s model
- Alternatively the forward swap rate can be assumed to follow an arithmetic (normal) process
- This leads to similar pricing formulas to those for caps

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 23. Deltas of Interest Rate Derivatives（衍生品）

**原文要点**
- Alternatives:
- Calculate a DV01 (the impact of a 1bps parallel shift in the zero curve)
- Calculate impact of small change in the quote for each instrument used to calculate the zero curve
- Divide zero curve (or forward curve) into buckets and calculate the impact of a shift in each bucket
- Carry out a principal components analysis for changes in the zero curve. Calculate delta with respect to each of the first two or three factors

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
