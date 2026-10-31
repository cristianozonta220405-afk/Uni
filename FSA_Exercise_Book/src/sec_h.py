from lib import *

SOLV5 = ["Total debt ratio", "Total debt to equity", "Long-term debt to equity", "Short-term debt to total debt", "Times interest earned"]

# ------------------------------------------------------------------ H.1
we1 = WE(
    "The four capital structure ratios — from the balance sheet and from percentages",
    P("<b>(a)</b> Ferro Spa: total assets €2,000,000; current liabilities €400,000; bonds payable (long-term) €600,000; equity €1,000,000. "
      "Compute the four capital structure ratios. <b>(b)</b> Show the same ratios from a common-size financing side: current liabilities "
      "20%, long-term debt 30%, equity 50%."),
    [
        ("Step 1 — (a) Four ratios, two families",
         CALC([("Total debt ratio", "Total liabilities ÷ Total assets = 1,000,000 ÷ 2,000,000", "50.0%"),
               ("Total debt to equity", "Total liabilities ÷ Equity = 1,000,000 ÷ 1,000,000", "1.00"),
               ("Long-term debt to equity", "Non-current liabilities ÷ Equity = 600,000 ÷ 1,000,000", "0.60"),
               ("Short-term debt to total debt", "Current liabilities ÷ Total liabilities = 400,000 ÷ 1,000,000", "40.0%")],
              w=(28, 56, 16))),
        ("Step 2 — (b) Size cancels: the percentages give the ratios directly",
         CALC([("Total debt ratio", "(20 + 30) ÷ 100", "50.0%"),
               ("Total debt to equity", "50 ÷ 50", "1.00"),
               ("Long-term debt to equity", "30 ÷ 50", "0.60"),
               ("Short-term debt to total debt", "20 ÷ 50", "40.0%")], w=(28, 56, 16))
         + RULE("Preferred stock is normally counted as equity; if it is redeemable or has a fixed maturity, treat it as debt. "
                "Either way, state the choice.", "Note")),
    ],
    comment=P("Half of Ferro’s assets are financed by creditors, one euro of debt per euro of equity; 40 per cent of the debt falls due within a year."),
)

h1 = EX("H1", "The four capital structure ratios", "solvency",
        P("Using the statements of Orso Spa and Lince Srl from exercise G1, compute the total debt ratio, the total debt to "
          "equity ratio, the long-term debt to equity ratio and the short-term debt to total debt ratio for both companies."),
        [A(BT(["Ratio", "Formula", "Orso", "Lince"], SOLV5[:4], w=(28, 36, 18, 18))), G(26)])

h7 = EX("H7", "Solvency from a common-size statement", "solvency",
        P("Only the common-size financing side of Marenco Spa is available. Total liabilities and equity are €3,000,000. Compute "
          "the four capital structure ratios directly from the percentages.")
        + T("""
^ | %
Current liabilities | 18.0%
Long-term debt | 27.0%
Preferred stock | 10.0%
Common stock | 32.0%
Paid-in capital | 3.0%
Retained earnings | 10.0%
""", w=(70, 30)),
        [A(BT(["Ratio", "From the percentages", "Result"], SOLV5[:4], w=(32, 46, 22))), L(2, "How you treated preferred stock")])

# ------------------------------------------------------------------ H.2
we2 = WE(
    "Times interest earned by both routes, and the trap",
    P("Gemma Spa reports operating income of €300,000, interest expense of €60,000, income before tax of €240,000, tax of €72,000 and "
      "net income of €168,000. <b>(a)</b> Compute times interest earned by both routes. <b>(b)</b> Repeat if the year also included a "
      "€90,000 gain on the sale of a subsidiary (tax 30 per cent on the higher income)."),
    [
        ("Step 1 — (a) Two routes to the same numerator, earnings before interest and taxes",
         CALC([("Route 1", "(Net income + Tax + Interest) ÷ Interest = (168 + 72 + 60) ÷ 60", "5.0x"),
               ("Route 2", "Operating income ÷ Interest = 300 ÷ 60", "5.0x")], w=(16, 68, 16))
         + P("Limitation: the ratio treats interest as the <b>only fixed charge</b> (it ignores lease payments and principal repayments) "
             "and uses accrual earnings, not cash.")),
        ("Step 2 — (b) A one-off gain separates the two routes",
         CALC([("Income before tax", "300 + 90 − 60", "330"),
               ("Tax 30% / Net income", "99 / 231", ""),
               ("Route 1", "(231 + 99 + 60) ÷ 60", "6.5x"),
               ("Route 2", "300 ÷ 60", "5.0x")], w=(24, 60, 16))),
    ],
    comment=P("Put <b>5.0x</b> in a credit report: interest is paid year after year out of recurring operating income, and the gain on the "
              "subsidiary will not come back. Route 1 flatters coverage whenever net income contains non-operating items."),
)

h2 = EX("H2", "Times interest earned, by both routes", "solvency",
        P("Compute the times interest earned ratio for Orso and Lince by both of the routes given in the formula, and show that "
          "they agree. Then state the limitation of the ratio named on the chapter 10 slide."),
        [A(BT(["Route", "Orso", "Lince"], ["(Net income + Tax + Interest) ÷ Interest", "Operating income ÷ Interest"], w=(50, 25, 25))),
         G(16), L(2, "Limitation")])

