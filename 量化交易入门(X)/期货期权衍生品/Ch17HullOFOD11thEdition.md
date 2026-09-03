# Ch17 股指和外汇期权

**相关笔记**: [[Ch16HullOFOD11thEdition|上一章：员工股票期权]] | [[Ch18HullOFOD11thEdition|下一章：期货期权与 Black 模型]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 17 Options on Stock Indices and Currencies
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：学习带连续收益率或外币利率的期权定价与应用。

💡 **核心理解**：股指分红率、外汇的外币利率，本质上都像持有标的带来的收益率。

本章可以按下面的顺序阅读：
1. Index Options)（期权）
2. Index Option Example（期权）
3. Using Index Options for Portfolio Insurance（期权）
4. Example 1
5. Example 2
6. Calculating Relation Between Index Level and Portfolio Value in 3 months (Table 17.1)
7. Determining the Strike Price (Table 17.2,)
8. Currency Options（期权）
9. Range Forward Contracts（远期合约）
10. Range Forward Contract continued Figure 17.1, page 368（远期）
11. European Options on AssetsProviding a Known Yield（期权）
12. European Options on AssetsProviding Known Yieldcontinued（期权）
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **期权**：买方支付权利金，获得未来按执行价买入或卖出标的的权利。
- **利率**：衍生品定价中的折现基础，也是重要的可交易风险因子。
- **波动率**：衡量价格变化不确定性的尺度，也是期权定价最关键输入之一。

---

## 三、逐页整理

### 2. Index Options)（期权）

**原文要点**
- The most popular underlying indices in the U.S. are
- The S&P 100 Index (OEX and XEO)
- The S&P 500 Index (SPX)
- The Dow Jones Index times 0.01 (DJX)
- The Nasdaq 100 Index (NDX)
- Exchange-traded contracts are on 100 times index; they are settled in cash; OEX is American; the XEO and all others are European

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 3. Index Option Example（期权）

**原文要点**
- Consider a call option on an index with a strike price of 880
- Suppose 1 contract is exercised when the index level is 900
- What is the payoff?

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 4. Using Index Options for Portfolio Insurance（期权）

**原文要点**
- Suppose the value of the index is S0 and the strike price is K
- If a portfolio has a b of 1.0, the portfolio insurance is obtained by buying 1 put option contract on the index for each 100S0 dollars held
- If the b is not 1.0, the portfolio manager buys b put options for each 100S0 dollars held
- In both cases, K is chosen to give the appropriate insurance level

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看跌期权对应卖出权，常用于下行保护或表达下跌观点。

---

### 5. Example 1

**原文要点**
- Portfolio has a beta of 1.0
- It is currently worth $500,000
- The index currently stands at 1000
- What trade is necessary to provide insurance against the portfolio value falling below $450,000?

📌 **中文解释**：这一页是“学习带连续收益率或外币利率的期权定价与应用。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 6. Example 2

**原文要点**
- Portfolio has a beta of 2.0
- It is currently worth $500,000 and index stands at 1000
- The risk-free rate is 12% per annum
- The dividend yield on both the portfolio and the index is 4%
- How many put option contracts should be purchased for portfolio insurance?

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看跌期权对应卖出权，常用于下行保护或表达下跌观点。

---

### 7. Calculating Relation Between Index Level and Portfolio Value in 3 months (Table 17.1)

**原文要点**
- If index rises to 1040, it provides a 40/1000 or 4% return in 3 months
- Total return (incl. dividends) = 5%
- Excess return over risk-free rate = 2%
- Excess return for portfolio = 4%
- Increase in Portfolio Value = 4+3−1=6%
- Portfolio value=$530,000

📌 **中文解释**：这一页是“学习带连续收益率或外币利率的期权定价与应用。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 8. Determining the Strike Price (Table 17.2,)

**原文要点**
- An option with a strike price of 960 will provide protection against a 10% decline in the portfolio value

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 9. Currency Options（期权）

**原文要点**
- Currency options trade on NASDAQ OMX
- There also exists a very active over-the-counter (OTC) market
- Currency options are used by corporations to buy insurance when they have an FX exposure

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。场外交易条款灵活，但必须额外管理交易对手信用、清算和监管报告。

---

### 10. Range Forward Contracts（远期合约）

**原文要点**
- Have the effect of ensuring that the exchange rate paid or received will lie within a certain range
- When currency is to be paid it involves selling a put with strike K1 and buying a call with strike K2 (with K2 > K1)
- When currency is to be received it involves buying a put with strike K1 and selling a call with strike K2
- Normally the price of the put equals the price of the call

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 11. Range Forward Contract continued Figure 17.1, page 368（远期）

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 12. European Options on Assets Providing a Known Yield（期权）

**原文要点**
- We get the same probability distribution for the asset price at time T in each of the following cases:
- 1. The asset starts at price S0 and provides a yield = q
- 2. The asset starts at price S0e–qT and provides no income

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 13. European Options on Assets Providing Known Yieldcontinued（期权）

**原文要点**
- We can value European options by reducing the asset price to S0e–qT and then behaving as though there is no income

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 14. Extension of Chapter 11 Results(Equations 17.1 to 17.3)

**原文要点**
- Lower Bound for calls:
- Lower Bound for puts
- Put Call Parity

📌 **中文解释**：看涨期权对应买入权，适合表达上涨观点或构造上行保护。看跌期权对应卖出权，常用于下行保护或表达下跌观点。

---

### 15. Extension of Chapter 15 Results (Equations 17.4 and 17.5)

📌 **中文解释**：这一页是“学习带连续收益率或外币利率的期权定价与应用。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 16. Alternative Formulas (equations 17.8 and 17.9)

📌 **中文解释**：这一页是“学习带连续收益率或外币利率的期权定价与应用。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 17. Valuing European Index Options（期权）

**原文要点**
- We can use these formulas for an option on an asset paying a dividend yield
- Set S0 = current index level
- Set F0= futures or forward index price for a contract maturing at the same time as the option
- Set q = average dividend yield expected during the life of the option

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 18. Implied Forward Prices and Dividend Yields (equation (17.10)（远期）

**原文要点**
- From European calls and puts with the same strike price and time to maturity
- These formulas allow term structures of forward prices and dividend yields to be estimated
- OTC European options are typically valued using the forward prices (Estimates of q are not then required)
- American options require the dividend yield term structure

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 19. Valuing European Currency Options（期权）

**原文要点**
- A foreign currency is an asset that provides a yield equal to rf
- We can use the formula for an option on a stock paying a dividend yield :
- S0 = current exchange rate
- q = rƒ

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 20. Formulas for European Currency Options (Equations 17.11 and 17.12)（期权）

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 21. Alternative Formulas (Equations 17.13 and 17.14)

**原文要点**
- Using

📌 **中文解释**：这一页是“学习带连续收益率或外币利率的期权定价与应用。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 22. The Binomial Model（二叉树）

**原文要点**
- S0u
- ƒu
- S0d
- ƒd
- S0
- ƒ
- p
- (1 – p )
- f=e-rT[pfu+(1−p)fd ]

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 23. The Binomial Model continued（二叉树）

**原文要点**
- In a risk-neutral world the asset price grows at r−q rather than at r when there is a dividend yield at rate q
- The probability, p, of an up movement must therefore satisfy
- pS0u+(1−p)S0d = S0e (r−q)T
- so that

📌 **中文解释**：树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 24. The Binomial Model continued（二叉树）

**原文要点**
- In the case of an option on a stock index we set q equal to the dividend yield on the index
- In the case of a currency we set q equal to the foreign risk-free rate

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
