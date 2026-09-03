# Ch25 信用衍生品

**相关笔记**: [[Ch24HullOFOD11thEdition|上一章：信用风险]] | [[Ch26HullOFOD11thEdition|下一章：奇异期权]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 25 Credit Derivatives
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：整理 CDS、CDO、合成 CDO、相关性微笑和信用指数产品。

💡 **核心理解**：信用衍生品把违约损失拆出来交易，核心难点是相关违约风险。

本章可以按下面的顺序阅读：
1. Credit Default Swaps（互换）
2. CDS Structure (Figure 25.1)（信用违约互换）
3. Other Details
4. Attractions of the CDS Market（信用违约互换）
5. Using a CDS to Hedge a Bond Position（套期保值）
6. CDS Valuation（信用违约互换）
7. Unconditional Default and Survival Probabilities (Table 25.1)
8. Calculation of PV of Payments(Table 25.2 Principal=$1)
9. Present Value of Expected Payoff (Table 25.3; Principal = $1)
10. PV of Accrual Payment Made in Event of a Default. (Table 25.4; Principal = $1)
11. Putting it all together（看跌期权）
12. Implying Default Probabilities from CDS spreads（信用违约互换）
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **信用违约互换**：买方支付保费，换取违约保护。
- **债务抵押债券**：把信用资产分层后发行的结构化产品。
- **信用风险**：债务人或交易对手不履约导致损失的风险。

---

## 三、逐页整理

### 2. Credit Default Swaps（互换）

**原文要点**
- Buyer of the instrument acquires protection from the seller against a default by a particular company or country (the reference entity)
- Example: Buyer pays a premium of 90 bps per year for $100 million of 5-year protection against company X
- Premium is known as the credit default spread. It is paid for life of contract or until default
- If there is a default, the buyer has the right to sell bonds with a face value of $100 million issued by company X for $100 million (Several bonds are typically deliverable)

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 3. CDS Structure (Figure 25.1)（信用违约互换）

**原文要点**
- Default
- Protection
- Buyer, A
- Default
- Protection
- Seller, B
- 90 bps per year
- Payoff if there is a default by reference entity=100(1-R)
- Recovery rate, R, is the ratio of the value of the bond issued by reference entity immediately after default to the face value of the bond

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 4. Other Details

**原文要点**
- Payments are usually made quarterly in arrears
- In the event of default there is a final accrual payment by the buyer
- Settlement can be specified as delivery of the bonds or (more usually) in cash
- An auction process usually determines the payoff
- Suppose payments are made quarterly in the example just considered. What are the cash flows if there is a default after 3 years and 1 month and recovery rate is 40%?

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 5. Attractions of the CDS Market（信用违约互换）

**原文要点**
- Allows credit risks to be traded in the same way as market risks
- Can be used to transfer credit risks to a third party
- Can be used to diversify credit risks

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 6. Using a CDS to Hedge a Bond Position（套期保值）

**原文要点**
- Portfolio consisting of a 5-year par yield corporate bond that provides a yield of 6% and a long position in a 5-year CDS costing 100 basis points per year is (approximately) a long position in a riskless instrument paying 5% per year
- This shows that bond yield spreads should be close to CDS spreads

📌 **中文解释**：套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。基差风险来自现货和期货价格不同步，这是套保后仍然留下的主要不确定性。

---

### 7. CDS Valuation（信用违约互换）

**原文要点**
- Hazard rate for reference entity is 2%.
- Assume payments are made annually in arrears, that defaults always happen half way through a year, and that the expected recovery rate is 40%
- Suppose that the breakeven CDS rate is s per dollar of notional principal

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 8. Unconditional Default and Survival Probabilities (Table 25.1)

**原始表格 / 图示**
| Time (years) | Survival Probability | Default  Probability |
|---|---|---|
| 1 | 0.9802 | 0.0198 |
| 2 | 0.9608 | 0.0194 |
| 3 | 0.9418 | 0.0190 |
| 4 | 0.9231 | 0.0186 |
| 5 | 0.9048 | 0.0183 |

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 9. Calculation of PV of Payments(Table 25.2 Principal=$1)

**原始表格 / 图示**
| Time (yrs) | Survival Prob | Expected Payment | Discount Factor | PV of Exp Pmt |
|---|---|---|---|---|
| 1 | 0.9802 | 0.9802s | 0.9512 | 0.9324s |
| 2 | 0.9608 | 0.9608s | 0.9048 | 0.8694s |
| 3 | 0.9418 | 0.9418s | 0.8607 | 0.8106s |
| 4 | 0.9231 | 0.9231s | 0.8187 | 0.7558s |
| 5 | 0.9048 | 0.9048s | 0.7788 | 0.7047s |
| Total |  |  |  | 4.0728s |

📌 **中文解释**：这一页是“整理 CDS、CDO、合成 CDO、相关性微笑和信用指数产品。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 10. Present Value of Expected Payoff (Table 25.3; Principal = $1)

**原始表格 / 图示**
| Time (yrs) | Default Probab. | Rec. Rate | Expected Payoff | Discount Factor | PV of Exp. Payoff |
|---|---|---|---|---|---|
| 0.5 | 0.0198 | 0.4 | 0.0119 | 0.9753 | 0.0116 |
| 1.5 | 0.0194 | 0.4 | 0.0116 | 0.9277 | 0.0108 |
| 2.5 | 0.0190 | 0.4 | 0.0114 | 0.8825 | 0.0101 |
| 3.5 | 0.0186 | 0.4 | 0.0112 | 0.8395 | 0.0094 |
| 4.5 | 0.0183 | 0.4 | 0.0110 | 0.7985 | 0.0088 |
| Total |  |  |  |  | 0.0506 |

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 11. PV of Accrual Payment Made in Event of a Default. (Table 25.4; Principal = $1)

**原始表格 / 图示**
| Time | Default Prob | Expected Accr Pmt | Disc Factor | PV of Pmt |
|---|---|---|---|---|
| 0.5 | 0.0198 | 0.0099s | 0.9753 | 0.0097s |
| 1.5 | 0.0194 | 0.0097s | 0.9277 | 0.0090s |
| 2.5 | 0.0190 | 0.0095s | 0.8825 | 0.0084s |
| 3.5 | 0.0186 | 0.0093s | 0.8395 | 0.0078s |
| 4.5 | 0.0183 | 0.0091s | 0.7985 | 0.0073s |
| Total |  |  |  | 0.0422s |

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 12. Putting it all together（看跌期权）

**原文要点**
- PV of expected payments is 4.0728s + 0.0422s = 4.1150s
- The breakeven CDS spread is given by
- 4.1150s = 0.0506 or s = 0.0123 (123 bps)
- The value of a swap negotiated some time ago with a CDS spread of 150bps would be 4.1150×0.0150−0.0506 = 0.0111
- per dollar of the principal.

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 13. Implying Default Probabilities from CDS spreads（信用违约互换）

**原文要点**
- Suppose that the mid market spread for a 5 year newly issued CDS is 100bps per year
- We can reverse engineer our calculations to conclude that the hazard is 1.63% per year.
- If probabilities are implied from CDS spreads and then used to value another CDS the result is not sensitive to the recovery rate providing the same recovery rate is used throughout

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 14. Binary CDS (See Table 25.5)（信用违约互换）

**原文要点**
- The payoff in the event of default is a fixed cash amount
- In our example the PV of the expected payoff for a binary swap is 0.0844 and the breakeven binary CDS spread is 205 bps

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 15. Credit Indices

**原文要点**
- CDX NA IG is a portfolio of 125 investment grade companies in North America
- iTraxx Europe is a portfolio of 125 European investment grade names
- The portfolios are updated on March 20 and Sept 20 each year
- The index can be thought of as the cost per name of buying protection against all 125 names

📌 **中文解释**：这一页是“整理 CDS、CDO、合成 CDO、相关性微笑和信用指数产品。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 16. The Use of Fixed Coupons

**原文要点**
- Increasingly CDSs and CDS indices trade like bonds
- A coupon is specified
- If spread is greater than coupon, the buyer of protection pays Notional Principal × Duration × (Spread−Coupon)
- Otherwise the seller of protection pays
- Notional Principal × Duration × (Coupon−Spread)
- Duration is the amount the spread has to be multiplied by to get the PV of spread payments

📌 **中文解释**：久期是一阶利率风险，适合小幅利率变动下的近似对冲。

---

### 17. CDS Forwards and Options（期权）

**原文要点**
- Example: Forward contract to buy 5 year protection on Ford for 280 bps in one year. If Ford defaults during the one-year life the forward contract ceases to exist
- Example: European option to buy 5 year protection on Ford for 280 bps in one year. If Ford defaults during the one-year life of the option, the option is knocked out

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 18. Basket CDS（信用违约互换）

**原文要点**
- Similar to a regular CDS except that several reference entities are specified
- In a first to default swap there is a payoff when the first entity defaults
- Second, third, and nth to default deals are defined similarly
- Why does pricing depends on default correlation?

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 19. Total Return Swap (Figure 25.2)（互换）

**原文要点**
- Agreement to exchange total return on a portfolio of assets for floating rate plus a spread
- At the end there is a payment reflecting the change in value of the assets
- Usually used as financing tools by companies that want exposure to assets

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 20. Asset Backed Securities

**原文要点**
- Securities created from a portfolio of loans, bonds, credit card receivables, mortgages, auto loans, aircraft leases, music royalties, etc
- Usually the income from the assets is tranched
- A “waterfall” defines how income is first used to pay the promised return to the senior tranche, then to the next most senior tranche, and so on.

📌 **中文解释**：这一页是“整理 CDS、CDO、合成 CDO、相关性微笑和信用指数产品。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 21. Collateralized Debt Obligations (Section 25.8)

**原文要点**
- A cash CDO is an ABS where the underlying assets are debt obligations
- A synthetic CDO involves forming a similar structure with short CDS contracts
- In a synthetic CDO most junior tranche bears losses first. After it has been wiped out, the second most junior tranche bears losses, and so on

📌 **中文解释**：证券化把资产池现金流重新分层出售，关键风险在资产相关性和分层吸收损失的顺序。

---

### 22. Synthetic CDO Example（债务抵押债券）

**原文要点**
- Equity tranche is responsible for losses on underlying CDSs until they reach 5% of total notional principal (earns 1000 bp spread)
- Mezzanine tranche is responsible for losses between 5% and 20% (earns 200 bp spread)
- Senior tranche is responsible for losses over 20% (earns 10 bp spread)

📌 **中文解释**：证券化把资产池现金流重新分层出售，关键风险在资产相关性和分层吸收损失的顺序。

---

### 23. Synthetic CDO Details（债务抵押债券）

**原文要点**
- The income is paid on the remaining tranche principal.
- Example: when losses have reached 8% of the total principal underlying the CDSs, tranche 1 has been wiped out, tranche 2 earns the promised spread (200 basis points) on 80% of its principal

📌 **中文解释**：基差风险来自现货和期货价格不同步，这是套保后仍然留下的主要不确定性。证券化把资产池现金流重新分层出售，关键风险在资产相关性和分层吸收损失的顺序。

---

### 24. Single Tranche Trading

**原文要点**
- This involves trading tranches of portfolios of CDSs without actually forming the portfolios
- Cash flows are calculated in the same way as they would be if the portfolios had been formed

📌 **中文解释**：这一页是“整理 CDS、CDO、合成 CDO、相关性微笑和信用指数产品。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 25. Quotes for Standard Tranches of i Traxx (Table 25.6)

**原文要点**
- Quotes are 30/360 in basis points per year except for the 0-3% tranche where the quote equals the percent of the tranche principal that must be paid upfront in addition to 500 bps per year.

**原始表格 / 图示**
| Date | 0-3% | 3-6% | 6-9% | 9-12% | 12-22% | Index |
|---|---|---|---|---|---|---|
| Jan 1, 2007 | 10.34% | 41.59 | 11.95 | 5.60 | 2.00 | 23 |
| Jan 1, 2008 | 30.98% | 316.90 | 212.40 | 140.00 | 73.60 | 77 |
| Jan 1, 2009 | 64.28% | 1185.63 | 606.69 | 315.63 | 97.13 | 165 |

📌 **中文解释**：基差风险来自现货和期货价格不同步，这是套保后仍然留下的主要不确定性。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 26. Valuation of Tranches of Synthetic CDOs and Basket CDSs (Section 25.10)（债务抵押债券）

**原文要点**
- A popular approach is to use a factor-based Gaussian copula model to define correlations between times to default
- Often all pairwise correlations and all the unconditional default distributions are assumed to be the same
- Market likes to imply a pairwise correlations from market quotes.

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 27. Cumulative Default Probability Conditional on Factor (equations 25.5 and 25.7)

**原文要点**
- From the binomial distribution, the probability of k defaults from n names by time t conditional on F is

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 28. Valuing CDO Tranches（债务抵押债券）

**原文要点**
- Consider times tj (eg: tj=0.25, 0.5, 0.75….)
- Calculate the expected tranche principal, Ej at each time
- The expected payoff between times ti and ti+1 is the reduction in expected principal
- The expected payment at time ti is proportional to the expected principal at that time

📌 **中文解释**：证券化把资产池现金流重新分层出售，关键风险在资产相关性和分层吸收损失的顺序。

---

### 29. Valuation continued. v(t) is discount factor for maturity of t (equations 25.9 to 25.11)

📌 **中文解释**：这一页是“整理 CDS、CDO、合成 CDO、相关性微笑和信用指数产品。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 30. Calculation of the E’s

**原文要点**
- Discretize the distribution of F so that there are, say, 30 values with 30 weights.
- Use binomial distribution to calculate the probability of 0,1, 2, 3… defaults by each time ti on the underlying portfolio for each value of F
- For each value of F calculate expected principal of tranche at each time ti
- Weight value of tranche by probability of F to obtain unconditional expected principals at each time ti

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 31. The F-values and their weights (equation 25.12)

**原文要点**
- Calculated from Gaussian quadrature (or copied from www-2.rotman.utoronto.ca/~hull)

📌 **中文解释**：这一页是“整理 CDS、CDO、合成 CDO、相关性微笑和信用指数产品。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 32. Implied Correlations

**原文要点**
- A compound (tranche) correlation is the correlation that is implied from the price of an individual tranche using the one-factor Gaussian copula model
- A base correlation is correlation that prices the 0 to X% tranche consistently with the market where X% is a detachment point (the end point of a standard tranche)

📌 **中文解释**：这一页是“整理 CDS、CDO、合成 CDO、相关性微笑和信用指数产品。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 33. Procedure for Calculating Base Correlation

**原文要点**
- Calculate compound correlation for each tranche
- Calculate PV of expected loss for each tranche
- Sum these to get PV of expected loss for base correlation tranches
- Calculate correlation parameter in one-factor gaussian copula model that is consistent with this expected loss

📌 **中文解释**：这一页是“整理 CDS、CDO、合成 CDO、相关性微笑和信用指数产品。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 34. Implied Correlations for i Traxx on January 31, 2007 (Table 25.8)

**原始表格 / 图示**
| Tranche | 0-3% | 3-6% | 6-9% | 9-12% | 12-22% |
|---|---|---|---|---|---|
| Compound Correlation | 17.7% | 7.8% | 14.0% | 18.2% | 23.3% |
| Tranche | 0-3% | 0-6% | 0-9% | 0-12% | 0-22% |
|---|---|---|---|---|---|
| Base Correlation | 17.7% | 28.4% | 36.5% | 43.2% | 60.5% |

📌 **中文解释**：这一页是“整理 CDS、CDO、合成 CDO、相关性微笑和信用指数产品。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 35. Non Standard Tranches

**原文要点**
- Better to interpolate expected losses rather than to interpolate base correlations
- For no arbitrage expected losses on the 0 to X% tranche must increase at a decreasing rate as a function of X

📌 **中文解释**：这一页是“整理 CDS、CDO、合成 CDO、相关性微笑和信用指数产品。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 36. Slide 36

**原文要点**
- Expected Losses on 0 to X% tranche as a percent of Total Underlying Principal for iTraxx on Jan 31, 2007 (Figure 25.3)

**原始表格 / 图示**
![[Ch25HullOFOD11thEdition/Ch25HullOFOD11thEdition_slide36_1.jpg]]

📌 **中文解释**：这一页是“整理 CDS、CDO、合成 CDO、相关性微笑和信用指数产品。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 37. More Advanced Models（债务估值调整）

**原文要点**
- Relax assumptions that all companies have the same default probabilities
- Use a different copula
- Let copula correlation be a function of F
- Imply copula from market data
- Use a dynamic model

📌 **中文解释**：信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
