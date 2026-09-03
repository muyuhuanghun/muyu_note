# Ch04 利率基础

**相关笔记**: [[Ch03HullOFOD11thEdition|上一章：期货套期保值策略]] | [[Ch05HullOFOD11thEdition|下一章：远期和期货价格的确定]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 4 Interest Rates
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：梳理零息利率、远期利率、复利方式、久期和凸性等定价基础。

💡 **核心理解**：利率是衍生品定价里的折现工具，也是很多产品的标的变量。

本章可以按下面的顺序阅读：
1. Types of Rates
2. Treasury Rate
3. Overnight Rates
4. Repo Rate
5. LIBOR（LIBOR）
6. LIBOR Phase Out（LIBOR）
7. The New Reference Rates
8. The New Reference Rates
9. The Risk-Free Rate
10. Impact of Compounding (Table 4.1)
11. Measuring Interest Rates（利率）
12. Continuous Compounding (equation 4.2)
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **利率**：衍生品定价中的折现基础，也是重要的可交易风险因子。
- **零息利率**：从今天到某个期限、一次性折现对应的利率。
- **远期利率**：今天隐含的未来某段期间利率。
- **久期**：债券价格对利率变化的一阶敏感度。
- **凸性**：债券价格对利率变化的二阶敏感度。

---

## 三、逐页整理

### 2. Types of Rates

**原文要点**
- Treasury rates
- Overnight rates
- Repo rates
- LIBOR

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。

---

### 3. Treasury Rate

**原文要点**
- Rate on instrument issued by a government in its own currency

📌 **中文解释**：这一页是“梳理零息利率、远期利率、复利方式、久期和凸性等定价基础。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 4. Overnight Rates

**原文要点**
- Unsecured borrowing and lending between banks as they adjust the reserve requirements they are required to keep with the central bank
- Referred to as the Fed Funds Rate in the U.S.
- The effective fed funds rate is the weighted average of the rates on brokered transactions
- Central bank may intervene with its own transactions to raise or lower the overnight rate

📌 **中文解释**：这一页是“梳理零息利率、远期利率、复利方式、久期和凸性等定价基础。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 5. Repo Rate

**原文要点**
- Repurchase agreement is an agreement where a financial institution that owns securities agrees to sell them for X and buy them bank in the future (usually the next day) for a slightly higher price, Y
- The financial institution obtains a loan.
- The rate of interest is calculated from the difference between X and Y and is known as the repo rate

📌 **中文解释**：这一页是“梳理零息利率、远期利率、复利方式、久期和凸性等定价基础。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 6. LIBOR（LIBOR）

**原文要点**
- LIBOR is the rate of interest at which a AA-rated bank estimates it can borrow money on an unsecured basis from another bank at 11am.
- Several currencies and maturities
- There have been some suggestions that banks manipulated LIBOR during certain periods. Why would they do this?

📌 **中文解释**：基差风险来自现货和期货价格不同步，这是套保后仍然留下的主要不确定性。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 7. LIBOR Phase Out（LIBOR）

**原文要点**
- Regulators plan to phase out LIBOR by the end of 2021 and replace it with rates based on transactions observed in the overnight market.
- The new reference rates (e.g. for a 3-month period) will be calculated at the end of the period as the compounded overnight rates for that period

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。

---

### 8. The New Reference Rates

**原文要点**
- US dollar: SOFR (secured overnight funding rate
- GBP: SONIA (sterling overnight index average
- EU: ESTER (euro short-term rate)
- Switzerland: SARON (Swiss average overnight rate)
- Japan: TONAR (Tokyo average overnight rate)

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。

---

### 9. The New Reference Rates

**原文要点**
- SOFR is calculated from repos and is therefore a secured rate
- The others are calculated from unsecured overnight borrowing and lending between banks

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。

---

### 10. The Risk-Free Rate

**原文要点**
- The Treasury rate is considered to be artificially low because
- Banks are not required to keep capital for Treasury instruments
- Treasury instruments are given favorable tax treatment in the US
- The new reference rates are considered to be proxies for the risk-free rate
- Other “risky” reference rates incorporating a credit spread may be developed

📌 **中文解释**：这一页是“梳理零息利率、远期利率、复利方式、久期和凸性等定价基础。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 11. Impact of Compounding (Table 4.1)

**原文要点**
- When we compound m times per year at rate R an amount A grows to A(1+R/m)m in one year

**原始表格 / 图示**
| Compounding frequency | Value of $100 in one year at 10% |
|---|---|
| Annual (m=1) | 110.00 |
| Semiannual (m=2) | 110.25 |
| Quarterly (m=4) | 110.38 |
| Monthly (m=12) | 110.47 |
| Weekly (m=52) | 110.51 |
| Daily (m=365) | 110.52 |

📌 **中文解释**：这一页是“梳理零息利率、远期利率、复利方式、久期和凸性等定价基础。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 12. Measuring Interest Rates（利率）

**原文要点**
- The compounding frequency used for an interest rate is the unit of measurement
- The difference between quarterly and annual compounding is analogous to the difference between miles and kilometers

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。鞅和测度转换用于把定价问题改写成可折现的期望问题。

---

### 13. Continuous Compounding (equation 4.2)

**原文要点**
- In the limit as we compound more and more frequently we obtain continuously compounded interest rates
- $100 grows to $100eRT when invested at a continuously compounded rate R for time T
- $100 received at time T discounts to $100e-RT at time zero when the continuously compounded discount rate is R

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。

---

### 14. Conversion Formulas (Equations 4.4 and 4.4)

**原文要点**
- Define
- Rc : continuously compounded rate
- Rm: same rate with compounding m times per year

📌 **中文解释**：这一页是“梳理零息利率、远期利率、复利方式、久期和凸性等定价基础。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 15. Examples

**原文要点**
- 10% with semiannual compounding is equivalent to 2ln(1.05)=9.758% with continuous compounding
- 8% with continuous compounding is equivalent to 4(e0.08/4 -1)=8.08% with quarterly compounding
- Rates used in option pricing are nearly always expressed with continuous compounding

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 16. Zero Rates（零息利率）

**原文要点**
- A zero rate (or spot rate), for maturity T is the rate of interest earned on an investment that provides a payoff only at time T

📌 **中文解释**：零息利率用于直接折现单笔到期现金流，是构建收益率曲线的基础。

---

### 17. Example (Table 4.2)

**原始表格 / 图示**
| Maturity (years) | Zero rate (cont. comp. |
|---|---|
| 0.5 | 5.0 |
| 1.0 | 5.8 |
| 1.5 | 6.4 |
| 2.0 | 6.8 |

📌 **中文解释**：零息利率用于直接折现单笔到期现金流，是构建收益率曲线的基础。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 18. Bond Pricing

**原文要点**
- To calculate the cash price of a bond we discount each cash flow at the appropriate zero rate
- In our example, the theoretical price of a two-year bond providing a 6% coupon semiannually is

📌 **中文解释**：零息利率用于直接折现单笔到期现金流，是构建收益率曲线的基础。

---

### 19. Bond Yield

**原文要点**
- The bond yield is the discount rate that makes the present value of the cash flows on the bond equal to the market price of the bond
- Suppose that the market price of the bond in our example equals its theoretical price of 98.39
- The bond yield (continuously compounded) is given by solving
- to get y=0.0676 or 6.76%.

📌 **中文解释**：这一页是“梳理零息利率、远期利率、复利方式、久期和凸性等定价基础。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 20. Par Yield

**原文要点**
- The par yield for a certain maturity is the coupon rate that causes the bond price to equal its face value.
- In our example we solve

📌 **中文解释**：这一页是“梳理零息利率、远期利率、复利方式、久期和凸性等定价基础。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 21. Par Yield continued

**原文要点**
- In general if m is the number of coupon payments per year, d is the present value of $1 received at maturity and A is the present value of an annuity of $1 on each coupon date
- (in our example, m = 2, d = 0.87284, and A = 3.70027)

📌 **中文解释**：这一页是“梳理零息利率、远期利率、复利方式、久期和凸性等定价基础。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 22. Data to Determine Zero Curve (Table 4.3)

**原文要点**
- Half the stated coupon is paid each year

**原始表格 / 图示**
| Bond Principal | Time to Maturity (yrs) | Coupon  per year ($)* | Bond price ($) |
|---|---|---|---|
| 100 | 0.25 | 0 | 99.6 |
| 100 | 0.50 | 0 | 99.0 |
| 100 | 1.00 | 0 | 97.8 |
| 100 | 1.50 | 4 | 102.5 |
| 100 | 2.00 | 5 | 105.0 |

📌 **中文解释**：这一页是“梳理零息利率、远期利率、复利方式、久期和凸性等定价基础。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 23. The Bootstrap Method

**原文要点**
- An amount 0.4 can be earned on 99.6 during 3 months.
- Because 100=99.4e0.01603×0.25 the 3-month rate is 1.603% with continuous compounding
- Similarly the 6 month and 1 year rates are 2.010% and 2.225% with continuous compounding

📌 **中文解释**：这一页是“梳理零息利率、远期利率、复利方式、久期和凸性等定价基础。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 24. The Bootstrap Method continued

**原文要点**
- To calculate the 1.5 year rate we solve
- to get R = 0.02284 or 2.284%
- Similarly the two-year rate is 2.416%

📌 **中文解释**：这一页是“梳理零息利率、远期利率、复利方式、久期和凸性等定价基础。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 25. Slide 25

**原文要点**
- Zero Curve Calculated from the Data (Figure 4.1)

**原始表格 / 图示**
![[Ch04HullOFOD11thEdition/Ch04HullOFOD11thEdition_slide25_1.x-wmf]]

📌 **中文解释**：这一页是“梳理零息利率、远期利率、复利方式、久期和凸性等定价基础。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 26. Forward Rates（远期利率）

**原文要点**
- The forward rate is the future zero rate implied by today’s term structure of interest rates

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 27. Formula for Forward Rates（远期利率）

**原文要点**
- Suppose that the zero rates for time periods T1 and T2 are R1 and R2 with both rates continuously compounded.
- The forward rate for the period between times T1 and T2 is
- This formula is only approximately true when rates are not expressed with continuous compounding

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。零息利率用于直接折现单笔到期现金流，是构建收益率曲线的基础。

---

### 28. Application of the Formula (Table 4.5)

**原始表格 / 图示**
| Year  (n) | Zero rate for n-year investment  (% per annum) | Forward rate for nth year (% per annum) |
|---|---|---|
| 1 | 3.0 |  |
| 2 | 4.0 | 5.0 |
| 3 | 4.6 | 5.8 |
| 4 | 5.0 | 6.2 |
| 5 | 5.5 | 6.5 |

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。零息利率用于直接折现单笔到期现金流，是构建收益率曲线的基础。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 29. Instantaneous Forward Rate（远期）

**原文要点**
- The instantaneous forward rate for a maturity T is the forward rate that applies for a very short time period starting at T. It is
- where R is the T-year rate

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。远期利率表示今天市场隐含的未来利率，是远期利率协议和利率模型的核心输入。

---

### 30. Upward vs Downward Sloping Yield Curve

**原文要点**
- For an upward sloping yield curve:
- Fwd Rate > Zero Rate > Par Yield
- For a downward sloping yield curve
- Par Yield > Zero Rate > Fwd Rate

📌 **中文解释**：零息利率用于直接折现单笔到期现金流，是构建收益率曲线的基础。

---

### 31. Forward Rate Agreement（远期）

**原文要点**
- A forward rate agreement (FRA) is an OTC agreement that the actual rate applicable to a certain period will be exchanged for a predetermined rate, RK, with both being applied to a predetermined principal

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。场外交易条款灵活，但必须额外管理交易对手信用、清算和监管报告。

---

### 32. Forward Rate Agreement: Key Results（远期）

**原文要点**
- An FRA can be valued by assuming that the forward interest rate, RF , is certain to be realized
- This means that the value of an FRA is the present value of the difference between the interest that would be paid at interest at rate RF and the interest that would be paid at rate RK

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 33. Example

**原文要点**
- An FRA entered into some time ago states that a company will receive 5.8% (s.a.) and pay SOFR on a principal of $100 million starting in 1.5 years
- Forward SOFR for the period between 1.5 and 2 years is 5% (s.a.)
- The 2 year (SOFR) risk-free rate is 4% with continuous compounding
- The value of the FRA (in $ millions) is
- 100×(0.058-0.050) ×0.5×e-0.04×2=0.3692

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 34. Duration (equation 4.8)（久期）

**原文要点**
- Duration of a bond that provides cash flow ci at time ti is
- where B is its price and y is its yield (continuously compounded)

📌 **中文解释**：久期是一阶利率风险，适合小幅利率变动下的近似对冲。

---

### 35. Key Duration Relationship（久期）

**原文要点**
- Duration is important because it leads to the following key relationship between the change in the yield on the bond and the change in its price

📌 **中文解释**：久期是一阶利率风险，适合小幅利率变动下的近似对冲。

---

### 36. Key Duration Relationship continued（久期）

**原文要点**
- When the yield y is expressed with compounding m times per year
- The expression
- is referred to as the “modified duration”

📌 **中文解释**：久期是一阶利率风险，适合小幅利率变动下的近似对冲。

---

### 37. Bond Portfolios

**原文要点**
- The duration for a bond portfolio is the weighted average duration of the bonds in the portfolio with weights proportional to prices
- The key duration relationship for a bond portfolio describes the effect of small parallel shifts in the yield curve
- What exposures remain if duration of a portfolio of assets equals the duration of a portfolio of liabilities?

📌 **中文解释**：久期是一阶利率风险，适合小幅利率变动下的近似对冲。

---

### 38. Convexity (equation 4.14)（凸性）

**原文要点**
- The convexity, C, of a bond is defined as
- This leads to a more accurate relationship
- When used for bond portfolios it allows larger shifts in the yield curve to be considered, but the shifts still have to be parallel

📌 **中文解释**：凸性描述非线性利率风险，利率变化较大时只看久期会低估误差。

---

### 39. Theories of the Term Structure

**原文要点**
- Expectations Theory: forward rates equal expected future zero rates
- Market Segmentation: short, medium and long rates determined independently of each other
- Liquidity Preference Theory: forward rates higher than expected future zero rates

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。零息利率用于直接折现单笔到期现金流，是构建收益率曲线的基础。

---

### 40. Liquidity Preference Theory (Table 4.7)

**原文要点**
- Suppose that the outlook for rates is flat and you have been offered the following choices
- Which would you choose as a depositor? Which for your mortgage?

**原始表格 / 图示**
| Maturity | Deposit rate | Mortgage rate |
|---|---|---|
| 1 year | 3% | 6% |
| 5 year | 3% | 6% |

📌 **中文解释**：这一页是“梳理零息利率、远期利率、复利方式、久期和凸性等定价基础。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 41. Liquidity Preference Theory cont (Table 4.8)

**原文要点**
- To match the maturities of borrowers and lenders a bank has to increase long rates above expected future short rates
- In our example the bank might offer

**原始表格 / 图示**
| Maturity | Deposit rate | Mortgage rate |
|---|---|---|
| 1 year | 3% | 6% |
| 5 year | 4% | 7% |

📌 **中文解释**：短利率模型把瞬时利率作为状态变量，再由它推出债券和利率衍生品价格。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
