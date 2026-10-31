from lib import *

CHG = ["Change €", "Change %"]
W5 = (34, 16, 16, 17, 17)

# ------------------------------------------------------------------ D.1
we1 = WE(
    "Horizontal analysis of an income statement",
    P("Prepare a horizontal analysis of the condensed income statement of Corvo Srl for 2025, base year 2024, and comment.")
    + T("""
^ | 2025 | 2024
Net sales | 600,000 | 500,000
Cost of goods sold | 390,000 | 310,000
Gross profit | 210,000 | 190,000
Operating expenses | 132,000 | 120,000
Net income | 78,000 | 70,000
""", w=(50, 25, 25)),
    [
        ("Step 1 — One formula for every line",
         F("Change € = Current year − Base year &nbsp;&nbsp;·&nbsp;&nbsp; Change % = Change € ÷ Base year × 100")),
        ("Step 2 — The schedule",
         T("""
^ | 2025 | 2024 | Change € | Change %
Net sales | 600,000 | 500,000 | +100,000 | +20.0%
Cost of goods sold | 390,000 | 310,000 | +80,000 | +25.8%
Gross profit | 210,000 | 190,000 | +20,000 | +10.5%
Operating expenses | 132,000 | 120,000 | +12,000 | +10.0%
Net income | 78,000 | 70,000 | +8,000 | +11.4%
""", w=W5, cls="small")),
    ],
    comment=P("Sales grew 20.0 per cent but cost of goods sold grew faster (25.8 per cent), so gross profit rose only 10.5 per cent: "
              "the gross margin is being squeezed. Operating expenses were held to +10.0 per cent, which lets net income grow 11.4 per cent. "
              "Favourable on volume and cost control, unfavourable on pricing or purchasing."),
)

d1 = EX("D1", "Horizontal analysis of a balance sheet", "horizontal",
        P("Prepare a schedule showing a horizontal analysis of the condensed statement of financial position of Trevi Group for "
          "2025, using 2024 as the base year. Then comment in three lines on how the growth has been financed.")
        + T("""
^ | 2025 | 2024
Plant assets (net) | 528,000 | 440,000
Current assets | 196,000 | 160,000
**Total assets | 724,000 | 600,000
Share capital | 250,000 | 200,000
Retained earnings | 174,000 | 185,000
**Total equity | 424,000 | 385,000
Non-current liabilities | 186,000 | 130,000
Current liabilities | 114,000 | 85,000
**Total liabilities | 300,000 | 215,000
**Total equity and liabilities | 724,000 | 600,000
""", w=W5, add=CHG, tall=True),
        [L(3, "How the growth has been financed")])

d2 = EX("D2", "Horizontal analysis of an income statement", "horizontal",
        P("Prepare a horizontal analysis of the condensed income statement of Hale Corporation for 2025, using 2024 as the "
          "base year, and say whether the picture is favourable.")
        + T("""
^ | 2025 | 2024
Net sales | 840,000 | 700,000
Cost of goods sold | 571,200 | 490,000
Gross profit | 268,800 | 210,000
Operating expenses | 151,200 | 126,000
Net income | 117,600 | 84,000
""", w=W5, add=CHG, tall=True),
        [G(20), L(3)])

# ------------------------------------------------------------------ D.2
we2 = WE(
    "When the percentage change cannot be computed",
    P("Compute the amount and percentage change for each account of Asola Spa, and flag the movements a creditor would ask about.")
    + T("""
^ | Year 2 | Year 1
Marketable securities | 30,000 | 0
Inventories | 84,000 | 70,000
Accounts payable | 45,000 | 60,000
Bank loans | 0 | 50,000
Net income (loss) | 12,000 | (8,000)
""", w=(50, 25, 25)),
    [
        ("Step 1 — The amount can always be computed; the percentage needs a positive base",
         T("""
^ | Year 2 | Year 1 | Change € | Change %
Marketable securities | 30,000 | 0 | +30,000 | n.m.
Inventories | 84,000 | 70,000 | +14,000 | +20.0%
Accounts payable | 45,000 | 60,000 | −15,000 | −25.0%
Bank loans | 0 | 50,000 | −50,000 | −100.0%
Net income (loss) | 12,000 | (8,000) | +20,000 | n.m.
""", w=W5, cls="small")),
        ("Step 2 — Why “n.m.” (not meaningful)",
         UL(["<b>Base of zero</b> (marketable securities): division by zero — a percentage cannot be computed.",
             "<b>Negative base</b> (loss to profit): the formula gives −250 per cent for an improvement, so the sign is misleading.",
             "A positive base falling to zero (bank loans) is fine: −100 per cent."])),
    ],
    comment=P("A creditor would ask why inventories rose 20 per cent while payables fell 25 per cent — together they absorbed €29,000 of cash — "
              "and how the €50,000 loan was repaid while €30,000 was parked in securities."),
)

