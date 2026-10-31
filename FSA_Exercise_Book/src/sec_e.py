from lib import *

W6 = (25, 15, 15, 15, 15, 15)

# ------------------------------------------------------------------ E.1
we1 = WE(
    "Trend percents for two accounts",
    P("Compute index-number trend percents for Gelso Spa, Year 1 = 100, and say whether the trend is favourable.")
    + T("""
^ | Year 1 | Year 2 | Year 3 | Year 4
Sales | 200,000 | 220,000 | 250,000 | 270,000
Cost of goods sold | 120,000 | 135,600 | 157,500 | 175,500
""", w=(28, 18, 18, 18, 18)),
    [
        ("Step 1 — Divide every year by the base year",
         F("Index<sub>t</sub> = Amount<sub>t</sub> ÷ Amount<sub>base</sub> × 100 &nbsp;&nbsp;— e.g. COGS Year 3 = 157,500 ÷ 120,000 × 100 = 131.3")
         + T("""
^Trend percents | Year 1 | Year 2 | Year 3 | Year 4
Sales | 100.0 | 110.0 | 125.0 | 135.0
Cost of goods sold | 100.0 | 113.0 | 131.3 | 146.3
""", w=(28, 18, 18, 18, 18), cls="small")),
    ],
    comment=P("Cost of goods sold grows faster than sales in every year (146 against 135 by Year 4), so the gross margin is shrinking: "
              "unfavourable, even though both lines are growing."),
)

e1 = EX("E1", "Trend percents for three accounts", "trend",
        P("Compute index-number trend percents for the following accounts of Donati Spa, using Year 1 as the base year. State "
          "whether the situation revealed by the trends appears favourable or unfavourable.")
        + T("""
^ | Year 1 | Year 2 | Year 3 | Year 4 | Year 5
Sales | 420,000 | 462,000 | 508,200 | 541,800 | 571,200
Cost of goods sold | 252,000 | 282,240 | 317,520 | 347,760 | 378,000
Accounts receivable | 60,000 | 68,400 | 78,000 | 85,800 | 94,800
##Trend percents (Year 1 = 100)
Sales | __ | __ | __ | __ | __
Cost of goods sold | __ | __ | __ | __ | __
Accounts receivable | __ | __ | __ | __ | __
""", w=W6, tall=True),
        [G(16), L(3)])

e2 = EX("E2", "Trend in assets against trend in equity", "trend",
        P("Compute trend percents with Year 1 as the base, then say what the divergence implies for the capital structure.")
        + T("""
^ | Year 1 | Year 2 | Year 3 | Year 4 | Year 5
Total assets | 1,200,000 | 1,260,000 | 1,392,000 | 1,560,000 | 1,776,000
Total equity | 700,000 | 721,000 | 756,000 | 798,000 | 840,000
##Trend percents (Year 1 = 100)
Total assets | __ | __ | __ | __ | __
Total equity | __ | __ | __ | __ | __
""", w=W6, tall=True),
        [G(16), L(3, "What the divergence implies")])

# ------------------------------------------------------------------ E.2
we2 = WE(
    "Rebasing a series, and reading an index table",
    P("<b>(a)</b> A sales index with Year 1 = 100 reads 100, 120, 150, 165. Rebase it to Year 2 = 100.")
    + P("<b>(b)</b> Only these indices are available (Year 1 = 100). Did return on sales and asset turnover rise or fall? What can’t you say?")
    + T("""
^ | Year 1 | Year 2 | Year 3
Sales | 100 | 115 | 130
Net income | 100 | 120 | 140
Total assets | 100 | 110 | 125
""", w=(40, 20, 20, 20)),
    [
        ("Step 1 — (a) Divide every index by the new base index",
         T("""
^ | Year 1 | Year 2 | Year 3 | Year 4
Year 1 = 100 | 100.0 | 120.0 | 150.0 | 165.0
Year 2 = 100 (÷ 1.20) | 83.3 | 100.0 | 125.0 | 137.5
""", w=(32, 17, 17, 17, 17), cls="small")
         + P("What changes: the level of every number. What does not: the relative movement between any two years "
             "(Year 4 ÷ Year 3 = 1.10 in both series).")),
        ("Step 2 — (b) A ratio rises when its numerator index outgrows its denominator index",
         CALC([("Return on sales (NI ÷ Sales)", "Year 3: 140 ÷ 130 = 1.077 → about 7.7% higher than in Year 1", "rose"),
               ("Asset turnover (Sales ÷ TA)", "Year 3: 130 ÷ 125 = 1.04 → about 4% higher than in Year 1", "rose")], w=(30, 56, 14))
         + P("<b>What we cannot say:</b> the level of either ratio (is a margin of 3% or 30%?), and anything about a competitor — indices only "
             "give the direction relative to the company’s own base.")),
    ],
)