h8 = EX("H8", "A trap in times interest earned", "solvency",
        P("Fenice Srl reports operating income of €480,000, a gain on the disposal of a subsidiary of €220,000, interest expense "
          "of €120,000, tax of €174,000 and net income of €406,000. Compute times interest earned by both routes, explain the "
          "discrepancy and say which figure you would put in a credit report."),
        [G(30), L(3)])

# ------------------------------------------------------------------ H.3
we3 = WE(
    "The full solvency set over two years",
    P("Lupo Spa, in € thousands. 2025: total assets 5,000; current liabilities 1,000; long-term debt 1,500; equity 2,500; operating income "
      "600; interest 150. 2024: total assets 4,000; current liabilities 900; long-term debt 1,100; equity 2,000; operating income 560; "
      "interest 110. Compute the five solvency ratios and comment on the direction of travel."),
    [
        ("Step 1 — One column per year",
         T("""
^Ratio | Working 2025 | 2025 | 2024
Total debt ratio | 2,500 ÷ 5,000 | 50.0% | 50.0%
Total debt to equity | 2,500 ÷ 2,500 | 1.00 | 1.00
Long-term debt to equity | 1,500 ÷ 2,500 | 0.60 | 0.55
Short-term debt to total debt | 1,000 ÷ 2,500 | 40.0% | 45.0%
Times interest earned | 600 ÷ 150 | 4.0x | 5.1x
""", w=(34, 30, 18, 18), cls="small")
         + P("2024 workings: 2,000 ÷ 4,000; 2,000 ÷ 2,000; 1,100 ÷ 2,000; 900 ÷ 2,000; 560 ÷ 110 = 5.09.")),
    ],
    comment=P("The overall weight of debt is unchanged at half of assets, and the mix has moved towards long-term debt — less refinancing "
              "risk. But coverage fell from 5.1 to 4.0 times because interest grew 36 per cent against 7 per cent for operating income: "
              "the new debt is expensive. Stable structure, weaker capacity to service it."),
)

h3 = EX("H3", "Full solvency set, two companies", "solvency",
        P("Calculate the five solvency ratios for Orso and Lince and say which company a bondholder should prefer."),
        [A(BT(["Ratio", "Orso", "Lince"], SOLV5, w=(50, 25, 25))), G(20), L(3, "Which one a bondholder should prefer")])

h4 = EX("H4", "Solvency over two years", "solvency",
        P("Using the Vela Group statements of exercise G5, compute the five solvency ratios for 2025 and 2024 and comment "
          "on the direction of travel."),
        [A(BT(["Ratio", "2025", "2024"], SOLV5, w=(50, 25, 25))), G(24), L(3)])

# ------------------------------------------------------------------ H.4
we4 = WE(
    "A financing decision through the ratios; the tax shield of interest",
    P("<b>(a)</b> Ponte Srl (€ thousands): current assets 600, current liabilities 400, long-term debt 200, total assets 1,500, equity 900, "
      "operating income 180, interest 20. It issues 150 of bonds at 8 per cent and uses the cash to pay 150 of accounts payable. "
      "Show the effect on the ratios.")
    + P("<b>(b)</b> Two identical companies earn income before interest and taxes of €400; Leva Spa has €2,000 of 8 per cent debt, Piana Spa none. "
        "Tax rate 30 per cent. Compare the total return to all security holders."),
    [
        ("Step 1 — (a) Before and after",
         T("""
^Ratio | Before | After | Why
Current ratio | 600 ÷ 400 = 1.50 | 600 ÷ 250 = 2.40 | cash in and out; CL −150
Total debt ratio | 600 ÷ 1,500 = 40.0% | 600 ÷ 1,500 = 40.0% | total debt unchanged
Long-term debt to equity | 200 ÷ 900 = 0.22 | 350 ÷ 900 = 0.39 | +150 bonds
Short-term to total debt | 400 ÷ 600 = 66.7% | 250 ÷ 600 = 41.7% | mix lengthens
Times interest earned | 180 ÷ 20 = 9.0x | 180 ÷ 32 = 5.6x | +12 interest (8% × 150)
""", w=(26, 24, 24, 26), cls="small")),
        ("Step 2 — (b) Interest is deductible; dividends are not",
         T("""
^ | Leva (debt) | Piana (no debt)
Income before interest and taxes | 400 | 400
Interest (8% × 2,000) | (160) | —
Income before tax | 240 | 400
Tax 30% | (72) | (120)
Net income to shareholders | 168 | 280
Interest to lenders | 160 | —
**Total return to all security holders | 328 | 280
""", w=(50, 25, 25), cls="small")),
    ],
    comment=P("(a) Liquidity improves and total leverage is unchanged, but the company swaps free supplier credit for interest-bearing debt, so "
              "coverage falls. (b) Leva’s holders receive 48 more: the tax saved on interest, 30% × 160. Debt is cheaper than it looks after tax."),
)

