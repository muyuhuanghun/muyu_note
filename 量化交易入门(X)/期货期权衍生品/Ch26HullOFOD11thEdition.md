# Ch26 奇异期权

**相关笔记**: [[Ch25HullOFOD11thEdition|上一章：信用衍生品]] | [[Ch27HullOFOD11thEdition|下一章：模型与数值方法进阶]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 26 Exotic Options
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：了解障碍、亚式、回望、复合、篮子等非标准期权。

💡 **核心理解**：奇异期权的价值通常由路径依赖、触发条件或多个标的共同决定。

本章可以按下面的顺序阅读：
1. Types of Exotics（奇异期权）
2. Packages (Section 26.1)
3. Perpetual American Options (Section 26.2)（期权）
4. Perpetual American Options continued（期权）
5. Non-Standard American Options (Section 26.3)（期权）
6. Gap Options (equations 26.1 and 26.2)（期权）
7. Forward Start Options (Section 26.5)（期权）
8. Cliquet Option (Section 26.6)（期权）
9. Compound Options (Section 26.7)（期权）
10. Chooser Option “As You Like It” (Section 26.8)（期权）
11. Chooser Option as a Package（期权）
12. Barrier Options (Section 26.9)（期权）
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **奇异期权**：条款比普通期权更复杂的非标准期权。
- **障碍期权**：价格触碰障碍水平后生效或失效的期权。
- **亚式期权**：收益依赖一段时间平均价格的期权。
- **期权**：买方支付权利金，获得未来按执行价买入或卖出标的的权利。

---

## 三、逐页整理

### 2. Types of Exotics（奇异期权）

**原文要点**
- Packages
- Perpetual American calls and puts
- Nonstandard American options
- Gap options
- Forward start options
- Cliquet options
- Compound options
- Chooser options
- Barrier options
- Binary options
- Lookback options
- Shout options
- Asian options
- Options to exchange one asset for another
- Options involving several assets
- Volatility and Variance swaps

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 3. Packages (Section 26.1)

**原文要点**
- Portfolios of standard options
- Examples from Chapter 11: bull spreads, bear spreads, straddles, etc
- Often structured to have zero cost
- One popular package is a range forward contract (see Chapter 17)

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 4. Perpetual American Options (Section 26.2)（期权）

**原文要点**
- Consider first a derivative that pays off Q when S = H for the first time and S0 < H
- (a > 0) satisfies the boundary conditions. It satisfies the differential equation
- when
- This has solutions a1>0 and a2<0
- The value of the derivative is therefore

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 5. Perpetual American Options continued（期权）

**原文要点**
- Consider next a perpetual American call option with strike price K
- If it is exercised when S=H the value is
- This is maximized when
- The value of the perpetual call is therefore
- The value of a perpetual put is similarly

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 6. Non-Standard American Options (Section 26.3)（期权）

**原文要点**
- Exercisable only on specific dates (Bermudans)
- Early exercise allowed during only part of life (initial “lock out” period)
- Strike price changes over the life (warrants, convertibles)

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 7. Gap Options (equations 26.1 and 26.2)（期权）

**原文要点**
- Gap call pays ST − K1 when ST > K2
- Gap put pays off K1 − ST when ST < K2
- Can be valued with a small modification to BSM

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。

---

### 8. Forward Start Options (Section 26.5)（期权）

**原文要点**
- Option starts at a future time, T1
- Implicit in employee stock option plans
- Often structured so that strike price equals asset price at time T1
- Value is then times the value of similar option starting today

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 9. Cliquet Option (Section 26.6)（期权）

**原文要点**
- A series of call or put options with rules determining how the strike price is determined
- For example, a cliquet might consist of 20 at-the-money three-month options. The total life would then be five years
- When one option expires a new similar at-the-money is comes into existence

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 10. Compound Options (Section 26.7)（期权）

**原文要点**
- Option to buy or sell an option
- Call on call
- Put on call
- Call on put
- Put on put
- Can be valued analytically
- Price is quite low compared with a regular option

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 11. Chooser Option “As You Like It” (Section 26.8)（期权）

**原文要点**
- Option starts at time 0, matures at T2
- At T1 (0 < T1 < T2) buyer chooses whether it is a put or call
- This is a package!

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 12. Chooser Option as a Package（期权）

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 13. Barrier Options (Section 26.9)（期权）

**原文要点**
- Option comes into existence only if stock price hits barrier before option maturity
- ‘In’ options
- Option dies if stock price hits barrier before option maturity
- ‘Out’ options

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 14. Barrier Options (continued)（期权）

**原文要点**
- Stock price must hit barrier from below
- ‘Up’ options
- Stock price must hit barrier from above
- ‘Down’ options
- Option may be a put or a call
- Eight possible combinations

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 15. Parity Relations

**原文要点**
- c = cui + cuo
- c = cdi + cdo
- p = pui + puo
- p = pdi + pdo

📌 **中文解释**：证券化把资产池现金流重新分层出售，关键风险在资产相关性和分层吸收损失的顺序。

---

### 16. Binary Options (Section 26.10)（期权）

**原文要点**
- Cash-or-nothing: pays Q if ST > K, otherwise pays nothing.
- Value = e–rT Q N(d2)
- Asset-or-nothing: pays ST if ST > K, otherwise pays nothing.
- Value = S0e-qT N(d1)

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 17. Decomposition of a Call Option（期权）

**原文要点**
- Long: Asset-or-Nothing option
- Short: Cash-or-Nothing option where payoff is K
- Value = S0e-qT N(d1) – e–rT KN(d2)

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 18. Lookback Options (Section 26.11)（期权）

**原文要点**
- Floating lookback call pays ST – Smin at time T (Allows buyer to buy stock at lowest observed price in some interval of time)
- Floating lookback put pays Smax– ST at time T
- (Allows buyer to sell stock at highest observed price in some interval of time)
- Fixed lookback call pays max(Smax−K, 0)
- Fixed lookback put pays max(K −Smin, 0)
- Analytic valuation for all types

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 19. Shout Options (Section 26.12)（期权）

**原文要点**
- Buyer can ‘shout’ once during option life
- Final payoff is either
- Usual option payoff, max(ST – K, 0), or
- Intrinsic value at time of shout, St – K
- Payoff: max(ST – St , 0) + St – K
- Similar to lookback option but cheaper

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 20. Asian Options (Section 26.13)（期权）

**原文要点**
- Payoff related to average stock price
- Average Price options pay:
- Call: max(Save – K, 0)
- Put: max(K – Save , 0)
- Average Strike options pay:
- Call: max(ST – Save , 0)
- Put: max(Save – ST , 0)

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 21. Asian Options（期权）

**原文要点**
- No exact analytic valuation
- Can be approximately valued by assuming that the average stock price is lognormally distributed

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 22. Exchange Options (Section 26.14)（期权）

**原文要点**
- Option to exchange one asset for another
- For example, an option to exchange one unit of U for one unit of V
- Payoff is max(VT – UT, 0)

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 23. Basket Options (Section 26.15)（期权）

**原文要点**
- A basket option is an option to buy or sell a portfolio of assets
- This can be valued by calculating the first two moments of the value of the basket at option maturity and then assuming it is lognormal

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 24. Volatility and Variance Swaps (Section 26.16)（波动率）

**原文要点**
- Volatility swap is agreement to exchange the realized volatility between time 0 and time T for a prespecified fixed volatility with both being multiplied by a prespecified principal
- Variance swap is agreement to exchange the realized variance rate between time 0 and time T for a prespecified fixed variance rate with both being multiplied by a prespecified principal
- Daily return is assumed to be zero in calculating the volatility or variance rate

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 25. Variance Swap (equation 26.6)（互换）

**原文要点**
- The (risk-neutral) expected variance rate between times 0 and T can be calculated from the prices of European call and put options with different strikes and maturity T
- For any value of S

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 26. Volatility Swap (equation 26.9)（波动率）

**原文要点**
- For a volatility swap it is necessary to use the approximate relation

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

### 27. VIX Index

**原文要点**
- The expected value of the variance of the S&P 500 over 30 days is calculated from the CBOE market prices of European put and call options on the S&P 500 using the expression for
- This is then multiplied by 365/30 and the VIX index is set equal to the square root of the result

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 28. How Difficult is it to Hedge Exotic Options?（期权）

**原文要点**
- In some cases exotic options are easier to hedge than the corresponding vanilla options (e.g., Asian options)
- In other cases they are more difficult to hedge (e.g., barrier options)

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

### 29. Static Options Replication(Section 26.17)（期权）

**原文要点**
- This involves approximately replicating an exotic option with a portfolio of vanilla options
- Underlying principle: if we match the value of an exotic option on some boundary , we have matched it at all interior points of the boundary
- Static options replication can be contrasted with dynamic options replication where we have to trade continuously to match the option

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 30. Example

**原文要点**
- A 9-month up-and-out call option an a non-dividend paying stock where S0 = 50, K = 50, the barrier is 60, r = 10%, and s = 30%
- Any boundary can be chosen but the natural one is
- c (S, 0.75) = max(S – 50, 0) when S < 60
- c (60, t ) = 0 when 0 £ t £ 0.75

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 31. Slide 31

**原文要点**
- The Boundary (Figure 26.1)

**原始表格 / 图示**
![[Ch26HullOFOD11thEdition/Ch26HullOFOD11thEdition_slide31_1.x-wmf]]

📌 **中文解释**：这一页是“了解障碍、亚式、回望、复合、篮子等非标准期权。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 32. Example (continued)

**原文要点**
- We might try to match the following points on the boundary
- c(S , 0.75) = MAX(S – 50, 0) for S < 60
- c(60, 0.50) = 0
- c(60, 0.25) = 0
- c(60, 0.00) = 0

📌 **中文解释**：这一页是“了解障碍、亚式、回望、复合、篮子等非标准期权。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 33. Example continued(See Table 26.1)

**原文要点**
- We can do this as follows:
- +1.00 call with maturity 0.75 & strike 50
- –2.66 call with maturity 0.75 & strike 60
- +0.97 call with maturity 0.50 & strike 60
- +0.28 call with maturity 0.25 & strike 60

📌 **中文解释**：这一页是“了解障碍、亚式、回望、复合、篮子等非标准期权。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 34. Example (continued)

**原文要点**
- This portfolio is worth 0.73 at time zero compared with 0.31 for the up-and out option
- As we use more options the value of the replicating portfolio converges to the value of the exotic option
- For example, with 18 points matched on the horizontal boundary the value of the replicating portfolio reduces to 0.38; with 100 points being matched it reduces to 0.32

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 35. Using Static Options Replication（期权）

**原文要点**
- To hedge an exotic option we short the portfolio that replicates the boundary conditions
- The portfolio must be unwound when any part of the boundary is reached

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