e3 = EX("E3", "Rebasing a trend series", "trend",
        P("The sales trend index of Donati Spa with Year 1 as base is 100, 110, 121, 129, 136. The company now wants the "
          "series rebased to Year 3 = 100. Produce the rebased series and explain what changes and what does not.")
        + T("""
^ | Year 1 | Year 2 | Year 3 | Year 4 | Year 5
Year 1 = 100 | 100 | 110 | 121 | 129 | 136
Year 3 = 100 | __ | __ | __ | __ | __
""", w=W6, tall=True),
        [G(12), L(2, "What changes and what does not")])

e4 = EX("E4", "Reading margins out of a trend table", "trend",
        P("You are given only the trend indices below, with Year 1 as base. Without any absolute figures, state whether (a) the "
          "return on sales rose or fell, (b) asset turnover rose or fell, and (c) what you cannot say.")
        + T("""
^ | Year 1 | Year 2 | Year 3
Sales | 100 | 118 | 136
Net income | 100 | 112 | 128
Total assets | 100 | 126 | 148
""", w=(40, 20, 20, 20)),
        [G(18), L(4, "(a), (b) and (c)")])

# ------------------------------------------------------------------ E.3
we3 = WE(
    "One trend against another",
    P("<b>(a)</b> The sales index of Arno Srl is 100, 108, 117. Receivables were €50,000, €60,000 and €75,000. Compare the two trends. "
      "<b>(b)</b> Non-current liabilities were €100,000, €130,000 and €160,000; interest expense €6,000, €8,450 and €12,000. "
      "Compute both trends and the implied interest rate."),
    [
        ("Step 1 — (a) Receivables against sales",
         T("""
^ | Year 1 | Year 2 | Year 3
Sales index | 100 | 108 | 117
Receivables | 50,000 | 60,000 | 75,000
Receivables index | 100 | 120 | 150
""", w=(40, 20, 20, 20), cls="small")
         + P("Receivables grow almost three times as fast as sales: collection is slowing, so check the days’ sales in receivables and the ageing.")),
        ("Step 2 — (b) Debt, its cost, and the implied rate",
         T("""
^ | Year 1 | Year 2 | Year 3
Non-current liabilities index | 100 | 130 | 160
Interest expense index | 100 | 140.8 | 200
Implied rate = Interest ÷ Debt | 6.0% | 6.5% | 7.5%
""", w=(40, 20, 20, 20), cls="small")),
    ],
    comment=P("Interest doubled while debt rose 60 per cent: the company is paying more per euro borrowed — lenders see it as riskier, "
              "or rates have risen. The trend in the cost of debt is as important as the trend in the debt."),
)

e5 = EX("E5", "Inventory outpacing sales", "trend",
        P("Using Year 1 as the base, compute the trend percents for inventories of Lanova Srl and compare them with the sales "
          "series of exercise E1 (100, 110, 121, 129, 136). Comment.")
        + T("""
^ | Year 1 | Year 2 | Year 3 | Year 4 | Year 5
Inventories | 180,000 | 212,400 | 250,200 | 297,000 | 352,800
Inventory index | __ | __ | __ | __ | __
Sales index (E1) | 100 | 110 | 121 | 129 | 136
""", w=W6, tall=True),
        [G(14), L(3)])

