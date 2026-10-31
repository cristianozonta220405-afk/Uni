from lib import *

CHAIN = ["NOPAT = Operating income × (1 − t)", "NOA", "RNOA = NOPAT ÷ NOA", "NFE = Interest × (1 − t)", "NFO",
         "NFR = NFE ÷ NFO", "LEV = NFO ÷ Equity", "Spread = RNOA − NFR", "ROCE = RNOA + LEV × Spread", "Check: Net income ÷ Equity"]

# ------------------------------------------------------------------ J.1
we1 = WE(
    "Return on common equity — with and without preferred shares",
    P("<b>(a)</b> Compute ROCE for Nova Spa (net income €182 thousand, equity €800 thousand, no preferred shares; one balance sheet date). "
      "<b>(b)</b> Sole Spa reports net income of €300,000; its equity of €2,000,000 includes €400,000 of 8 per cent preferred stock, "
      "whose dividend was paid in full. Compute ROCE."),
    [
        ("Step 1 — (a) The common shareholders’ return",
         F("ROCE = (Net income − Preferred dividends) ÷ Average common equity")
         + P("Can we calculate the average? No, we can’t — year-end equity is used.")
         + CALC([("ROCE, Nova", "182 ÷ 800", "22.75%")])),
        ("Step 2 — (b) Take the preferred out of both terms",
         CALC([("Preferred dividend", "8% × 400,000", "32,000"),
               ("Earnings to common", "300,000 − 32,000", "268,000"),
               ("Common equity", "2,000,000 − 400,000", "1,600,000"),
               ("ROCE, Sole", "268,000 ÷ 1,600,000", "16.75%"),
               ("The careless answer", "300,000 ÷ 2,000,000", "15.0% ✗")])),
    ],
    comment=P("ROCE measures the return to the <b>ordinary</b> shareholders: preferred dividends leave the numerator and preferred stock leaves the "
              "denominator. Forgetting either understates (or overstates) the return."),
)

j1 = EX("J1", "Return on common equity", "roce",
        P("Compute the return on ordinary shareholders’ equity for Orso and Lince, using the data of exercise G1. Neither "
          "company has preferred shares."),
        [A(BT(["", "Orso", "Lince"], ["Net income", "Equity (year-end — average not available)", "ROCE"], w=(50, 25, 25))),
         L(2)])

j6 = EX("J6", "ROCE with preferred shares", "roce",
        P("Aurelia NV reports net income of €420,000. Its shareholders’ equity of €2,900,000 includes €500,000 of 9 per cent "
          "preferred stock, on which the dividend was declared and paid in full. Compute the return on common equity, and "
          "state what a careless answer would have been."),
        [G(36), L(2)])

# ------------------------------------------------------------------ J.2
we2 = WE(
    "The full disaggregation: ROCE = RNOA + LEV × Spread",
    P("Disaggregate Nova Spa’s ROCE (statements in Section I). All assets except marketable securities, and all current liabilities, are "
      "operating; tax rate 30 per cent; no interest income on the securities; year-end figures."),
    [
        ("Step 1 — The chain, one line at a time",
         CALC([("NOPAT", "300 × (1 − 0.30)", "210"),
               ("NOA", "(1,500 − 50) − 300", "1,150"),
               ("RNOA", "210 ÷ 1,150", "18.26%"),
               ("NFE", "40 × (1 − 0.30)", "28"),
               ("NFO", "400 − 50", "350"),
               ("NFR", "28 ÷ 350", "8.00%"),
               ("LEV", "NFO ÷ Equity = 350 ÷ 800", "0.4375"),
               ("Spread", "RNOA − NFR = 18.26% − 8.00%", "10.26%"),
               ("ROCE", "18.26% + 0.4375 × 10.26% = 18.26% + 4.49%", "22.75%"),
               ("Check", "Net income ÷ Equity = 182 ÷ 800  (and NOPAT − NFE = 210 − 28 = 182)", "22.75% ✓")], w=(14, 68, 18))),
    ],
    comment=P("Operations earn 18.3 per cent on net operating assets; debt costs 8.0 per cent after tax. The positive spread of 10.3 points, "
              "applied to 0.44 euros of net debt per euro of equity, adds 4.5 points: financial leverage is working for the shareholders."),
)

j2 = EX("J2", "Full disaggregation — Orso", "roce",
        P("Disaggregate Orso’s ROCE into its operating and non-operating components, using ROCE = RNOA + (LEV × Spread). "
          "Assume all assets except marketable securities, and all current liabilities, are operating, and a 30 per cent tax rate. "
          "Comment on the use of financial leverage."),
        [A(BT(["Step", "Working", "Result"], CHAIN, w=(34, 46, 20))), L(3)])

j3 = EX("J3", "Full disaggregation — Lince", "roce",
        P("Repeat the disaggregation for Lince Srl and compare the two leverage stories."),
        [A(BT(["Step", "Working", "Result"], CHAIN, w=(34, 46, 20))), L(3, "The two leverage stories")])

