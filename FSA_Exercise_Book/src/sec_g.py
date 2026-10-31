from lib import *

ORSO_IS = T("""
^Income statement 2025 | Orso | Lince
Sales | 1,200,000 | 900,000
Cost of goods sold | 780,000 | 495,000
Selling and administrative expense | 210,000 | 165,000
Operating income | 210,000 | 240,000
Interest expense | 36,000 | 60,000
Income before taxes | 174,000 | 180,000
Income tax expense | 52,200 | 54,000
**Net income | 121,800 | 126,000
""", w=(56, 22, 22))

ORSO_BS = T("""
^Balance sheet, 31 December 2025 | Orso | Lince
##Assets
Fixed assets, net | 760,000 | 640,000
Inventory | 240,000 | 120,000
Accounts receivable, net | 180,000 | 105,000
Marketable securities | 30,000 | 10,000
Cash | 50,000 | 45,000
Total current assets | 500,000 | 280,000
**Total assets | 1,260,000 | 920,000
##Equity and liabilities
Share capital and retained earnings | 660,000 | 470,000
Bonds payable | 240,000 | 210,000
Accounts payable | 300,000 | 180,000
Income taxes payable | 60,000 | 60,000
Total current liabilities | 360,000 | 240,000
Total liabilities | 600,000 | 450,000
**Total equity and liabilities | 1,260,000 | 920,000
""", w=(56, 22, 22))

# ------------------------------------------------------------------ G.1
we1 = WE(
    "Current, acid test and cash ratios — and what is behind them",
    P("The current section of the balance sheet of Delta Srl at 31 December is given below. Compute the three liquidity ratios "
      "and the composition of current assets, and say whether a supplier should grant 60-day credit.")
    + T("""
^Current assets | € | Current liabilities | €
Cash | 40,000 | Accounts payable | 160,000
Marketable securities | 20,000 | Accrued liabilities | 40,000
Accounts receivable | 140,000 | |
Inventory | 180,000 | |
Prepaid expenses | 20,000 | |
**Total | 400,000 | Total | 200,000
""", w=(32, 18, 32, 18)),
    [
        ("Step 1 — The three ratios, from the widest to the strictest",
         CALC([("Current ratio", "Current assets ÷ Current liabilities = 400,000 ÷ 200,000", "2.00"),
               ("Acid test ratio", "(Cash + Mkt sec. + Receivables) ÷ CL = (40 + 20 + 140) ÷ 200", "1.00"),
               ("Cash ratio", "(Cash + Mkt sec.) ÷ CL = (40 + 20) ÷ 200", "0.30"),
               ("Working capital", "400,000 − 200,000", "200,000")], w=(22, 62, 16))),
        ("Step 2 — Composition of current assets",
         T("""
^ | € | % of current assets
Cash and marketable securities | 60,000 | 15.0%
Accounts receivable | 140,000 | 35.0%
Inventory | 180,000 | 45.0%
Prepaid expenses | 20,000 | 5.0%
""", w=(50, 25, 25), cls="small")),
    ],
    comment=P("The current ratio meets the 2:1 rule of thumb, but half of current assets are inventory and prepaid expenses. Without them "
              "the company covers its current liabilities exactly once, and only if receivables are collected; cash covers 30 per cent. "
              "A supplier can grant 60-day credit, but should first check the age of the receivables."),
)

g1 = EX("G1", "Liquidity ratios for two companies", "liquidity",
        [P("The statements of Orso Spa and Lince Srl at 31 December 2025 are reproduced below. Calculate the current ratio, "
           "the acid test ratio and the cash ratio for both companies, and say which one a supplier would rather extend 60-day credit to.")
         + ORSO_IS, ORSO_BS],
        [A(BT(["Ratio", "Formula", "Orso", "Lince"], ["Current ratio", "Acid test ratio", "Cash ratio"], w=(22, 38, 20, 20))),
         G(26), L(3, "Which one a supplier would prefer")])

