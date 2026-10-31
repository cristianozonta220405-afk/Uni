from lib import *

W5 = (36, 16, 16, 16, 16)

# ------------------------------------------------------------------ F.1
we1 = WE(
    "Common-size income statement, two years",
    P("Express the income statement of Pino Srl in common-size percents for both years and assess the situation.")
    + T("""
^ | 2025 | 2024
Net sales | 800,000 | 640,000
Cost of goods sold | 488,000 | 371,200
Gross profit | 312,000 | 268,800
Operating expenses | 208,000 | 179,200
Net income | 104,000 | 89,600
""", w=(50, 25, 25)),
    [
        ("Step 1 — Every line divided by net sales of the same year",
         F("Common-size % = Line ÷ Net sales × 100 &nbsp;&nbsp;— e.g. COGS 2025 = 488,000 ÷ 800,000 = 61.0%")
         + T("""
^ | 2025 | 2024 | % 2025 | % 2024
Net sales | 800,000 | 640,000 | 100.0% | 100.0%
Cost of goods sold | 488,000 | 371,200 | 61.0% | 58.0%
Gross profit | 312,000 | 268,800 | 39.0% | 42.0%
Operating expenses | 208,000 | 179,200 | 26.0% | 28.0%
Net income | 104,000 | 89,600 | 13.0% | 14.0%
""", w=W5, cls="small")),
    ],
    comment=P("Net income grew in euros, but each euro of sales now earns 13.0 cents against 14.0: cost of goods sold took 3 points more "
              "of sales (pricing pressure or input costs), only partly offset by 2 points saved on operating expenses. Mildly unfavourable."),
)

f1 = EX("F1", "Common-size income statement, two years", "common-size",
        P("Express the income statement of Carro Spa in common-size percents for both years and assess whether the "
          "company’s situation is favourable or unfavourable.")
        + T("""
^ | 2025 | 2024
Net sales | 1,500,000 | 1,200,000
Cost of goods sold | 915,000 | 708,000
Gross profit | 585,000 | 492,000
Selling expenses | 240,000 | 180,000
Administrative expenses | 135,000 | 108,000
Total operating expenses | 375,000 | 288,000
Operating profit | 210,000 | 204,000
Interest expense | 30,000 | 24,000
Income before tax | 180,000 | 180,000
Income tax expense | 54,000 | 54,000
Net income | 126,000 | 126,000
""", w=W5, add=["% 2025", "% 2024"], tall=True),
        [L(3)])

f4 = EX("F4", "Favourable or unfavourable", "common-size",
        P("Express the income statement information of Harman Corporation in common-size percents and assess whether the "
          "company’s situation is favourable or unfavourable.")
        + T("""
^ | 2025 | 2024
Sales | 960,000 | 750,000
Cost of goods sold | 604,800 | 435,000
Gross profit | 355,200 | 315,000
Operating expenses | 201,600 | 150,000
Net income | 153,600 | 165,000
""", w=W5, add=["% 2025", "% 2024"], tall=True),
        [G(16), L(3)])

# ------------------------------------------------------------------ F.2
we2 = WE(
    "Common-size balance sheet",
    P("Express the balance sheet of Alto Spa in common-size percents (one decimal) and comment on the change in structure.")
    + T("""
^ | 2025 | 2024
Cash | 30,000 | 40,000
Accounts receivable | 90,000 | 60,000
Inventories | 120,000 | 100,000
Plant assets, net | 360,000 | 300,000
Accounts payable | 90,000 | 50,000
Long-term debt | 150,000 | 150,000
Share capital | 200,000 | 200,000
Retained earnings | 160,000 | 100,000
**Total (assets = equity and liabilities) | 600,000 | 500,000
""", w=(50, 25, 25)),
    [
        ("Step 1 — Divide by total assets (= total equity and liabilities)",
         T("""
^ | 2025 | 2024 | % 2025 | % 2024
Cash | 30,000 | 40,000 | 5.0% | 8.0%
Accounts receivable | 90,000 | 60,000 | 15.0% | 12.0%
Inventories | 120,000 | 100,000 | 20.0% | 20.0%
Plant assets, net | 360,000 | 300,000 | 60.0% | 60.0%
**Total assets | 600,000 | 500,000 | 100.0% | 100.0%
Accounts payable | 90,000 | 50,000 | 15.0% | 10.0%
Long-term debt | 150,000 | 150,000 | 25.0% | 30.0%
Share capital | 200,000 | 200,000 | 33.3% | 40.0%
Retained earnings | 160,000 | 100,000 | 26.7% | 20.0%
**Total equity and liabilities | 600,000 | 500,000 | 100.0% | 100.0%
""", w=W5, cls="small")),
    ],
    comment=P("The asset mix is stable except that cash (8.0 → 5.0 per cent) has turned into receivables (12.0 → 15.0 per cent): less "
              "liquid. On the financing side equity stays at 60 per cent, but suppliers (10 → 15 per cent) have replaced long-term "
              "debt (30 → 25 per cent): cheaper, but shorter-term financing."),
)

