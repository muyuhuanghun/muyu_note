# Ch16 员工股票期权

**相关笔记**: [[Ch15HullOFOD11thEdition|上一章：Black-Scholes-Merton 模型]] | [[Ch17HullOFOD11thEdition|下一章：股指和外汇期权]] | [[可能有用|量化交易入门总览]]

---

## 🏷️ 文档元数据
* **教材来源**: Options, Futures, and Other Derivatives, 11th Edition, John C. Hull
* **英文章节**: Chapter 16 Employee Stock Options
* **整理状态**: 已按仓库笔记风格重排，保留原始 slide 要点并补充中文解释
* **重要性**: ⭐⭐⭐⭐（量化交易/衍生品基础）

---

## 一、本章导读

📌 **学习目标**：理解员工期权的归属期、提前行权、稀释、会计处理和估值近似。

💡 **核心理解**：员工期权不是标准交易所期权，不能直接套用普通美式/欧式期权直觉。

本章可以按下面的顺序阅读：
1. Nature of Employee Stock Options（期权）
2. Typical Features of Employee Stock Options（期权）
3. Exercise Decision
4. Drawbacks of Employee Stock Options（期权）
5. Accounting for Employee Stock Options（期权）
6. Traditional At-the-Money Call Options（期权）
7. Nontraditional Plans
8. Valuation of Employee Stock Options（期权）
9. Example (Example 16.1)
10. Other Approaches
11. Dilution
12. Backdating

---

## 二、核心概念速记

- **期权**：买方支付权利金，获得未来按执行价买入或卖出标的的权利。
- **看涨期权**：赋予买入标的资产的权利。

---

## 三、逐页整理

### 2. Nature of Employee Stock Options（期权）

**原文要点**
- Employee stock options are call options issued by a company on its own stock
- They are often at-the-money at the time of issue
- They often last as long as 10 years

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 3. Typical Features of Employee Stock Options（期权）

**原文要点**
- There is a vesting period during which options cannot be exercised
- When employees leave during the vesting period options are forfeited
- When employees leave after the vesting period in-the-money options are exercised immediately and out of the money options are forfeited
- Employees are not permitted to sell options
- When options are exercised the company issues new shares

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 4. Exercise Decision

**原文要点**
- To realize cash from an employee stock option the employee must exercise the options and sell the underlying shares
- Even when the underlying stock pays no dividend an employee stock option (unlike a regular call option) is often exercised early

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。看涨期权对应买入权，适合表达上涨观点或构造上行保护。

---

### 5. Drawbacks of Employee Stock Options（期权）

**原文要点**
- Gain to executives from good performance is much greater than the penalty for bad performance
- Executives do very well when the stock market as a whole goes up, even if their firm does relatively poorly
- Executives are encouraged to focus on short-term performance at the expense of long-term performance
- Executives are tempted to time announcements or take other decisions that maximize the value of the options

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 6. Accounting for Employee Stock Options（期权）

**原文要点**
- Prior to 1995 the cost of an employee stock option on the income statement was its intrinsic value on the issue date
- After 1995 a “fair value” had to be reported in the notes (but expensing fair value on the income statement was optional)
- Since 2005 both FASB and IASB have required the fair value of options to be charged against income at the time of issue

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 7. Traditional At-the-Money Call Options（期权）

**原文要点**
- The attraction of at-the-money call options used to be that they led to no expense on the income statement because they had zero intrinsic value on the exercise date
- Other plans were liable to lead an expense
- Now that the accounting rules have changed some companies are considering other types of plans

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 8. Nontraditional Plans

**原文要点**
- Strike price is linked to stock index so that the company’s stock price has to outperform the index for options to move in the money
- Strike price increases in a predetermined way
- Options vest only if specified profit targets are met

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 9. Valuation of Employee Stock Options（期权）

**原文要点**
- Most common approach is to use Black-Scholes-Merton with time to maturity equal to an estimate of expected life
- There is no theoretical justification for this but it seems to give reasonable results in most circumstances

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。Black/BSM 类模型通常在风险中性测度下取期望再折现，波动率是最敏感的输入。

---

### 10. Example (Example 16.1)

**原文要点**
- A company issues one million10-year ATM options
- stock price is $30.
- It estimates the long term volatility using historical data to be 25% and the average time to exercise to be 4.5 years
- The 4.5 year interest rate is 5% and dividends during the next 4.5 years are estimated to have a PV of $4
- Using BSM with S0 =30, K=30, r=5%, s=25%, and T=4.5 years gives value of each option equal to $6.31
- The income statement expense would be $6.31 million

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。利率章节要同时看现金流折现和利率本身的随机变化。

---

### 11. Other Approaches

**原文要点**
- Estimate the probability of exercise as a function of the stock price and remaining life. Use a binomial tree with roll back rules reflecting the probabilities
- A simple version of this is to assume that the option is exercised when the ratio of the stock price to the strike price reaches some multiple
- Use an auction to determine the market prices of securities whose payoffs mirror the payoffs from the options
- This is an approach used by Zions Bancorp in 2007

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。树模型通过离散状态递推，适合理解复制组合、风险中性概率和提前行权。

---

### 12. Dilution

**原文要点**
- Employee stock options are liable to dilute the interests of shareholders because new shares are bought at below market price
- However this dilution takes place at the time the market hears that the options have been granted (Business Snapshot 15.3)
- It does not take place at the time the options are exercised

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

### 13. Backdating

**原文要点**
- Backdating appears to have been a widespread (illegal) practice in the United States. It was uncovered by academic researchers (Yermack, Lie, Heron)
- A company might issue at-the-money options on April 30 when the stock price is $50 and then backdate the grant date to April 3 when the stock price is $42
- Why would they do this?

📌 **中文解释**：期权的关键在非线性收益：买方损失有限、收益可能随标的变化放大，卖方则相反。

---

## 四、复习抓手

- 先用自己的话说清楚本章产品或模型解决什么风险问题。
- 遇到公式时，先标出每个变量的金融含义，再代入数值。
- 对表格和图示，重点看现金流方向、损益形状、风险暴露和隐含假设。