# ------------------------------------------------------------------ J.3
we3 = WE(
    "When the spread turns negative",
    P("Mira Spa, € thousands, year-end figures. Year A: NOPAT 120, NOA 1,000, NFE 24, NFO 400, equity 600. Year B: NOPAT 60, NOA 1,000, "
      "NFE 32, NFO 400, equity 600. Disaggregate ROCE for both years; then state the rule."),
    [
        ("Step 1 — Two columns of the same chain",
         T("""
^ | Year A | Year B
RNOA = NOPAT ÷ NOA | 120 ÷ 1,000 = 12.0% | 60 ÷ 1,000 = 6.0%
NFR = NFE ÷ NFO | 24 ÷ 400 = 6.0% | 32 ÷ 400 = 8.0%
LEV = NFO ÷ Equity | 400 ÷ 600 = 0.667 | 0.667
Spread = RNOA − NFR | +6.0% | −2.0%
LEV × Spread | +4.0% | −1.33%
**ROCE | 16.0% | 4.67%
Check: (NOPAT − NFE) ÷ Equity | 96 ÷ 600 = 16.0% | 28 ÷ 600 = 4.67%
""", w=(36, 32, 32), cls="small")),
        ("Step 2 — What happened",
         P("Operations halved their return (12 → 6 per cent) while the cost of debt rose (6 → 8 per cent). The spread turned negative, so the "
           "same leverage that added 4.0 points in Year A now <b>subtracts</b> 1.3 points: an unlevered twin would earn 6.0 per cent, more than Mira.")),
    ],
    comment=RULE("Leverage magnifies: it raises ROCE when RNOA exceeds the net financial rate and lowers it when RNOA falls below it — "
                 "ROCE = RNOA + LEV × (RNOA − NFR).", "The rule in one sentence"),
)

j4 = EX("J4", "When the spread turns negative", "roce",
        P("Using the Vela Group statements of exercise G5 and a tax rate of 40 per cent, disaggregate ROCE for 2025 and for "
          "2024 on year-end figures. Explain what happened between the two years."),
        [A(BT(["Step", "2025", "2024"], CHAIN, w=(40, 30, 30))), L(3, "What happened")])

j8 = EX("J8", "Leverage that destroys value", "roce",
        P("Two companies have identical operating businesses, each earning an RNOA of 7.0 per cent. Company U is financed "
          "entirely by equity. Company L has net financial obligations equal to 1.5 times its equity, at an after-tax net financial "
          "rate of 9.0 per cent.")
        + REQ(["Compute ROCE for both.",
               "Compute what Company L’s ROCE would be if its RNOA rose to 12.0 per cent, leverage and NFR unchanged.",
               "State the rule in one sentence."]),
        [G(40), L(2, "The rule")])

# ------------------------------------------------------------------ J.4
we4 = WE(
    "Disaggregation from long-term assets and working capital",
    P("Fiume Srl: revenue 3,000; operating income 360; interest expense 50; pre-tax income 310; income taxes (40%) 124; net income 186. "
      "Balance sheet: long-term assets 1,400; working capital 600; total liabilities 700; total shareholders’ equity 1,300. "
      "Long-term assets and working capital are operating; tax rate 40 per cent."),
    [
        ("Step 1 — Read the condensed balance sheet",
         P("Working capital is already <b>net</b> of current liabilities, so long-term assets + working capital = NOA = 2,000, and the "
           "liabilities shown (700) are the financing ones = NFO. Check: NOA 2,000 = NFO 700 + Equity 1,300 ✓.")),
        ("Step 2 — The chain",
         CALC([("NOPAT", "360 × (1 − 0.40)", "216"),
               ("RNOA", "216 ÷ 2,000", "10.80%"),
               ("NFE", "50 × (1 − 0.40)", "30"),
               ("NFR", "30 ÷ 700", "4.29%"),
               ("LEV", "700 ÷ 1,300", "0.538"),
               ("Spread", "10.80% − 4.29%", "6.51%"),
               ("ROCE", "10.80% + 0.538 × 6.51% = 10.80% + 3.51%", "14.31%"),
               ("Check", "186 ÷ 1,300", "14.31% ✓")], w=(14, 68, 18))),
    ],
    comment=P("ROCE of 14.3 per cent: 10.8 points come from operations and 3.5 from leverage, which works because debt costs 4.3 per cent "
              "after tax against an operating return of 10.8."),
)

