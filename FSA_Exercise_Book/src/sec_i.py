from lib import *

NOVA = (COMPANY("NOVA SPA", "Statements for 2025 — used in every worked example of Sections I and J. Tax rate 30 per cent.")
        + T("""
^Income statement 2025 | € 000 | Balance sheet 31 Dec 2025 | € 000
Sales | 2,000 | Fixed assets, net | 900
Cost of goods sold | 1,200 | Inventory | 250
Selling and administrative expense | 500 | Accounts receivable | 200
<b>Operating income</b> | <b>300</b> | Marketable securities | 50
Interest expense | 40 | Cash | 100
<b>Income before tax</b> | <b>260</b> | <b>Total assets</b> | <b>1,500</b>
Income tax (30%) | 78 | Equity | 800
<b>Net income</b> | <b>182</b> | Bonds payable | 400
 | | Accounts payable | 220
 | | Income taxes payable | 80
 | | <b>Total equity and liabilities</b> | <b>1,500</b>
""", w=(34, 14, 38, 14), cls="small"))

# ------------------------------------------------------------------ I.1
we1 = WE(
    "NOPAT, the operating profit margin and its components",
    NOVA + P("Compute the profit margin of Nova Spa and disaggregate it."),
    [
        ("Step 1 — Name the substitution, then the formula",
         P("<em>“Operating profit margin (instead of Profit margin)”</em> — the course measures the margin on operations, after tax, "
           "before financing: NOPAT ÷ Sales. Tax rate assumed: 30 per cent.")
         + CALC([("NOPAT", "Operating income × (1 − t) = 300 × 0.70", "210"),
                 ("Operating profit margin", "NOPAT ÷ Sales = 210 ÷ 2,000", "10.5%")])),
        ("Step 2 — Disaggregate the margin line by line",
         CALC([("Gross profit margin", "(2,000 − 1,200) ÷ 2,000", "40.0%"),
               ("− S&amp;A as % of sales", "500 ÷ 2,000", "25.0%"),
               ("= Operating income margin, pre-tax", "40.0% − 25.0% = 300 ÷ 2,000", "15.0%"),
               ("× (1 − tax rate)", "15.0% × 0.70", "10.5% ✓")], w=(34, 48, 18))),
    ],
    comment=P("Nova keeps 40 cents of gross profit per euro of sales and spends 25 on selling and administration; after tax, 10.5 cents of each "
              "euro of sales is operating profit. To compare two companies, compare the components: that is where the difference arises."),
)

i1 = EX("I1", "NOPAT and the operating profit margin", "profitability",
        P("Using the statements of Orso Spa and Lince Srl given in exercise G1, compute the profit margin for both companies. "
          "Assume a tax rate of 30 per cent."),
        [L(1, "Substitution and formula"),
         A(BT(["", "Orso", "Lince"], ["Operating income", "NOPAT = Operating income × (1 − 0.30)", "Sales", "Operating profit margin"],
              w=(50, 25, 25))),
         L(2)])

i5 = EX("I5", "Disaggregating the margin", "profitability",
        P("For Orso Spa, disaggregate the operating profit margin into its components: gross profit margin, and selling and "
          "administrative expense as a percentage of sales. Do the same for Lince and comment on where the difference arises."),
        [A(BT(["Component", "Orso", "Lince"],
              ["Gross profit margin", "− S&A expense as % of sales", "= Operating income margin (pre-tax)", "× (1 − 0.30) = Operating profit margin"],
              w=(50, 25, 25))),
         G(16), L(3, "Where the difference arises")])

# ------------------------------------------------------------------ I.2
we2 = WE(
    "Net operating assets, net financial obligations and the turnover",
    P("Use the Nova Spa statements. Treat marketable securities as a financial asset and all current liabilities as operating. Compute NOA "
      "and NFO, check the identity, and compute the asset turnover."),
    [
        ("Step 1 — Re-cut the balance sheet",
         T("""
^Operating side | € 000 | Financial side | € 000
Total assets | 1,500 | Bonds payable | 400
− Marketable securities | (50) | − Marketable securities | (50)
= Operating assets | 1,450 | <b>= Net financial obligations (NFO)</b> | <b>350</b>
− Operating liabilities (all CL: 220 + 80) | (300) | Equity | 800
**= Net operating assets (NOA) | 1,150 | NFO + Equity | 1,150 ✓
""", w=(36, 14, 36, 14), cls="small")),
        ("Step 2 — The turnover, on what is available",
         P("<em>“Operating asset turnover (instead of Asset turnover)”</em>. Can we calculate the average? No, we can’t — only one balance sheet "
           "date is given, so we use year-end NOA.")
         + CALC([("Operating asset turnover", "Sales ÷ NOA = 2,000 ÷ 1,150", "1.74x")])),
    ],
    comment=P("Every euro of capital invested in operations generates €1.74 of sales. NOA = NFO + Equity is the check that nothing was lost or "
              "counted twice in the re-cut."),
)

