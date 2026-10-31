from lib import *

# ------------------------------------------------------------------ A.1
we1 = WE(
    "Classify ten balance sheet items",
    P("Classify each item of Ostro Srl as a current or non-current asset, a current or non-current liability, "
      "equity, or a contra account — and say in a few words why.")
    + T("""
^Item | Item
Raw materials | Trade receivables due in 60 days
Software licences (5-year) | Loan to a supplier, repayable in 3 years
Prepaid rent for the next six months | Unearned revenue (customer deposits)
Bank loan, final instalment in 4 years | Warranty provision, used next year
Allowance for doubtful accounts | Legal reserve
""", w=(50, 50)),
    [
        ("Step 1 — Apply the twelve-month test",
         RULE("An item is <b>current</b> if it will be realised, consumed or settled within twelve months "
              "(or the operating cycle, if longer). Everything else is <b>non-current</b>. Contra accounts are "
              "neither assets nor liabilities: they reduce the account they belong to.", "Rule")),
        ("Step 2 — Classify",
         T("""
^Item | Classification | Why
Raw materials | <span class="ans">Current asset</span> | consumed within the operating cycle
Trade receivables, 60 days | <span class="ans">Current asset</span> | collected within twelve months
Software licences (5-year) | <span class="ans">Non-current asset</span> | intangible, used over five years
Loan to a supplier, 3 years | <span class="ans">Non-current asset</span> | collected after twelve months
Prepaid rent, six months | <span class="ans">Current asset</span> | service received within twelve months
Unearned revenue | <span class="ans">Current liability</span> | owed in goods or services next year
Bank loan, 4 years | <span class="ans">Non-current liability</span> | the instalment due next year is a current liability
Warranty provision, next year | <span class="ans">Current liability</span> | provision expected to be used within twelve months
Allowance for doubtful accounts | <span class="ans">Contra-asset</span> | deducted from receivables, not a liability
Legal reserve | <span class="ans">Equity</span> | retained profit set aside by law, not a liability
""", w=(32, 24, 44), cls="small")),
    ],
    comment=P("Look for three traps: the <b>current portion</b> of a long-term loan, <b>contra accounts</b> "
              "(accumulated depreciation, allowance, treasury shares) and <b>equity reserves</b>, which are never liabilities."),
)

a1 = EX("A1", "Current / non-current classification", "classification",
        P("Classify each of the following balance sheet items as a current or a non-current asset, or as a current or a non-current liability.")
        + T("""
^Item | Classification | Item | Classification
Inventories | __ | Marketable securities | __
Goodwill | __ | Deferred tax assets (long-term) | __
Short-term investments | __ | Accrued expenses | __
Prepaid insurance | __ | Provisions | __
Accounts receivable | __ | Income tax payables | __
Land | __ | Long-term borrowings | __
Construction in progress | __ | Accounts payable | __
Investments in associates | __ | Current portion of long-term borrowings | __
Machinery | __ | Bonds | __
Cash and cash equivalents | __ | Advances received from customers | __
""", w=(27, 21, 31, 21), tall=True),
        [L(1, "Notes")])

a2 = EX("A2", "Classification including equity items", "classification",
        P("Classify each item below. Three of them are neither assets nor liabilities — say what they are.")
        + T("""
^Item | Classification | Item | Classification
Patents | __ | Short-term derivative liabilities | __
Cash at bank | __ | Employee benefit liabilities | __
Property, plant and equipment | __ | Dividends payable | __
Current income tax assets | __ | Long-term obligations under leases | __
Trademarks | __ | Bank overdraft | __
Merchandise inventory | __ | Notes payable due in 20 months | __
Financial assets held to maturity (8 years) | __ | Deferred tax liabilities (long-term) | __
Notes receivable due in 5 months | __ | Retained earnings | __
Accumulated depreciation | __ | Share premium (paid-in capital in excess of par) | __
Treasury shares | __ | Wages payable | __
""", w=(29, 19, 33, 19), tall=True),
        [L(3, "The items that are neither assets nor liabilities")])

