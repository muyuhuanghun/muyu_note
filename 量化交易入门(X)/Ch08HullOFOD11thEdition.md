# Ch08 证券化与金融危机

**相关笔记**: [[Ch07HullOFOD11thEdition|上一章：互换]] | [[Ch09HullOFOD11thEdition|下一章：XVA 调整]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 8 Securitization and the Financial Crisis of 2007-8
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：理解 ABS、CDO、分层结构、违约相关性和 2007-2008 金融危机的传导链条。

💡 **核心理解**：证券化能分散单笔贷款风险，但在相关性上升时会把系统性风险集中到复杂产品里。

本章可以按下面的顺序阅读：
1. Securitization（证券化）
2. Asset Backed Security (Figure 8.1)
3. The Waterfall (Figure 8.2)
4. ABS CDOs (Figure 8.3)（资产支持证券）
5. Losses to AAA Senior Tranche of ABS CDO (Table 8.1)（资产支持证券）
6. Slide 7
7. What happened…
8. What happened...
9. What Many Market Participants Did Not Realize…
10. Regulatory Arbitrage
11. Incentives
12. The Aftermath…

---

## 二、核心概念速记

- **证券化**：把贷款等资产现金流打包并发行证券。
- **资产支持证券**：由贷款、应收账款等资产池支持的证券。
- **债务抵押债券**：把信用资产分层后发行的结构化产品。
- **信用风险**：债务人或交易对手不履约导致损失的风险。

---

## 三、逐页整理

### 2. Securitization（证券化）

**原文要点**
- Traditionally banks have funded loans with deposits
- Securitization is a way that loans can increase much faster than deposits

📌 **中文解释**：证券化把资产池现金流重新分层出售，关键风险在资产相关性和分层吸收损失的顺序。

---

### 3. Asset Backed Security (Figure 8.1)

📌 **中文解释**：这一页是“理解 ABS、CDO、分层结构、违约相关性和 2007-2008 金融危机的传导链条。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 4. The Waterfall (Figure 8.2)

**原文要点**
- Equity Tranche

📌 **中文解释**：这一页是“理解 ABS、CDO、分层结构、违约相关性和 2007-2008 金融危机的传导链条。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 5. ABS CDOs (Figure 8.3)（资产支持证券）

**原文要点**
- ABSs
- ABS CDOs

📌 **中文解释**：证券化把资产池现金流重新分层出售，关键风险在资产相关性和分层吸收损失的顺序。

---

### 6. Losses to AAA Senior Tranche of ABS CDO (Table 8.1)（资产支持证券）

**原始表格 / 图示**
| Losses on Subprime portfolios | Losses on Mezzanine Tranche of ABS | Losses on Equity Tranche of ABS CDO | Losses on Mezzanine Tranche of ABS CDO | Losses on Senior Tranche of ABS CDO |
|---|---|---|---|---|
| 10% | 33.3% | 100% | 93.3% | 0% |
| 13% | 53.3% | 100% | 100% | 28.2% |
| 17% | 80.0% | 100% | 100% | 69.2% |
| 20% | 100% | 100% | 100% | 100% |

📌 **中文解释**：证券化把资产池现金流重新分层出售，关键风险在资产相关性和分层吸收损失的顺序。表格里的数值通常是例题或市场报价，复习时要能说明每一列的金融含义。

---

### 7. Slide 7

**原文要点**
- U.S. Real Estate Prices, 1987 to 2019: S&P/Case-Shiller Composite-10 Index

**原始表格 / 图示**
![[Ch08HullOFOD11thEdition/Ch08HullOFOD11thEdition_slide7_1.x-wmf]]

📌 **中文解释**：这一页是“理解 ABS、CDO、分层结构、违约相关性和 2007-2008 金融危机的传导链条。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。图示用于帮助理解现金流、树结构或曲线形状，建议和本页公式/要点一起看。

---

### 8. What happened…

**原文要点**
- Starting in 2000, mortgage originators in the US relaxed their lending standards and created large numbers of subprime first mortgages.
- This, combined with very low interest rates, increased the demand for real estate and prices rose.
- To continue to attract first time buyers and keep prices increasing they relaxed lending standards further
- Features of the market: 100% mortgages, ARMs, teaser rates, NINJAs, liar loans, non-recourse borrowing
- Mortgages were packaged in financial products and sold to investors

📌 **中文解释**：利率章节要同时看现金流折现和利率本身的随机变化。

---

### 9. What happened...

**原文要点**
- Banks found it profitable to invest in the AAA rated tranches because the promised return was significantly higher than the cost of funds and capital requirements were low
- In 2007 the bubble burst. Some borrowers could not afford their payments when the teaser rates ended. Others had negative equity and recognized that it was optimal for them to exercise their put options.
- Foreclosures increased supply and caused U.S. real estate prices to fall. Products, created from the mortgages, that were previously thought to be safe began to be viewed as risky
- There was a “flight to quality” and credit spreads increased to very high levels
- Many banks incurred huge losses

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 10. What Many Market Participants Did Not Realize…

**原文要点**
- Default correlation goes up in stressed market conditions
- Recovery rates are less in stressed market conditions
- A tranche with a certain rating cannot be equated with a bond with the same rating. For example, the BBB tranches used to create ABS CDOs were typically about 1% wide and had “all or nothing” loss distributions (quite different from BBB bond)
- This is quite different from the loss distribution for a BBB bond from a BBB bond

📌 **中文解释**：证券化把资产池现金流重新分层出售，关键风险在资产相关性和分层吸收损失的顺序。信用风险的三件事是违约概率、违约损失和违约时风险暴露。

---

### 11. Regulatory Arbitrage

**原文要点**
- The regulatory capital banks were required to keep for the tranches created from mortgages was less than that for the mortgages themselves

📌 **中文解释**：这一页是“理解 ABS、CDO、分层结构、违约相关性和 2007-2008 金融危机的传导链条。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 12. Incentives

**原文要点**
- The crisis highlighted what are referred to as agency costs
- Mortgage originators (Their prime interest was in in originating mortgages that could be securitized)
- Valuers (They were under pressure to provide high valuations so that the loan-to-value ratios looked good)
- Traders (They were focused on the next end-of year bonus and not worried about any longer term problems in the market)

📌 **中文解释**：这一页是“理解 ABS、CDO、分层结构、违约相关性和 2007-2008 金融危机的传导链条。”下的一个子主题，先把概念、现金流和风险方向对应起来，再看公式。

---

### 13. The Aftermath…

**原文要点**
- A huge amount of new regulation (Basel II.5, Basel III, Dodd-Frank, etc). For example:
- Banks required to hold more equity capital with the definition of equity capital being tightened
- Banks required to satisfy liquidity ratios
- CCPs and SEFs for OTC derivatives
- Bonuses limited in Europe
- Bonuses spread over several years
- Proprietary trading restricted

📌 **中文解释**：衍生品的价值来自标的资产，所以分析时要先问：标的是什么、现金流怎样发生、风险被转移给谁。场外交易条款灵活，但必须额外管理交易对手信用、清算和监管报告。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
