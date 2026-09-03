# Ch11 股票期权性质

**相关笔记**: [[Ch10HullOFOD11thEdition|上一章：期权市场机制]] | [[Ch12HullOFOD11thEdition|下一章：期权交易策略]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 11 Properties of Stock Options
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：学习影响期权价格的变量、上下界、提前行权和看涨看跌平价。

💡 **核心理解**：这一章建立期权价格的无套利边界，是后续模型定价的约束条件。

本章可以按下面的顺序阅读：
1. Notation
2. Effect of Variables on Option Pricing (Table 11.1)（期权）
3. American vs European Options（期权）
4. Calls: An Arbitrage Opportunity?（看涨期权）
5. Lower Bound for European Call Option Prices; No Dividends (Equation 11.4)（期权）
6. Puts: An Arbitrage Opportunity?（看跌期权）
7. Lower Bound for European Put Prices; No Dividends (Equation 11.5)（看跌期权）
8. Put-Call Parity: No Dividends（看涨期权）
9. Values of Portfolios (Table 11.2)
10. The Put-Call Parity Result (Equation 11.6)（看涨期权）
11. Suppose that
12. Early Exercise
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **期权**：买方支付权利金，获得未来按执行价买入或卖出标的的权利。
- **看涨期权**：赋予买入标的资产的权利。
- **看跌期权**：赋予卖出标的资产的权利。
- **欧式期权**：只能在到期日行权。
- **美式期权**：到期前任意时点都可以行权。

---

## 三、逐页整理

### 2. Notation

**原始表格 / 图示**
| c: | European call option price |
|---|---|
| p: | European put option price |
| S0: | Stock price today |
| K: | Strike price |
| T: | Life of option |
| s: | Volatility of stock price |
| C: | American call option price |
|---|---|
| P: | American put option price |
| ST: | Stock price at option maturity |
| D: | PV of dividends paid during life of option |
| r | Risk-free rate for maturity T with cont. comp. |

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 3. Effect of Variables on Option Pricing (Table 11.1)（期权）

**原始表格 / 图示**
| Variable | c | p | C | P |
|---|---|---|---|---|
| S0 | + | − | + | − |
| K | − | + | − | + |
| T | ? | ? | + | + |
| s | + | + | + | + |
| r | + | − | + | − |
| D | − | + | − | + |

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 4. American vs European Options（期权）

**原文要点**
- An American option is worth at least as much as the corresponding European option
- C  c
- P  p

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 5. Calls: An Arbitrage Opportunity?（看涨期权）

**原文要点**
- Suppose that
- Is there an arbitrage opportunity?

**原始表格 / 图示**
| c = 3 | S0 = 20 |
|---|---|
| T = 1 | r = 10% |
| K = 18 | D = 0 |

📌 **中文解释**：看涨期权对应买入权，适合表达上涨观点或构造上行保护。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 6. Lower Bound for European Call Option Prices; No Dividends (Equation 11.4)（期权）

**原文要点**
- c  max(S0 –Ke –rT, 0)

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 7. Puts: An Arbitrage Opportunity?（看跌期权）

**原文要点**
- Suppose that
- Is there an arbitrage opportunity?

**原始表格 / 图示**
| p= 1 | S0 = 37 |
|---|---|
| T = 0.5 | r =5% |
| K = 40 | D  = 0 |

📌 **中文解释**：看跌期权对应卖出权，常用于下行保护或表达下跌观点。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 8. Lower Bound for European Put Prices; No Dividends (Equation 11.5)（看跌期权）

**原文要点**
- p  max(Ke -rT–S0, 0)

📌 **中文解释**：这一页是“学习影响期权价格的变量、上下界、提前行权和看涨看跌平价。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 9. Put-Call Parity: No Dividends（看涨期权）

**原文要点**
- Consider the following 2 portfolios:
- Portfolio A: European call on a stock + zero-coupon bond that pays K at time T
- Portfolio C: European put on the stock + the stock

📌 **中文解释**：零息利率用于直接折现单笔到期现金流，是构建收益率曲线的基础。

---

### 10. Values of Portfolios (Table 11.2)

**原始表格 / 图示**
|  |  | ST > K | ST < K |
|---|---|---|---|
| Portfolio A | Call option | ST − K | 0 |
|  | Zero-coupon bond | K | K |
|  | Total | ST | K |
| Portfolio C | Put Option | 0 | K− ST |
|  | Share | ST | ST |
|  | Total | ST | K |

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 11. The Put-Call Parity Result (Equation 11.6)（看涨期权）

**原文要点**
- Both are worth max(ST , K ) at the maturity of the options
- They must therefore be worth the same today. This means that c + Ke -rT = p + S0

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 12. Suppose that

**原文要点**
- What are the arbitrage possibilities when
- p = 2.25 ?
- p = 1 ?
- Arbitrage Opportunities

**原始表格 / 图示**
| c= 3 | S0= 31 |
|---|---|
| T = 0.25 | r = 10% |
| K =30 | D = 0 |

📌 **中文解释**：这一页是“学习影响期权价格的变量、上下界、提前行权和看涨看跌平价。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 13. Early Exercise

**原文要点**
- Usually there is some chance that an American option will be exercised early
- An exception is an American call on a non-dividend paying stock
- This should never be exercised early

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 14. An Extreme Situation

**原文要点**
- For an American call option:
- S0 = 100; T = 0.25; K = 60; D = 0
- Should you exercise immediately?
- What should you do if
- You want to hold the stock for the next 3 months?
- You do not feel that the stock is worth holding for the next 3 months?

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 15. Reasons For Not Exercising a Call Early (No Dividends)（看涨期权）

**原文要点**
- No income is sacrificed
- You delay paying the strike price
- Holding the call provides insurance against stock price falling below strike price

📌 **中文解释**：这一页是“学习影响期权价格的变量、上下界、提前行权和看涨看跌平价。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 16. Bounds for European or American Call Options (No Dividends) Figure 11.3（期权）

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 17. Should Puts Be Exercised Early ?（看跌期权）

**原文要点**
- Are there any advantages to exercising an American put when
- S0 = 60; T = 0.25; r=10%
- K = 100; D = 0

📌 **中文解释**：看跌期权对应卖出权，常用于下行保护或表达下跌观点。

---

### 18. Slide 18

**原文要点**
- Bounds for European and American Put Options (No Dividends) Figure 11.4

**原始表格 / 图示**
![[Ch11HullOFOD11thEdition/Ch11HullOFOD11thEdition_slide18_1.jpg]]

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 19. The Impact of Dividends on Lower Bounds to Option Prices(Equations 11.8 and 11.9)（期权）

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 20. Extensions of Put-Call Parity（看涨期权）

**原文要点**
- American options; D = 0
- S0 − K < C − P < S0 − Ke−rT
- Equation 11.7
- European options; D > 0
- c + D + Ke −rT = p + S0
- Equation 11.10
- American options; D > 0
- S0 − D − K < C − P < S0 − Ke −rT
- Equation 11.11

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
