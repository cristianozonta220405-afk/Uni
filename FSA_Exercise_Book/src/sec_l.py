from lib import *

# ------------------------------------------------------------------ L.1
we1 = WE(
    "Classifying cash flows, and where each disclosure goes",
    P("<b>(a)</b> Classify each transaction as operating, investing, financing or non-cash, inflow or outflow. "
      "<b>(b)</b> Say where each item is reported: body of the statement, schedule of non-cash activities, supplemental disclosures, or nowhere."),
    [
        ("Step 1 — (a) Ask what the cash was for",
         T("""
^Transaction | Activity | Direction
Cash paid to employees | <span class="ans">Operating</span> | outflow
Interest received on a loan to a customer | <span class="ans">Operating</span> | inflow
Dividends received from an associate | <span class="ans">Operating</span> | inflow
Purchase of a patent for cash | <span class="ans">Investing</span> | outflow
Sale of shares held as an investment | <span class="ans">Investing</span> | inflow
Proceeds from a bank loan | <span class="ans">Financing</span> | inflow
Repurchase of own shares | <span class="ans">Financing</span> | outflow
Repayment of lease principal | <span class="ans">Financing</span> | outflow
Land acquired by issuing a mortgage to the seller | <span class="ans">Non-cash</span> | —
""", w=(52, 26, 22), cls="small")
         + RULE("Operating = running the business, including interest paid and received and dividends received. Investing = buying and selling "
                "long-term assets and investments, lending. Financing = raising and repaying capital, including dividends paid. No cash = schedule.", "Course convention")),
        ("Step 2 — (b) Where it is reported",
         T("""
^Item | Where
Depreciation expense | <span class="ans">Body</span> — add-back in operating (indirect method)
Cash paid for interest and for taxes | <span class="ans">Supplemental disclosures</span> (indirect method)
Land acquired by issuing shares | <span class="ans">Schedule of non-cash activities</span>
A stock split | <span class="ans">Nowhere</span> — no resources move, only the number of shares
""", w=(40, 60), cls="small")),
    ],
)

l1 = EX("L1", "Classify eighteen transactions", "cash flow",
        P("Classify each transaction as operating, investing, financing or non-cash, and state whether it is an inflow or an outflow.")
        + T("""
^Transaction | Activity | In / out
Cash collected from customers | __ | __
Cash paid to suppliers for inventory | __ | __
Interest received on a bank deposit | __ | __
Interest paid to lenders | __ | __
Income taxes paid | __ | __
Dividends received from an investment | __ | __
Purchase of a delivery van for cash | __ | __
Proceeds from selling a warehouse | __ | __
Loan made to an associated company | __ | __
Collection of the principal of a note receivable | __ | __
Purchase of shares in another company | __ | __
Proceeds from issuing ordinary shares | __ | __
Dividends paid to shareholders | __ | __
Repayment of the principal of a bond | __ | __
Purchase of treasury shares | __ | __
Issue of shares to acquire a building | __ | __
Conversion of bonds into ordinary shares | __ | __
Exchange of one plant asset for another | __ | __
""", w=(56, 26, 18), tall=True),
        [L(1, "Notes")])

l5 = EX("L5", "Which disclosures are required", "cash flow",
        P("For each item, state whether it appears in the body of the statement of cash flows, in the schedule of non-cash "
          "activities, in the supplemental disclosures, or nowhere.")
        + T("""
^Item | Where it appears
1. Cash paid during the year for interest | __
2. Cash paid during the year for income taxes | __
3. A capital lease of €1,000 incurred on the lease of equipment | __
4. Acquisition of fixed assets by issuing bonds of €30,000 | __
5. Conversion of bonds into common stock of €10,000 | __
6. A stock dividend declared and distributed | __
7. A three-for-one stock split | __
8. Depreciation expense for the year | __
""", w=(56, 44), tall=True),
        [L(1, "Notes")])

