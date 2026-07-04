# Ch09 XVA 调整

**相关笔记**: [[Ch08HullOFOD11thEdition|上一章：证券化与金融危机]] | [[Ch10HullOFOD11thEdition|下一章：期权市场机制]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 9 XVAs
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：了解 CVA、DVA、FVA、MVA、KVA 等估值调整如何反映信用、融资和资本成本。

💡 **核心理解**：真实交易价格不是无风险模型价，还要叠加交易对手、融资、保证金和监管资本成本。

本章可以按下面的顺序阅读：
1. CVA（信用估值调整）
2. Netting
3. DVA（债务估值调整）
4. Valuing Bilaterally Cleared Derivatives Portfolios continued（衍生品）
5. The CVA Calculation（信用估值调整）
6. The DVA Calculation（债务估值调整）
7. FVA and MVA (Figure 9.1)（融资估值调整）
8. FVA and MVA continued（融资估值调整）
9. The Cost
10. KVA
11. Calculation Issues

---

## 二、核心概念速记

- **XVA**：对无风险模型价格叠加信用、融资、保证金和资本成本等估值调整。
- **信用估值调整**：交易对手可能违约造成的价值折减。
- **债务估值调整**：自身违约可能带来的估值影响。
- **融资估值调整**：融资成本对交易价值的影响。
- **保证金**：为覆盖潜在亏损而存入的履约资金。
- **信用风险**：债务人或交易对手不履约导致损失的风险。

---

## 三、逐页整理

### 2. CVA（信用估值调整）

**原文要点**
- Credit valuation adjustment (CVA) is an adjustment to the no-default value of derivatives arising from the possibility of a counterparty default

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 3. Netting

**原文要点**
- Master agreements for bilaterally cleared transactions typically state that outstanding transactions are netted in the event of a default. For example, if there are two outstanding transactions worth +10 and -6 with a counterparty the potential loss in the event of default (assuming no collateral) is 4 not 10.
- This means that CVA must be calculated on a counterparty-by-counterparty basis, not on a transaction-by-transaction basis.

📌 **中文解释**：基差风险来自现货和期货价格不同步，这是套保后仍然留下的主要不确定性。信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 4. DVA（债务估值调整）

**原文要点**
- Debit (or debt) valuation adjustment is an adjustment to a bank’s no-default value because the bank itself might default.
- The banks DVA is the counterparty’s CVA
- Like CVA, DVA must be calculated on a counterparty-by-counterparty basis

📌 **中文解释**：基差风险来自现货和期货价格不同步，这是套保后仍然留下的主要不确定性。信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 5. Valuing Bilaterally Cleared Derivatives Portfolios continued（衍生品）

**原文要点**
- Value after credit adjustments is:
- No-default value − CVA + DVA
- CVA and DVA adjustments should reflect collateral arrangements
- Why does DVA increase the value of the portfolio of transactions with the counterparty?

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 6. The CVA Calculation（信用估值调整）

**原文要点**
- Time
- 0
- t1
- t2
- t3
- t4
- tn=T
- Counterparty default probability
- q1
- q2
- q3
- q4
- ………………
- ………………
- qn
- PV of dealer’s loss given default
- v1
- v2
- v3
- v4
- vn
- ………………

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。CVA 把交易对手可能违约造成的损失反映到估值里，是无风险价格到真实交易价格的桥梁。

---

### 7. The DVA Calculation（债务估值调整）

**原文要点**
- Time
- 0
- t1
- t2
- t3
- t4
- tn=T
- Dealer default probability
- q1
- q2
- q3
- q4
- ………………
- ………………
- qn
- PV of counterparty’s loss given default
- v1
- v2
- v3
- v4
- vn
- ………………

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。XVA 说明真实交易价格还要考虑信用、融资、保证金和资本占用。

---

### 8. FVA and MVA (Figure 9.1)（融资估值调整）

**原文要点**
- Consider the situation where a bank enters into a transaction with an end user where no margin is posted and hedges this by entering into an offsetting transaction with another bank:

📌 **中文解释**：保证金机制把潜在违约损失提前现金化，是清算体系控制风险的重要手段。XVA 说明真实交易价格还要考虑信用、融资、保证金和资本占用。

---

### 9. FVA and MVA continued（融资估值调整）

**原文要点**
- FVA is the expected cost of the incremental variation margin on the hedge transaction
- MVA is the expected cost of the incremental initial margin on the hedge transaction

📌 **中文解释**：保证金机制把潜在违约损失提前现金化，是清算体系控制风险的重要手段。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

### 10. The Cost

**原文要点**
- Many banks use their average debt funding cost to calculate the cost of FVA and MVA
- Financial economic theory would suggest that the initial margin and variation margin are low risk investments. The required return is less than the bank’s average funding cost
- If the return required on margin is the fed funds rate plus 10 bps and the interest earned on margin is the fed funds rate minus 20 basis points, the funding cost (possibly a benefit in the case of FVA) is 30bps

📌 **中文解释**：保证金机制把潜在违约损失提前现金化，是清算体系控制风险的重要手段。基差风险来自现货和期货价格不同步，这是套保后仍然留下的主要不确定性。

---

### 11. KVA

**原文要点**
- KVA is the capital valuation adjustment.
- This is an adjustment for the incremental capital requirements associated with a derivative
- Many banks consider the cost of incremental capital to be the required return on equity
- Financial economists would argue that additional equity makes the bank less risky and should reduce the required return on both debt and equity

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。XVA 说明真实交易价格还要考虑信用、融资、保证金和资本占用。

---

### 12. Calculation Issues

**原文要点**
- The calculation of all the XVAs involve very time-consuming Monte Carlo simulations.
- This is because it is necessary to calculate
- expected future exposures for both bank and counterparty (in the case of CVA and DVA)
- expected future variation and initial margin requirements (in the case of FVA and MVA)
- expected future capital requirements (in the case of KVA)

📌 **中文解释**：保证金机制把潜在违约损失提前现金化，是清算体系控制风险的重要手段。CVA 把交易对手可能违约造成的损失反映到估值里，是无风险价格到真实交易价格的桥梁。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
