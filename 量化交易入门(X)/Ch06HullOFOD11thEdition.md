# Ch06 利率期货

**相关笔记**: [[Ch05HullOFOD11thEdition|上一章：远期和期货价格的确定]] | [[Ch07HullOFOD11thEdition|下一章：互换]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 6 Interest Rate Futures
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：理解国债期货、SOFR/Eurodollar 类利率期货、久期套保和凸性调整。

💡 **核心理解**：利率期货的难点在报价、交割和久期匹配，不只是简单的期货价格变化。

本章可以按下面的顺序阅读：
1. Day Count Convention
2. Day Count Conventions in the U.S.
3. Examples
4. Examples continued
5. The February Effect (Business Snapshot 6.1)
6. Treasury Bill Prices in the US
7. Treasury Bond Price Quotesin the U.S
8. Treasury Bond Futures（期货）
9. Example
10. Conversion Factor
11. CBOT T-Bonds & T-Notes
12. Eurodollar Futures（期货）
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **利率**：衍生品定价中的折现基础，也是重要的可交易风险因子。
- **期货**：交易所标准化合约，每日盯市结算，由保证金制度控制违约风险。
- **SOFR**：美元担保隔夜融资利率，LIBOR 退出后的核心基准之一。
- **久期**：债券价格对利率变化的一阶敏感度。
- **凸性**：债券价格对利率变化的二阶敏感度。

---

## 三、逐页整理

### 2. Day Count Convention

**原文要点**
- Defines:
- the period of time to which the interest rate applies
- The period of time used to calculate accrued interest (relevant when the instrument is bought of sold

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。

---

### 3. Day Count Conventions in the U.S.

**原始表格 / 图示**
| Treasury Bonds: | Actual/Actual (in period) |
|---|---|
| Corporate Bonds: | 30/360 |
| Money Market  Instruments: | Actual/360 |

📌 **中文解释**：这一页是“理解国债期货、SOFR/Eurodollar 类利率期货、久期套保和凸性调整。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 4. Examples

**原文要点**
- Bond: 8% Actual/ Actual in period.
- 4% is earned between coupon payment dates. Accruals on an Actual basis. When coupons are paid on March 1 and Sept 1, how much interest is earned between March 1 and April 1?
- Bond: 8% 30/360
- Assumes 30 days per month and 360 days per year. When coupons are paid on March 1 and Sept 1, how much interest is earned between March 1 and April 1?

📌 **中文解释**：基差风险来自现货和期货价格不同步，这是套保后仍然留下的主要不确定性。

---

### 5. Examples continued

**原文要点**
- T-Bill: 8% Actual/360:
- 8% is earned in 360 days. Accrual calculated by dividing the actual number of days in the period by 360. How much interest is earned between March 1 and April 1?

📌 **中文解释**：这一页是“理解国债期货、SOFR/Eurodollar 类利率期货、久期套保和凸性调整。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 6. The February Effect (Business Snapshot 6.1)

**原文要点**
- How many days of interest are earned between February 28, 2021 and March 1, 2021 when
- day count is Actual/Actual in period?
- day count is 30/360?

📌 **中文解释**：这一页是“理解国债期货、SOFR/Eurodollar 类利率期货、久期套保和凸性调整。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 7. Treasury Bill Prices in the US

📌 **中文解释**：这一页是“理解国债期货、SOFR/Eurodollar 类利率期货、久期套保和凸性调整。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 8. Treasury Bond Price Quotesin the U.S

**原文要点**
- Cash price = Quoted price + Accrued Interest

📌 **中文解释**：这一页是“理解国债期货、SOFR/Eurodollar 类利率期货、久期套保和凸性调整。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 9. Treasury Bond Futures（期货）

**原文要点**
- Cash price received by party with short position =
- Most recent settlement price × Conversion factor + Accrued interest

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。

---

### 10. Example

**原文要点**
- Most recent settlement price = 90.00
- Conversion factor of bond delivered = 1.3800
- Accrued interest on bond =3.00
- Price received for bond is 1.3800×90.00+3.00 = $127.20 per $100 of principal

📌 **中文解释**：这一页是“理解国债期货、SOFR/Eurodollar 类利率期货、久期套保和凸性调整。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 11. Conversion Factor

**原文要点**
- The conversion factor for a bond is approximately equal to the value of the bond on the assumption that the yield curve is flat at 6% with semiannual compounding

📌 **中文解释**：这一页是“理解国债期货、SOFR/Eurodollar 类利率期货、久期套保和凸性调整。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 12. CBOT T-Bonds & T-Notes

**原文要点**
- Factors that affect the futures price:
- Delivery can be made any time during the delivery month
- Any of a range of eligible bonds can be delivered
- The wild card play

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。

---

### 13. Eurodollar Futures（期货）

**原文要点**
- Eurodollar futures are futures on the 3-month LIBOR rate
- One contract is on the rate earned on $1 million
- A change of one basis point or 0.01 in a Eurodollar futures quote corresponds to a contract price change of $25

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。基差风险来自现货和期货价格不同步，这是套保后仍然留下的主要不确定性。

---

### 14. Eurodollar Futures continued（期货）

**原文要点**
- A Eurodollar futures contract is settled in cash
- When it expires the final settlement price is 100 minus 3-month LIBOR
- The LIBOR rate is observed two days before the third Wednesday of the month

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 15. Eurodollar Futures Example (Table 6.2)（期货）

**原始表格 / 图示**
| Date | Trade Price | Settlement futures price | Change | Gain per contract |
|---|---|---|---|---|
| May 21 | 99.720 |  |  |  |
| May 21 |  | 99.715 | -0.005 | -12.50 |
| May 22 |  | 99.665 | -0.050 | -125 |
| ……. | …… | …… | …… | …… |
| Sept 14 |  | 99.810 | +0.010 | +25 |
| Total |  |  | +0.090 | +225 |

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 16. Hedging（套期保值）

**原文要点**
- The contract can be used for hedging in a situation where a 3-month interest rate on $1 million, linked to LIBOR, is due to be received for a 3-month period starting on Sept 14
- What rate does the contract lock in?

📌 **中文解释**：套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 17. SOFR Futures（期货）

**原文要点**
- The one-month SOFR futures is designed to be as similar as possible to the one-month Fed Fund futures contract and is based on an arithmetic average of overnight rates
- The three-month SOFR futures is designed to be as similar as possible to the three-month Eurodollar futures and is based on the result of compounding overnight rates

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 18. 3-Month Eurodollar Futures vs. 3-month SOFR Futures（期货）

**原文要点**
- The 3-month Eurodollar futures for a contract month is settled on the third Wednesday of the month and equal to the 3-month LIBOR rate observed two days earlier
- The 3-month SOFR futures for the same contract month is settled 3-months later (when all the relevant overnight rates have been observed)

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 19. Using SOFR for Hedging (Example 6.3)（套期保值）

**原文要点**
- A company has agreed to pay three month SOFR plus 200 basis points on $100 million for three months starting on December 16, 2021
- The December SOFR futures price is 99.990
- What rate can the company lock in?

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

### 20. Forward Rates（远期利率）

**原文要点**
- We can usually assume that forward prices equal futures prices
- For interest rate futures that last more than about two years we cannot do this

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 21. There are Two Reasons

**原文要点**
- Futures is settled daily whereas FRA is settled once (true for both Eurodollar and SOFR)
- Futures is settled at the beginning of the underlying three-month period; FRA is settled at the end of the underlying three- month period (true for Eurodollar)

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 22. Convexity adjustment（凸性）

**原文要点**
- Forward Rate = Futures Rate − c
- where c is referred to as a convexity adjustment

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。

---

### 23. Extending Zero Curves

**原文要点**
- Forward rates can be used to bootstrap the zero curve

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。远期利率表示今天市场隐含的未来利率，是远期利率协议和利率模型的核心输入。

---

### 24. Example (equation 6.2)

**原文要点**
- so that
- If the 400-day zero rate has been calculated as 4.80% and the forward rate for the period between 400 and 491 days is 5.30 the 491 day rate is 4.893%

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。零息利率用于直接折现单笔到期现金流，是构建收益率曲线的基础。

---

### 25. Duration Matching（久期）

**原文要点**
- This involves hedging against interest rate risk by matching the durations of assets and liabilities
- It provides protection against small parallel shifts in the zero curve

📌 **中文解释**：套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 26. Duration-Based Hedge Ratio (equation 6.3)（套期保值）

**原始表格 / 图示**
| VF | Contract price for interest rate futures |
|---|---|
| DF | Duration of asset underlying futures at maturity |
| P | Value of portfolio being hedged |
| DP | Duration of portfolio at hedge maturity |

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 27. Example

**原文要点**
- It is August. A fund manager has $10 million invested in a portfolio of government bonds with a duration of 6.80 years and wants to hedge against interest rate moves between August and December
- The manager decides to use December T-bond futures. The futures price is 93-02 or 93.0625 and the duration of the cheapest to deliver bond will be 9.2 years at the futures contract maturity
- The number of contracts that should be shorted is

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

### 28. Limitations of Duration-Based Hedging（套期保值）

**原文要点**
- Assumes that only parallel shift in yield curve take place
- Assumes that yield curve changes are small
- When T-Bond futures is used assumes there will be no change in the cheapest-to-deliver bond

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。

---

### 29. GAP Management (Business Snapshot 6.3)

**原文要点**
- This is a more sophisticated approach used by banks to hedge interest rate. It involves
- Bucketing the zero curve
- Hedging exposure to situation where rates corresponding to one bucket change and all other rates stay the same

📌 **中文解释**：套保不是预测市场，而是用一个头寸抵消另一个头寸的风险暴露。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 30. Liquidity Risk

**原文要点**
- If a bank funds long term assets with short term liabilities such as commercial paper, it can use FRAs, futures, and swaps to hedge its interest rate exposure
- But it still has a liquidity exposure.
- It may find it impossible to roll over the commercial paper if the market loses confidence in the bank
- Northern Rock is an example of this type of liquidity problem

📌 **中文解释**：期货重点关注标准化合约、保证金和每日结算；价格变化会每天转化为现金流。互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