i2 = EX("I2", "Net operating assets and net financial obligations", "profitability",
        P("For both Orso and Lince, re-cut the balance sheet into operating and financial components. Treat marketable "
          "securities as a financial asset and all current liabilities as operating. Show that NOA equals NFO plus equity."),
        [A(BT(["", "Orso", "Lince"],
              ["Total assets", "− Financial assets (marketable securities)", "= Operating assets", "− Operating liabilities",
               "= NOA", "Financial obligations (bonds)", "− Financial assets", "= NFO", "Equity", "Check: NFO + Equity"],
              w=(50, 25, 25)))])

i3 = EX("I3", "Operating asset turnover", "profitability",
        P("Compute the asset turnover for Orso and Lince. Only one year of balance sheet data is available."),
        [L(2, "Substitution, and the average"),
         A(BT(["", "Orso", "Lince"], ["Sales", "NOA", "Operating asset turnover"], w=(50, 25, 25))),
         L(2)])

# ------------------------------------------------------------------ I.3
we3 = WE(
    "RNOA as margin times turnover",
    P("<b>(a)</b> Compute the return on assets of Nova Spa and verify that it decomposes into margin × turnover. "
      "<b>(b)</b> Two companies each earn NOPAT of 300 on NOA of 2,000; X has sales of 1,000, Y of 6,000. Complete the decomposition."),
    [
        ("Step 1 — (a) Substitution, formula, check",
         P("<em>“Return on net operating assets, RNOA (instead of Return on assets)”</em>.")
         + CALC([("RNOA", "NOPAT ÷ NOA = 210 ÷ 1,150", "18.3%"),
                 ("Check", "Operating profit margin × Operating asset turnover = 10.5% × 1.739", "18.3% ✓")], w=(16, 66, 18))),
        ("Step 2 — (b) Same return, two business models",
         T("""
^ | X | Y
NOPAT | 300 | 300
Sales | 1,000 | 6,000
Net operating assets | 2,000 | 2,000
NOPAT margin (NOPAT ÷ Sales) | 30.0% | 5.0%
NOA turnover (Sales ÷ NOA) | 0.5x | 3.0x
**RNOA (margin × turnover) | 15.0% | 15.0%
""", w=(50, 25, 25), cls="small")),
    ],
    comment=P("X earns a lot on each sale but turns its capital slowly (a luxury or capital-intensive model); Y earns little per sale but turns "
              "its capital six times faster (a discount retailer). The return on capital is identical: margin and turnover are substitutes."),
)

i4 = EX("I4", "RNOA, and the check that it decomposes", "profitability",
        P("Compute the return on assets for Orso and Lince, then verify that it equals the operating profit margin multiplied by "
          "the operating asset turnover."),
        [L(1, "Substitution"),
         A(BT(["", "Orso", "Lince"], ["NOPAT", "NOA", "RNOA = NOPAT ÷ NOA", "Check: margin × turnover"], w=(50, 25, 25))),
         L(2)])

i7 = EX("I7", "Margin and turnover are interchangeable", "profitability",
        P("Three companies report the following. Complete the table and explain in four lines what it says about business models.")
        + T("""
^ | A | B | C
NOPAT | 500,000 | 500,000 | 100,000
Sales | 5,000,000 | 10,000,000 | 10,000,000
Net operating assets | 5,000,000 | 5,000,000 | 1,000,000
NOPAT margin | __ | __ | __
NOA turnover | __ | __ | __
RNOA | __ | __ | __
""", w=(40, 20, 20, 20), tall=True),
        [L(4)])

# ------------------------------------------------------------------ I.4
we4 = WE(
    "Year-end or average NOA; operating liabilities leverage",
    P("<b>(a)</b> Nova’s NOA at 31 December 2024 was €850 thousand. Compute RNOA on year-end and on average NOA. "
      "<b>(b)</b> Compute OLLEV at year end and verify RNOA = (NOPAT ÷ Sales) × (Sales ÷ OA) × (1 + OLLEV)."),
    [
        ("Step 1 — (a) Two dates → use the average",
         CALC([("RNOA on year-end NOA", "210 ÷ 1,150", "18.3%"),
               ("Average NOA", "(850 + 1,150) ÷ 2", "1,000"),
               ("RNOA on average NOA", "210 ÷ 1,000", "21.0%")])
         + P("NOA grew 35 per cent during the year. NOPAT was earned on the capital employed through the year, not on the year-end figure, "
             "which understates the return by 2.7 points. With two dates, present the average.")),
        ("Step 2 — (b) Operating liabilities lift the return on the capital the firm provides",
         CALC([("OLLEV", "Operating liabilities ÷ NOA = 300 ÷ 1,150", "0.261"),
               ("NOPAT ÷ Sales", "210 ÷ 2,000", "10.5%"),
               ("Sales ÷ Operating assets", "2,000 ÷ 1,450", "1.379x"),
               ("RNOA", "10.5% × 1.379 × (1 + 0.261)", "18.3% ✓")], w=(26, 56, 18))),
    ],
    comment=P("In words: suppliers and the tax authority finance 300 of Nova’s 1,450 of operating assets free of interest. The return on "
              "operating assets (14.5 per cent) is multiplied by 1.26 to give the return on the net capital Nova itself invests."),
)