g9 = EX("G9", "Quality of current assets", "liquidity",
        P("Two companies report identical current ratios of 2.0 and identical current liabilities of €500,000. Their current assets "
          "are composed as follows.")
        + T("""
^ | Company X | Company Y
Cash | 250,000 | 40,000
Accounts receivable, net | 400,000 | 260,000
Inventories | 300,000 | 620,000
Prepaid expenses | 50,000 | 80,000
**Total current assets | 1,000,000 | 1,000,000
""", w=(56, 22, 22))
        + REQ(["Compute the acid test and cash ratios, and the common-size composition of current assets, for each company.",
               "State which company is more liquid and why the current ratio did not show it."]),
        [A(BT(["Measure", "Company X", "Company Y"],
              ["Acid test ratio", "Cash ratio", "Cash %", "Receivables %", "Inventories %", "Prepaid %"], w=(44, 28, 28))),
         L(3)])

# ------------------------------------------------------------------ G.2
we2 = WE(
    "Receivables and inventory: turnover and days",
    P("Eco Spa: sales (all on credit) €1,080,000; cost of goods sold €720,000; accounts receivable €100,000 at the start of the year "
      "and €140,000 at the end; inventory €110,000 at the start and €130,000 at the end. Compute the turnover and days measures."),
    [
        ("Step 1 — Receivables",
         CALC([("Accounts receivable turnover", "Sales ÷ Average AR = 1,080,000 ÷ [(100,000 + 140,000) ÷ 2 = 120,000]", "9.0x"),
               ("Collection period", "360 ÷ AR turnover = 360 ÷ 9.0", "40.0 days"),
               ("Days’ sales in receivables", "Closing AR ÷ (Sales ÷ 360) = 140,000 ÷ 3,000", "46.7 days")], w=(28, 56, 16))),
        ("Step 2 — Inventory",
         CALC([("Inventory turnover", "COGS ÷ Average inventory = 720,000 ÷ [(110,000 + 130,000) ÷ 2 = 120,000]", "6.0x"),
               ("Days to sell inventory", "360 ÷ inventory turnover = 360 ÷ 6.0", "60.0 days"),
               ("Days’ sales in inventory", "Closing inventory ÷ (COGS ÷ 360) = 130,000 ÷ 2,000", "65.0 days")], w=(28, 56, 16))),
        ("Step 3 — Why the two days measures differ",
         P("The closing-balance measures (46.7 and 65.0 days) are longer than the average-based ones (40 and 60 days) because both balances "
           "<b>rose during the year</b>: the year-end position is worse than the year’s average. If the two were equal, balances were flat.")
         + RULE("Switching from FIFO to LIFO with rising prices raises cost of goods sold and lowers inventory, so inventory turnover rises "
                "and both days measures fall — the company looks faster without selling faster.", "Note")),
    ],
)

g2 = EX("G2", "Receivables liquidity", "liquidity",
        P("Using the data of Orso Spa in exercise G1, and assuming that accounts receivable at the start of the year were "
          "€156,000 and that all sales are on credit, compute the accounts receivable turnover, the days’ sales in receivables on "
          "the closing balance, and the receivables collection period. Comment on the difference between the last two."),
        [A(BT(["Measure", "Computation", "Result"],
              ["Accounts receivable turnover", "Days’ sales in receivables", "Collection period"], w=(32, 46, 22))),
         L(3, "Why the last two differ")])

g3 = EX("G3", "Inventory liquidity", "liquidity",
        P("Still with Orso Spa. Opening inventory was €200,000. Compute the inventory turnover, the days’ sales in inventory on "
          "the closing balance, and the days-to-sell-inventory ratio. Then state what would happen to each if the company "
          "switched from FIFO to LIFO in a period of rising prices."),
        [A(BT(["Measure", "Computation", "Result", "If FIFO → LIFO"],
              ["Inventory turnover", "Days’ sales in inventory", "Days to sell inventory"], w=(28, 36, 16, 20))),
         L(2)])

