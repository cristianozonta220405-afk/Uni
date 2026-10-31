from lib import *
from sec_k import CFS


def Q(n, marks, text):
    return f'<div class="qh"><b>Question {n}</b> <span class="mk">({marks} marks)</span></div>' + text


PAPER = '<div class="paper">{}</div>'

# ------------------------------------------------------------------ X.1
we1 = WE(
    "How to sit a paper — a solved mini paper (30 minutes, 30 marks)",
    RULE("Minutes per question = marks ÷ total marks × time allowed. In a 90-minute, 100-mark paper a 25-mark question gets about "
         "22 minutes; keep five minutes at the end to check the totals. Answer the cheap questions first, but in the order printed on your sheet.",
         "Time budget")
    + P("<b>Q1 (8 marks)</b> Classify: prepaid rent; bonds due in 2031; treasury shares; customer deposits received. "
        "<b>Q2 (12 marks)</b> A machine bought on 1 January Year 1 for €120,000, residual value €12,000, 6 years straight-line, is sold at the "
        "end of Year 3 for €60,000: plan, gain or loss, and where it goes in the cash flow statement. "
        "<b>Q3 (10 marks)</b> Net income €50,000; depreciation €15,000; receivables up €8,000; inventory down €4,000; payables down €3,000; "
        "equipment bought for €30,000 cash; dividends paid €12,000. Compute cash from operations and free cash flow."),
    [
        ("Q1 — one word and one reason each",
         T("""
^Item | Answer
Prepaid rent | <span class="ans">Current asset</span> — service received within twelve months
Bonds due in 2031 | <span class="ans">Non-current liability</span> — financing
Treasury shares | <span class="ans">Contra-equity</span> — deducted from equity
Customer deposits received | <span class="ans">Current liability</span> — operating, settled in goods
""", w=(36, 64), cls="small")),
        ("Q2 — plan, disposal, cash flow",
         T("""
^Year | Depreciation | Accumulated | Book value
Year 1 | 18,000 | 18,000 | 102,000
Year 2 | 18,000 | 36,000 | 84,000
Year 3 | 18,000 | 54,000 | 66,000
""", w=(25, 25, 25, 25), cls="small")
         + P("Annual charge (120,000 − 12,000) ÷ 6 = 18,000. Loss = 60,000 − 66,000 = <span class='ans'>€6,000</span>: added back in "
             "operating activities; the €60,000 proceeds are an investing inflow.")),
        ("Q3 — the indirect method in one line",
         CALC([("Cash from operations", "50,000 + 15,000 − 8,000 + 4,000 − 3,000", "58,000"),
               ("Free cash flow", "58,000 − 30,000 − 12,000", "16,000")])),
    ],
    comment=P("Every answer: formula, numbers, result with its unit, one line of meaning. Marks are lost on missing steps far more than on arithmetic."),
)

x1 = EX("X1", "Paper 1 — accounting foundations and comparative analysis", "exam",
        [P("<b>Time allowed 90 minutes · Total 100 marks · four questions, all compulsory</b>"),
         Q(1, 20, P("Classify each item as a current asset, non-current asset, current liability, non-current liability or equity.")
           + T("""
^Item | Classification | Item | Classification
Advances received from customers | __ | Goodwill | __
Current portion of long-term borrowings | __ | Treasury shares | __
Accumulated depreciation | __ | Marketable securities | __
Deferred tax liabilities, long-term | __ | Prepaid insurance | __
Notes payable due in eight months | __ | Construction in progress | __
""", w=(30, 20, 30, 20), tall=True)),
         Q(2, 25, P("The income statement of Prato Srl is presented in T-format. Rewrite it in two-step format.")
           + T("""
^Left side / debit | | Right side / credit |
Cost of goods sold | 540 | Revenue | 870
SG&A expenses | 180 | Gain on sale of equipment | 15
Depreciation expense | 60 | |
Interest expense | 24 | |
Income tax expense | 29 | |
""", w=(34, 14, 38, 14))),
         A(BT(["Prato Srl — two-step income statement", "€"], [""] * 11, w=(75, 25))),
         Q(3, 30, P("On 1 January Year 1 Prato purchased a machine for €240,000, with an estimated useful life of six years and a residual "
                    "value of €24,000. The company uses the straight-line method.")
           + REQ(["Prepare the depreciation plan for the first four years, showing the annual expense, accumulated depreciation and book value.",
                  "The machine is sold at the end of Year 4 for €105,000. Compute the gain or loss on disposal.",
                  "State where the gain or loss and the proceeds appear in the statement of cash flows."])),
         A(BT(["Year", "Annual depreciation", "Accumulated depreciation", "Book value"],
              ["Year 1", "Year 2", "Year 3", "Year 4"], w=(25, 25, 25, 25)), "1."),
         G(22, "2."), L(2, "3."),
         Q(4, 25, P("Prepare a horizontal analysis and a common-size analysis of the following condensed income statements, and "
                    "comment in no more than six lines.")
           + T("""
^ | 2025 | 2024 | Change € | Change % | % 2025 | % 2024
Net sales | 870 | 750 | __ | __ | __ | __
Cost of goods sold | 540 | 450 | __ | __ | __ | __
Gross profit | 330 | 300 | __ | __ | __ | __
Operating expenses | 240 | 195 | __ | __ | __ | __
Operating profit | 90 | 105 | __ | __ | __ | __
""", w=(25, 11, 11, 13, 13, 13, 14), tall=True)),
         L(6, "Comment")],
        [])