i6 = EX("I6", "Year-end or average, and how much it matters", "profitability",
        P("Using the Vela Group statements of exercise G5, compute RNOA for 2025 twice: once on the year-end NOA, once on "
          "the average of the opening and closing NOA. The tax rate is 40 per cent. Comment on the difference and say which "
          "you would present."),
        [G(50), L(3)])

i8 = EX("I8", "Operating liabilities leverage", "profitability",
        [P("For Orso Spa, compute the operating liabilities leverage ratio OLLEV and verify the identity"),
         F("RNOA = (NOPAT ÷ Sales) × (Sales ÷ Average OA) × (1 + OLLEV)") + P("Then state what the identity means in words.")],
        [G(44), L(3, "What the identity means")])

# ------------------------------------------------------------------ I.5
we5 = WE(
    "Disaggregating the turnover; writing the profitability comparison",
    P("<b>(a)</b> At the start of 2025 Nova had receivables of €160 thousand, inventory 230, accounts payable 180 and long-term operating "
      "assets 820. Compute the component turnovers and days on average balances. <b>(b)</b> A competitor, Stella, has an operating profit "
      "margin of 8.0 per cent, an operating asset turnover of 2.50 and an RNOA of 20.0 per cent. Write the comparison."),
    [
        ("Step 1 — (a) One turnover for each piece of NOA",
         T("""
^Component | Average balance | Turnover | Days (360 ÷ turnover)
Receivables (Sales ÷ avg AR) | (160 + 200) ÷ 2 = 180 | 2,000 ÷ 180 = 11.1x | 32.4
Inventory (COGS ÷ avg inv.) | (230 + 250) ÷ 2 = 240 | 1,200 ÷ 240 = 5.0x | 72.0
Accounts payable (COGS ÷ avg AP) | (180 + 220) ÷ 2 = 200 | 1,200 ÷ 200 = 6.0x | 60.0
Long-term operating assets (Sales ÷ avg) | (820 + 900) ÷ 2 = 860 | 2,000 ÷ 860 = 2.33x | —
""", w=(34, 24, 26, 16), cls="small")
         + P("The weakest component is <b>inventory</b>: 72 days of stock against 32 days to collect. Payables at 60 days finance most of it.")),
        ("Step 2 — (b) A model comparison, in the comparative register",
         P("<i>Nova earns a higher operating profit margin than Stella (10.5 against 8.0 per cent), thanks to a 40 per cent gross margin, but it "
           "turns its net operating assets more slowly (1.74 against 2.50 times). The slower turnover more than offsets the higher margin: "
           "Nova’s RNOA is 18.3 per cent against Stella’s 20.0. The gap lies in asset use, chiefly the 72 days of inventory; reducing "
           "stock would raise Nova’s RNOA without touching its margin.</i>")),
    ],
)

i9 = EX("I9", "Disaggregating the turnover", "profitability",
        P("Orso Spa opened the year with receivables of €156,000, inventory of €200,000, accounts payable of €264,000 and "
          "long-term operating assets of €700,000. Compute the receivables turnover, the inventory turnover, the accounts "
          "payable turnover and the long-term operating asset turnover, with the accompanying days ratios, and say which "
          "component of the operating asset turnover is weakest."),
        [A(BT(["Component", "Average balance", "Turnover", "Days"],
              ["Receivables", "Inventory", "Accounts payable", "Long-term operating assets"], w=(34, 24, 24, 18))),
         G(14), L(2, "Weakest component")])

i10 = EX("I10", "Write the profitability comparison", "profitability",
         P("Using everything computed in exercises I1 to I5, write the profitability paragraph of a report comparing Orso and "
           "Lince. Eight lines at most, in the comparative register the published solutions use."),
         [L(9, "Profitability — Orso and Lince")])

SEC = SECTION(
    "I", "Profitability, NOPAT and RNOA",
    "The substitutions the lecturer makes, the operating / financial cut of the balance sheet, and the two-way decomposition of the "
    "return on operating capital.",
    [
        BLOCK("I.1", "NOPAT and the operating profit margin", "Name the substitution, compute, then break the margin into its lines.", we1, [i1, i5]),
        BLOCK("I.2", "Net operating assets and the turnover", "The operating / financial cut, the identity, and the turnover.", we2, [i2, i3]),
        BLOCK("I.3", "RNOA = margin × turnover", "The decomposition, and why margin and turnover are substitutes.", we3, [i4, i7]),
        BLOCK("I.4", "Averages and operating liabilities leverage", "How much the denominator matters, and what OLLEV adds.", we4, [i6, i8]),
        BLOCK("I.5", "Disaggregating the turnover; the written comparison", "Days for every piece of NOA, then the paragraph.", we5, [i9, i10]),
    ],
)