j5 = EX("J5", "Disaggregation from summary data", "roce",
        P("Financial information for Prisma Spa follows. Calculate the ROCE and then its disaggregation ROCE = RNOA + "
          "Leverage × Spread. Assume long-term assets and working capital are operating and a 40 per cent tax rate.")
        + T("""
^Income statement data | 2025 | Balance sheet data | 2025
Revenue | 2,500 | Long-term assets | 700
Operating income | 300 | Working capital | 500
Interest expense | 40 | Total liabilities | 320
Pre-tax income | 260 | Total shareholders’ equity | 880
Income taxes | 104 | |
Net income | 156 | |
""", w=(34, 16, 34, 16)),
        [A(BT(["Step", "Working", "Result"], ["ROCE = Net income ÷ Equity"] + CHAIN[:-1], w=(34, 46, 20)))])

j9 = EX("J9", "Disaggregation from long-term assets and working capital", "roce",
        P("Montaldo Srl reports revenue of €5,000, operating income of €450, interest expense of €60, income taxes of €156 "
          "and net income of €234. Its long-term assets are €2,000, its working capital €600, its total liabilities €900 and its "
          "equity €1,700. Assume long-term assets and working capital are operating. Compute RNOA, ROCE and the full disaggregation."),
        [G(14, "Tax rate implied"), A(BT(["Step", "Working", "Result"], CHAIN, w=(34, 46, 20)))])

# ------------------------------------------------------------------ J.5
we5 = WE(
    "The alternate view of ROCE; writing the return analysis",
    P("<b>(a)</b> Sole Spa (example J.1) reports sales of €4,000,000, average total assets of €3,200,000 and common equity of €1,600,000. "
      "Verify ROCE = Adjusted profit margin × Asset turnover × Leverage. <b>(b)</b> Write the return section of a note on Nova Spa."),
    [
        ("Step 1 — (a) Three ratios that multiply back to ROCE",
         CALC([("Adjusted profit margin", "(Net income − Pref. div.) ÷ Sales = 268,000 ÷ 4,000,000", "6.70%"),
               ("Asset turnover", "Sales ÷ Average total assets = 4,000,000 ÷ 3,200,000", "1.25x"),
               ("Leverage", "Average total assets ÷ Average common equity = 3,200,000 ÷ 1,600,000", "2.00"),
               ("ROCE", "6.70% × 1.25 × 2.00", "16.75% ✓")], w=(24, 60, 16))
         + P("<b>Difference in purpose.</b> The alternate view mixes operating and financing items (net income after interest, total assets "
             "including financial assets): it tells you <i>how much</i> margin, turnover and leverage there is. RNOA + LEV × Spread separates "
             "the two activities and tells you <i>whether</i> leverage creates value.")),
        ("Step 2 — (b) A model return section (ten lines at most)",
         P("<i>Nova earned a ROCE of 22.8 per cent. Of this, 18.3 points come from operations (RNOA), driven by a 10.5 per cent operating margin "
           "and a turnover of 1.74 times; 4.5 points come from financial leverage. Net debt is 0.44 times equity and costs 8.0 per cent after "
           "tax, so the spread of 10.3 points is comfortably positive and leverage is creating value. The operating return is the engine and "
           "the turnover its weak spot. <b>Recommendation to management:</b> reduce the 72 days of inventory to lift turnover; additional debt "
           "remains value-creating only while RNOA stays above the 8 per cent cost of borrowing.</i>")),
    ],
)

j7 = EX("J7", "The alternate view of the disaggregation", "roce",
        [P("Continuing from exercise J6, Aurelia reports sales of €6,000,000 and average total assets of €4,000,000. Verify the "
           "alternate view of the ROCE disaggregation"),
         F("ROCE = Adjusted profit margin × Asset turnover × Leverage") + P("and say how it differs in purpose from the RNOA + LEV × Spread version.")],
        [A(BT(["Component", "Working", "Result"], ["Adjusted profit margin", "Asset turnover", "Leverage", "ROCE (product)"], w=(30, 50, 20))),
         L(3, "Difference in purpose")])

j10 = EX("J10", "Write the return analysis", "roce",
         P("Using the Vela Group disaggregation of exercise J4, write the return section of an equity research note: ten lines at "
           "most, ending with a recommendation to management."),
         [L(11, "Return analysis — Vela Group")])

SEC = SECTION(
    "J", "Return on common equity and its disaggregation",
    "ROCE, the six-line chain that produces LEV and Spread, and the cases where leverage works against the shareholder.",
    [
        BLOCK("J.1", "Return on common equity", "Net income to ordinary shareholders over their equity — and the preferred trap.", we1, [j1, j6]),
        BLOCK("J.2", "ROCE = RNOA + LEV × Spread", "The full chain from NOPAT to ROCE, with the check.", we2, [j2, j3]),
        BLOCK("J.3", "Negative spread", "When leverage subtracts from the shareholders’ return.", we3, [j4, j8]),
        BLOCK("J.4", "Disaggregation from summary data", "Long-term assets plus working capital as NOA.", we4, [j5, j9]),
        BLOCK("J.5", "The alternate view; the written return analysis", "Margin × turnover × leverage, and the research-note paragraph.", we5, [j7, j10]),
    ],
)