# ------------------------------------------------------------------ L.2
we2 = WE(
    "Accrual reporting against cash reporting; the effect on cash from operations",
    P("<b>(a)</b> Mora Srl reports the statement below. Receivables rose by €10,000 and payables rose by €6,000. Contrast net income with cash "
      "flow from operations side by side, then reconcile.")
    + T("""
Sales | 150,000
Gain on sale of land | 4,000
Purchases | (85,000)
Increase in inventory (credited to cost of sales) | 5,000
Depreciation | (12,000)
Expenses paid in cash | (25,000)
**Net income | 37,000
""", w=(75, 25), cls="small")
    + P("<b>(b)</b> Effect on cash from operations of: (1) collecting €20,000 on account; (2) selling equipment with a book value of €30,000 "
        "for €35,000; (3) recording €8,000 of amortisation; (4) paying a previously declared €10,000 dividend; (5) paying €12,000 of salaries; "
        "(6) buying €7,000 of inventory for cash."),
    [
        ("Step 1 — (a) Side by side: for each line, how much cash moved?",
         T("""
^Line | Accrual basis | Cash basis | Why
Sales | 150,000 | 140,000 | receivables +10,000 not collected
Gain on sale of land | 4,000 | — | proceeds are investing
Purchases | (85,000) | (79,000) | payables +6,000 not paid
Increase in inventory | 5,000 | — | no cash
Depreciation | (12,000) | — | non-cash
Expenses paid in cash | (25,000) | (25,000) | already cash
**Total | 37,000 | 36,000 | net income / CFO
""", w=(30, 18, 18, 34), cls="small")),
        ("Step 2 — (a) The indirect reconciliation",
         CALC([("Net income", "", "37,000"), ("+ Depreciation", "non-cash expense", "12,000"),
               ("− Gain on sale of land", "reclassified to investing", "(4,000)"),
               ("− Increase in receivables", "", "(10,000)"), ("− Increase in inventory", "", "(5,000)"),
               ("+ Increase in payables", "", "6,000"), ("= Cash from operations", "", "36,000")], w=(34, 46, 20))
         + P("Net income reflects <b>profitability</b>; cash from operations reflects <b>liquidity</b>.")),
        ("Step 3 — (b) Only cash that comes from or goes to operations counts",
         T("""
^Transaction | Effect on cash from operations
(1) Collect €20,000 on account | <span class="ans">Increase 20,000</span>
(2) Sell equipment, book value 30,000, for 35,000 | <span class="ans">No effect</span> — 35,000 in investing; the gain is deducted
(3) Amortisation 8,000 | <span class="ans">No effect</span> — non-cash
(4) Pay a declared dividend 10,000 | <span class="ans">No effect</span> — financing
(5) Pay salaries 12,000 | <span class="ans">Decrease 12,000</span>
(6) Buy inventory for cash 7,000 | <span class="ans">Decrease 7,000</span>
""", w=(46, 54), cls="small")),
    ],
)

l2 = EX("L2", "Accrual reporting against cash reporting", "cash flow",
        P("Pirra Srl reports the following for the year. Accounts receivable increased by €12,000, inventory decreased by €6,000 "
          "and accounts payable decreased by €9,000.")
        + T("""
Sales | 220,000
Gain on sale of investments | 8,000
 | 228,000
Purchases | (130,000)
Decrease in inventory charged to cost of sales | (6,000)
Depreciation | (14,000)
Expenses paid in cash | (42,000)
Loss on sale of fixed assets | (3,000)
**Net income | 33,000
""", w=(75, 25))
        + REQ(["Prepare a side-by-side comparative statement contrasting the two bases of reporting: net income and cash flows from operations.",
               "Reconcile the two figures by the indirect method.",
               "Which of the two better reflects profitability, and which liquidity?"]),
        [A(BT(["Line", "Accrual basis", "Cash basis"],
              ["Sales", "Gain on sale of investments", "Purchases", "Decrease in inventory", "Depreciation", "Expenses paid in cash",
               "Loss on sale of fixed assets", "Total"], w=(50, 25, 25)), "1. Side by side"),
         G(44, "2. Indirect reconciliation"), L(2, "3. Profitability and liquidity")])