# ------------------------------------------------------------------ A.2
we2 = WE(
    "A classified balance sheet, with operating and financing liabilities",
    P("The balances of Velia Srl at 31 December, in thousands, are listed below. Prepare a classified balance sheet "
      "in horizontal format and mark each liability as operating (O) or financing (F).")
    + T("""
Cash | 60 | Accounts payable | 140
Accounts receivable | 210 | Accrued wages | 25
Inventories | 180 | Unearned revenue | 30
Prepaid expenses | 15 | Bank overdraft | 40
Equipment | 900 | Bank loan, due in 5 years | 350
Accumulated depreciation | (300) | Share capital | 400
Trademarks | 75 | Retained earnings | 155
""", w=(34, 14, 38, 14)),
    [
        ("Step 1 — Sort every balance into its block",
         P("Assets: non-current (equipment net of accumulated depreciation, trademarks) and current (inventories, receivables, "
           "prepaid, cash). Financing side: equity, non-current liabilities, current liabilities. Accumulated depreciation is "
           "<b>not</b> a liability: it is netted against equipment.")),
        ("Step 2 — Lay out the two sides and check they balance",
         T("""
^Assets | € 000 | Equity and liabilities | € 000
##Non-current assets
Equipment | 900 | Share capital | 400
Less accumulated depreciation | (300) | Retained earnings | 155
Equipment, net | 600 | <b>Total equity</b> | <b>555</b>
Trademarks | 75 | Bank loan, 5 years <span class="ans">(F)</span> | 350
<b>Total non-current assets</b> | <b>675</b> | <b>Total non-current liabilities</b> | <b>350</b>
##Current assets / current liabilities
Inventories | 180 | Accounts payable <span class="ans">(O)</span> | 140
Accounts receivable | 210 | Accrued wages <span class="ans">(O)</span> | 25
Prepaid expenses | 15 | Unearned revenue <span class="ans">(O)</span> | 30
Cash | 60 | Bank overdraft <span class="ans">(F)</span> | 40
<b>Total current assets</b> | <b>465</b> | <b>Total current liabilities</b> | <b>235</b>
**Total assets | 1,140 | Total equity and liabilities | 1,140
""", w=(32, 14, 40, 14), cls="small")),
        ("Step 3 — Why operating versus financing matters",
         P("Operating liabilities (suppliers, employees, customers, tax authority) arise from running the business and carry no "
           "explicit interest; financing liabilities (overdraft, loans, bonds, leases) are borrowed money. In chapter 8 the first "
           "group is netted against operating assets to give <b>NOA</b>, the second goes into <b>NFO</b>; mixing them distorts "
           "RNOA, leverage and the net financial rate.")),
    ],
    comment=P("Total assets 1,140 = total equity and liabilities 1,140: always close with the check."),
)

a3 = EX("A3", "Operating versus financing liabilities", "classification",
        P("Chapter 3 splits liabilities by the activity that creates them, and Chapter 8 then uses that split to build net "
          "operating assets. Classify each item as an operating or a financing liability, and say in one line why the distinction matters.")
        + T("""
^Liability | Operating or financing
Accounts payable | __
Bank loan, 5 years | __
Unearned revenue | __
Bonds payable | __
Taxes payable | __
Current portion of long-term debt | __
Accrued wages | __
Finance lease obligation | __
Postretirement liabilities | __
Short-term notes payable to a bank | __
""", w=(62, 38), tall=True),
        [L(2, "Why the distinction matters")])

a7 = EX("A7", "Build a classified balance sheet", "format",
        P("From the balances below, prepare a classified balance sheet in horizontal format for Delaro NV at 31 December. All amounts in thousands.")
        + T("""
Cash | 140 | Accounts payable | 310
Accounts receivable, net | 420 | Accrued liabilities | 95
Inventories | 515 | Income taxes payable | 60
Prepaid expenses | 35 | Bank loan, due in 4 years | 500
Equipment | 1,180 | Bonds payable | 300
Accumulated depreciation | (390) | Share capital | 700
Patents | 180 | Retained earnings | 115
""", w=(34, 14, 38, 14)),
        [A(BT(["Assets", "€ 000", "Equity and liabilities", "€ 000"], [""] * 15, w=(32, 14, 40, 14)),
           "Classified balance sheet — Delaro NV, 31 December")])

# ------------------------------------------------------------------ A.3
we3 = WE(
    "From T-format to multi-step",
    P("The income statement of Sorel Srl is presented in T-format. Rewrite it in the multi-step (two-step) format.")
    + T("""
^Left side / debit | | Right side / credit |
Cost of sales | 240 | Revenue | 380
Marketing expenses | 30 | Rental income (spare warehouse) | 6
General and administrative | 42 | |
Depreciation expense | 18 | |
Interest expense | 12 | |
Income tax expense | 17 | |
""", w=(34, 14, 38, 14)),
    [
        ("Step 1 — Find net income: the balancing figure of the T",
         CALC([("Total credits", "380 + 6", "386"), ("Total debits", "240 + 30 + 42 + 18 + 12 + 17", "359"),
               ("Net income", "386 − 359", "27")])),
        ("Step 2 — Rebuild it in steps",
         T("""
^Sorel Srl — Income statement | €
Revenue | 380
Cost of sales | (240)
**Gross profit | 140
Marketing expenses | (30)
General and administrative expenses | (42)
Depreciation expense | (18)
**Operating profit | 50
Other income: rental income | 6
Interest expense | (12)
**Income before tax | 44
Income tax expense | (17)
**Net income | 27
""", w=(75, 25), cls="small")),
    ],
    comment=P("Only sales and cost of sales sit above gross profit. Rental income is not part of sales, so it goes below "
              "operating profit as other income (state your choice). The two routes must give the same net income: 27."),
)