# ------------------------------------------------------------------ G.3
we3 = WE(
    "Payables and the net trade cycle",
    P("Continue with Eco Spa: accounts payable at year end are €72,000. Assume all cost of sales items are purchased. Compute the "
      "days’ purchases in accounts payable and the net trade cycle, and comment."),
    [
        ("Step 1 — Days’ purchases in accounts payable",
         CALC([("Purchases (assumed = COGS)", "720,000 ÷ 360 = 2,000 per day", ""),
               ("Days’ purchases in AP", "Closing AP ÷ (Purchases ÷ 360) = 72,000 ÷ 2,000", "36.0 days")], w=(30, 54, 16))),
        ("Step 2 — The net trade cycle",
         F("Net trade cycle = Days’ sales in receivables + Days’ sales in inventory − Days’ purchases in AP")
         + CALC([("Net trade cycle", "46.7 + 65.0 − 36.0", "75.7 days")], w=(30, 54, 16))),
        ("Step 3 — Two companies or two years: one column each",
         T("""
^Days | Eco Spa | How to read it
Receivables | 46.7 | money owed by customers
+ Inventory | 65.0 | goods waiting to be sold
− Payables | 36.0 | credit received from suppliers
**= Net trade cycle | 75.7 | days of sales the company must finance itself
""", w=(30, 18, 52), cls="small")),
    ],
    comment=P("Eco pays its suppliers in 36 days but recovers cash from sales only after about 112 days: almost 76 days of operations must "
              "be financed with equity or debt. Shortening the cycle (collecting faster, holding less stock) frees cash."),
)

g4 = EX("G4", "Payables and the trade cycle", "liquidity",
        P("Compute the days’ purchases in accounts payable for Orso and for Lince, assume all cost of sales items are "
          "purchased, and then build the net trade cycle for each company using the figures already computed in exercises G1 "
          "to G3 (Lince: days’ sales in receivables 42, days’ sales in inventory 87). Comment."),
        [A(BT(["Days", "Orso", "Lince"],
              ["Days’ sales in receivables", "+ Days’ sales in inventory", "− Days’ purchases in accounts payable", "= Net trade cycle"],
              w=(52, 24, 24))),
         G(24), L(3)])

g5 = EX("G5", "Full liquidity set, two years", "liquidity",
        [P("The statements of Vela Group for 2025 and 2024 are given below, in thousands of euro. Compute the current ratio, "
           "acid test ratio, cash ratio, days’ sales in receivables, days’ sales in inventory and days’ purchases in accounts "
           "payable for both years, then comment on the change in liquidity.")
         + T("""
^Income statement | 2025 | 2024
Sales | 14,400 | 12,000
Cost of goods sold | 9,000 | 7,200
Selling and administrative expense | 2,160 | 1,800
Operating income | 3,240 | 3,000
Interest expense | 600 | 720
Income before taxes | 2,640 | 2,280
Income tax expense | 1,056 | 912
**Net income | 1,584 | 1,368
""", w=(56, 22, 22)),
         T("""
^Balance sheet | 2025 | 2024
##Assets
Fixed assets, net | 5,400 | 4,200
Inventory | 1,500 | 1,200
Accounts receivable, net | 1,680 | 1,200
Marketable securities | 0 | 0
Cash | 420 | 600
Total current assets | 3,600 | 3,000
**Total assets | 9,000 | 7,200
##Equity and liabilities
Share capital and retained earnings | 5,400 | 3,900
Bonds payable | 1,200 | 1,500
Accounts payable | 2,100 | 1,500
Income taxes payable | 300 | 300
Total current liabilities | 2,400 | 1,800
Total liabilities | 3,600 | 3,300
**Total equity and liabilities | 9,000 | 7,200
""", w=(56, 22, 22))],
        [A(BT(["Ratio", "2025", "2024"],
              ["Current ratio", "Acid test ratio", "Cash ratio", "Days’ sales in receivables", "Days’ sales in inventory",
               "Days’ purchases in accounts payable"], w=(52, 24, 24))),
         G(40), L(3)])