x2 = EX("X2", "Paper 2 — cash flow analysis", "exam",
        [P("<b>Time allowed 90 minutes · Total 100 marks · four questions, all compulsory</b>"),
         Q(1, 55, P("The comparative statements of financial position of Gallo Spa follow.")
           + T("""
^ | 2025 | 2024
##Assets
Cash | 74,000 | 58,000
Accounts receivable | 136,000 | 118,000
Inventory | 162,000 | 185,000
Prepaid expenses | 12,000 | 9,000
Equipment | 640,000 | 560,000
Accumulated depreciation | (214,000) | (188,000)
**Total assets | 810,000 | 742,000
##Equity and liabilities
Accounts payable | 118,000 | 134,000
Accrued liabilities | 26,000 | 21,000
Long-term note payable | 160,000 | 120,000
Share capital | 340,000 | 310,000
Retained earnings | 166,000 | 157,000
**Total equity and liabilities | 810,000 | 742,000
""", w=(34, 15, 15, 16, 20), add=["Change", "Classification"], tall=True)),
         P("Additional information. Net income for 2025 was €69,000. Equipment costing €48,000 with accumulated depreciation of €31,000 was "
           "sold for €22,000. Equipment costing €40,000 was acquired by issuing a long-term note to the supplier; all other equipment purchases "
           "were for cash. Shares were issued for cash. Dividends were declared and paid.")
         + REQ(["Prepare the comparative statement with the change and the classification of each difference (columns above).",
                "Prepare the statement of cash flows for 2025, indirect method, with the schedule of non-cash activities."]),
         G(26, "Gain, depreciation, purchases, dividends"),
         CFS(9, 2, 4, noncash=1),
         Q(2, 15, P("Compute free cash flow and interpret it in three lines.")),
         G(16), L(3),
         Q(3, 20, P("Net income is €69,000 and net cash provided by operating activities is €112,000. Explain the difference item by item "
                    "and state what each of the two figures measures.")),
         A(BT(["Item", "€"], ["Net income"] + [""] * 7 + ["Net cash provided by operating activities"], w=(75, 25))),
         L(3, "What each figure measures"),
         Q(4, 10, P("State, with one line of reasoning each, where the following appear in a statement of cash flows.")
           + T("""
^Item | Where, and why
Interest paid | __
Dividends paid | __
Dividends received | __
Proceeds from issuing bonds | __
Conversion of bonds into ordinary shares | __
""", w=(34, 66), tall=True))],
        [])

# ------------------------------------------------------------------ X.2
CORALLO = T("""
^Corallo Srl — income statement | € 000 | Balance sheet | € 000
Sales | 1,000 | Cash | 50
Cost of goods sold | 600 | Marketable securities | 20
Selling and administrative | 250 | Accounts receivable | 130
<b>Operating income</b> | <b>150</b> | Inventory | 150
Interest expense | 30 | Fixed assets, net | 650
<b>Income before tax</b> | <b>120</b> | <b>Total assets</b> | <b>1,000</b>
Income tax (30%) | 36 | Accounts payable | 150
<b>Net income</b> | <b>84</b> | Income tax payable | 50
 | | Bonds payable | 300
 | | Equity | 500
""", w=(30, 14, 42, 14), cls="small")