a4 = EX("A4", "From T-format to multi-step", "format",
        P("The income statement of Avelli Srl for the year is presented in T-format. Rewrite it in the two-step (multi-step) horizontal format.")
        + T("""
^Left side / debit | | Right side / credit |
Cost of sales | 128 | Revenue | 186
R&D expenses | 11 | |
SG&A expenses | 24 | |
Depreciation expense | 6 | |
Interest expense | 5 | |
Income tax expense | 4 | |
""", w=(34, 14, 38, 14)),
        [G(18, "Net income check"),
         A(BT(["Avelli Srl — Income statement", "€"], [""] * 11, w=(75, 25)), "Multi-step statement")])

a5 = EX("A5", "Multi-step with a second revenue line", "format",
        P("Rewrite the following T-format statement of Kenwood Ltd in two-step format. Rental revenue is not part of sales.")
        + T("""
^Left side / debit | | Right side / credit |
Cost of goods sold | 412 | Sales | 690
Marketing expenses | 58 | Rental revenue | 9
SG&A expenses | 96 | |
Depreciation expense | 37 | |
Interest expense | 18 | |
Income tax expense | 23 | |
""", w=(34, 14, 38, 14)),
        [G(18, "Net income check"),
         A(BT(["Kenwood Ltd — Income statement", "€"], [""] * 12, w=(75, 25)), "Multi-step statement")])

# ------------------------------------------------------------------ A.4
we4 = WE(
    "Multi-step and single-step from a scrambled list",
    P("The balances of Tavola SpA for the year, in thousands, are listed in no particular order. Prepare the income statement "
      "in multi-step and in single-step format, and say which one an analyst needs.")
    + T("""
Net sales | 860 | Cost of goods sold | 510
Selling expenses | 95 | Administrative expenses | 70
Interest expense | 14 | Loss on sale of equipment | 8
Income tax expense | 49 | Depreciation | 25
""", w=(34, 14, 38, 14)),
    [
        ("Step 1 — Multi-step: one subtotal per layer",
         T("""
^Tavola SpA — multi-step | € 000
Net sales | 860
Cost of goods sold | (510)
**Gross profit | 350
Selling expenses | (95)
Administrative expenses | (70)
Depreciation | (25)
**Operating profit | 160
Loss on sale of equipment | (8)
Interest expense | (14)
**Income before tax | 138
Income tax expense | (49)
**Net income | 89
""", w=(75, 25), cls="small")),
        ("Step 2 — Single-step: all revenues, then all expenses",
         T("""
^Tavola SpA — single-step | € 000
Net sales | 860
##Expenses
Cost of goods sold | 510
Selling expenses | 95
Administrative expenses | 70
Depreciation | 25
Loss on sale of equipment | 8
Interest expense | 14
Income tax expense | 49
**Total expenses | (771)
**Net income | 89
""", w=(75, 25), cls="small")),
    ],
    comment=P("The analyst needs the <b>multi-step</b> format: it shows gross profit and operating profit, the inputs of gross margin, "
              "operating margin, NOPAT and times interest earned. The single-step format reaches the same 89 but hides them."),
)

a6 = EX("A6", "Build the statement from a scrambled list", "format",
        P("The following balances, in thousands, belong to Mirani SpA for the year ended 31 December. Prepare a multi-step income statement.")
        + T("""
Interest expense | 26 | Net sales | 1,240
Income tax expense | 61 | Cost of goods sold | 806
Selling expenses | 142 | Administrative expenses | 95
Depreciation and amortisation | 48 | Gain on sale of equipment | 12
""", w=(34, 14, 38, 14)),
        [A(BT(["Mirani SpA — Income statement", "€ 000"], [""] * 13, w=(75, 25)), "Multi-step statement")])

a9 = EX("A9", "Single-step and multi-step, same data", "format",
        P("Pell Company reports net sales 940, cost of goods sold 611, selling and administrative expenses 188, interest "
          "expense 21 and income tax expense 36. Prepare the income statement in both the single-step and the multi-step "
          "format, and say in two lines which one a financial analyst needs and why."),
        [A(BT(["Single-step", "€"], [""] * 8, w=(75, 25)), "Single-step"),
         A(BT(["Multi-step", "€"], [""] * 10, w=(75, 25)), "Multi-step"),
         L(2, "Which one the analyst needs, and why")])

