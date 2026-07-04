# Ch07 互换

**相关笔记**: [[Ch06HullOFOD11thEdition|上一章：利率期货]] | [[Ch08HullOFOD11thEdition|下一章：证券化与金融危机]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 7 Swaps
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：掌握利率互换、货币互换的现金流结构、定价和比较优势解释。

💡 **核心理解**：互换可以看成一组远期合约的组合，本质是交换未来现金流。

本章可以按下面的顺序阅读：
1. Nature of Swaps（互换）
2. An Example of a “Plain Vanilla” Overnight Indexed Swap（互换）
3. Cash Flows to Apple for One Outcome(See Table 7.1)
4. Determination of Risk-Free Interest Rates（利率）
5. Bootstrap Example (Table 7.3)
6. Slide 7
7. Typical Uses of an Interest Rate Swap（互换）
8. OIS Between Apple and Citigroup (Figure 7.1)（隔夜指数互换）
9. Apple Transforms a Liability from Floating to Fixed(Figure 7.3)
10. Interest Rate Swap Between Citigroup and Intel（互换）
11. Intel Transforms a Liability from Fixed to Floating (Figure 7.4)
12. Apple Transforms an Asset from Fixed to Floating (Figure 7.5)
13. ……其余内容见下方逐页整理。

---

## 二、核心概念速记

- **互换**：双方按约定规则交换未来现金流，可看成一组远期合约。
- **隔夜指数互换**：以隔夜利率复利为浮动端的利率互换。
- **SOFR**：美元担保隔夜融资利率，LIBOR 退出后的核心基准之一。
- **零息利率**：从今天到某个期限、一次性折现对应的利率。
- **远期利率**：今天隐含的未来某段期间利率。

---

## 三、逐页整理

### 2. Nature of Swaps（互换）

**原文要点**
- A swap is an agreement to exchange cash flows at specified future times according to certain specified rules

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 3. An Example of a “Plain Vanilla” Overnight Indexed Swap（互换）

**原文要点**
- Deal entered into on March 8, 2022 where Apple agrees to receive 3-month SOFR & pay a fixed rate of 3% per annum every 3 months for 2 years on a notional principal of $100 million
- Next slide illustrates cash flows that could occur (Day count conventions are not considered)

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 4. Cash Flows to Apple for One Outcome(See Table 7.1)

**原始表格 / 图示**
| Date | SOFR Rate (%) | Floating Received (‘000s) | Fixed Paid (‘000s) | Net cash flow (‘000s) |
|---|---|---|---|---|
| June 8, 2022 | 2.20 | 550 | 750 | -200 |
| Sept 8, 2022 | 2.60 | 650 | 750 | -100 |
| Dec. 8, 2022 | 2.80 | 700 | 750 | -50 |
| Mar. 8, 2023 | 3.10 | 775 | 750 | +25 |
| June 8, 2023 | 3.30 | 825 | 750 | +75 |
| Sept 8, 2023 | 3.40 | 850 | 750 | +100 |
| Dec 8, 2023 | 3.60 | 900 | 750 | +150 |
| Mar 8, 2024 | 3.80 | 950 | 750 | +200 |

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 5. Determination of Risk-Free Interest Rates（利率）

**原文要点**
- OIS rates out to one year define zero rates because they typically involve a single exchange
- OIS rate for contracts lasting longer than one year define par yield
- The bootstrap method can be used to determine the zero curve

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。零息利率用于直接折现单笔到期现金流，是构建收益率曲线的基础。

---

### 6. Bootstrap Example (Table 7.3)

**原始表格 / 图示**
| OIS Maturity | OIS Rate | Compound. Freq. for OIS rate | Zero rate  (cont comp.) |
|---|---|---|---|
| 1 month | 1.8% | Monthly | 1.7987% |
| 3 months | 2.0% | Quarterly | 1.9950% |
| 6 months | 2.2% | Semiannually | 2.1880% |
| 12 month | 2.5% | Annually | 2.4693% |
| 2 years | 3.0% | Quarterly | 2.9994% |
| 5 years | 4.0% | Quarterly | 4.0401% |

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。零息利率用于直接折现单笔到期现金流，是构建收益率曲线的基础。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 7. Slide 7

**原文要点**
- Zero Rate Given by Bootstrap Method (Figure 7.2)

**原始表格 / 图示**
![[Ch07HullOFOD11thEdition/Ch07HullOFOD11thEdition_slide7_1.x-wmf]]

📌 **中文解释**：零息利率用于直接折现单笔到期现金流，是构建收益率曲线的基础。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 8. Typical Uses of an Interest Rate Swap（互换）

**原文要点**
- Converting a liability from
- fixed rate to floating rate
- floating rate to fixed rate
- Converting an investment from
- fixed rate to floating rate
- floating rate to fixed rate

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 9. OIS Between Apple and Citigroup (Figure 7.1)（隔夜指数互换）

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。

---

### 10. Apple Transforms a Liability from Floating to Fixed(Figure 7.3)

📌 **中文解释**：这一页是“掌握利率互换、货币互换的现金流结构、定价和比较优势解释。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 11. Interest Rate Swap Between Citigroup and Intel（互换）

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 12. Intel Transforms a Liability from Fixed to Floating (Figure 7.4)

📌 **中文解释**：这一页是“掌握利率互换、货币互换的现金流结构、定价和比较优势解释。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 13. Apple Transforms an Asset from Fixed to Floating (Figure 7.5)

📌 **中文解释**：这一页是“掌握利率互换、货币互换的现金流结构、定价和比较优势解释。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 14. Intel Transforms an Asset from Floating to Fixed (Figure 7.6)

📌 **中文解释**：这一页是“掌握利率互换、货币互换的现金流结构、定价和比较优势解释。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 15. Quotes By a Swap Market Maker (Table 7.4)（互换）

**原始表格 / 图示**
| Maturity | Bid (%) | Ask (%) | Swap Rate (%) |
|---|---|---|---|
| 2 years | 2.97 | 3.00 | 2.985 |
| 3 years | 3.05 | 3.08 | 3.065 |
| 4 years | 3.15 | 3.19 | 3.170 |
| 5 years | 3.26 | 3.30 | 3.280 |
| 7 years | 3.40 | 3.44 | 3.420 |
| 10 years | 3.48 | 3.52 | 3.500 |

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 16. Day Count

**原文要点**
- A day count convention is specified for fixed and floating payments
- For example, SOFR is likely to be actual/360 in the U.S.
- The fixed rate might be quoted with actual/365 or 30/360

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。

---

### 17. Confirmations

**原文要点**
- Confirmations specify the terms of a transaction
- The International Swaps and Derivatives has developed Master Agreements that can be used to cover all agreements between two counterparties
- CCPs are used for standard swaps between two financial institutions

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 18. The Comparative Advantage Argument (Table 7.5)（债务估值调整）

**原文要点**
- AAACorp wants to borrow floating
- BBBCorp wants to borrow fixed

📌 **中文解释**：这一页是“掌握利率互换、货币互换的现金流结构、定价和比较优势解释。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 19. A Swap where Companies Trade Directly with Each Other (Figure 7.7)（互换）

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 20. The Swap when a Financial Institution (F.I.) is Involved (Figure 7.8)（互换）

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 21. Criticism of the Comparative Advantage Argument（债务估值调整）

**原文要点**
- The 4.0% and 5.2% rates available to AAACorp and BBBCorp in fixed rate markets are 5-year rates
- The rates available in the floating rate market are 3-month rates
- BBBCorp’s fixed rate depends on the spread above floating it borrows at in the future

📌 **中文解释**：这一页是“掌握利率互换、货币互换的现金流结构、定价和比较优势解释。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 22. Valuation of an Interest Rate Swap（互换）

**原文要点**
- Initially interest rate swaps are worth close to zero
- At later times they can be valued as a portfolio of forward rate agreements (FRAs)
- The procedure is to
- Calculate floating forward rates
- Calculate the swap cash flows that will occur if floating forward rates are realized
- Discount these swap cash flows at OIS rates

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 23. Example (Example 7.1)

**原文要点**
- Swap involves paying 3% per annum and receiving SOFR every six months on $100 million
- Swap has 1.2 years remaining (exchanges in 0.2, 0.7, and 1.2 years)
- Risk-free rate for 0.2, 0.7, and 1.2 years are 2.8%, 3.2% and 3.4%, respectively (continuously compounded)
- Rate observed for last 0.3 years is 2.3% continuously compounded

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 24. Example continued

**原文要点**
- Floating rate for the exchange at 0.2 years is assumed to be 0.6×2.3%+0.4×2.8% or 2.50% (cont comp) or 2.516% (sa)
- Forward rate for 0.2 to 0.7 years is 3.36% (cont comp) or 3.388% (sa)
- Forward rate for 0.7 to 1.2 years is 3.68% (cont comp) or 3.714% (sa)

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。远期利率表示今天市场隐含的未来利率，是远期利率协议和利率模型的核心输入。

---

### 25. Calculations ($ million)

**原文要点**
- Value of swap is $0.292 million

**原始表格 / 图示**
| Time  (yrs) | Fixed cash flow | Floating cash flow | Net cash flow | Discount factor | PV of net cash flow |
|---|---|---|---|---|---|
| 0.2 | −1.5000 | +1.258 | −0.242 | 0.9944 | −0.241 |
| 0.7 | −1.5000 | +1.694 | +0.194 | 0.9778 | +0.190 |
| 1.2 | −1.5000 | +1.857 | +0.357 | 0.9600 | +0.343 |
|  |  |  |  |  | +0.292 |

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 26. Value Changes Through Time

**原文要点**
- To party paying fixed
- How is swap value expected to change through time when term structure is upward sloping?
- How is swap value expected to change through time when term structure is downward sloping?

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 27. An Example of a Fixed-for-Fixed Currency Swap (Figure 7.10)（互换）

**原文要点**
- Five year agreement by BP to
- Pay 3% on a US dollar principal of $15,000,000
- Receive 4% on a sterling principal of £10,000,000

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 28. Exchange of Principal

**原文要点**
- In an interest rate swap the principal is not exchanged
- In a currency swap the principal is exchanged at the beginning and the end of the swap

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 29. The Cash Flows (Table 7.6)

**原始表格 / 图示**
| Date | Dollar Cash Flows (millions) | Sterling cash flow (millions) |
|---|---|---|
| Feb 1, 2022 | +15.00 | −10.00 |
| Feb 1, 2023 | −0.45 | +0.40 |
| Feb 1, 2024 | −0.45 | +0.40 |
| Feb 1, 2025 | −0.45 | +0.40 |
| Feb 1, 2026 | −0.45 | +0.40 |
| Feb 1, 2027 | −15.45 | +10.40 |

📌 **中文解释**：这一页是“掌握利率互换、货币互换的现金流结构、定价和比较优势解释。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 30. Typical Uses of a Currency Swap（互换）

**原文要点**
- Conversion from a liability in one currency to a liability in another currency
- Conversion from an investment in one currency to an investment in another currency

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 31. Comparative Advantage May Be Real Because of Taxes（债务估值调整）

**原文要点**
- General Electric wants to borrow AUD
- Quantas wants to borrow USD
- Borrowing costs after adjusting for the differential impact of taxes could be:

**原始表格 / 图示**
|  | USD | AUD |
|---|---|---|
| General Electric | 5.0% | 7.6% |
| Quantas | 7.0% | 8.0% |

📌 **中文解释**：这一页是“掌握利率互换、货币互换的现金流结构、定价和比较优势解释。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 32. Valuation of Fixed-for-Fixed Currency Swaps（互换）

**原文要点**
- Fixed for fixed currency swaps can be valued either using forward rates or as the difference between 2 bonds

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 33. Currency Swap Example（互换）

**原文要点**
- All Japanese interest rates are 1.5% per annum (cont. comp.)
- All USD interest rates are 2.5% per annum (cont. comp.)
- 3% is received in yen; 4% is paid in dollars. Payments are made annually
- Principals are $10 million and 1,200 million yen
- Swap will last for 3 more years
- Current exchange rate is 110 yen per dollar

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 34. Valuation in Terms of Forward Rates (Example 7.2)（远期利率）

**原始表格 / 图示**
| Time | DollarCash Flow | Yen cash flow | Forward rate | Dollar value of yen cash flow | Net cash flow | Present value |
|---|---|---|---|---|---|---|
| 1 | −0.4 | +36 | 0.009182 | 0.3306 | −0.0694 | −0.0677 |
| 2 | −0.4 | +36 | 0.009275 | 0.3339 | −0.0661 | −0.0629 |
| 3 | −10.4 | +1236 | 0.009368 | 11.5786 | +1.1786 | +1.0934 |
| Total |  |  |  |  |  | +0.9629 |

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。远期利率表示今天市场隐含的未来利率，是远期利率协议和利率模型的核心输入。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 35. Valuation in Terms of Bonds (Example 7.3)

**原文要点**
- Value = 1,252.01/110−10.4191 = +0.9629 millions of dollars

**原始表格 / 图示**
| Time | Cash Flows ($ millions) | PV  ($ millions) | Cash flows (millions of yen) | PV ( millions of yen) |
|---|---|---|---|---|
| 1 | 0.4 | 0.3901 | 36 | 35.46 |
| 2 | 0.4 | 0.3805 | 36 | 34.94 |
| 3 | 10.4 | 9.6485 | 1,236 | 1,181.61 |
| Total |  | 10.4191 |  | 1,252.01 |

📌 **中文解释**：这一页是“掌握利率互换、货币互换的现金流结构、定价和比较优势解释。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 36. Other Currency Swaps（互换）

**原文要点**
- Fixed-for-floating: equivalent to a fixed-for-fixed currency swap plus a fixed for floating interest rate swap
- Floating-for-floating: equivalent to a fixed-for-fixed currency swap plus two floating interest rate swaps

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 37. Swaps & Forwards（互换）

**原文要点**
- A swap can be regarded as a convenient way of packaging forward contracts
- When a swap is initiated the swap has zero value, but typically some forwards have a positive value and some have a negative value

📌 **中文解释**：远期合约更灵活但信用风险更集中，定价通常用无套利复制来推导。互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。

---

### 38. Credit Risk（信用风险）

**原文要点**
- When derivatives transactions with a counterparty are cleared bilaterally, they are netted
- There is exposure if the net value of outstanding transactions is greater than the collateral posted

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 39. Credit Default Swaps: A Quick First Look（互换）

**原文要点**
- Notional principal (e.g. $100 million) and maturity (e.g. 5 yrs) specified
- Protection buyer pays a fixed rate (e.g. 150 bp) on the notional principal (the CDS spread)
- If the reference entity (a country or company) defaults protection seller buys bonds issued by the reference entity for their face value and the spread payments stop. Total face value of bonds bought equals notional principal

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 40. Other Types of Swaps（互换）

**原文要点**
- Amortizing/ step up
- Compounding swap
- Quanto (diff swap)
- Equity swap
- Extendible or puttable swap
- Commodity swap
- Volatility swap

📌 **中文解释**：互换可以拆成一系列未来现金流交换，估值时分别折现固定端和浮动端。波动率既是历史统计量，也是市场通过期权价格反推的隐含预期。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
