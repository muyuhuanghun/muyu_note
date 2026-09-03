# Ch01 衍生品导论

**相关笔记**: [[Ch02HullOFOD11thEdition|下一章：期货市场与中央对手方]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 1 Introduction
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：理解衍生品是什么、为什么重要，以及远期、期货、期权等基础工具的用途。

💡 **核心理解**：衍生品不是独立资产，它的价值来自标的资产；入门时先抓住风险转移、投机、套利三条主线。

本章可以按下面的顺序阅读：
1. What is a Derivative?（衍生品是什么）
2. Why Derivatives Are Important（为什么衍生品重要）
3. How Derivatives Are Traded（衍生品如何交易）
4. The OTC Market Prior to 2008（场外市场）
5. Since 2008…
6. Size of OTC and Exchange-Traded Markets(Figure 1.1)（场外市场）
7. The Lehman Bankruptcy (Business Snapshot 1.1)
8. How Derivatives are Used（衍生品的用途）
9. Foreign Exchange Quotes for GBP, May 21, 2020 (Table 1.1)
10. Forward Price（远期）
11. Terminology
12. Example
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **衍生品**：价值依赖股票、利率、汇率、商品等标的资产的金融合约。
- **远期**：场外定制合约，到期按约定价格买卖标的，信用风险通常更集中。
- **期货**：交易所标准化合约，每日盯市结算，由保证金制度控制违约风险。
- **互换**：双方按约定规则交换未来现金流，可看成一组远期合约。
- **期权**：买方支付权利金，获得未来按执行价买入或卖出标的的权利。
- **看涨期权**：赋予买入标的资产的权利。
- **看跌期权**：赋予卖出标的资产的权利。
- **场外市场**：交易双方直接协商条款，灵活但更依赖信用管理。
- **中央对手方**：站在交易双方中间清算，降低双边信用风险。

---

## 三、逐页整理

### 2. What is a Derivative?（衍生品是什么）

**原文要点**
- A derivative is an instrument whose value depends on, or is derived from, the value of another asset.
- Examples: futures, forwards, swaps, options, exotics…

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。

---

### 3. Why Derivatives Are Important（为什么衍生品重要）

**原文要点**
- Derivatives play a key role in transferring risks in the economy
- The underlying assets include stocks, currencies, interest rates, commodities, debt instruments, electricity prices, insurance payouts, the weather, etc
- Many financial transactions have embedded derivatives
- The real options approach to assessing capital investment decisions has become widely accepted

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 4. How Derivatives Are Traded（衍生品如何交易）

**原文要点**
- On exchanges such as the Chicago Board Options Exchange (CBOE)
- In the over-the-counter (OTC) market where traders working for banks, fund managers and corporate treasurers contact each other directly

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 5. The OTC Market Prior to 2008（场外市场）

**原文要点**
- Largely unregulated
- Banks acted as market makers quoting bids and asks
- Master agreements usually defined how transactions between two parties would be handled
- But some transactions were cleared through central counterparties (CCPs). A CCP stands between the two sides to a transaction in the same way that an exchange does

📌 **中文解释**：场外交易条款灵活，但必须额外管理交易对手信用、清算和监管报告。中央对手方通过保证金、盯市和清算会员制度降低双边违约风险。

---

### 6. Since 2008…

**原文要点**
- OTC market has become regulated. Objectives:
- Reduce systemic risk (see Business Snapshot 1.2)
- Increase transparency
- In the U.S and some other countries, standardized OTC products must be traded on swap execution facilities (SEFs) which are electronic platforms similar to exchanges
- CCPs must be used to clear standardized transactions between financial institutions in most countries
- All trades must be reported to a central repository

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。场外交易条款灵活，但必须额外管理交易对手信用、清算和监管报告。

---

### 7. Size of OTC and Exchange-Traded Markets(Figure 1.1)（场外市场）

**原文要点**
- Source: Bank for International Settlements. Chart shows total principal amounts for OTC market and value of underlying assets for exchange market

📌 **中文解释**：场外交易条款灵活，但必须额外管理交易对手信用、清算和监管报告。

---

### 8. The Lehman Bankruptcy (Business Snapshot 1.1)

**原文要点**
- Lehman’s filed for bankruptcy on September 15, 2008. This was the biggest bankruptcy in US history
- Lehman was an active participant in the OTC derivatives markets and got into financial difficulties because it took high risks and found it was unable to roll over its short term funding
- It had hundreds of thousands of transactions outstanding with about 8,000 counterparties
- Unwinding these transactions has been challenging for both the Lehman liquidators and their counterparties

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。场外交易条款灵活，但必须额外管理交易对手信用、清算和监管报告。

---

### 9. How Derivatives are Used（衍生品的用途）

**原文要点**
- To hedge risks
- To speculate (take a view on the future direction of the market)
- To lock in an arbitrage profit
- To change the nature of a liability
- To change the nature of an investment without incurring the costs of selling one portfolio and buying another

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

### 10. Foreign Exchange Quotes for GBP, May 21, 2020 (Table 1.1)

**原始表格 / 图示**
|  | Bid | Ask |
|---|---|---|
| Spot | 1.2217 | 1.2220 |
| 1-month forward | 1.2218 | 1.2222 |
| 3-month forward | 1.2220 | 1.2225 |
| 6-month forward | 1.2224 | 1.2230 |

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 11. Forward Price（远期）

**原文要点**
- The forward price for a contract is the delivery price that would be applicable to the contract if were negotiated today (i.e., it is the delivery price that would make the contract worth exactly zero)
- The forward price may be different for contracts of different maturities (as shown by the table)

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 12. Terminology

**原文要点**
- The party that has agreed to buy has what is termed a long position
- The party that has agreed to sell has what is termed a short position

📌 **中文解释**：这一页是“理解衍生品是什么、为什么重要，以及远期、期货、期权等基础工具的用途。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 13. Example

**原文要点**
- On May 21, 2020, the treasurer of a corporation enters into a long forward contract to buy £1 million in six months at an exchange rate of 1.2230
- This obligates the corporation to pay $1,223,000 for £1 million on November 21, 2020
- What are the possible outcomes?

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 14. Profit from a Long Forward Position (K= delivery price=forward price at time contract is entered into)（远期）

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 15. Profit from a Short Forward Position (K= delivery price=forward price at time contract is entered into)（远期）

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 16. Futures Contracts（期货合约）

**原文要点**
- Agreement to buy or sell an asset for a certain price at a certain time
- Similar to forward contract
- Whereas a forward contract is traded OTC, a futures contract is traded on an exchange

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 17. Exchanges Trading Futures（期货）

**原文要点**
- CME Group (formed when Chicago Mercantile Exchange and Chicago Board of Trade merged)
- InterContinental Exchange
- B3 (Brazil)
- Tokyo Financial Exchange (Tokyo)
- and many more (see list at end of book)

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。

---

### 18. Examples of Futures Contracts（期货合约）

**原文要点**
- Agreement to:
- Buy 100 oz. of gold @ US$1800/oz. in December
- Sell £62,500 @ 1.2500 US$/£ in March
- Sell 1,000 bbl. of oil @ US$40/bbl. in April

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。

---

### 19. 1. An Arbitrage Opportunity?

**原文要点**
- Suppose that:
- The price of a non-dividend-paying stock is $60
- The 1-year forward price of the stock is $65
- The 1-year US$ interest rate is 5% per annum
- Is there an arbitrage opportunity?

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 20. 2. Another Arbitrage Opportunity?

**原文要点**
- Suppose that:
- The price of a non-dividend-paying stock is $60
- The 1-year forward price of the stock is $60
- The 1-year US$ interest rate is 5% per annum
- Is there an arbitrage opportunity?

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 21. The Forward Price of a Non-Dividend Paying Stock（远期）

**原文要点**
- If the spot price is S and the forward price for a contract deliverable in T years is F, then
- F = S (1+r )T
- where r is the 1-year (domestic currency) risk-free rate of interest.
- In our examples, S = 60, T = 1, and r =0.05 so that
- F = 60(1+0.05) = 63

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 22. 1. Oil: An Arbitrage Opportunity?

**原文要点**
- Suppose that:
- The spot price of oil is US$50
- The quoted 1-year futures price of oil is US$60
- The 1-year US$ interest rate is 5% per annum
- The storage costs of oil are 2% per annum
- Is there an arbitrage opportunity?

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 23. 2. Oil: Another Arbitrage Opportunity?

**原文要点**
- Suppose that:
- The spot price of oil is US$50
- The quoted 1-year futures price of oil is US$40
- The 1-year US$ interest rate is 5% per annum
- The storage costs of oil are 2% per annum
- Is there an arbitrage opportunity?

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 24. Options（期权）

**原文要点**
- A call option is an option to buy a certain asset by a certain date for a certain price (the strike price)
- A put option is an option to sell a certain asset by a certain date for a certain price (the strike price)

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 25. American vs European Options（期权）

**原文要点**
- An American option can be exercised at any time during its life
- A European option can be exercised only at maturity

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 26. Apple Call Option Prices from CBOE (May 21, 2020); Stock Price is bid 316.23, ask 316.50 (Table 1.2)（期权）

**原始表格 / 图示**
| Strike Price | Jun 2020 Bid | Jun 2020 Ask | Sep 2020 Bid | Sep 2020 Ask | Dec 2020 Bid | Dec 2020 Ask |
|---|---|---|---|---|---|---|
| 290 | 29.80 | 30.85 | 39.35 | 40.40 | 46.20 | 47.60 |
| 300 | 21.55 | 22.40 | 32.50 | 33.90 | 40.00 | 41.15 |
| 310 | 14.35 | 15.30 | 26.35 | 27.25 | 34.25 | 35.65 |
| 320 | 8.65 | 9.00 | 20.45 | 21.70 | 28.65 | 29.75 |
| 330 | 4.20 | 5.00 | 15.85 | 16.25 | 23.90 | 24.75 |
| 340 | 1.90 | 2.12 | 11.35 | 12.00 | 19.50 | 20.30 |

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 27. Apple Put Option Prices from CBOE (May 21, 2020); Stock Price is bid 316.23, ask 316.50 (Table 1.3)（期权）

**原始表格 / 图示**
| Strike Price | Jun 2020 Bid | Jun 2020 Ask | Sep 2020 Bid | Sep 2020 Ask | Dec 2020 Bid | Dec 2020 Ask |
|---|---|---|---|---|---|---|
| 290 | 3.00 | 3.30 | 12.70 | 13.65 | 20.05 | 21.30 |
| 300 | 4.80 | 5.20 | 15.85 | 16.85 | 23.60 | 24.90 |
| 310 | 7.15 | 7.85 | 19.75 | 20.50 | 28.00 | 28.95 |
| 320 | 11.25 | 12.05 | 24.05 | 24.80 | 32.45 | 33.35 |
| 330 | 17.10 | 17.85 | 28.75 | 29.85 | 37.45 | 38.40 |
| 340 | 24.40 | 25.45 | 34.45 | 35.65 | 42.95 | 44.05 |

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看跌期权对应卖出权，常用于下行保护或表达下跌观点。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 28. Options vs Futures/Forwards（期权）

**原文要点**
- A futures/forward contract gives the holder the obligation to buy or sell at a certain price
- An option gives the holder the right to buy or sell at a certain price

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 29. Types of Traders

**原文要点**
- Hedgers
- Speculators
- Arbitrageurs

📌 **中文解释**：这一页是“理解衍生品是什么、为什么重要，以及远期、期货、期权等基础工具的用途。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 30. Hedging Examples（套期保值）

**原文要点**
- A US company will pay £10 million for imports from Britain in 3 months and decides to hedge using a long position in a forward contract
- An investor owns 1,000 shares currently worth $28 per share. A two-month put with a strike price of $27.50 costs $1. The investor decides to hedge by buying 10 contracts

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

### 31. Value of Shares with and without Hedging (Figure 1.4)（套期保值）

📌 **中文解释**：套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

### 32. Speculation Example

**原文要点**
- An investor with $2,000 to invest feels that a stock price will increase over the next 2 months. The current stock price is $20 and the price of a 2-month call option with a strike of 22.50 is $1
- What are the alternative strategies?

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 33. Arbitrage Example

**原文要点**
- A stock price is quoted as £100 in London and $120 in New York
- The current exchange rate is 1.2300
- What is the arbitrage opportunity?

📌 **中文解释**：这一页是“理解衍生品是什么、为什么重要，以及远期、期货、期权等基础工具的用途。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 34. Dangers

**原文要点**
- Traders can switch from being hedgers to speculators or from being arbitrageurs to speculators
- It is important to set up controls to ensure that trades are using derivatives in for their intended purpose
- Soc Gen (see Business Snapshot 1.4) is an example of what can go wrong

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。

---

### 35. Hedge Funds (see Business Snapshot 1.3)（套期保值）

**原文要点**
- Hedge funds are not subject to the same rules as mutual funds and cannot offer their securities publicly.
- Mutual funds must
- disclose investment policies,
- make shares redeemable at any time,
- limit use of leverage
- Hedge funds are not subject to these constraints.
- Hedge funds use complex trading strategies are big users of derivatives for hedging, speculation and arbitrage

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

### 36. Examples of Hedge Fund Strategies（套期保值）

**原文要点**
- Long/Short Equities
- Convertible Arbitrage
- Distressed Securities
- Emerging Markets
- Global Macro
- Merger Arbitrage

📌 **中文解释**：套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
