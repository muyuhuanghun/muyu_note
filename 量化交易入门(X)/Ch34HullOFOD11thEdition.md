# Ch34 互换再讨论

**相关笔记**: [[Ch33HullOFOD11thEdition|上一章：远期利率建模]] | [[Ch35HullOFOD11thEdition|下一章：能源和商品衍生品]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 34 Swaps Revisited
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：整理非标准互换、复利互换、股权互换和内嵌期权互换。

💡 **核心理解**：一旦现金流规则偏离 plain vanilla，就要重新检查远期利率实现假设是否仍可用。

本章可以按下面的顺序阅读：
1. Valuation of Swaps（互换）
2. Variations on Vanilla Interest Rate Swaps (Section 34.1; Business Snapshot 34.1)（互换）
3. Compounding Swaps (Section 34.3; Business Snapshot 34.2)（互换）
4. Currency Swaps（互换）
5. Equity Swaps (Section 34.4; Business Snapshot 34.3)（互换）
6. Swaps with Embedded Options (Section 34.5)（期权）
7. Other Swaps（互换）

---

## 二、核心概念速记

- **互换**：双方按约定规则交换未来现金流，可看成一组远期合约。
- **期权**：买方支付权利金，获得未来按执行价买入或卖出标的的权利。

---

## 三、逐页整理

### 2. Valuation of Swaps（互换）

**原文要点**
- The standard approach is to assume that forward rates will be realized
- This works for plain vanilla interest rate and plain vanilla currency swaps, but does not necessarily work for non-standard swaps

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 3. Variations on Vanilla Interest Rate Swaps (Section 34.1; Business Snapshot 34.1)（互换）

**原文要点**
- Principal different on two sides
- Payment frequency different on two sides
- Can be floating-for-floating instead of floating-for-fixed
- It is still correct to assume that forward rates are realized

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 4. Compounding Swaps (Section 34.3; Business Snapshot 34.2)（互换）

**原文要点**
- Interest is compounded instead of being paid
- Example: the fixed side is 6% compounded forward at 6.3% while the floating side is SOFR plus 20 bps compounded forward at SOFR
- This type of compounding swap can be valued (approximately) using the “assume forward rates are realized” rule.
- Approximation is exact if spread over floating for compounding is zero

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 5. Currency Swaps（互换）

**原文要点**
- In theory, a swap where floating in one currency is exchanged for floating in another currency is worth zero
- In practice it is sometimes the case that floating in currency A is exchanged for floating plus a spread in currency B

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 6. Equity Swaps (Section 34.4; Business Snapshot 34.3)（互换）

**原文要点**
- Total return on an equity index is exchanged periodically for a fixed or floating return
- When the return on an equity index is exchanged for floating the value of the swap is always zero immediately after a payment

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 7. Swaps with Embedded Options (Section 34.5)（期权）

**原文要点**
- Accrual swaps
- Cancelable swaps
- Cancelable compounding swaps

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 8. Other Swaps（互换）

**原文要点**
- Indexed principal swap
- Commodity swap
- Bizarre deals (for example, the P&G 5/30 swap in Business Snapshot 34.4)

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。商品衍生品定价要考虑储存、运输、库存和便利收益，不能完全套用金融资产逻辑。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
