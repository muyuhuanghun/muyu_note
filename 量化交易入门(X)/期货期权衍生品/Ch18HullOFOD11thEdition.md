# Ch18 期货期权与 Black 模型

**相关笔记**: [[Ch17HullOFOD11thEdition|上一章：股指和外汇期权]] | [[Ch19HullOFOD11thEdition|下一章：希腊字母]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 18 Futures Options and Black’s Model
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：理解期货期权、Black 模型、期权与期货保证金现金流之间的关系。

💡 **核心理解**：当标的是期货价格时，定价变量和贴现逻辑会与股票期权不同。

本章可以按下面的顺序阅读：
1. Options on Futures（期权）
2. Mechanics of Call Futures Options（期权）
3. Mechanics of Put Futures Option（期货）
4. Example 18.1
5. Example 18.2
6. The Payoffs
7. Interest Rate Futures Options（期权）
8. Potential Advantages of Futures Options over Spot Options（期权）
9. European Futures Options（期权）
10. Put-Call Parity for Futures Options (Equation 18.1)（期权）
11. Other Relations (equations 18.2 to 18.4)
12. Growth Rates For Futures Prices（期货）
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **期货**：交易所标准化合约，每日盯市结算，由保证金制度控制违约风险。
- **期权**：买方支付权利金，获得未来按执行价买入或卖出标的的权利。
- **Black-Scholes 模型**：经典欧式期权定价模型。

---

## 三、逐页整理

### 2. Options on Futures（期权）

**原文要点**
- Referred to by the maturity month of the underlying futures
- The option is American and usually expires on or a few days before the earliest delivery date of the underlying futures contract

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 3. Mechanics of Call Futures Options（期权）

**原文要点**
- When a call futures option is exercised the holder acquires
- A long position in the futures
- A cash amount equal to the excess of the futures price at the time of the most recent settlement over the strike price

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 4. Mechanics of Put Futures Option（期货）

**原文要点**
- When a put futures option is exercised the holder acquires
- A short position in the futures
- A cash amount equal to the excess of the strike price over the futures price at the time of the most recent settlement

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 5. Example 18.1

**原文要点**
- Sept. call option contract on copper futures has a strike of 320 cents per pound. It is exercised when futures price is 331 cents and most recent settlement is 330. One contract is on 25,000 pounds
- Trader receives
- Long Sept. futures contract on copper
- 25,000 times 10 cents or $2,500 in cash

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 6. Example 18.2

**原文要点**
- Dec put option contract on corn futures has a strike price of 600 cents per bushel. It is exercised when the futures price is 580 cents per bushel and the most recent settlement price is 579 cents per bushel. One contract is on 5000 bushels
- Trader receives
- Short Dec futures contract on corn
- $1,050 in cash

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 7. The Payoffs

**原文要点**
- If the futures position is closed out immediately:
- Payoff from call = F– K
- Payoff from put = K – F
- where F is futures price at time of exercise

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。

---

### 8. Interest Rate Futures Options（期权）

**原文要点**
- Options on T-Bond futures (quoted as percentage of face value to the nearest 1/64 of 1%)
- Options on 3-month SOFR futures or Eurodollar futures. Each one basis point in the quote represents $25
- If you think interest rates will go up should you buy call or put options?

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 9. Potential Advantages of Futures Options over Spot Options（期权）

**原文要点**
- Futures contracts may be easier to trade and more liquid than the underlying asset
- Exercise of option does not lead to delivery of underlying asset
- Futures options and futures usually trade on same exchange
- Futures options may entail lower transactions costs

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 10. European Futures Options（期权）

**原文要点**
- European futures options and European spot options are equivalent when futures contract matures at the same time as the option
- It is common to regard European spot options as European futures options when they are valued

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 11. Put-Call Parity for Futures Options (Equation 18.1)（期权）

**原文要点**
- Consider the following two portfolios:
- 1. European call plus Ke−rT of cash
- 2. European put plus long futures plus cash equal to F0e−rT
- They must be worth the same at time T so that
- c + Ke−rT = p + F0e−rT

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 12. Other Relations (equations 18.2 to 18.4)

**原文要点**
- F0 e−rT – K < C – P < F0 – Ke−rT
- c > (F0 – K)e−rT
- p > (F0 – K)e−rT

📌 **中文解释**：这一页是“理解期货期权、Black 模型、期权与期货保证金现金流之间的关系。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 13. Growth Rates For Futures Prices（期货）

**原文要点**
- A futures contract requires no initial investment
- In a risk-neutral world the expected return should be zero
- The expected growth rate of the futures price is therefore zero
- The futures price can therefore be treated like a stock paying a dividend yield of r

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。

---

### 14. Valuing European Futures Options（期权）

**原文要点**
- We can use the formula for an option on a stock paying a dividend yield
- S0 = current futures price, F0
- q = domestic risk-free rate, r
- Setting q = r ensures that the expected growth of F in a risk-neutral world is zero
- The result is referred to as Black’s model because it was first suggested in a paper by Fischer Black in 1976

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 15. Black’s Model (Equations 18.7 and 18.8)

📌 **中文解释**：Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。

---

### 16. How Black’s Model is Used in Practice

**原文要点**
- Black’s model is frequently used to value European options on the spot price of an asset
- This avoids the need to estimate income on the asset

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。

---

### 17. Using Black’s Model Instead of Black-Scholes-Merton (Example 18.7)（Black-Scholes-Merton 模型）

**原文要点**
- Consider a 6-month European call option on spot gold
- 6-month futures price is 1,240, 6-month risk-free rate is 5%, strike price is 1,200, and volatility of futures price is 20%
- Value of option is given by Black’s model with F0 = 1,240, K=1,200, r = 0.05, T=0.5, and s = 0.2
- It is 88.37

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 18. Binomial Tree Example (Figure 18.1)（二叉树）

**原文要点**
- A 1-month call option on futures has a strike price of 29.
- Futures Price = $28
- Option Price = $0

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 19. Setting Up a Riskless Portfolio

**原文要点**
- Consider the Portfolio: long D futures short 1 call option
- Portfolio is riskless when 3D − 4 = −2D or D = 0.8

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 20. Valuing the Portfolio( Risk-Free Rate is 6% )

**原文要点**
- The riskless portfolio is:
- long 0.8 futures short 1 call option
- The value of the portfolio in 1 month is −1.6
- The value of the portfolio today is −1.6e−0.06/12 = −1.592

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 21. Valuing the Option（期权）

**原文要点**
- The portfolio that is
- long 0.8 futures short 1 option
- is worth −1.592
- The value of the futures is zero
- The value of the option must therefore be 1.592

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 22. Generalization of Binomial Tree Example (Figure 18.2)（二叉树）

**原文要点**
- A derivative lasts for time T and is dependent on a futures price

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。

---

### 23. Generalization(continued)

**原文要点**
- Consider the portfolio that is long D futures and short 1 derivative
- The portfolio is riskless when
- F0u D - F0 D – ƒu
- F0d D- F0D – ƒd

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。

---

### 24. Generalization(continued)

**原文要点**
- Value of the portfolio at time T is F0u D – F0D – ƒu
- Value of portfolio today is –ƒ
- Hence ƒ = − [F0uD − F0D − ƒu]e−rT

📌 **中文解释**：这一页是“理解期货期权、Black 模型、期权与期货保证金现金流之间的关系。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 25. Generalization(continued)

**原文要点**
- Substituting for D we obtain
- ƒ = [ p ƒu + (1 – p )ƒd ]e–rT
- where

📌 **中文解释**：这一页是“理解期货期权、Black 模型、期权与期货保证金现金流之间的关系。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 26. Futures Option Price vs Spot Option Price（期货）

**原文要点**
- If futures prices are higher than spot prices (normal market), an American call on futures is worth more than a similar American call on spot. An American put on futures is worth less than a similar American put on spot.
- When futures prices are lower than spot prices (inverted market) the reverse is true.

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 27. Futures Style Options（期权）

**原文要点**
- A futures-style option is a futures contract on the option payoff
- Some exchanges trade these in preference to regular futures options
- The futures price for a call futures-style option is
- The futures price for a put futures-style option is

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 28. Summary: Put-Call Parity Results（看涨期权）

📌 **中文解释**：这一页是“理解期货期权、Black 模型、期权与期货保证金现金流之间的关系。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 29. Summary of Key Results from Chapters 17 and 18

**原文要点**
- We can treat stock indices, currencies, and futures like a stock paying a dividend yield of q
- For stock indices, q is average dividend yield on the index over the option life
- For currencies, q = rƒ
- For futures, q = r

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