f2 = EX("F2", "Common-size balance sheet", "common-size",
        P("Express the balance sheet of Nordia Ltd in common-size percents, rounding to one decimal place, and comment on "
          "the change in the structure of the company.")
        + T("""
^ | 2025 | 2024
Cash | 40,000 | 44,800
Accounts receivable | 128,000 | 83,200
Inventories | 176,000 | 102,400
Prepaid expenses | 16,000 | 12,800
Plant assets, net | 440,000 | 396,800
Accounts payable | 152,000 | 76,800
Accrued liabilities | 48,000 | 44,800
Long-term debt | 200,000 | 166,400
Share capital | 280,000 | 280,000
Retained earnings | 120,000 | 72,000
**Total | 800,000 | 640,000
""", w=W5, add=["% 2025", "% 2024"], tall=True),
        [L(3)])

f7 = EX("F7", "Common-size capital structure", "common-size",
        P("Construct a common-size statement of the liabilities and equity side of the balance sheet of Marenco Spa and "
          "comment on the composition. Total liabilities and equity are €3,000,000.")
        + T("""
^ | Amount
Current liabilities | 540,000
Long-term debt | 810,000
Preferred stock | 300,000
Common stock | 960,000
Paid-in capital | 90,000
Retained earnings | 300,000
**Total liabilities and equity | 3,000,000
""", w=(50, 25, 25), add=["%"], tall=True),
        [L(3)])

# ------------------------------------------------------------------ F.3
we3 = WE(
    "Two companies of different size; the composition of current assets",
    P("<b>(a)</b> Prepare a vertical analysis of Rossa (large) and Blu (small) and compare their profitability.")
    + T("""
^ | Rossa | Blu
Net sales | 5,000,000 | 800,000
Cost of goods sold | 3,250,000 | 480,000
Operating expenses | 1,000,000 | 200,000
Operating income | 750,000 | 120,000
Net income | 500,000 | 72,000
""", w=(50, 25, 25))
    + P("<b>(b)</b> Current assets of Neva Srl were Year 1: cash 20,000, receivables 30,000, inventories 30,000; Year 2: cash 8,000, "
        "receivables 28,000, inventories 44,000. Analyse the change in liquidity."),
    [
        ("Step 1 — (a) Percentages remove size",
         T("""
^ | Rossa | Blu | Rossa % | Blu %
Net sales | 5,000,000 | 800,000 | 100.0% | 100.0%
Cost of goods sold | 3,250,000 | 480,000 | 65.0% | 60.0%
Operating expenses | 1,000,000 | 200,000 | 20.0% | 25.0%
Operating income | 750,000 | 120,000 | 15.0% | 15.0%
Net income | 500,000 | 72,000 | 10.0% | 9.0%
""", w=W5, cls="small")
         + P("Same operating margin, two cost structures: Blu buys or produces more cheaply (60 against 65 per cent) but carries heavier "
             "overheads (25 against 20 per cent), typical of a smaller scale. Below operating income Blu loses 6 points to interest and "
             "tax against Rossa’s 5, so Rossa ends slightly ahead.")),
        ("Step 2 — (b) Same total, different quality",
         T("""
^ | Year 1 | % | Year 2 | %
Cash | 20,000 | 25.0% | 8,000 | 10.0%
Receivables | 30,000 | 37.5% | 28,000 | 35.0%
Inventories | 30,000 | 37.5% | 44,000 | 55.0%
**Total current assets | 80,000 | 100.0% | 80,000 | 100.0%
""", w=(36, 16, 16, 16, 16), cls="small")
         + P("The total is unchanged, but liquidity worsened: cash fell from a quarter to a tenth of current assets, while inventory — "
             "the least liquid item — rose to more than half. The current ratio would not show this.")),
    ],
)