# ------------------------------------------------------------------ A.5
we5 = WE(
    "Missing subtotals, and a statement with errors",
    [P("<b>(a)</b> Complete the statement of Lodi Spa: net sales ?, cost of goods sold (720), gross profit 480, operating expenses ?, "
       "operating profit 180, interest expense (30), income before tax ?, income tax expense (30%) ?, net income ?.")
     + P("<b>(b)</b> A junior analyst prepared the statement below for Brera Srl (tax rate 30 per cent). Find the errors and redraft it.")
     + T("""
Net sales | 900
Cost of goods sold | (540)
**Gross profit | 360
Administrative expenses | (120)
Dividends paid | (40)
**Operating profit | 200
Interest expense | (20)
**Income before tax | 180
Income tax expense (30%) | (60)
**Net income | 120
""", w=(75, 25), cls="small")],
    [
        ("Step 1 — (a) Walk the statement, one identity at a time",
         CALC([("Net sales", "Gross profit + COGS = 480 + 720", "1,200"),
               ("Operating expenses", "Gross profit − operating profit = 480 − 180", "300"),
               ("Income before tax", "180 − 30", "150"),
               ("Income tax expense", "30% × 150", "45"),
               ("Net income", "150 − 45", "105")])),
        ("Step 2 — (b) Test every line against its layer",
         UL(["<b>Error 1</b> — <i>Dividends paid</i> are a distribution of profit to shareholders, not an expense: they go to the "
             "statement of changes in equity, never in the income statement.",
             "<b>Error 2</b> — the tax charge (60) is 30% of operating profit; tax is computed on <b>income before tax</b>."])),
        ("Step 3 — Redraft",
         T("""
^Brera Srl — corrected | €
Net sales | 900
Cost of goods sold | (540)
**Gross profit | 360
Administrative expenses | (120)
**Operating profit | 240
Interest expense | (20)
**Income before tax | 220
Income tax expense (30% × 220) | (66)
**Net income | 154
""", w=(75, 25), cls="small")),
    ],
    comment=P("Checklist: only sales and cost of sales above gross profit; only operating expenses between gross and operating "
              "profit; interest and non-operating gains or losses below it; tax on income before tax; no dividends anywhere."),
)

a8 = EX("A8", "Fill the missing subtotals", "format",
        P("Complete the income statement of Hoven Industries. Each question mark is recoverable from the others.")
        + T("""
^Hoven Industries | Given | Your figure
Net sales | ? | __
Cost of goods sold | (1,452) | __
Gross profit | 968 | __
Operating expenses | ? | __
Operating profit | 311 | __
Interest expense | (44) | __
Income before tax | ? | __
Income tax expense (30%) | ? | __
Net income | ? | __
""", w=(56, 20, 24), tall=True),
        [G(40)])

a10 = EX("A10", "Find the four errors", "format",
         P("A junior analyst has prepared the statement below. Identify the errors and redraft the statement correctly.")
         + T("""
Net sales | 1,500
Gain on disposal of a warehouse | 40
Cost of goods sold | (900)
**Gross profit | 640
Selling expenses | (210)
Interest expense | (30)
Income tax expense | (60)
**Operating profit | 340
**Net income | 340
""", w=(75, 25)),
         [L(4, "The four errors"),
          A(BT(["Corrected statement", "€"], [""] * 11, w=(75, 25)), "Redraft")])

SEC = SECTION(
    "A", "Statements, formats and classification",
    "Ten drills on what goes where. These come straight from Exercise Session 1 and from the accounting-topics class, "
    "and they are the cheapest marks on the paper.",
    [
        BLOCK("A.1", "Current or non-current: classifying balance sheet items",
              "The twelve-month test, contra accounts and equity items.", we1, [a1, a2]),
        BLOCK("A.2", "Operating versus financing, and the classified balance sheet",
              "Sorting every balance into its block, and splitting liabilities by the activity that created them.", we2, [a3, a7]),
        BLOCK("A.3", "From T-format to multi-step",
              "Find net income as the balancing figure, then rebuild the statement layer by layer.", we3, [a4, a5]),
        BLOCK("A.4", "Multi-step and single-step from a list",
              "Placing each line in the right layer, and knowing which format the analyst needs.", we4, [a6, a9]),
        BLOCK("A.5", "Missing subtotals and errors",
              "Recovering figures from the identities, and testing every line against its layer.", we5, [a8, a10]),
    ],
)
