# Ch35 能源和商品衍生品

**相关笔记**: [[Ch34HullOFOD11thEdition|上一章：互换再讨论]] | [[Ch36HullOFOD11thEdition|下一章：实物期权]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 35 Energy and Commodity Derivatives
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：理解商品远期曲线、储存成本、便利收益、季节性和均值回复。

💡 **核心理解**：商品不是单纯金融资产，库存、运输、季节性和供需约束会进入定价。

本章可以按下面的顺序阅读：
1. Agricultural Commodities
2. Metals
3. Energy Commodities（能源）
4. Crude Oil
5. Oil Derivatives（衍生品）
6. Natural Gas and Electricity
7. Natural Gas Derivatives（衍生品）
8. Electricity Derivatives（衍生品）
9. Electricity Derivatives continued（衍生品）
10. Commodity Prices（商品）
11. The Process for the Commodity Price（商品）
12. Tree for ln(S) Assuming q(t)=0 (Figure 35.1)
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **商品衍生品**：标的为能源、金属、农产品等实物商品的衍生品。
- **便利收益**：持有实物商品带来的非现金收益。

---

## 三、逐页整理

### 2. Agricultural Commodities

**原文要点**
- Corn, wheat, soybeans, cocoa, coffee, sugar, cotton, frozen orange juice, cattle, hogs, pork bellies, etc
- Supply-demand measured by stocks-to-use ratio
- Seasonality and mean reversion in prices (farmers have a choice about what they produce)
- Weather important

📌 **中文解释**：鞅和测度转换用于把定价问题改写成可折现的期望问题。

---

### 3. Metals

**原文要点**
- Gold, silver, platinum, palladium, copper, tin, lead, zinc, nickel, aluminium, etc
- No seasonality; weather unimportant
- Investment vs consumption metals
- Some mean reversion (It can become uneconomic to extract a metal)
- Recycling

📌 **中文解释**：这一页是“理解商品远期曲线、储存成本、便利收益、季节性和均值回复。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 4. Energy Commodities（能源）

**原文要点**
- Main energy sources
- Oil
- Gas
- Electricity
- All have mean reverting prices
- Gas and electricity exhibit jumps

📌 **中文解释**：商品衍生品定价要考虑储存、运输、库存和便利收益，不能完全套用金融资产逻辑。

---

### 5. Crude Oil

**原文要点**
- Largest commodity market in the world
- Many grades. For example
- Brent crude oil (sourced from North Sea)
- West Texas Intermediate (WTI) crude
- Refined products, for example:
- Gasoline
- Heating oil
- Kerosene

📌 **中文解释**：商品衍生品定价要考虑储存、运输、库存和便利收益，不能完全套用金融资产逻辑。

---

### 6. Oil Derivatives（衍生品）

**原文要点**
- Virtually all derivatives available on stocks and stock indices are also available in the OTC market with oil as the underlying asset
- Futures and futures options traded on the New York Mercantile Exchange (NYMEX) and the International Petroleum Exchange (IPE) are also popular

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。

---

### 7. Natural Gas and Electricity

**原文要点**
- Deregulated
- Elimination of government monopolies
- Producer and supplier not necessarily the same

📌 **中文解释**：这一页是“理解商品远期曲线、储存成本、便利收益、季节性和均值回复。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 8. Natural Gas Derivatives（衍生品）

**原文要点**
- A typical OTC contract is for the delivery of a specified amount of natural gas at a roughly uniform rate to specified location during a month.
- NYMEX and IPE trade contracts that require delivery of 10,000 million British thermal units of natural gas to a specified location

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。场外交易条款灵活，但必须额外管理交易对手信用、清算和监管报告。

---

### 9. Electricity Derivatives（衍生品）

**原文要点**
- Electricity is an unusual commodity in that it cannot be stored
- The U.S is divided into about 140 control areas and a market for electricity is created by trading between control areas.

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。商品衍生品定价要考虑储存、运输、库存和便利收益，不能完全套用金融资产逻辑。

---

### 10. Electricity Derivatives continued（衍生品）

**原文要点**
- A typical contract allows one side to receive a specified number of megawatt hours for a specified price at a specified location during a particular month
- Types of contracts:
- 5x8, 5x16, 7x24, daily or monthly exercise,
- swing options

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 11. Commodity Prices（商品）

**原文要点**
- Futures prices can be used to define the process followed by a commodity price in a risk-neutral world.
- We can build in mean reversion and use a process for constructing trinomial trees that is analogous to that used for interest rates in Chapter 32

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 12. The Process for the Commodity Price（商品）

**原文要点**
- A simple mean reverting process is
- d ln(S) = [q(t) − aln(S)] dt + s dz
- Can also be written
- Assume a = 0.1, s = 0.2, and Dt = 1 year

📌 **中文解释**：商品衍生品定价要考虑储存、运输、库存和便利收益，不能完全套用金融资产逻辑。

---

### 13. Tree for ln(S) Assuming q(t)=0 (Figure 35.1)

**原始表格 / 图示**
| Node | A | B | C | D | E | F | G | H | I |
|---|---|---|---|---|---|---|---|---|---|
| pu | 0.1667 | 0.1217 | 0.1667 | 0.2217 | 0.8867 | 0.1217 | 0.1667 | 0.2217 | 0.0867 |
| pm | 0.6666 | 0.6566 | 0.6666 | 0.6566 | 0.0266 | 0.6566 | 0.6666 | 0.6566 | 0.0266 |
| pd | 0.1667 | 0.2217 | 0.1667 | 0.1217 | 0.0867 | 0.2217 | 0.1667 | 0.1217 | 0.8867 |

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 14. Determining q(t)

**原文要点**
- The nodes on the tree are moved so that the expected commodity price equals the futures price
- Assume that the one-year, two-year and three-years futures price for the commodity are $22, $23, and $24, respectively

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 15. Final Tree (Figure 35.2)

**原始表格 / 图示**
| Node | A | B | C | D | E | F | G | H | I |
|---|---|---|---|---|---|---|---|---|---|
| pu | 0.1667 | 0.1217 | 0.1667 | 0.2217 | 0.8867 | 0.1217 | 0.1667 | 0.2217 | 0.0867 |
| pm | 0.6666 | 0.6566 | 0.6666 | 0.6566 | 0.0266 | 0.6566 | 0.6666 | 0.6566 | 0.0266 |
| pd | 0.1667 | 0.2217 | 0.1667 | 0.1217 | 0.0867 | 0.2217 | 0.1667 | 0.1217 | 0.8867 |

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 16. Interpolation and Seasonality

**原文要点**
- A simple approach
- Use a 12 month moving average of spot prices to determine a percentage seasonality factor for each month
- De-seasonalize the futures prices that are known
- Interpolate to determine other de-seasonalized futures prices
- Re-seasonalize all futures prices and construct tree

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 17. Jumps

**原文要点**
- Some commodity prices such as gas and electricity exhibit jumps
- A process that can be assumed is then
- where dp is a Poisson process generating jumps
- If Poisson process is known we can use tree to model process without jumps and thereby determine q(t)
- Can be implemented with Monte Carlo simulation

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。蒙特卡罗通过模拟大量路径估计期望，适合路径依赖或高维问题。

---

### 18. Other Models

**原文要点**
- Convenience yield follows a mean reverting process (Gibson and Schwartz)
- Volatility stochastic (Eydeland and Geman)
- Reversion level stochastic (Geman)

📌 **中文解释**：波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。商品衍生品定价要考虑储存、运输、库存和便利收益，不能完全套用金融资产逻辑。

---

### 19. Weather Derivatives (Section 35.5))（衍生品）

**原文要点**
- Heating degree days (HDD): For each day this is max(0, 65 – A) where A is the average of the highest and lowest temperature in ºF.
- Cooling Degree Days (CDD): For each day this is max(0, A – 65)
- Contracts specify the weather station to be used

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。

---

### 20. Weather Derivatives: Products（衍生品）

**原文要点**
- A typical product is a forward contract or an option on the cumulative CDD or HDD during a month
- Weather derivatives are often used by energy companies to hedge the volume of energy required for heating or cooling during a particular month
- How would you value an option on August CDD at a particular weather station?

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 21. How an Energy Producer Hedges Risks (Section 35.8)（能源）

**原文要点**
- Estimate a relationship of the form
- Y=a+bP+cT+e
- where Y is the monthly profit, P is the average energy prices, T is temperature, and e is an error term
- Take a position of –b in energy forwards and –c in weather forwards.

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。商品衍生品定价要考虑储存、运输、库存和便利收益，不能完全套用金融资产逻辑。

---

### 22. Insurance Derivatives (Section 35.6)（衍生品）

**原文要点**
- CAT bonds are an alternative to traditional reinsurance
- This is a bond issued by a subsidiary of an insurance company that pays a higher-than-normal interest rate.
- If claims of a certain type are in a certain range, the interest and possibly the principal on the bond are used to meet claims

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 23. Pricing Issues (Section 35.7)

**原文要点**
- To a good approximation many underlying variables in insurance, weather, and energy derivatives contracts can be assumed to have zero systematic risk.
- This means that we can calculate expected payoff in the real world and discount at the risk-free rate

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。商品衍生品定价要考虑储存、运输、库存和便利收益，不能完全套用金融资产逻辑。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