# ------------------------------------------------------------------ G.4
we4 = WE(
    "The effect of transactions on the ratios; window dressing",
    P("<b>(a)</b> At 1 March Sorgente Srl has current assets of €300,000 (including inventory €60,000 and prepaid expenses €10,000) and current "
      "liabilities of €150,000. Trace the current ratio and the acid test ratio through: (1) €20,000 of receivables collected; (2) inventory "
      "of €30,000 bought on credit; (3) €40,000 of payables paid; (4) a cash dividend of €15,000 declared; (5) equipment bought for €25,000 cash.")
    + P("<b>(b)</b> Show the effect of paying €100,000 of payables early, for a company with CA 500 / CL 250 and one with CA 200 / CL 250 (thousands)."),
    [
        ("Step 1 — (a) Track the three totals, then divide",
         T("""
^ | Current assets | Quick assets | Current liabilities | Current ratio | Acid test
1 March | 300,000 | 230,000 | 150,000 | 2.00 | 1.53
(1) Collect receivables | 300,000 | 230,000 | 150,000 | 2.00 | 1.53
(2) Inventory on credit | 330,000 | 230,000 | 180,000 | 1.83 | 1.28
(3) Pay payables | 290,000 | 190,000 | 140,000 | 2.07 | 1.36
(4) Dividend declared | 290,000 | 190,000 | 155,000 | 1.87 | 1.23
(5) Equipment for cash | 265,000 | 165,000 | 155,000 | 1.71 | 1.06
""", w=(26, 16, 15, 17, 13, 13), cls="small")
         + P("Quick assets = current assets − inventory − prepaid expenses = 300,000 − 60,000 − 10,000 = 230,000 at the start. "
             "(1) only swaps one current asset for another; (4) creates a liability without touching assets.")),
        ("Step 2 — (b) Window dressing",
         T("""
^ € 000 | CR before | WC before | CR after | WC after
CA 500, CL 250, pay 100 | 2.00 | 250 | 400 ÷ 150 = 2.67 | 250
CA 200, CL 250, pay 100 | 0.80 | −50 | 100 ÷ 150 = 0.67 | −50
""", w=(30, 15, 15, 25, 15), cls="small")),
    ],
    comment=P("Subtracting the same amount from both terms pushes a ratio away from 1: up if it was above 1, down if below. Working "
              "capital does not move. A year-end ratio can therefore be dressed up; the analyst looks at working capital, at the "
              "ratio during the year and at the cash flow statement."),
)

g6 = EX("G6", "Effect of transactions on the ratios", "liquidity",
        P("Leach SpA had the following transactions involving current assets and current liabilities during February.")
        + T("""
^Date | Transaction
Feb 3 | Accounts receivable of €30,000 are collected
Feb 7 | Equipment is purchased for €56,000 cash
Feb 11 | Paid €6,000 for a three-year insurance policy
Feb 14 | Accounts payable of €24,000 are paid
Feb 18 | Cash dividends of €10,000 are declared
""", w=(16, 84))
        + P("At 1 February current assets were €260,000 and current liabilities €100,000. Current assets included €30,000 of "
            "inventory and €4,000 of prepaid expenses.")
        + REQ(["Compute the current ratio at the beginning of the month and after each transaction.",
               "Compute the acid test ratio at the beginning of the month and after each transaction."]),
        [A(BT(["", "Current assets", "Quick assets", "Current liabilities", "Current ratio", "Acid test"],
              ["1 February", "Feb 3", "Feb 7", "Feb 11", "Feb 14", "Feb 18"], w=(16, 17, 17, 18, 16, 16))),
         G(28)])

g7 = EX("G7", "Window dressing", "liquidity",
        P("Towards the close of the year a finance director instructs that €200,000 of accounts payable be settled early out of "
          "cash. Before the payment, current assets are €600,000 and current liabilities €400,000.")
        + REQ(["Compute the current ratio and working capital before and after.",
               "Repeat the computation for a second company whose current assets are €300,000 and current liabilities €400,000, paying €100,000.",
               "Explain what this tells an analyst."]),
        [A(BT(["", "CR before", "WC before", "CR after", "WC after"], ["First company", "Second company"], w=(28, 18, 18, 18, 18))),
         G(18), L(3, "What this tells an analyst")])