f3 = EX("F3", "Common-size comparison of two competitors", "common-size",
        P("Prepare a vertical analysis of the 2025 income statement data for Alpha Company and Beta Company in columnar "
          "form, and comment on their relative profitability.")
        + T("""
^ | Alpha | Beta
Net sales | 2,400,000 | 480,000
Cost of goods sold | 1,632,000 | 345,600
Gross profit | 768,000 | 134,400
Operating expenses | 456,000 | 115,200
Income from operations | 312,000 | 19,200
Interest expense | 14,400 | 3,360
Income before income taxes | 297,600 | 15,840
Income tax expense | 96,000 | 5,760
Net income | 201,600 | 10,080
""", w=W5, add=["Alpha %", "Beta %"], tall=True),
        [L(3)])

f6 = EX("F6", "Current asset composition", "common-size",
        P("The current assets of Lerici Energia are reproduced below for Year 1 and Year 2, with their common-size percentages. "
          "Complete the percentages and analyse the change in current asset liquidity.")
        + T("""
^ | Year 1 | % | Year 2 | %
Cash | 36,000 | __ | 18,000 | __
Accounts receivable | 54,000 | __ | 45,000 | __
Inventories | 60,000 | __ | 87,000 | __
**Total current assets | 150,000 | __ | 150,000 | __
""", w=(36, 16, 16, 16, 16), tall=True),
        [L(3)])

# ------------------------------------------------------------------ F.4
we4 = WE(
    "Back from percentages to euros; two traps",
    P("<b>(a)</b> A common-size income statement shows cost of goods sold 70.0%, operating expenses 18.0% and operating profit 12.0%. "
      "Gross profit is €270,000. Reconstruct the statement down to operating profit.")
    + P("<b>(b)</b> Explain what is wrong: (1) a student divides each liability by <i>total liabilities</i> in a common-size balance sheet; "
        "(2) a student concludes that the company with the lower cost-of-goods-sold percentage is the more efficient one."),
    [
        ("Step 1 — (a) Find the anchor: the line whose euro amount and percentage are both known",
         CALC([("Gross profit %", "100% − 70.0%", "30.0%"),
               ("Net sales", "270,000 ÷ 0.30", "900,000"),
               ("Cost of goods sold", "70.0% × 900,000", "630,000"),
               ("Operating expenses", "18.0% × 900,000", "162,000"),
               ("Operating profit", "12.0% × 900,000 = 270,000 − 162,000", "108,000")])),
        ("Step 2 — (b) The traps",
         UL(["(1) The base of a common-size balance sheet is <b>total assets</b> (= total equity and liabilities). Dividing by total "
             "liabilities makes the financing side incomparable with the asset side and hides the weight of debt against equity.",
             "(2) Percentages remove size, not <b>business model</b> or <b>classification</b>: one company may book depreciation or "
             "distribution in cost of goods sold, the other in operating expenses. Compare operating margin, not one line."])),
    ],
)

f5 = EX("F5", "Recovering absolute figures from percentages", "common-size",
        P("An extract of a common-size income statement shows cost of goods sold at 64.0 per cent, operating expenses at "
          "22.0 per cent and operating profit at 14.0 per cent. Gross profit in absolute terms is €468,000. Reconstruct the "
          "income statement down to operating profit."),
        [G(16),
         A(BT(["Line", "%", "€"], ["Net sales", "Cost of goods sold", "Gross profit", "Operating expenses", "Operating profit"],
              w=(50, 20, 30)))])

f8 = EX("F8", "Two traps in a common-size statement", "common-size",
        P("Answer both in three lines each.")
        + OL(["A student’s common-size balance sheet column adds to 100.2 per cent. The arithmetic has been checked and is "
              "right. What happened, and what should the student write?",
              "A second student prepares a common-size income statement by dividing every line by net income rather than by "
              "net sales, reasoning that net income is the bottom line. Explain why this is wrong and what it would do to a "
              "comparison between two companies."]),
        [L(3, "1."), L(3, "2.")])

SEC = SECTION(
    "F", "Common-size (vertical) analysis",
    "Income statement and balance sheet in percentages, two-company comparison, composition analysis, and the two traps.",
    [
        BLOCK("F.1", "Common-size income statement", "Every line as a percentage of net sales, two years side by side.", we1, [f1, f4]),
        BLOCK("F.2", "Common-size balance sheet and capital structure", "Every line as a percentage of total assets.", we2, [f2, f7]),
        BLOCK("F.3", "Comparing companies; composition of current assets",
              "Removing size to compare cost structures, and the quality of a total.", we3, [f3, f6]),
        BLOCK("F.4", "Back from percentages; the traps", "Reconstructing euros from percentages, and the wrong bases.", we4, [f5, f8]),
    ],
)