we2 = WE(
    "Credit and profitability on one set of statements — a solved mini paper",
    P("Corallo Srl. Assume all cost of sales items are purchased, marketable securities are financial, all current liabilities operating, "
      "tax 30 per cent; one balance sheet date.") + CORALLO,
    [
        ("Q1 — Liquidity",
         CALC([("Current ratio", "350 ÷ 200", "1.75"),
               ("Acid test", "(50 + 20 + 130) ÷ 200", "1.00"),
               ("Cash ratio", "(50 + 20) ÷ 200", "0.35"),
               ("Days’ sales in receivables", "130 ÷ (1,000 ÷ 360)", "46.8"),
               ("Days’ sales in inventory", "150 ÷ (600 ÷ 360)", "90.0"),
               ("Days’ purchases in payables", "150 ÷ (600 ÷ 360)", "90.0"),
               ("Net trade cycle", "46.8 + 90.0 − 90.0", "46.8 days")], w=(30, 52, 18))),
        ("Q2 — Solvency",
         CALC([("Total debt ratio", "500 ÷ 1,000", "50.0%"), ("Total debt to equity", "500 ÷ 500", "1.00"),
               ("Long-term debt to equity", "300 ÷ 500", "0.60"), ("Short-term to total debt", "200 ÷ 500", "40.0%"),
               ("Times interest earned", "150 ÷ 30", "5.0x")], w=(30, 52, 18))),
        ("Q3 — Returns, with every intermediate figure",
         CALC([("NOPAT", "150 × 0.70", "105"), ("NOA", "(1,000 − 20) − 200", "780"),
               ("NFO / Equity / check", "300 − 20 = 280; 280 + 500 = 780", "✓"),
               ("Operating profit margin", "105 ÷ 1,000", "10.5%"), ("Operating asset turnover", "1,000 ÷ 780", "1.28x"),
               ("RNOA", "105 ÷ 780", "13.46%"), ("NFE / NFR", "30 × 0.70 = 21; 21 ÷ 280", "7.50%"),
               ("LEV / Spread", "280 ÷ 500 = 0.56; 13.46% − 7.50%", "5.96%"),
               ("ROCE", "13.46% + 0.56 × 5.96% = 84 ÷ 500", "16.80% ✓")], w=(30, 52, 18))),
    ],
    comment=P("Leverage starts to destroy value when RNOA falls below the 7.5 per cent net financial rate. Model memo line: <i>“Liquid enough "
              "(acid test 1.0), moderately geared (debt 50 per cent of assets, coverage 5 times) and profitably levered (spread +6 points): "
              "approve, with a covenant on times interest earned.”</i>"),
)

ADRIA = T("""
^Income statement | Adria | Tirrena
Sales | 2,400,000 | 1,800,000
Cost of goods sold | 1,560,000 | 1,296,000
Selling and administrative expense | 480,000 | 324,000
Operating income | 360,000 | 180,000
Interest expense | 72,000 | 90,000
Income before taxes | 288,000 | 90,000
Income tax expense | 86,400 | 27,000
**Net income | 201,600 | 63,000
""", w=(56, 22, 22))

ADRIA_BS = T("""
^Balance sheet | Adria | Tirrena
Cash | 90,000 | 36,000
Marketable securities | 30,000 | 0
Accounts receivable, net | 300,000 | 252,000
Inventory | 420,000 | 324,000
Total current assets | 840,000 | 612,000
Fixed assets, net | 1,560,000 | 1,188,000
**Total assets | 2,400,000 | 1,800,000
Accounts payable | 360,000 | 396,000
Income taxes payable | 60,000 | 24,000
Total current liabilities | 420,000 | 420,000
Bonds payable | 780,000 | 720,000
Total liabilities | 1,200,000 | 1,140,000
Total equity | 1,200,000 | 660,000
**Total equity and liabilities | 2,400,000 | 1,800,000
""", w=(56, 22, 22))

