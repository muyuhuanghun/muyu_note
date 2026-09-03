# Ch33 远期利率建模

**相关笔记**: [[Ch32HullOFOD11thEdition|上一章：短利率无套利模型]] | [[Ch34HullOFOD11thEdition|下一章：互换再讨论]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 33 Modeling Forward Rates
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：理解 HJM、LMM 等对远期利率曲线动态的建模。

💡 **核心理解**：利率产品很多依赖整条曲线，远期利率模型直接描述曲线如何随机移动。

本章可以按下面的顺序阅读：
1. HJM Model: Notation（HJM）
2. Notation continued
3. Modeling Bond Prices (Equation 33.1)
4. The process for F(t,T)Equation 33.4 and 33.5)
5. Tree Evolution of Term Structure is Non-Recombining
6. The BGM Model
7. Notation
8. Volatility Structure（波动率）
9. In Theory the L’s can be Determined from Cap Prices
10. Example 33.1
11. Example 33.2
12. The Process for Fk in a One-Factor BGM Market Model
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **远期利率**：今天隐含的未来某段期间利率。
- **HJM**：直接建模整条远期利率曲线动态的框架。
- **Libor Market Model**：直接建模市场远期利率的利率模型。

---

## 三、逐页整理

### 2. HJM Model: Notation（HJM）

**原始表格 / 图示**
| P(t,T ): | price at time t of a discount bond with principal of $1 maturing at T |
|---|---|
| Wt : | vector  of past and present values of interest rates and bond prices at time t that are relevant for determining bond price volatilities  at that time |
| v(t,T,Wt ): | volatility of P(t,T) |

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 3. Notation continued

**原始表格 / 图示**
| ƒ(t,T1,T2): | forward rate as seen at t for the period between T1 and  T2 |
|---|---|
| F(t,T): | instantaneous forward rate as seen at t for a contract maturing at T |
| r(t): | short-term risk-free interest rate at t |
| dz(t): | Wiener process driving term structure movements |

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。利率章节要同时看现金流折现和利率本身的随机变化。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 4. Modeling Bond Prices (Equation 33.1)

📌 **中文解释**：这一页是“理解 HJM、LMM 等对远期利率曲线动态的建模。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 5. The process for F(t,T)Equation 33.4 and 33.5)

📌 **中文解释**：这一页是“理解 HJM、LMM 等对远期利率曲线动态的建模。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 6. Tree Evolution of Term Structure is Non-Recombining

**原文要点**
- Tree for the short rate r is non-Markov

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。短利率模型把瞬时利率作为状态变量，再由它推出债券和利率衍生品价格。

---

### 7. The BGM Model

**原文要点**
- The BGM model is a model constructed in terms of the forward rates applicable to periods such as 3 months or 6 months (not instantaneous forward rates)
- The forward rate volatilities for the periods considered can be determined from cap prices

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。远期利率表示今天市场隐含的未来利率，是远期利率协议和利率模型的核心输入。

---

### 8. Notation

📌 **中文解释**：这一页是“理解 HJM、LMM 等对远期利率曲线动态的建模。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 9. Volatility Structure（波动率）

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 10. In Theory the L’s can be Determined from Cap Prices

📌 **中文解释**：这一页是“理解 HJM、LMM 等对远期利率曲线动态的建模。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 11. Example 33.1

**原文要点**
- If Black volatilities for the first three
- caplets are 24%, 22%, and 20%, then
- L0=24.00%
- L1=19.80%
- L2=15.23%

📌 **中文解释**：这一页是“理解 HJM、LMM 等对远期利率曲线动态的建模。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 12. Example 33.2

📌 **中文解释**：这一页是“理解 HJM、LMM 等对远期利率曲线动态的建模。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 13. The Process for Fk in a One-Factor BGM Market Model

📌 **中文解释**：这一页是“理解 HJM、LMM 等对远期利率曲线动态的建模。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 14. Rolling Risk-Neutrality (Equation 33.12)（风险中性测度）

**原文要点**
- It is often convenient to choose a world defined by a numeraire that is always the bond maturing at the next reset date. In this case, we can discount from ti+1 to ti at the di rate observed at time ti. The process for Fk is

📌 **中文解释**：这一页是“理解 HJM、LMM 等对远期利率曲线动态的建模。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 15. The BGM and HJM models（HJM）

**原文要点**
- In the limit as the time between resets tends to zero, the BGM model with rolling risk neutrality becomes the HJM model in the traditional risk-neutral world

📌 **中文解释**：远期利率模型直接描述曲线如何随机移动，便于和市场利率产品报价校准。

---

### 16. Monte Carlo Implementation of BGM Model (Equation 33.14)（蒙特卡罗）

📌 **中文解释**：蒙特卡罗通过模拟大量路径估计期望，适合路径依赖或高维问题。

---

### 17. Multifactor Versions of BGM

**原文要点**
- BGM can be extended so that there are several components to the volatility
- A factor analysis can be used to determine how the volatility of Fk is split into components

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 18. Ratchet Caps, Sticky Caps, and Flexi Caps

**原文要点**
- A plain vanilla cap depends only on one forward rate. Its price is not dependent on the number of factors.
- Ratchet caps, sticky caps, and flexi caps depend on the joint distribution of two or more forward rates. Their prices tend to increase with the number of factors

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。远期利率表示今天市场隐含的未来利率，是远期利率协议和利率模型的核心输入。

---

### 19. Valuing European Options in the BGM Model（期权）

**原文要点**
- There is an analytic approximation that can be used to value European swap options in the BGM model.

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 20. Calibrating the BGM Model

**原文要点**
- In theory BGM can be exactly calibrated to cap prices as described earlier
- In practice we proceed as for short rate models to minimize a function of the form
- where Ui is the market price of the ith calibrating instrument, Vi is the model price of the ith calibrating instrument and P is a function that penalizes big changes or curvature in a and s

📌 **中文解释**：短利率模型把瞬时利率作为状态变量，再由它推出债券和利率衍生品价格。

---

### 21. Types of Agency Mortgage-Backed Securities (MBSs)

**原文要点**
- Pass-Through
- Collateralized Mortgage Obligation (CMO)
- Interest Only (IO)
- Principal Only (PO)

📌 **中文解释**：这一页是“理解 HJM、LMM 等对远期利率曲线动态的建模。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 22. Option-Adjusted Spread(OAS)（期权）

**原文要点**
- To calculate the OAS for an interest rate derivative we value it assuming that the initial yield curve is the Treasury curve + a spread
- We use an iterative procedure to calculate the spread that makes the derivative’s model price = market price.
- This spread is the OAS.

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
