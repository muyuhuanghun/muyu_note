# Ch32 短利率无套利模型

**相关笔记**: [[Ch31HullOFOD11thEdition|上一章：短利率均衡模型]] | [[Ch33HullOFOD11thEdition|下一章：远期利率建模]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 32 No-Arbitrage Models of the Short Rate
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：学习 Hull-White、Black-Karasinski 等能拟合初始期限结构的短利率模型。

💡 **核心理解**：无套利短利率模型先匹配今天的市场曲线，再描述未来利率随机演化。

本章可以按下面的顺序阅读：
1. No-arbitrage Term Structure Models
2. Developing No-Arbitrage Model for r
3. Ho-Lee Model
4. Diagrammatic Representation of Ho-Lee (Figure 32.1)
5. Hull-White Model（Hull-White 模型）
6. Diagrammatic Representation of Hull and White (Figure 32.2)
7. Black-Karasinski Model (equation 32.9)
8. Options on Zero-Coupon Bonds (equation 32.10)（期权）
9. Options on Coupon-Bearing Bonds（期权）
10. Interest Rate Trees vs Stock Price Trees
11. Two-Step Tree Example (Figure 32.4)
12. Alternative Branching Processes in a Trinomial Tree (Figure 32.5)
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **短利率**：当前瞬时无风险利率，是短利率模型的状态变量。
- **Hull-White 模型**：能拟合初始期限结构的扩展 Vasicek 模型。

---

## 三、逐页整理

### 2. No-arbitrage Term Structure Models

**原文要点**
- A no-arbitrage model is a model designed to fit today’s term structure of interest rates

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。

---

### 3. Developing No-Arbitrage Model for r

**原文要点**
- A model for r can be made to fit the initial term structure by including a function of time in the drift

📌 **中文解释**：这一页是“学习 Hull-White、Black-Karasinski 等能拟合初始期限结构的短利率模型。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 4. Ho-Lee Model

**原文要点**
- dr = q(t)dt + sdz
- Many analytic results for bond prices and option prices
- Interest rates normally distributed
- One volatility parameter, s
- All forward rates have the same standard deviation

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 5. Diagrammatic Representation of Ho-Lee (Figure 32.1)

📌 **中文解释**：这一页是“学习 Hull-White、Black-Karasinski 等能拟合初始期限结构的短利率模型。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 6. Hull-White Model（Hull-White 模型）

**原文要点**
- dr = [q(t ) – ar ]dt + sdz
- Many analytic results for bond prices and option prices
- Two volatility parameters, a and s
- Interest rates normally distributed
- Standard deviation of a forward rate is a declining function of its maturity

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 7. Diagrammatic Representation of Hull and White (Figure 32.2)

📌 **中文解释**：这一页是“学习 Hull-White、Black-Karasinski 等能拟合初始期限结构的短利率模型。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 8. Black-Karasinski Model (equation 32.9)

**原文要点**
- Future value of r is lognormal
- Very little analytic tractability

📌 **中文解释**：这一页是“学习 Hull-White、Black-Karasinski 等能拟合初始期限结构的短利率模型。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 9. Options on Zero-Coupon Bonds (equation 32.10)（期权）

**原文要点**
- In Vasicek and Hull-White model, price of call maturing at T on a zero-coupon bond lasting to s is
- LP(0,s)N(h)−KP(0,T)N(h−sP)
- Price of put is
- KP(0,T)N(−h+sP)−LP(0,s)N(h)
- where

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。零息利率用于直接折现单笔到期现金流，是构建收益率曲线的基础。

---

### 10. Options on Coupon-Bearing Bonds（期权）

**原文要点**
- In a one-factor model a European option on a coupon-bearing bond can be expressed as a portfolio of options on zero-coupon bonds.
- We first calculate the critical interest rate at the option maturity for which the coupon-bearing bond price equals the strike price at maturity
- The strike price for each zero-coupon bond is set equal to its value when the interest rate equals this critical value

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 11. Interest Rate Trees vs Stock Price Trees

**原文要点**
- The variable at each node in an interest rate tree is the Dt-period rate
- Interest rate trees work similarly to stock price trees except that the discount rate used varies from node to node

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 12. Two-Step Tree Example (Figure 32.4)

**原文要点**
- Payoff after 2 years is max[100(r – 0.11), 0]
- pu=0.25; pm=0.5; pd=0.25; Time step=1yr
- 10%
- 0.35
- 12% 1.11
- 10% 0.23
- 8% 0.00
- 14% 3
- 12% 1
- 10% 0
- 8% 0
- 6% 0
- : (0.25×3 + 0.50×1 + 0.25×0)e–0.12×1
- : (0.25×1.11 + 0.50×0.23 +0.25×0)e–0.10×1

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 13. Alternative Branching Processes in a Trinomial Tree (Figure 32.5)

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 14. Procedure for Building Tree

**原文要点**
- dr = [q(t ) – ar ]dt + sdz
- 1. Assume q(t ) = 0 and r (0) = 0
- 2. Draw a trinomial tree for r to match the mean and standard deviation of the process for r
- 3. Determine q(t ) one step at a time so that the tree matches the initial term structure

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 15. Example

**原文要点**
- s = 0.01
- a = 0.1
- Dt = 1 year

**原始表格 / 图示**
| Maturity | Zero Rate |
|---|---|
| 0.5 | 3.430 |
| 1 | 3.824 |
| 1.5 | 4.183 |
| 2 | 4.512 |
| 2.5 | 4.812 |
| 3 | 5.086 |

📌 **中文解释**：零息利率用于直接折现单笔到期现金流，是构建收益率曲线的基础。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 16. Building the First Tree for the Dt rate R

**原文要点**
- Set vertical spacing:
- Change branching when jmax nodes from middle where jmax is smallest integer greater than 0.184/(aDt)
- Choose probabilities on branches so that mean change in R is -aRDt and S.D. of change is

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 17. The First Tree(Figure 32.6)

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 18. Shifting Nodes

**原文要点**
- Work forward through tree
- Remember Qij the value of a derivative providing a $1 payoff at node j at time iDt
- Shift nodes at time iDt by ai so that the (i+1)Dt bond is correctly priced

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 19. The Final Tree(Figure 31.7)

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 20. Extensions

**原文要点**
- The tree building procedure can be extended to cover more general models of the form:
- dƒ(r ) = [q(t ) – a ƒ(r )]dt + sdz
- We set x=f(r) and proceed similarly to before
- x=ln(r) gives the Black-Karasinski model

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 21. Calibration to Determine a and s

**原文要点**
- The volatility parameters a and s (perhaps functions of time) are chosen so that the model fits the prices of actively traded instruments such as caps and European swap options as closely as possible
- We minimize a function of the form
- where Ui is the market price of the ith calibrating instrument, Vi is the model price of the ith calibrating instrument and P is a function that penalizes big changes or curvature in a and s

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