d3 = EX("D3", "When the percentage change cannot be computed", "horizontal",
        P("Compute the amount and the percentage of increase or decrease for each account below. Where a percentage "
          "cannot be computed, say so and explain why in one line.")
        + T("""
^ | Year 2 | Year 1
Short-term investments | 225,000 | 180,000
Accounts receivable | 84,000 | 96,000
Notes payable | 45,000 | 0
Deficit on retained earnings | 15,000 | (40,000)
""", w=W5, add=CHG, tall=True),
        [L(3, "Where the percentage cannot be computed, and why")])

d4 = EX("D4", "Year-to-year change over a set of accounts", "horizontal",
        P("Compute the amount and percentage of increase or decrease for each account of Orvieto Spa, and identify which "
          "movements a creditor would want explained.")
        + T("""
^ | Year 2 | Year 1
Cash | 52,000 | 65,000
Inventories | 148,000 | 120,000
Prepaid expenses | 9,000 | 12,000
Goodwill | 90,000 | 90,000
Bank loans | 70,000 | 0
Accrued liabilities | 34,500 | 30,000
""", w=W5, add=CHG, tall=True),
        [L(3, "Movements a creditor would want explained")])

# ------------------------------------------------------------------ D.3
we3 = WE(
    "Recovering the base year, and choosing it",
    P("<b>(a)</b> Sales rose 15.0 per cent in Year 2 to €690,000. Cost of goods sold rose 20.0 per cent from a Year 1 figure of €360,000. "
      "Compute Year 1 sales, Year 2 cost of goods sold, gross profit for both years and its change.")
    + P("<b>(b)</b> Danae Ltd reports net sales of €400,000 in 2023, €320,000 in 2024 and €360,000 in 2025. Analyse 2025 against 2024 "
        "and against 2023."),
    [
        ("Step 1 — (a) Undo the percentage by dividing, apply it by multiplying",
         CALC([("Year 1 sales", "690,000 ÷ 1.15", "600,000"),
               ("Year 2 cost of goods sold", "360,000 × 1.20", "432,000"),
               ("Gross profit Year 1", "600,000 − 360,000", "240,000"),
               ("Gross profit Year 2", "690,000 − 432,000", "258,000"),
               ("Change", "+18,000 ÷ 240,000", "+7.5%")])
         + P("Never compute Year 1 as 690,000 × 0.85 = 586,500: the 15 per cent is a percentage of Year 1, not of Year 2.")),
        ("Step 2 — (b) Same 2025 figure, two bases",
         CALC([("2025 vs 2024", "(360,000 − 320,000) ÷ 320,000", "+12.5%"),
               ("2025 vs 2023", "(360,000 − 400,000) ÷ 400,000", "−10.0%")])),
    ],
    comment=P("(a) Sales +15.0 per cent but gross profit only +7.5 per cent: costs outran prices. (b) Both answers are correct — one tells "
              "a story of recovery, the other of a business still below its 2023 level. Always state the base year, and check the base "
              "chosen by whoever prepared an analysis you are reading."),
)

d5 = EX("D5", "Recovering the base year", "horizontal",
        P("Sales increased 18.0 per cent during Year 2 and reached €1,062,000. Cost of goods sold increased 24.0 per cent "
          "from a Year 1 figure of €600,000.")
        + REQ(["Compute Year 1 sales and Year 2 cost of goods sold.",
               "Compute gross profit for both years and its percentage change.", "Comment."]),
        [G(45), L(2)])

d6 = EX("D6", "Choosing the base year changes the story", "horizontal",
        P("Kerrel Ltd reports net sales of €500,000 in 2023, €750,000 in 2024 and €690,000 in 2025.")
        + REQ(["Prepare a horizontal analysis of 2025 using 2024 as the base.",
               "Prepare a horizontal analysis of 2025 using 2023 as the base.",
               "Explain in two lines why both are correct and what that implies for reading someone else’s analysis."]),
        [A(BT(["Comparison", "Base year", "Change €", "Change %"], ["2025 vs 2024", "2025 vs 2023"], w=(28, 24, 24, 24))),
         G(14), L(2)])