h5 = EX("H5", "Effect of a new bond issue", "solvency",
        P("Orso Spa is considering issuing €300,000 of ten-year bonds at 7 per cent and using the proceeds to repay €300,000 "
          "of accounts payable. Using the data of exercise G1, and assuming the operating income and the tax rate are "
          "unchanged, compute the effect on the current ratio, the total debt ratio, the long-term debt to equity ratio, the short-"
          "term debt to total debt ratio and times interest earned."),
        [A(BT(["Ratio", "Before", "After"],
              ["Current ratio", "Total debt ratio", "Long-term debt to equity", "Short-term debt to total debt", "Times interest earned"],
              w=(40, 30, 30))),
         G(26), L(2)])

h6 = EX("H6", "Tax deductibility of interest", "solvency",
        P("Two identical companies each earn income before interest and taxes of €250. Risky Spa is financed with €1,000 of 10 "
          "per cent debt; Safety Spa has no debt. The tax rate is 40 per cent. Prepare the comparison that shows the total return "
          "to all security holders, and state the conclusion."),
        [A(BT(["", "Risky Spa", "Safety Spa"],
              ["Income before interest and taxes", "Interest", "Income before tax", "Tax (40%)", "Net income", "Interest to lenders",
               "Total return to all security holders"], w=(50, 25, 25))),
         L(2, "Conclusion")])

# ------------------------------------------------------------------ H.5
we5 = WE(
    "Working back from the ratios; when liquidity and solvency disagree",
    P("<b>(a)</b> Total assets are €5,000,000, the total debt ratio is 40 per cent, short-term debt to total debt 30 per cent, times interest "
      "earned 6.0, and the average interest rate on all debt 5 per cent. Recover the balance sheet blocks and the income figures.")
    + P("<b>(b)</b> Over two years a company’s current ratio went from 1.4 to 1.8 and its acid test from 0.8 to 1.0, while its total debt ratio "
        "rose from 45 to 58 per cent and times interest earned fell from 6.0 to 3.2. Write the conclusion."),
    [
        ("Step 1 — (a) Peel the ratios one at a time",
         CALC([("Total liabilities", "40% × 5,000,000", "2,000,000"),
               ("Current liabilities", "30% × 2,000,000", "600,000"),
               ("Non-current liabilities", "2,000,000 − 600,000", "1,400,000"),
               ("Total equity", "5,000,000 − 2,000,000", "3,000,000"),
               ("Interest expense", "5% × 2,000,000", "100,000"),
               ("Operating income", "6.0 × 100,000", "600,000"),
               ("Total debt to equity", "2,000,000 ÷ 3,000,000", "0.67"),
               ("Long-term debt to equity", "1,400,000 ÷ 3,000,000", "0.47")], w=(28, 54, 18))),
        ("Step 2 — (b) A model conclusion",
         P("<i>Liquidity has improved: the current ratio rose from 1.4 to 1.8 and the acid test reached 1.0. Solvency has deteriorated: debt now "
           "finances 58 per cent of assets and coverage has almost halved to 3.2 times. The two diverge because the company has raised long-term "
           "debt and kept part of it in current assets — it is liquid today because it has borrowed for tomorrow. We would monitor times "
           "interest earned, the maturity schedule of the new debt and whether operating income grows enough to service it.</i>")),
    ],
)

h9 = EX("H9", "Working backwards from the ratios", "solvency",
        P("Dorelli NV discloses a total debt ratio of 60 per cent, a short-term debt to total debt ratio of 35 per cent and times "
          "interest earned of 4.5. Total assets are €8,000,000 and the average interest rate on all debt is 6 per cent.")
        + REQ(["Compute total liabilities, current liabilities, non-current liabilities and total equity.",
               "Compute interest expense and operating income.",
               "Compute the total debt to equity and the long-term debt to equity ratios."]),
        [G(62)])

h10 = EX("H10", "Liquidity and solvency can point opposite ways", "solvency",
         P("Using everything computed for Vela Group in exercises G5 and H4, write the eight-line conclusion of a credit analysis: "
           "state the direction of liquidity, the direction of solvency, the reason they diverge, and what you would monitor."),
         [L(9, "Conclusion of the credit analysis")])

SEC = SECTION(
    "H", "Solvency and capital structure",
    "The four structure ratios, earnings coverage, and the cases where the solvency answer contradicts the liquidity answer.",
    [
        BLOCK("H.1", "The capital structure ratios", "From the balance sheet or straight from a common-size statement.", we1, [h1, h7]),
        BLOCK("H.2", "Times interest earned", "Both routes, why they agree, and when they do not.", we2, [h2, h8]),
        BLOCK("H.3", "The full solvency set", "Five ratios, two columns, one direction of travel.", we3, [h3, h4]),
        BLOCK("H.4", "Financing decisions and the tax shield", "Before-and-after ratios, and why interest costs less than it seems.", we4, [h5, h6]),
        BLOCK("H.5", "Back from the ratios; liquidity against solvency", "Recovering the blocks, and the written conclusion.", we5, [h9, h10]),
    ],
)
