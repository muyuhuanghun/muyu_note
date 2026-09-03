# Ch10 期权市场机制

**相关笔记**: [[Ch09HullOFOD11thEdition|上一章：XVA 调整]] | [[Ch11HullOFOD11thEdition|下一章：股票期权性质]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 10 Mechanics of Options Markets
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：认识看涨/看跌、欧式/美式、执行价、到期日、交易规则和期权报价。

💡 **核心理解**：先把期权头寸的收益结构画清楚，再谈复杂策略和定价模型。

本章可以按下面的顺序阅读：
1. Review of Option Types（期权）
2. Option Positions（期权）
3. Long Call (Figure 10.1)（看涨期权）
4. Short Call (Figure 10.3)（看涨期权）
5. Long Put (Figure 10.2)（看跌期权）
6. Short Put (Figure 10.4)（看跌期权）
7. Payoffs from Options (Figure 10.5)What is the Option Position in Each Case?（期权）
8. Assets Underlying Exchange-Traded Options（期权）
9. Specification of Exchange-Traded Options（期权）
10. Terminology
11. Terminology(continued)
12. Other CBOE Product
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **期权**：买方支付权利金，获得未来按执行价买入或卖出标的的权利。
- **看涨期权**：赋予买入标的资产的权利。
- **看跌期权**：赋予卖出标的资产的权利。
- **欧式期权**：只能在到期日行权。
- **美式期权**：到期前任意时点都可以行权。
- **实值/平值/虚值**：描述标的价格与执行价的相对关系。

---

## 三、逐页整理

### 2. Review of Option Types（期权）

**原文要点**
- A call is an option to buy
- A put is an option to sell
- A European option can be exercised only at the end of its life
- An American option can be exercised at any time

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 3. Option Positions（期权）

**原文要点**
- Long call
- Long put
- Short call
- Short put

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 4. Long Call (Figure 10.1)（看涨期权）

**原文要点**
- Profit from buying one European call option: option price = $5, strike price = $100, option life = 2 months

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 5. Short Call (Figure 10.3)（看涨期权）

**原文要点**
- Profit from writing one European call option: option price = $5, strike price = $100

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 6. Long Put (Figure 10.2)（看跌期权）

**原文要点**
- Profit from buying a European put option: option price = $7, strike price = $70

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看跌期权对应卖出权，常用于下行保护或表达下跌观点。

---

### 7. Short Put (Figure 10.4)（看跌期权）

**原文要点**
- Profit from writing a European put option: option price = $7, strike price = $70

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看跌期权对应卖出权，常用于下行保护或表达下跌观点。

---

### 8. Payoffs from Options (Figure 10.5)What is the Option Position in Each Case?（期权）

**原文要点**
- K = Strike price, ST = Price of asset at maturity
- Payoff
- Payoff

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 9. Assets Underlying Exchange-Traded Options（期权）

**原文要点**
- Stocks
- ETFs (and other ETPs)
- Foreign Currency
- Stock Indices
- Futures

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 10. Specification of Exchange-Traded Options（期权）

**原文要点**
- Expiration date
- Strike price
- European or American
- Call or Put (option class)

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 11. Terminology

**原文要点**
- Moneyness :
- At-the-money option
- In-the-money option
- Out-of-the-money option

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 12. Terminology(continued)

**原文要点**
- Option class
- Option series
- Intrinsic value
- Time value

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 13. Other CBOE Product

**原文要点**
- Flex options
- Weeklys

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 14. Dividends & Stock Splits

**原文要点**
- Suppose you own N options with a strike price of K :
- No adjustments are made to the option terms for cash dividends
- When there is an n-for-m stock split,
- the strike price is reduced to mK/n
- the no. of options is increased to nN/m
- Stock dividends are handled similarly to stock splits

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 15. Dividends & Stock Splits(continued)

**原文要点**
- Consider a call option to buy 100 shares for $20/share
- How should terms be adjusted:
- for a 2-for-1 stock split?
- for a 5% stock dividend?

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 16. Market Makers

**原文要点**
- Most exchanges use market makers to facilitate options trading
- A market maker quotes both bid and ask prices when requested
- The market maker does not know whether the individual requesting the quotes wants to buy or sell

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 17. Margin（保证金）

**原文要点**
- Margin is required when options are sold
- When a naked option is written the margin is the greater of:
- A total of 100% of the proceeds of the sale plus 20% of the underlying share price less the amount (if any) by which the option is out of the money
- A total of 100% of the proceeds of the sale plus 10% of the underlying share price (call) or exercise price (put)
- For other trading strategies there are special rules

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。保证金机制把潜在违约损失提前现金化，是清算体系控制风险的重要手段。

---

### 18. Warrants

**原文要点**
- Warrants are options that are issued by a corporation or a financial institution
- The number of warrants outstanding is determined by the size of the original issue and changes only when they are exercised or when they expire

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 19. Warrants(continued)

**原文要点**
- The issuer settles up with the holder when a warrant is exercised
- When call warrants are issued by a corporation on its own stock, exercise will usually lead to new treasury stock being issued

📌 **中文解释**：这一页是“认识看涨/看跌、欧式/美式、执行价、到期日、交易规则和期权报价。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 20. Employee Stock Options (see also Chapter 16)（期权）

**原文要点**
- Employee stock options are a form of remuneration issued by a company to its executives
- They are usually at the money when issued
- When options are exercised the company issues more stock and sells it to the option holder for the strike price
- Expensed on the income statement

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 21. Convertible Bonds

**原文要点**
- Convertible bonds are regular bonds that can be exchanged for equity at certain times in the future according to a predetermined exchange ratio
- Usually a convertible is callable
- The call provision is a way in which the issuer can force conversion at a time earlier than the holder might otherwise choose

📌 **中文解释**：这一页是“认识看涨/看跌、欧式/美式、执行价、到期日、交易规则和期权报价。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