e6 = EX("E6", "Trend in debt and in its cost", "trend",
        P("Compute trend percents with Year 1 as base for the non-current liabilities and the interest expense of Verona Group, "
          "then compute the implied average interest rate in Year 1 and Year 5 and comment.")
        + T("""
^ | Year 1 | Year 2 | Year 3 | Year 4 | Year 5
Non-current liabilities | 200,000 | 230,000 | 290,000 | 360,000 | 450,000
Interest expense | 16,000 | 18,400 | 24,650 | 32,320 | 42,750
##Trend percents (Year 1 = 100)
Non-current liabilities | __ | __ | __ | __ | __
Interest expense | __ | __ | __ | __ | __
Implied rate | __ | | | | __
""", w=W6, tall=True),
        [G(14), L(2)])

# ------------------------------------------------------------------ E.4
we4 = WE(
    "Trend and common-size together; what a trend cannot tell you",
    P("<b>(a)</b> Sales of Lago Ltd were €400,000 in Year 1 and the sales index is 100, 115, 125. Cost of goods sold as a percentage of "
      "sales was 55.0, 58.0 and 61.0 per cent. Compute gross profit for each year and reconcile the two stories.")
    + P("<b>(b)</b> A colleague notes that Company R’s net income index went from 100 to 180 while Company S’s went from 100 to 130, and "
        "concludes that R is the more profitable company. Comment."),
    [
        ("Step 1 — (a) Turn indices and percentages back into euros",
         T("""
^ | Year 1 | Year 2 | Year 3
Sales (400,000 × index) | 400,000 | 460,000 | 500,000
COGS (% × sales) | 220,000 | 266,800 | 305,000
Gross profit | 180,000 | 193,200 | 195,000
Gross profit index | 100 | 107.3 | 108.3
""", w=(40, 20, 20, 20), cls="small")
         + P("The trend says the company grew 25 per cent; the common-size says each euro of sales keeps 6 cents less. Together: gross profit grew only 8.3 per cent.")),
        ("Step 2 — (b) Growth is not profitability",
         UL(["Each index is on its <b>own base</b>: R may have started from a tiny profit, so +80 per cent may be few euros.",
             "Profitability is a <b>return</b> (net income ÷ sales, ROCE, RNOA), which indices do not show.",
             "A single year’s base can be <b>abnormal</b> (a bad Year 1 flatters every later index)."])),
    ],
)

e7 = EX("E7", "Trend and common-size together", "trend",
        P("Sales of Castano Ltd were €500,000 in Year 1 and the sales trend index is 100, 112, 126. Cost of goods sold, "
          "expressed as a common-size percentage of sales, was 60.0 per cent, 63.0 per cent and 66.0 per cent. Compute "
          "gross profit in absolute terms for each year and reconcile the two stories."),
        [A(BT(["", "Year 1", "Year 2", "Year 3"], ["Sales", "Cost of goods sold", "Gross profit", "Gross profit index"], w=(40, 20, 20, 20))),
         L(3, "Reconcile the two stories")])

e8 = EX("E8", "What a trend series cannot do", "trend",
        P("Two competitors report the following sales trend indices, each on its own Year 1 base. A colleague concludes that "
          "Company Q is the better investment. List the three reasons the conclusion is unsupported.")
        + T("""
^ | Year 1 | Year 2 | Year 3 | Year 4
Company P | 100 | 104 | 109 | 113
Company Q | 100 | 128 | 161 | 204
""", w=(32, 17, 17, 17, 17)),
        [L(6, "Three reasons")])

SEC = SECTION(
    "E", "Index-number trend analysis",
    "Trend percents, rebasing, and what a series of indices can and cannot support.",
    [
        BLOCK("E.1", "Trend percents", "Every year divided by the base year, then the reading.", we1, [e1, e2]),
        BLOCK("E.2", "Rebasing and reading an index table", "Changing the base, and inferring ratios from indices alone.", we2, [e3, e4]),
        BLOCK("E.3", "One trend against another", "Inventory or receivables against sales; debt against its cost.", we3, [e5, e6]),
        BLOCK("E.4", "Trend with common-size, and the limits of trends",
              "Back to euros, and the conclusions a trend cannot carry.", we4, [e7, e8]),
    ],
)