x3 = EX("X3", "Paper 3 — credit analysis", "exam",
        [P("<b>Time allowed 90 minutes · Total 100 marks · four questions, all compulsory</b>")
         + P("You are a lending officer at a commercial bank. Two companies have applied for a three-year term loan. Their "
             "statements at 31 December 2025 are reproduced below, in euro.") + ADRIA,
         ADRIA_BS,
         Q(1, 35, P("Compute the following liquidity ratios for both companies: current ratio, acid test ratio, cash ratio, days’ sales in "
                    "accounts receivable, days’ sales in inventory, days’ purchases in accounts payable. Assume all cost of sales items are purchased.")),
         A(BT(["Ratio", "Adria", "Tirrena"],
              ["Current ratio", "Acid test ratio", "Cash ratio", "Days’ sales in accounts receivable", "Days’ sales in inventory",
               "Days’ purchases in accounts payable"], w=(52, 24, 24))),
         G(24),
         Q(2, 30, P("Compute the total debt ratio, total debt to equity, long-term debt to equity, short-term debt to total debt and times "
                    "interest earned for both companies.")),
         A(BT(["Ratio", "Adria", "Tirrena"],
              ["Total debt ratio", "Total debt to equity", "Long-term debt to equity", "Short-term debt to total debt", "Times interest earned"],
              w=(52, 24, 24))),
         Q(3, 25, P("Write the credit memorandum: no more than twelve lines, stating which application you would approve, on what terms, "
                    "and the two pieces of information you would require first.")),
         L(13, "Credit memorandum"),
         Q(4, 10, P("State whether each is true or false, with one line of reasoning.")
           + TF(["A current ratio of 4:1 is unambiguously better than one of 2:1.",
                 "Paying a supplier early raises a current ratio that is already above 1.",
                 "Interest paid is classified as a financing outflow.",
                 "Times interest earned treats interest as the only fixed charge.",
                 "A negative net trade cycle means the company is insolvent."], why_line=True, title=None))],
        [])

x4 = EX("X4", "Paper 4 — profitability and return on invested capital", "exam",
        [P("<b>Time allowed 90 minutes · Total 100 marks · four questions, all compulsory</b>")
         + P("Adria Spa, whose 2025 statements appear in Paper 3, reported the following at 31 December 2024: total assets €2,160,000, "
             "marketable securities €30,000, current liabilities €360,000, bonds payable €780,000 and total equity €1,020,000. Assume a tax "
             "rate of 30 per cent, and that all assets except marketable securities and all current liabilities are operating."),
         Q(1, 20, P("Compute the net operating assets and the net financial obligations at both dates, and show that NOA equals NFO plus equity.")),
         A(BT(["", "31 Dec 2025", "31 Dec 2024"],
              ["Operating assets", "− Operating liabilities", "= NOA", "Bonds − marketable securities = NFO", "Equity", "Check: NFO + Equity"],
              w=(52, 24, 24))),
         Q(2, 30, P("Compute Adria’s profit margin, asset turnover and return on assets for 2025, and verify that the third is the product of the first two.")),
         A(BT(["Measure (name the substitution)", "Working", "Result"],
              ["Margin", "Turnover", "Return", "Check: margin × turnover"], w=(36, 44, 20))),
         Q(3, 35, P("Compute the return on ordinary shareholders’ equity for 2025 and disaggregate it as ROCE = RNOA + (LEV × Spread), "
                    "showing every intermediate figure.")),
         A(BT(["Step", "Working", "Result"],
              ["NOPAT", "Average NOA", "RNOA", "NFE", "Average NFO", "NFR", "LEV", "Spread", "ROCE = RNOA + LEV × Spread",
               "Check: Net income ÷ Average equity"], w=(34, 46, 20))),
         Q(4, 15, P("Comment in no more than eight lines on what the disaggregation shows, and state the level of RNOA at which the "
                    "company’s leverage would begin to destroy value for shareholders.")),
         L(9)],
        [])

# ------------------------------------------------------------------ X.3
we3 = WE(
    "Short answers — one line of method, one of arithmetic, one of meaning",
    P("Five short questions of the kind in Paper 6, each solved the way the marker wants to read it."),
    [
        ("1. Opening accumulated depreciation €300,000, closing €330,000; disposal of an asset with accumulated depreciation of €45,000. Depreciation expense?",
         CALC([("Depreciation", "Closing − Opening + Disposals = 330,000 − 300,000 + 45,000", "75,000")])),
        ("2. Inventory turnover 6.0, COGS €900,000, opening inventory €140,000. Closing inventory and days’ sales in inventory?",
         CALC([("Average inventory", "900,000 ÷ 6.0", "150,000"), ("Closing inventory", "2 × 150,000 − 140,000", "160,000"),
               ("Days’ sales in inventory", "160,000 ÷ (900,000 ÷ 360 = 2,500)", "64 days")])),
        ("3. A 5-year bond, face €1,000, 5% annual coupon, priced at the end of its third year at a required rate of 7%?",
         CALC([("Price, n = 2", "50 ÷ 1.07 + 1,050 ÷ 1.07<sup>2</sup> = 46.73 + 917.11", "€963.84")])
         + P("Below par, as it must be: coupon 5 per cent under the 7 per cent required.")),
        ("4. RNOA 12.0%, NFR 5.0%, LEV 0.50. ROCE?",
         CALC([("ROCE", "12.0% + 0.50 × (12.0% − 5.0%)", "15.5%")])
         + P("Positive spread: leverage adds 3.5 points to the shareholders’ return.")),
        ("5. Why is interest paid an operating cash flow in this course?",
         P("Interest expense is deducted in arriving at net income, so the operating section — which starts from net income — already contains it; "
           "dividends paid are not an expense but a distribution to owners, hence financing.")),
    ],
)