l6 = EX("L6", "Effect on cash from operations", "cash flow",
        P("State the effect of each independent transaction on cash from operations: increase, decrease or no effect, and by how much.")
        + T("""
^Transaction | Effect on cash from operations
1. A customer pays €40,000 owed on account. | __
2. Inventory is purchased on credit for €25,000. | __
3. A machine is sold for €18,000; its book value was €22,000. | __
4. Depreciation of €60,000 is recorded. | __
5. A dividend of €30,000 is declared but not yet paid. | __
6. A supplier is paid €15,000. | __
7. €9,000 of rent is prepaid for next year. | __
8. Equipment is bought for €80,000 cash. | __
""", w=(58, 42), tall=True),
        [L(1, "Notes")])

# ------------------------------------------------------------------ L.3
we3 = WE(
    "From accrual figures to cash: customers and suppliers",
    P("<b>(a)</b> Tirso Spa reports net sales of €600,000. Accounts receivable, net, were €80,000 at the start of the year and €95,000 at the end; "
      "the allowance for doubtful accounts rose from €4,000 to €6,000 and bad debt expense was €5,000. Compute cash collected from customers.")
    + P("<b>(b)</b> Cost of goods sold was €400,000; inventory rose from €50,000 to €60,000 and accounts payable from €30,000 to €36,000. "
        "Compute purchases and cash paid to suppliers."),
    [
        ("Step 1 — (a) Collections, first ignoring the allowance",
         CALC([("Collections (naive)", "Sales − increase in net AR = 600,000 − 15,000", "585,000")])),
        ("Step 2 — (a) Now with the allowance: bad debts reduce receivables without cash",
         CALC([("Write-offs", "Opening allowance + bad debt expense − closing = 4,000 + 5,000 − 6,000", "3,000"),
               ("Gross receivables", "84,000 opening → 101,000 closing: increase 17,000", ""),
               ("Collections", "Sales − increase in gross AR − write-offs = 600,000 − 17,000 − 3,000", "580,000"),
               ("Same, on net AR", "Sales − increase in net AR − bad debt expense = 600,000 − 15,000 − 5,000", "580,000 ✓")], w=(22, 62, 16))
         + P("The naive figure overstates collections by exactly the bad debt expense (5,000): that part of sales will never be collected.")),
        ("Step 3 — (b) Two adjustments: inventory, then payables",
         CALC([("Purchases", "COGS + increase in inventory = 400,000 + 10,000", "410,000"),
               ("Cash paid to suppliers", "Purchases − increase in payables = 410,000 − 6,000", "404,000")])),
    ],
)

l3 = EX("L3", "From sales to cash collected", "cash flow",
        P("Nerva Spa reports net sales of €960,000. Accounts receivable, net, were €118,000 at the start of the year and "
          "€142,000 at the end. The allowance for doubtful accounts rose from €6,000 to €9,000 and the bad debt expense for "
          "the year was €11,000.")
        + REQ(["Compute cash collected from customers ignoring the allowance.",
               "Compute cash collected from customers taking the allowance into account, and reconcile the two answers."]),
        [G(52), L(2, "Reconciliation of the two answers")])

l4 = EX("L4", "From cost of goods sold to cash paid", "cash flow",
        P("Ostia Srl reports cost of goods sold of €540,000. Inventory moved from €96,000 to €128,000 and accounts payable "
          "from €74,000 to €61,000. Compute purchases for the year and cash paid to suppliers."),
        [G(36)])