# ------------------------------------------------------------------ D.4
we4 = WE(
    "Horizontal analysis with a sign change, and writing the comment",
    P("<b>(a)</b> Complete the horizontal analysis of this extract from the income statement of Lerma NV and write the comment.")
    + T("""
^ | 2025 | 2024
Operating profit | 50,000 | 40,000
Interest expense | (30,000) | (10,000)
Income before tax | 20,000 | 30,000
Income tax expense | (6,000) | (9,000)
Net income | 14,000 | 21,000
""", w=(50, 25, 25))
    + P("<b>(b)</b> A completed analysis of Tosca Spa shows: sales +10.0%, receivables +25.0%, inventories +5.0%, net income +12.0%. "
        "Write the comment (six lines at most) and state what you cannot conclude."),
    [
        ("Step 1 — (a) Compute on the size of each line; read the sign as more or less expense",
         T("""
^ | 2025 | 2024 | Change € | Change %
Operating profit | 50,000 | 40,000 | +10,000 | +25.0%
Interest expense | (30,000) | (10,000) | +20,000 | +200.0%
Income before tax | 20,000 | 30,000 | −10,000 | −33.3%
Income tax expense | (6,000) | (9,000) | −3,000 | −33.3%
Net income | 14,000 | 21,000 | −7,000 | −33.3%
""", w=W5, cls="small")
         + P("“Interest expense +200%” means the expense tripled. State the convention once, then apply it to every expense line.")),
        ("Step 2 — (a) The comment",
         P("Operating profit improved by 25.0 per cent, but interest expense tripled and wiped out the gain: net income fell 33.3 per cent. "
           "The deterioration comes from financing, not from operations.")),
        ("Step 3 — (b) Comment on a table you did not prepare",
         P("Receivables grew 25 per cent against sales growth of 10 per cent: collection is slowing or credit terms were loosened, and part "
           "of the 12 per cent rise in net income is not yet cash. Inventories grew less than sales, which is favourable. "
           "<b>What we cannot conclude:</b> whether the receivables reflect one large customer, a year-end timing effect or bad debts — "
           "we need the days’ sales in receivables, an ageing schedule and the cash flow statement.")),
    ],
)

d7 = EX("D7", "Horizontal analysis with a sign change", "horizontal",
        P("Below is an extract from the income statement of Sendra NV. Complete the horizontal analysis and write the two-line comment.")
        + T("""
^ | 2025 | 2024
Operating profit | 96,000 | 80,000
Interest expense | (54,000) | (20,000)
Income before tax | 42,000 | 60,000
Income tax expense | (12,600) | (18,000)
Net income | 29,400 | 42,000
""", w=W5, add=CHG, tall=True),
        [L(2)])

d8 = EX("D8", "Read the table, write the comment", "horizontal",
        P("You are handed the following completed horizontal analysis of Alcide Group. No further information is available. Write "
          "the comment, no more than six lines, and state clearly what you cannot conclude.")
        + T("""
^ | Change | Percent
Net sales | +420,000 | +14.0%
Cost of goods sold | +357,000 | +17.0%
Gross profit | +63,000 | +7.0%
Selling expenses | +96,000 | +24.0%
Administrative expenses | −18,000 | −6.0%
Operating profit | −15,000 | −7.5%
Accounts receivable | +198,000 | +33.0%
Inventories | +240,000 | +30.0%
""", w=(50, 25, 25)),
        [L(7, "Comment (six lines) and what you cannot conclude")])

SEC = SECTION(
    "D", "Horizontal and year-to-year change analysis",
    "Amount and percentage changes, the cases where the percentage cannot be computed, and the comment that goes under the table.",
    [
        BLOCK("D.1", "Horizontal analysis of a statement",
              "Change in euro and in per cent against the base year, then the comment.", we1, [d1, d2]),
        BLOCK("D.2", "When the percentage cannot be computed",
              "Zero and negative bases, and the movements a creditor asks about.", we2, [d3, d4]),
        BLOCK("D.3", "Recovering and choosing the base year",
              "Working backwards from a percentage, and why the base changes the story.", we3, [d5, d6]),
        BLOCK("D.4", "Sign changes and the written comment",
              "Expense lines, and commenting on a table without over-reaching.", we4, [d7, d8]),
    ],
)