SIRIO_IS = T("""
^Income statement | 2025 | 2024
Net sales | 3,600,000 | 3,000,000
Cost of goods sold | 2,232,000 | 1,800,000
Gross profit | 1,368,000 | 1,200,000
Selling expenses | 540,000 | 420,000
Administrative expenses | 288,000 | 270,000
Depreciation expense | 180,000 | 150,000
Operating profit | 360,000 | 360,000
Interest expense | 84,000 | 90,000
Income before tax | 276,000 | 270,000
Income tax expense | 82,800 | 81,000
**Net income | 193,200 | 189,000
""", w=(56, 22, 22))

SIRIO_BS = T("""
^Balance sheet at 31 December | 2025 | 2024
Cash | 120,000 | 180,000
Marketable securities | 60,000 | 60,000
Accounts receivable, net | 540,000 | 420,000
Inventory | 620,000 | 480,000
Prepaid expenses | 40,000 | 30,000
Total current assets | 1,380,000 | 1,170,000
Property, plant and equipment | 2,400,000 | 2,050,000
Accumulated depreciation | (780,000) | (640,000)
**Total assets | 3,000,000 | 2,580,000
Accounts payable | 480,000 | 390,000
Accrued liabilities | 110,000 | 95,000
Income taxes payable | 70,000 | 55,000
Total current liabilities | 660,000 | 540,000
Bonds payable | 840,000 | 900,000
Total liabilities | 1,500,000 | 1,440,000
Share capital | 1,100,000 | 800,000
Retained earnings | 400,000 | 340,000
Total equity | 1,500,000 | 1,140,000
**Total equity and liabilities | 3,000,000 | 2,580,000
""", w=(56, 22, 22))

x5 = EX("X5", "Paper 5 — comprehensive case", "exam",
        [P("<b>Time allowed 180 minutes · Total 200 marks · six questions, all compulsory — the full-length paper</b>")
         + P("Sirio Spa manufactures industrial components. Its statements for 2025 and 2024 follow, in euro. The tax rate is 30 per cent.")
         + SIRIO_IS,
         SIRIO_BS,
         P("Additional information for 2025. Equipment that had cost €150,000, with accumulated depreciation of €40,000, was sold for "
           "€125,000. All other movements in property, plant and equipment were cash purchases. Share capital was issued for cash. Bonds "
           "were repaid in cash. Dividends were declared and paid. Marketable securities did not change. All sales are on credit and all cost "
           "of sales items are purchased."),
         Q(1, 30, P("Prepare a horizontal analysis of the income statement for 2025, base 2024, and a common-size income statement for both years.")),
         A(BT(["", "Change €", "Change %", "% 2025", "% 2024"],
              ["Net sales", "Cost of goods sold", "Gross profit", "Selling expenses", "Administrative expenses", "Depreciation expense",
               "Operating profit", "Interest expense", "Income before tax", "Income tax expense", "Net income"],
              w=(32, 17, 17, 17, 17))),
         Q(2, 45, P("Prepare the change-and-classification table and the statement of cash flows for 2025, indirect method. Then compute free cash flow.")),
         A(BT(["Account", "Change", "Classification"],
              ["Cash", "Marketable securities", "Accounts receivable", "Inventory", "Prepaid expenses", "Property, plant and equipment",
               "Accumulated depreciation", "Accounts payable", "Accrued liabilities", "Income taxes payable", "Bonds payable",
               "Share capital", "Retained earnings"], w=(36, 20, 44)), "Change and classification"),
         G(28, "Gain, purchases, dividends"),
         CFS(10, 2, 3),
         G(16, "Free cash flow"),
         Q(3, 35, P("Compute, for both years: current ratio, acid test ratio, cash ratio, days’ sales in accounts receivable, days’ sales in "
                    "inventory, days’ purchases in accounts payable and the net trade cycle.")),
         A(BT(["Ratio", "2025", "2024"],
              ["Current ratio", "Acid test ratio", "Cash ratio", "Days’ sales in accounts receivable", "Days’ sales in inventory",
               "Days’ purchases in accounts payable", "Net trade cycle"], w=(52, 24, 24))),
         G(24),
         Q(4, 25, P("Compute, for both years: total debt ratio, total debt to equity, long-term debt to equity, short-term debt to total debt "
                    "and times interest earned.")),
         A(BT(["Ratio", "2025", "2024"],
              ["Total debt ratio", "Total debt to equity", "Long-term debt to equity", "Short-term debt to total debt", "Times interest earned"],
              w=(52, 24, 24))),
         Q(5, 45, P("For 2025, compute NOPAT, net operating assets at both dates, the operating profit margin, the operating asset turnover, "
                    "RNOA and ROCE, all on average balances, and disaggregate ROCE as RNOA + (LEV × Spread).")),
         A(BT(["Step", "Working", "Result"],
              ["NOPAT", "NOA 31 Dec 2025", "NOA 31 Dec 2024", "Average NOA", "Operating profit margin", "Operating asset turnover", "RNOA",
               "NFE", "Average NFO", "NFR", "Average equity / LEV", "Spread", "ROCE = RNOA + LEV × Spread", "Check: Net income ÷ Average equity"],
              w=(34, 46, 20))),
         Q(6, 20, P("Write the conclusion of the analysis: fifteen lines at most, covering profitability, liquidity and solvency, and ending "
                    "with the single question you would put to management.")),
         L(16, "Conclusion")],
        [])