# ------------------------------------------------------------------ L.4
we4 = WE(
    "Free cash flow across companies; profit rising, cash falling",
    P("<b>(a)</b> Rank by financial flexibility: Pietra (CFO 200, capex 120, dividends 30, net income 140) and Quarzo (CFO 150, capex 30, "
      "dividends 60, net income 110), € thousands.")
    + P("<b>(b)</b> Lumo Group, € thousands:")
    + T("""
^ | Year 1 | Year 2
Net sales | 1,000 | 1,300
Net income | 60 | 80
Net cash provided by operating activities | 70 | 10
Accounts receivable | 150 | 300
Inventory | 200 | 320
Accounts payable | 120 | 140
""", w=(52, 24, 24), cls="small"),
    [
        ("Step 1 — (a) FCF = CFO − capex − dividends",
         CALC([("Pietra", "200 − 120 − 30", "50"), ("Quarzo", "150 − 30 − 60", "60")])
         + P("Quarzo has more free cash despite lower operating cash flow, so more flexibility today; Pietra is investing heavily (capex 60 per "
             "cent of CFO), which may mean growth tomorrow. Neither ranking is complete without knowing what the capex buys.")),
        ("Step 2 — (b) Read the gap between profit and cash",
         CALC([("Sales growth", "1,300 ÷ 1,000 − 1", "+30%"),
               ("Receivables growth", "300 ÷ 150 − 1", "+100%"),
               ("Days’ sales in receivables", "150 ÷ (1,000/360) → 300 ÷ (1,300/360)", "54 → 83"),
               ("CFO ÷ Net income", "70 ÷ 60 → 10 ÷ 80", "1.17 → 0.13")], w=(28, 54, 18))
         + P("<i>Profit grows but cash does not: receivables doubled and inventory rose 60 per cent against 30 per cent sales growth, while "
             "payables barely moved. Growth is being financed with working capital, and earnings quality is falling. Next: days’ sales in "
             "receivables and inventory, net trade cycle, CFO ÷ net income. Ask management about credit terms, the largest customers’ "
             "balances, bad debts and slow-moving stock.</i>")),
    ],
)

l7 = EX("L7", "Free cash flow across three companies", "cash flow",
        P("Compute free cash flow for each company and rank them by financial flexibility. Comment in four lines.")
        + T("""
^ | Alfa | Beta | Gamma
Net cash provided by operating activities | 180,000 | 180,000 | 95,000
Capital expenditures | 40,000 | 150,000 | 20,000
Cash dividends paid | 60,000 | 20,000 | 0
Net income | 120,000 | 165,000 | 40,000
**Free cash flow | __ | __ | __
**Rank | __ | __ | __
""", w=(46, 18, 18, 18), tall=True),
        [L(4)])

l8 = EX("L8", "Rising profit, falling cash", "cash flow",
        P("Below are three years of summary data for Talea Group. Write the analysis: what is happening, which ratios you "
          "would compute next, and what you would ask management.")
        + T("""
^ | Year 1 | Year 2 | Year 3
Net sales | 4,000,000 | 5,200,000 | 6,760,000
Net income | 240,000 | 338,000 | 473,000
Net cash provided by operating activities | 310,000 | 190,000 | (40,000)
Accounts receivable | 500,000 | 866,000 | 1,420,000
Inventory | 600,000 | 910,000 | 1,420,000
Accounts payable | 400,000 | 480,000 | 520,000
""", w=(46, 18, 18, 18)),
        [G(40, "Supporting figures"), L(8, "Analysis")])

SEC = SECTION(
    "L", "Cash flow analysis beyond the statement",
    "Classification, the accrual-versus-cash comparison, the direct-method conversions, free cash flow, and the reading of a "
    "company whose profit and cash are moving in opposite directions.",
    [
        BLOCK("L.1", "Classifying flows and disclosures", "Operating, investing, financing or non-cash — and where each item is reported.", we1, [l1, l5]),
        BLOCK("L.2", "Accrual against cash", "Line-by-line comparison, the reconciliation, and single-transaction effects.", we2, [l2, l6]),
        BLOCK("L.3", "Direct-method conversions", "Cash collected from customers and cash paid to suppliers.", we3, [l3, l4]),
        BLOCK("L.4", "Free cash flow and the profit–cash gap", "Ranking flexibility, and reading growth that consumes cash.", we4, [l7, l8]),
    ],
)