# ------------------------------------------------------------------ G.5
we5 = WE(
    "Working back from the ratios; writing the liquidity paragraph",
    P("<b>(a)</b> Rivo Ltd: receivables turnover 8.0 times on net credit sales of €960,000, opening receivables €100,000; inventory turnover "
      "5.0 times on cost of goods sold of €600,000, opening inventory €110,000. Current liabilities €300,000, cash €50,000, no other current "
      "assets. Compute the closing balances, the collection period, days’ sales in inventory, current and acid test ratios.")
    + P("<b>(b)</b> Write the liquidity section of a credit memorandum on Rivo (eight lines at most)."),
    [
        ("Step 1 — (a) Turnover → average → closing balance",
         CALC([("Average receivables", "960,000 ÷ 8.0", "120,000"),
               ("Closing receivables", "2 × 120,000 − 100,000", "140,000"),
               ("Average inventory", "600,000 ÷ 5.0", "120,000"),
               ("Closing inventory", "2 × 120,000 − 110,000", "130,000"),
               ("Collection period", "360 ÷ 8.0", "45 days"),
               ("Days’ sales in inventory", "130,000 ÷ (600,000 ÷ 360)", "78 days"),
               ("Current ratio", "(50,000 + 140,000 + 130,000) ÷ 300,000", "1.07"),
               ("Acid test ratio", "(50,000 + 140,000) ÷ 300,000", "0.63")], w=(28, 54, 18))),
        ("Step 2 — (b) A model paragraph",
         P("<i>Rivo’s liquidity is weak. The current ratio of 1.07 is well below the 2:1 benchmark and the acid test of 0.63 means that, without "
           "selling inventory, the company can meet only 63 per cent of its current liabilities. Inventory sits for 78 days and customers pay "
           "in 45, so cash comes back slowly. <b>Recommendation:</b> grant only short-term credit, secured and with a limit. Before lending we "
           "would request (1) an ageing schedule of receivables and (2) a monthly cash flow forecast for the next twelve months.</i>")),
    ],
    comment=P("Structure of every written answer: the figures with their benchmark → what they mean → the recommendation → the information you would ask for."),
)

g8 = EX("G8", "Backwards from the ratios", "liquidity",
        P("Monrio Ltd discloses that its accounts receivable turnover for the year was 7.2 times and its inventory turnover 6.0 "
          "times. Net credit sales were €2,160,000 and cost of goods sold €1,440,000. Opening accounts receivable were "
          "€280,000 and opening inventory €210,000.")
        + REQ(["Compute closing accounts receivable and closing inventory.",
               "Compute the collection period and days’ sales in inventory.",
               "The company reports current liabilities of €520,000 and cash of €60,000, with no marketable securities and no "
               "prepaid expenses. Compute the current ratio and the acid test ratio."]),
        [G(62)])

g10 = EX("G10", "Write the liquidity section of a credit report", "liquidity",
         P("You are the lending officer. Using the ratios computed for Orso and Lince in exercises G1 to G4, write the liquidity "
           "section of a credit memorandum: no more than eight lines, with a recommendation and the two pieces of information "
           "you would request before lending."),
         [L(9, "Credit memorandum — liquidity")])

SEC = SECTION(
    "G", "Liquidity and working capital",
    "Current, acid test and cash ratios, the turnover and days measures, and what they do and do not reveal. "
    "The shape of Exercises A and B of the third review session.",
    [
        BLOCK("G.1", "Current, acid test and cash ratios", "From the widest to the strictest measure, and the quality behind the total.", we1, [g1, g9]),
        BLOCK("G.2", "Receivables and inventory turnover", "Turnover on averages, days on closing balances, and why they differ.", we2, [g2, g3]),
        BLOCK("G.3", "Payables and the net trade cycle", "How many days of operations the company must finance itself.", we3, [g4, g5]),
        BLOCK("G.4", "Transactions, ratios and window dressing", "Tracking the totals, and why equal changes move a ratio.", we4, [g6, g7]),
        BLOCK("G.5", "Back from the ratios; the written credit paragraph", "Recovering balances, then the eight-line memorandum.", we5, [g8, g10]),
    ],
)