X6Q = [
    "A company reports net sales of €1,800,000, cost of goods sold of €1,170,000, operating expenses of €414,000, interest expense "
    "of €36,000 and a tax rate of 30 per cent. Compute operating profit, net income and NOPAT.",
    "Opening accumulated depreciation is €410,000 and closing is €388,000. During the year an asset with accumulated depreciation "
    "of €96,000 was disposed of. Compute depreciation expense.",
    "Inventory turnover is 4.5 times and cost of goods sold is €1,350,000. Opening inventory was €280,000. Compute closing inventory "
    "and days’ sales in inventory on the closing balance.",
    "Sales rose 25 per cent to €2,250,000 while cost of goods sold rose 32 per cent from €1,200,000. Compute gross profit for both "
    "years and the percentage change.",
    "A ten-year bond with a face value of €1,000 and a 6 per cent annual coupon is priced at the end of its seventh year when the "
    "required rate is 9 per cent. Compute the price.",
    "Total assets are €5,000,000, total liabilities €3,000,000, current liabilities €1,200,000 and marketable securities €200,000. "
    "Compute net operating assets and net financial obligations, assuming marketable securities are financial and all current liabilities are operating.",
    "RNOA is 9.0 per cent, the net financial rate is 11.0 per cent and leverage is 0.80. Compute ROCE and comment in one line.",
    "A company collects €50,000 from a customer, prepays €12,000 of rent and declares a €20,000 dividend. Current assets were "
    "€400,000, of which inventory €80,000, and current liabilities €200,000. Compute the current ratio and the acid test ratio after all three events.",
    "Explain in three lines why a gain on the disposal of a fixed asset is deducted in the operating section of the cash flow statement.",
    "State the three sources of accounting distortions named in chapter 2, and give one example of each.",
]
X6W = [G(34), G(26), G(30), G(32), G(34), G(30), [G(18), L(1)], G(34), L(3, "Answer"), L(4, "Answer")]

x6_body = [P("<b>Time allowed 90 minutes · Total 100 marks · ten short questions, all compulsory — ten marks each</b>")]
for i, (q, w) in enumerate(zip(X6Q, X6W)):
    x6_body.append(f'<div class="qh"><b>{i + 1}.</b> {q}</div>')
    x6_body += w if isinstance(w, list) else [w]
x6 = EX("X6", "Paper 6 — short answers across the course", "exam", x6_body, [])

SEC = SECTION(
    "X", "Mixed papers — exam simulation",
    "Six full papers. Work them under time, with a calculator and nothing else, and mark yourself against the solutions before "
    "reading them in full.",
    [
        BLOCK("X.1", "Foundations and cash flow papers", "Time budget, then answers laid out the way the marker reads them.", we1, [x1, x2]),
        BLOCK("X.2", "Credit and profitability papers", "One set of statements, three families of ratios, one memorandum.", we2, [x3, x4]),
        BLOCK("X.3", "The full-length paper and the short answers", "Method, arithmetic, meaning — in three lines.", we3, [x5, x6]),
    ],
)
