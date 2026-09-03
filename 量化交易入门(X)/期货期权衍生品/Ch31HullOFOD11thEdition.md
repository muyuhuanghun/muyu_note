# Ch31 短利率均衡模型

**相关笔记**: [[Ch30HullOFOD11thEdition|上一章：凸性、时机与 Quanto 调整]] | [[Ch32HullOFOD11thEdition|下一章：短利率无套利模型]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 31 Equilibrium Models of the Short Rate
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：学习 Vasicek、CIR 等从经济均衡角度建模短利率的模型。

💡 **核心理解**：均衡模型给出利率动态假设，但不一定精确拟合当前收益率曲线。

本章可以按下面的顺序阅读：
1. The Zero Curve
2. Term Structure Models
3. Equilibrium Models (Risk Neutral World)
4. Mean Reversion (Figure 31.1)
5. Alternative Term Structures in Vasicek & CIR (Figure 31.2)（Vasicek 模型）
6. Properties of Vasicek and CIR（Vasicek 模型）
7. Alternative Convexity and Duration Measures（测度）
8. Bond Price Processes in a Risk Neutral World (equations 31.11 and 31.12)
9. Real vs. Risk-Neutral Processes: Vasicek（风险中性测度）
10. Real vs. Risk-Neutral Processes: CIR（风险中性测度）
11. Estimating Parameters (Section 31.4)
12. The Two-Factor Hull-White model (Section 31.5)（Hull-White 模型）

---

## 二、核心概念速记

- **短利率**：当前瞬时无风险利率，是短利率模型的状态变量。
- **Vasicek 模型**：带均值回复且利率可为负的短利率模型。

---

## 三、逐页整理

### 2. The Zero Curve

**原文要点**
- The process for the instantaneous short rate, r, in the traditional risk-neutral world defines the process for the whole zero curve in this world
- The price at time t of a zero-coupon bond maturing at time T is
- where is the average r between times t and T and the yield on the bond is

📌 **中文解释**：零息利率用于直接折现单笔到期现金流，是构建收益率曲线的基础。短利率模型把瞬时利率作为状态变量，再由它推出债券和利率衍生品价格。

---

### 3. Term Structure Models

**原文要点**
- Term structure models attempt to describe the evolution of the whole term structure
- An equilibrium model usually starts with assumptions about economic variables and derives a process for the short rate
- A no-arbitrage model is designed to exactly match today’s term structure

📌 **中文解释**：短利率模型把瞬时利率作为状态变量，再由它推出债券和利率衍生品价格。

---

### 4. Equilibrium Models (Risk Neutral World)

📌 **中文解释**：这一页是“学习 Vasicek、CIR 等从经济均衡角度建模短利率的模型。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 5. Mean Reversion (Figure 31.1)

📌 **中文解释**：这一页是“学习 Vasicek、CIR 等从经济均衡角度建模短利率的模型。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 6. Alternative Term Structures in Vasicek & CIR (Figure 31.2)（Vasicek 模型）

📌 **中文解释**：短利率模型把瞬时利率作为状态变量，再由它推出债券和利率衍生品价格。

---

### 7. Properties of Vasicek and CIR（Vasicek 模型）

**原文要点**
- P(t,T) = A(t,T)e−B(t,T)r
- The A and B functions are different for the two models:

📌 **中文解释**：短利率模型把瞬时利率作为状态变量，再由它推出债券和利率衍生品价格。

---

### 8. Alternative Convexity and Duration Measures（测度）

**原文要点**
- These can be used with a Taylor series expansion to determine the effect of a small change in r on a bond portfolio

📌 **中文解释**：久期是一阶利率风险，适合小幅利率变动下的近似对冲。凸性描述非线性利率风险，利率变化较大时只看久期会低估误差。

---

### 9. Bond Price Processes in a Risk Neutral World (equations 31.11 and 31.12)

**原文要点**
- From Itô’s lemma, risk neutral processes are
- What is the Vasicek real-world process for P(t,T) if the market price of risk is a constant, l?

📌 **中文解释**：伊藤引理用于给随机过程的函数做微分，是推导 BSM 方程的数学工具。短利率模型把瞬时利率作为状态变量，再由它推出债券和利率衍生品价格。

---

### 10. Real vs. Risk-Neutral Processes: Vasicek（风险中性测度）

**原文要点**
- The risk-neutral world process is
- If the market price of interest rate risk is l (negative) the real world process is
- where

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。短利率模型把瞬时利率作为状态变量，再由它推出债券和利率衍生品价格。

---

### 11. Real vs. Risk-Neutral Processes: CIR（风险中性测度）

**原文要点**
- The risk-neutral world process is
- If the market price of interest rate risk is (negative), the real world process is
- where

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。短利率模型把瞬时利率作为状态变量，再由它推出债券和利率衍生品价格。

---

### 12. Estimating Parameters (Section 31.4)

**原文要点**
- The real world parameters can be estimated from historical movements in the three month rate
- The market price of risk can then be estimated so that yields match the current term structure as closely as possible

📌 **中文解释**：这一页是“学习 Vasicek、CIR 等从经济均衡角度建模短利率的模型。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 13. The Two-Factor Hull-White model (Section 31.5)（Hull-White 模型）

📌 **中文解释**：短利率模型把瞬时利率作为状态变量，再由它推出债券和利率衍生品价格。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
