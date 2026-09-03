# Ch12 期权交易策略

**相关笔记**: [[Ch11HullOFOD11thEdition|上一章：股票期权性质]] | [[Ch13HullOFOD11thEdition|下一章：二叉树]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 12 Trading Strategies Involving Options
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：整理保护性看跌、备兑看涨、价差、跨式、宽跨式等组合策略。

💡 **核心理解**：期权组合是在塑造到期收益曲线：先看你想买/卖哪一种风险。

本章可以按下面的顺序阅读：
1. Strategies to be Considered
2. Principal Protected Note
3. Principal Protected Notes continued
4. Positions in an Option & the Underlying (Figure 12.1)（期权）
5. Bull Spread Using Calls(Figure 12.2)（看涨期权）
6. Bull Spread Using Puts Figure 12.3（看跌期权）
7. Bear Spread Using Puts Figure 12.4（看跌期权）
8. Bear Spread Using CallsFigure 12.5（看涨期权）
9. Box Spread
10. Butterfly Spread Using CallsFigure 12.6（看涨期权）
11. Butterfly Spread Using Puts Figure 12.7（看跌期权）
12. Calendar Spread Using CallsFigure 12.8（看涨期权）
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **期权**：买方支付权利金，获得未来按执行价买入或卖出标的的权利。
- **看涨期权**：赋予买入标的资产的权利。
- **看跌期权**：赋予卖出标的资产的权利。

---

## 三、逐页整理

### 2. Strategies to be Considered

**原文要点**
- Bond plus option to create principal protected note
- Stock plus option
- Two or more options of the same type (a spread)
- Two or more options of different types (a combination)

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 3. Principal Protected Note

**原文要点**
- Allows investor to take a risky position without risking any principal
- Example: $1000 instrument consisting of
- 3-year zero-coupon bond with principal of $1000
- 3-year at-the-money call option on a stock portfolio currently worth $1000

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 4. Principal Protected Notes continued

**原文要点**
- Viability depends on
- Level of dividends
- Level of interest rates
- Volatility of the portfolio
- Variations on standard product
- Out of the money strike price
- Caps on investor return
- Knock outs, averaging features, etc

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 5. Positions in an Option & the Underlying (Figure 12.1)（期权）

**原文要点**
- Profit
- ST
- K
- Profit
- ST
- K
- Profit
- ST
- K
- Profit
- ST
- K
- (a)
- (b)
- (c)
- (d)

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 6. Bull Spread Using Calls(Figure 12.2)（看涨期权）

**原文要点**
- K1
- K2
- Profit
- ST

📌 **中文解释**：看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 7. Bull Spread Using Puts Figure 12.3（看跌期权）

📌 **中文解释**：看跌期权对应卖出权，常用于下行保护或表达下跌观点。

---

### 8. Bear Spread Using Puts Figure 12.4（看跌期权）

📌 **中文解释**：看跌期权对应卖出权，常用于下行保护或表达下跌观点。

---

### 9. Bear Spread Using Calls Figure 12.5（看涨期权）

**原文要点**
- K1
- K2
- Profit
- ST

📌 **中文解释**：看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 10. Box Spread

**原文要点**
- A combination of a bull call spread and a bear put spread
- If all options are European a box spread is worth the present value of the difference between the strike prices
- If they are American this is not necessarily so (see Business Snapshot 11.1)

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 11. Butterfly Spread Using Calls Figure 12.6（看涨期权）

**原文要点**
- K1
- K3
- Profit
- ST
- K2

📌 **中文解释**：看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 12. Butterfly Spread Using Puts Figure 12.7（看跌期权）

**原文要点**
- K1
- K3
- Profit
- ST
- K2

📌 **中文解释**：看跌期权对应卖出权，常用于下行保护或表达下跌观点。

---

### 13. Calendar Spread Using Calls Figure 12.8（看涨期权）

**原文要点**
- Profit
- ST
- K

📌 **中文解释**：看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 14. Calendar Spread Using Puts Figure 12.9（看跌期权）

**原文要点**
- Profit
- ST
- K

📌 **中文解释**：看跌期权对应卖出权，常用于下行保护或表达下跌观点。

---

### 15. A Straddle Combination Figure 12.10

**原文要点**
- Profit
- ST
- K

📌 **中文解释**：这一页是“整理保护性看跌、备兑看涨、价差、跨式、宽跨式等组合策略。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 16. Strip & Strap Figure 12.11

**原文要点**
- Profit
- K
- ST
- Profit
- K
- ST
- Strip
- Strap

📌 **中文解释**：这一页是“整理保护性看跌、备兑看涨、价差、跨式、宽跨式等组合策略。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 17. A Strangle Combination Figure 12.12

**原文要点**
- K1
- K2
- Profit
- ST

📌 **中文解释**：这一页是“整理保护性看跌、备兑看涨、价差、跨式、宽跨式等组合策略。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 18. Other Payoff Patterns

**原文要点**
- When the strike prices are close together a butterfly spread provides a payoff consisting of a small “spike”
- If options with all strike prices were available any payoff pattern could (at least approximately) be created by combining the spikes obtained from different butterfly spreads

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
