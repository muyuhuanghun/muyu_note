# Ch36 实物期权

**相关笔记**: [[Ch35HullOFOD11thEdition|上一章：能源和商品衍生品]] | [[Ch37HullOFOD11thEdition|下一章：衍生品事故与教训]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 36 Real Options
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：用期权思想分析投资项目中的延期、扩张、放弃和切换权。

💡 **核心理解**：实物期权把管理灵活性当成价值来源，而不是只做静态 NPV。

本章可以按下面的顺序阅读：
1. An Alternative to the NPV Rule for Capital Investments
2. The Problem with using NPV to Value Options（期权）
3. Correct Discount Rates are Counter-Intuitive
4. General Approach to Valuation
5. Extension to Many Underlying Variables
6. Estimating the Market Price of Risk Using CAPM (equation 36.2)
7. Types of Options（期权）
8. Example of Application of Real Options Approach to Valuing Amazon.com at end of 1999 (Business Snapshot 36.1; Schwartz and Moon)（实物期权）
9. Example
10. The Process for the Commodity Price（商品）
11. The Tree of Commodity Prices (Figure 36.1)（商品）
12. Valuation of Base Project (Figure 36.2)
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **实物期权**：投资项目中延期、扩张、放弃等管理灵活性的价值。
- **期权**：买方支付权利金，获得未来按执行价买入或卖出标的的权利。

---

## 三、逐页整理

### 2. An Alternative to the NPV Rule for Capital Investments

**原文要点**
- Define stochastic processes for the key underlying variables and use risk-neutral valuation
- This approach (known as the real options approach) is likely to do a better job at valuing growth options, abandonment options, etc than NPV

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。实物期权把项目中的延期、扩张、放弃等管理灵活性当作期权价值。

---

### 3. The Problem with using NPV to Value Options（期权）

**原文要点**
- Consider the example from Chapter 13: risk-free rate =4%; strike price = $21
- Suppose that the expected return required by investors in the real world on the stock is 10%. What discount rate should we use to value an option with strike price $21?

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 4. Correct Discount Rates are Counter-Intuitive

**原文要点**
- Correct discount rate for a call option is 55.96%
- Correct discount rate for a put option is –70.4%

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 5. General Approach to Valuation

**原文要点**
- We can value any asset dependent on a variable q by
- Reducing the expected growth rate of q by ls where l is the market price of q-risk and s is the volatility of q
- Assuming that all investors are risk-neutral

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 6. Extension to Many Underlying Variables

**原文要点**
- When there are several underlying variables qi we reduce the growth rate of each one by its market price of risk times its volatility and then behave as though the world is risk-neutral
- Note that the variables do not have to be prices of traded securities

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 7. Estimating the Market Price of Risk Using CAPM (equation 36.2)

📌 **中文解释**：这一页是“用期权思想分析投资项目中的延期、扩张、放弃和切换权。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 8. Types of Options（期权）

**原文要点**
- Abandonment
- Expansion
- Contraction
- Option to defer
- Option to extend life

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 9. Example of Application of Real Options Approach to Valuing Amazon.com at end of 1999 (Business Snapshot 36.1; Schwartz and Moon)（实物期权）

**原文要点**
- Estimate stochastic processes for the company’s sales revenue and its average growth rate.
- Estimated the market price of risk and other key parameters (cost of goods sold as a percent of sales, variable expenses as a percent of sales, fixed expenses, etc.)
- Use Monte Carlo simulation to generate different scenarios in a risk-neutral world.
- The stock price is the average of the present values of the net cash flows discounted at the risk-free rate.

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。蒙特卡罗通过模拟大量路径估计期望，适合路径依赖或高维问题。

---

### 10. Example

**原文要点**
- A company has to decide whether to invest $15 million to obtain 6 million units of a commodity at the rate of 2 million units per year for three years.
- The fixed operating costs are $6 million per year and the variable costs are $17 per unit.
- The spot price of the commodity is $20 per unit and 1, 2, and 3-year futures prices are $22, $23, and $24, respectively.
- The risk-free rate is 10% per annum for all maturities.

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。商品衍生品定价要考虑储存、运输、库存和便利收益，不能完全套用金融资产逻辑。

---

### 11. The Process for the Commodity Price（商品）

**原文要点**
- We assume that this is
- d ln(S) = [q(t) − aln(S)] dt + s dz
- where a = 0.1 and s = 0.2
- We build a tree as in Chapter 33

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。商品衍生品定价要考虑储存、运输、库存和便利收益，不能完全套用金融资产逻辑。

---

### 12. The Tree of Commodity Prices (Figure 36.1)（商品）

**原始表格 / 图示**
| Node | A | B | C | D | E | F | G | H | I |
|---|---|---|---|---|---|---|---|---|---|
| pu | 0.1667 | 0.1217 | 0.1667 | 0.2217 | 0.8867 | 0.1217 | 0.1667 | 0.2217 | 0.0867 |
| pm | 0.6666 | 0.6566 | 0.6666 | 0.6566 | 0.0266 | 0.6566 | 0.6666 | 0.6566 | 0.0266 |
| pd | 0.1667 | 0.2217 | 0.1667 | 0.1217 | 0.0867 | 0.2217 | 0.1667 | 0.1217 | 0.8867 |

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。商品衍生品定价要考虑储存、运输、库存和便利收益，不能完全套用金融资产逻辑。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 13. Valuation of Base Project (Figure 36.2)

**原始表格 / 图示**
| Node | A | B | C | D | E | F | G | H | I |
|---|---|---|---|---|---|---|---|---|---|
| pu | 0.1667 | 0.1217 | 0.1667 | 0.2217 | 0.8867 | 0.1217 | 0.1667 | 0.2217 | 0.0867 |
| pm | 0.6666 | 0.6566 | 0.6666 | 0.6566 | 0.0266 | 0.6566 | 0.6666 | 0.6566 | 0.0266 |
| pd | 0.1667 | 0.2217 | 0.1667 | 0.1217 | 0.0867 | 0.2217 | 0.1667 | 0.1217 | 0.8867 |

📌 **中文解释**：这一页是“用期权思想分析投资项目中的延期、扩张、放弃和切换权。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 14. Valuation of Option to Abandon (Figure 36.3)No Salvage Value; No Further Payments（期权）

**原始表格 / 图示**
| Node | A | B | C | D | E | F | G | H | I |
|---|---|---|---|---|---|---|---|---|---|
| pu | 0.1667 | 0.1217 | 0.1667 | 0.2217 | 0.8867 | 0.1217 | 0.1667 | 0.2217 | 0.0867 |
| pm | 0.6666 | 0.6566 | 0.6666 | 0.6566 | 0.0266 | 0.6566 | 0.6666 | 0.6566 | 0.0266 |
| pd | 0.1667 | 0.2217 | 0.1667 | 0.1217 | 0.0867 | 0.2217 | 0.1667 | 0.1217 | 0.8867 |

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 15. Value of Expansion Option; Figure 36.4 (Company Can Increase Scale of Project by 20% for $2 million)（期权）

**原始表格 / 图示**
| Node | A | B | C | D | E | F | G | H | I |
|---|---|---|---|---|---|---|---|---|---|
| pu | 0.1667 | 0.1217 | 0.1667 | 0.2217 | 0.8867 | 0.1217 | 0.1667 | 0.2217 | 0.0867 |
| pm | 0.6666 | 0.6566 | 0.6666 | 0.6566 | 0.0266 | 0.6566 | 0.6666 | 0.6566 | 0.0266 |
| pd | 0.1667 | 0.2217 | 0.1667 | 0.1217 | 0.0867 | 0.2217 | 0.1667 | 0.1217 | 0.8867 |

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
