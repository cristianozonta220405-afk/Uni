from lib import *

CC = ["Change", "Classification"]
W5 = (34, 15, 15, 16, 20)


def CFS(op=8, inv=3, fin=4, noncash=0):
    """Blank indirect-method statement with its three sections."""
    lines = ["^Statement of cash flows — indirect method | €", "##Cash flows from operating activities"]
    lines += ["__ | __"] * op
    lines += ["<b>Net cash from operating activities</b> | __", "##Cash flows from investing activities"]
    lines += ["__ | __"] * inv
    lines += ["<b>Net cash from investing activities</b> | __", "##Cash flows from financing activities"]
    lines += ["__ | __"] * fin
    lines += ["<b>Net cash from financing activities</b> | __", "<b>Net increase (decrease) in cash</b> | __",
              "Cash at 1 January | __", "Cash at 31 December | __"]
    if noncash:
        lines += ["##Non-cash investing and financing activities"] + ["__ | __"] * noncash
    return A(T("\n".join(lines), w=(72, 28), tall=True, cls="cfs"))


# ------------------------------------------------------------------ K.1
we1 = WE(
    "The change-and-classification table, then the statement",
    [COMPANY("PAVONE SRL", "Comparative Statements of Financial Position — 31 December")
     + T("""
^ | 2025 | 2024
##Assets
Land | €50,000 | €70,000
Equipment | 210,000 | 160,000
Accumulated depreciation | (64,000) | (40,000)
Inventories | 90,000 | 100,000
Accounts receivable | 70,000 | 55,000
Cash | 49,000 | 20,000
**Total | €405,000 | €365,000
##Equity and liabilities
Share capital — ordinary | €180,000 | €150,000
Retained earnings | 125,000 | 85,000
Bonds payable | 60,000 | 80,000
Accounts payable | 40,000 | 50,000
**Total | €405,000 | €365,000
""", w=(50, 25, 25), cls="small")
     + P("Additional information. Net income for 2025 was €70,000. Cash dividends of €30,000 were declared and paid. Bonds of €20,000 were "
         "redeemed for cash. Ordinary shares were issued for €30,000 cash. No equipment was sold; land was sold at cost.")],
    [
        ("Step 1 — Change and classification of every line",
         T("""
^ | 2025 | 2024 | Change | Classification
Land | 50,000 | 70,000 | −20,000 | Investing: sale at cost, inflow 20,000
Equipment | 210,000 | 160,000 | +50,000 | Investing: purchase, outflow 50,000
Accumulated depreciation | (64,000) | (40,000) | +24,000 | Operating: depreciation, add back
Inventories | 90,000 | 100,000 | −10,000 | Operating: decrease, +10,000
Accounts receivable | 70,000 | 55,000 | +15,000 | Operating: increase, −15,000
Cash | 49,000 | 20,000 | +29,000 | the result to explain
Share capital | 180,000 | 150,000 | +30,000 | Financing: issue, +30,000
Retained earnings | 125,000 | 85,000 | +40,000 | Operating NI +70,000; Financing dividends −30,000
Bonds payable | 60,000 | 80,000 | −20,000 | Financing: redemption, −20,000
Accounts payable | 40,000 | 50,000 | −10,000 | Operating: decrease, −10,000
""", w=(22, 12, 12, 12, 42), cls="small")
         + RULE("Asset up = cash down; asset down = cash up. Liability or equity up = cash up; down = cash down. "
                "Depreciation is the change in accumulated depreciation when nothing was sold.", "Signs")),
        ("Step 2 — The statement",
         T("""
^Pavone Srl — Statement of cash flows 2025 | €
##Cash flows from operating activities
Net income | 70,000
Depreciation expense | 24,000
Decrease in inventories | 10,000
Increase in accounts receivable | (15,000)
Decrease in accounts payable | (10,000)
**Net cash provided by operating activities | 79,000
##Cash flows from investing activities
Sale of land | 20,000
Purchase of equipment | (50,000)
**Net cash used in investing activities | (30,000)
##Cash flows from financing activities
Issue of ordinary shares | 30,000
Redemption of bonds | (20,000)
Dividends paid | (30,000)
**Net cash used in financing activities | (20,000)
**Net increase in cash | 29,000
Cash at 1 January | 20,000
**Cash at 31 December | 49,000
""", w=(75, 25), cls="small")),
    ],
    comment=P("Close with the check: 79,000 − 30,000 − 20,000 = 29,000, exactly the change in the cash line of the balance sheet. If it does "
              "not reconcile, a line of the change table has not been used, or has been used twice."),
)

k1 = EX("K1", "Indirect statement of cash flows", "cash flow",
        [COMPANY("ARDEA LTD", "Comparative Statements of Financial Position — 31 December")
         + T("""
^ | 2025 | 2024
##Assets
Land | €60,000 | €90,000
Equipment | 320,000 | 250,000
Accumulated depreciation | (78,000) | (46,000)
Inventories | 140,000 | 165,000
Accounts receivable | 95,000 | 82,000
Cash | 88,000 | 35,000
**Total | €625,000 | €576,000
##Equity and liabilities
Share capital — ordinary | €260,000 | €215,000
Retained earnings | 215,000 | 150,000
Bonds payable | 110,000 | 150,000
Accounts payable | 40,000 | 61,000
**Total | €625,000 | €576,000
""", w=W5, add=CC, tall=True),
         P("Additional information. Net income for 2025 was €125,000. Cash dividends of €60,000 were declared and paid. "
           "Bonds payable of €40,000 were redeemed for cash. Ordinary shares were issued for €45,000 cash. No equipment "
           "was sold during 2025, but land was sold at cost.")
         + REQ(["Prepare the comparative statement with the change and the classification of each difference (fill in the columns above).",
                "Prepare a statement of cash flows for 2025 using the indirect method."])],
        [CFS(6, 3, 4)])

k5 = EX("K5", "A fuller set of current accounts", "cash flow",
        [COMPANY("DORIA NV", "Comparative Statements of Financial Position — 31 December")
         + T("""
^ | 2025 | 2024
##Assets
Land | €120,000 | €120,000
Buildings | 400,000 | 400,000
Accumulated depreciation | (90,000) | (72,000)
Long-term investments | 65,000 | 95,000
Inventory | 112,000 | 96,000
Accounts receivable | 84,000 | 91,000
Prepaid expenses | 11,000 | 7,000
Cash | 53,000 | 38,000
**Total | €755,000 | €775,000
##Equity and liabilities
Share capital — ordinary | €300,000 | €300,000
Retained earnings | 182,000 | 150,000
Bonds payable | 150,000 | 200,000
Accounts payable | 94,000 | 101,000
Accrued liabilities | 29,000 | 24,000
**Total | €755,000 | €775,000
""", w=W5, add=CC, tall=True),
         P("Additional information. Net income was €72,000 and dividends of €40,000 were declared and paid. Long-term "
           "investments were sold at cost. No buildings were bought or sold. Bonds of €50,000 were redeemed.")
         + REQ(["Prepare the statement of cash flows for 2025, indirect method.",
                "Comment in three lines on how the company funded its dividend."])],
        [CFS(8, 2, 3), L(3, "How the dividend was funded")])

# ------------------------------------------------------------------ K.2
we2 = WE(
    "Disposals: the gain or loss, the depreciation and the purchases",
    P("Rondine Spa reports net income of €50,000. Equipment was €260,000 at the start of 2025 and €300,000 at the end; accumulated "
      "depreciation €90,000 and €110,000. During the year equipment that cost €40,000, with accumulated depreciation of €28,000, was sold "
      "for €16,000. Find the gain, the depreciation expense and the purchases, and show how they enter the statement."),
    [
        ("Step 1 — Gain or loss on the sale",
         CALC([("Book value sold", "40,000 − 28,000", "12,000"), ("Gain", "16,000 − 12,000", "4,000")])),
        ("Step 2 — Two T-accounts: opening + increases − decreases = closing",
         CALC([("Accumulated depreciation", "90,000 + Depreciation − 28,000 (removed on sale) = 110,000", "Dep. 48,000"),
               ("Equipment", "260,000 + Purchases − 40,000 (cost sold) = 300,000", "Purch. 80,000")], w=(26, 56, 18))),
        ("Step 3 — Where each figure goes",
         T("""
^Extract of the statement | €
##Operating activities
Net income | 50,000
Depreciation expense | 48,000
Gain on sale of equipment | (4,000)
##Investing activities
Proceeds from sale of equipment | 16,000
Purchase of equipment | (80,000)
**Net cash used in investing activities | (64,000)
""", w=(75, 25), cls="small")),
    ],
    comment=P("The gain appears twice with opposite signs: it is inside net income (+4,000), and it is deducted in operating (−4,000) because "
              "the cash it relates to — the whole 16,000 of proceeds — belongs to investing. Had the equipment been sold for 9,000, the "
              "loss of 3,000 would be <b>added back</b> in operating and 9,000 shown in investing."),
)

k2 = EX("K2", "Disposal at a gain", "cash flow",
        [COMPANY("BOREA SPA", "Comparative Statements of Financial Position — 31 December")
         + T("""
^ | 2025 | 2024
##Assets
Equipment | €180,000 | €200,000
Accumulated depreciation | (52,000) | (44,000)
Investments | 50,000 | 38,000
Accounts receivable | 72,000 | 64,000
Cash | 44,000 | 51,000
**Total | €294,000 | €309,000
##Equity and liabilities
Share capital — ordinary | €130,000 | €118,000
Retained earnings | 96,000 | 84,000
Bonds payable | 28,000 | 70,000
Accounts payable | 40,000 | 37,000
**Total | €294,000 | €309,000
""", w=W5, add=CC, tall=True),
         P("Additional information. Net income was €46,000 and dividends declared and paid were €34,000. Equipment that "
           "cost €20,000 and had accumulated depreciation of €14,000 was sold for €9,000; no equipment was purchased. All "
           "other changes in non-current account balances had a direct effect on cash flows, except the change in accumulated depreciation.")
         + REQ(["Prepare a statement of cash flows for 2025 using the indirect method.",
                "Explain in two lines why the gain appears twice in the statement, with opposite signs."])],
        [G(24, "Gain and depreciation"), CFS(7, 3, 4), L(2, "Why the gain appears twice")])

k3 = EX("K3", "Disposal at a loss, and a derived purchase", "cash flow",
        [COMPANY("CALIPSO SRL", "Comparative Statements of Financial Position — 31 December")
         + T("""
^ | 2025 | 2024
##Assets
Equipment | €240,000 | €210,000
Accumulated depreciation | (62,000) | (55,000)
Inventory | 88,000 | 70,000
Accounts receivable | 64,000 | 78,000
Prepaid expenses | 6,000 | 9,000
Cash | 29,000 | 41,000
**Total | €365,000 | €353,000
##Equity and liabilities
Share capital — ordinary | €150,000 | €150,000
Retained earnings | 92,000 | 71,000
Long-term notes payable | 60,000 | 85,000
Accounts payable | 48,000 | 35,000
Income taxes payable | 15,000 | 12,000
**Total | €365,000 | €353,000
""", w=W5, add=CC, tall=True),
         P("Additional information. Net income was €54,000 and dividends of €33,000 were declared and paid. Equipment "
           "costing €25,000 with accumulated depreciation of €17,000 was sold for €5,000. Long-term notes of €25,000 were repaid.")
         + REQ(["Prepare the statement of cash flows for 2025, indirect method.",
                "State the amount of equipment purchased during the year and how you derived it."])],
        [G(30, "T-accounts: loss, depreciation, purchases"), CFS(9, 3, 3), L(2, "Equipment purchased, and how")])

# ------------------------------------------------------------------ K.3
we3 = WE(
    "Starting from the income statement; a non-cash acquisition",
    [COMPANY("IBIS SRL", "Income statement 2025 and comparative statements of financial position")
     + T("""
^Income statement 2025 | €
Net sales | 500,000
Cost of goods sold | (300,000)
**Gross profit | 200,000
Operating expenses excluding depreciation | (100,000)
Depreciation expense | (30,000)
**Operating profit | 70,000
Gain on sale of equipment | 6,000
Interest expense | (10,000)
**Income before tax | 66,000
Income tax expense | (19,800)
**Net income | 46,200
""", w=(75, 25), cls="small"),
     T("""
^ | 2025 | 2024 | | 2025 | 2024
Cash | 45,200 | 30,000 | Accounts payable | 45,000 | 40,000
Accounts receivable | 60,000 | 50,000 | Interest payable | 2,000 | 3,000
Inventory | 70,000 | 75,000 | Long-term note payable | 80,000 | 0
Equipment | 400,000 | 300,000 | Bank loan | 50,000 | 70,000
Accumulated depreciation | (100,000) | (90,000) | Share capital | 200,000 | 180,000
 | | | Retained earnings | 98,200 | 72,000
<b>Total assets</b> | <b>475,200</b> | <b>365,000</b> | <b>Total</b> | <b>475,200</b> | <b>365,000</b>
""", w=(24, 13, 13, 24, 13, 13), cls="small")
     + P("Additional information. Equipment costing €50,000 with accumulated depreciation of €20,000 was sold. A machine costing €80,000 was "
         "acquired by issuing a long-term note to the supplier; all other equipment was bought for cash. Shares were issued for cash, part of "
         "the bank loan was repaid and dividends were paid.")],
    [
        ("Step 1 — Derive the missing cash figures",
         CALC([("Proceeds from the sale", "Book value + gain = (50,000 − 20,000) + 6,000", "36,000"),
               ("Check on depreciation", "90,000 + 30,000 − 20,000 = closing 100,000", "✓"),
               ("Total equipment acquired", "400,000 − 300,000 + 50,000", "150,000"),
               ("of which for cash", "150,000 − 80,000 (note to supplier)", "70,000"),
               ("Dividends paid", "72,000 + 46,200 − 98,200", "20,000"),
               ("Shares issued / loan repaid", "200,000 − 180,000 / 70,000 − 50,000", "20,000 / 20,000")], w=(28, 54, 18))),
        ("Step 2 — The statement and the non-cash schedule",
         T("""
^Ibis Srl — Statement of cash flows 2025 | €
Net income | 46,200
Depreciation expense | 30,000
Gain on sale of equipment | (6,000)
Increase in accounts receivable | (10,000)
Decrease in inventory | 5,000
Increase in accounts payable | 5,000
Decrease in interest payable | (1,000)
**Net cash provided by operating activities | 69,200
Proceeds from sale of equipment | 36,000
Purchase of equipment | (70,000)
**Net cash used in investing activities | (34,000)
Issue of shares | 20,000
Repayment of bank loan | (20,000)
Dividends paid | (20,000)
**Net cash used in financing activities | (20,000)
**Net increase in cash (30,000 → 45,200) | 15,200
##Non-cash investing and financing activities
Machine acquired by issuing a long-term note to the supplier | 80,000
""", w=(75, 25), cls="small")),
    ],
    comment=P("The €80,000 machine moved no cash: showing it as an investing outflow and a financing inflow would inflate both sections. "
              "It is disclosed in the schedule of non-cash activities instead."),
)

k6 = EX("K6", "Non-cash investing and financing", "cash flow",
        [COMPANY("EOLO SPA", "Comparative Statements of Financial Position — 31 December")
         + T("""
^ | 2025 | 2024
##Assets
Cash | €62,000 | €47,000
Accounts receivable | 58,000 | 49,000
Inventory | 71,000 | 80,000
Prepaid expenses | 8,000 | 11,000
Plant assets | 520,000 | 410,000
Accumulated depreciation | (168,000) | (145,000)
**Total assets | €551,000 | €452,000
##Equity and liabilities
Accounts payable | €54,000 | €61,000
Accrued expenses | 21,000 | 16,000
Long-term note payable | 90,000 | 0
Mortgage payable | 0 | 120,000
Common stock | 240,000 | 180,000
Retained earnings | 146,000 | 75,000
**Total liabilities and equity | €551,000 | €452,000
""", w=W5, add=CC, tall=True),
         P("Additional information.")
         + OL(["A machine was purchased during the year at a cost of €90,000, financed in full by a long-term note issued to the manufacturer.",
               "Other equipment was purchased for €45,000 cash.",
               "A machine with a cost of €25,000 and a net book value of €4,000 was sold for €11,000.",
               "Net income was €111,000 and dividends paid were €40,000.",
               "Common stock was issued for €60,000 cash and the mortgage was repaid in full."])
         + REQ(["Prepare the statement of cash flows for 2025, indirect method, including the schedule of non-cash activities.",
                "Explain why the €90,000 machine does not appear in the investing section."])],
        [G(20, "Gain and depreciation"), CFS(9, 3, 4, noncash=1), L(2, "Why the machine is not in investing")])

k7 = EX("K7", "Starting from the income statement", "cash flow",
        [P("Faro Srl reports the following income statement for 2025.")
         + T("""
Net sales | 640,000
Cost of goods sold | (384,000)
**Gross profit | 256,000
Operating expenses excluding depreciation | (142,000)
Depreciation expense | (38,000)
**Operating profit | 76,000
Loss on sale of equipment | (6,000)
Interest expense | (12,000)
**Income before tax | 58,000
Income tax expense | (17,400)
**Net income | 40,600
""", w=(75, 25)),
         COMPANY("FARO SRL", "Comparative Statements of Financial Position — 31 December")
         + T("""
^ | 2025 | 2024
##Assets
Cash | €51,000 | €33,000
Accounts receivable | 76,000 | 68,000
Inventory | 92,000 | 104,000
Equipment | 310,000 | 280,000
Accumulated depreciation | (126,000) | (102,000)
**Total assets | €403,000 | €383,000
##Equity and liabilities
Accounts payable | €58,000 | €66,000
Interest payable | 4,000 | 3,000
Bank loan | 100,000 | 120,000
Share capital | 180,000 | 150,000
Retained earnings | 61,000 | 44,000
**Total liabilities and equity | €403,000 | €383,000
""", w=W5, add=CC, tall=True),
         P("Additional information. Equipment costing €34,000 with accumulated depreciation of €14,000 was sold during the "
           "year. Shares were issued for cash and part of the bank loan was repaid. Dividends were declared and paid.")
         + REQ(["Compute the proceeds from the equipment sale, the equipment purchased and the dividends paid.",
                "Prepare the statement of cash flows for 2025, indirect method."])],
        [A(BT(["Figure", "Working", "Result"], ["Proceeds from equipment sale", "Equipment purchased", "Dividends paid"],
              w=(30, 50, 20))), G(16), CFS(8, 2, 3)])

# ------------------------------------------------------------------ K.4
we4 = WE(
    "Accumulated depreciation puzzles; dividends and treasury shares",
    P("<b>(a)</b> Compute depreciation expense: case 1 — opening accumulated depreciation 50,000, closing 64,000, an asset with accumulated "
      "depreciation of 9,000 disposed of; case 2 — opening 120,000, closing 110,000, an asset that cost 30,000 and was 80 per cent depreciated "
      "disposed of.")
    + P("<b>(b)</b> Retained earnings went from €140,000 to €152,000 with net income of €45,000. Common stock rose from €200,000 to €230,000, "
        "bonds fell from €60,000 to €40,000 and treasury stock went from 0 to (€12,000). Prepare the financing section."),
    [
        ("Step 1 — (a) One formula",
         F("Depreciation expense = Closing accumulated depreciation − Opening + Accumulated depreciation on disposals")
         + CALC([("Case 1", "64,000 − 50,000 + 9,000", "23,000"),
                 ("Case 2", "110,000 − 120,000 + (80% × 30,000 = 24,000)", "14,000")])
         + P("A <b>fall</b> in accumulated depreciation does not mean negative depreciation: the disposal removed more than the year added.")),
        ("Step 2 — (b) Dividends from retained earnings, then the section",
         CALC([("Dividends paid", "140,000 + 45,000 − 152,000", "33,000")])
         + T("""
^Cash flows from financing activities | €
Issue of common stock | 30,000
Repayment of bonds | (20,000)
Purchase of treasury stock | (12,000)
Dividends paid | (33,000)
**Net cash used in financing activities | (35,000)
""", w=(75, 25), cls="small")),
    ],
    comment=P("Treasury stock is a contra-equity account: its increase is cash paid to buy back shares, a financing outflow. Net, the company "
              "returned 35,000 to its capital providers — 45,000 to shareholders through dividends and buyback, less 30,000 of new shares, "
              "plus 20,000 to bondholders."),
)

k8 = EX("K8", "Four accumulated depreciation puzzles", "cash flow",
        P("For each independent case, compute the depreciation expense for the year. This is the single step that unlocks most "
          "cash flow questions.")
        + T("""
^Case | Opening acc. dep. | Closing | Disposals during the year | Depreciation expense
1 | 92,000 | 118,000 | none | __
2 | 92,000 | 118,000 | an asset with accumulated depreciation of 15,000 | __
3 | 140,000 | 126,000 | an asset with accumulated depreciation of 48,000 | __
4 | 86,000 | 86,000 | an asset that cost 40,000 and was two-thirds depreciated | __
""", w=(8, 16, 13, 43, 20), tall=True),
        [G(28)])

k9 = EX("K9", "Treasury stock in the financing section", "cash flow",
        [COMPANY("NEMO SPA", "Comparative Statements of Financial Position — 31 December")
         + T("""
^ | 2025 | 2024
##Assets
Cash | €40,500 | €35,000
Accounts receivable | 62,000 | 55,000
Inventory | 88,000 | 92,000
Fixed assets | 300,000 | 260,000
Accumulated depreciation | (95,000) | (80,000)
**Total assets | €395,500 | €362,000
##Equity and liabilities
Accounts payable | €47,000 | €52,000
Bonds payable | 70,000 | 40,000
Common stock | 200,000 | 180,000
Retained earnings | 96,500 | 90,000
Treasury stock | (18,000) | 0
**Total liabilities and equity | €395,500 | €362,000
""", w=W5, add=CC, tall=True),
         P("Additional information. Net income was €38,500. No fixed assets were sold. Bonds and common stock were issued "
           "for cash, treasury stock was purchased for cash, and dividends were declared and paid.")
         + REQ(["Compute the dividends paid.", "Prepare the statement of cash flows for 2025, indirect method.",
                "Comment on the financing section."])],
        [G(14, "Dividends paid"), CFS(6, 1, 5), L(3, "Comment on financing")])

# ------------------------------------------------------------------ K.5
we5 = WE(
    "Free cash flow; why net income and operating cash flow differ",
    P("Use the Pavone Srl statement of example K.1 (net income 70,000; net cash from operating activities 79,000; equipment purchased 50,000; "
      "dividends 30,000). Compute free cash flow, then reconcile net income to operating cash flow and classify each reconciling item."),
    [
        ("Step 1 — Free cash flow (course definition)",
         F("FCF = Cash from operations − Capital expenditures − Cash dividends")
         + CALC([("FCF", "79,000 − 50,000 − 30,000", "(1,000)"),
                 ("FCF without the dividend", "79,000 − 50,000", "29,000")])),
        ("Step 2 — The reconciliation",
         T("""
^Reconciling item | € | Type
Net income | 70,000 |
Depreciation expense | +24,000 | non-cash expense
Increase in accounts receivable | (15,000) | working capital movement
Decrease in inventories | +10,000 | working capital movement
Decrease in accounts payable | (10,000) | working capital movement
**Net cash provided by operating activities | 79,000 | difference +9,000
""", w=(48, 18, 34), cls="small")
         + P("A <b>reclassification</b> item would be a gain or loss on a disposal: removed from operating because its cash sits in investing.")),
    ],
    comment=P("Operations covered capital spending but not capital spending plus the dividend: the 1,000 gap, and more, was filled by selling "
              "land and issuing shares — not repeatable every year. Net income measures profitability on an accrual basis; cash from "
              "operations measures the cash the business actually generated, i.e. liquidity."),
)

k4 = EX("K4", "Free cash flow", "cash flow",
        P("Using the statement of cash flows prepared for Calipso Srl in exercise K3, compute free cash flow and interpret it in "
          "three lines. Then state what free cash flow would have been if the company had not paid a dividend."),
        [G(24), L(3, "Interpretation"), L(1, "Without the dividend")])

k10 = EX("K10", "Why net income and operating cash flow differ", "cash flow",
         P("Eolo Spa (exercise K6) reports net income of €111,000 and net cash provided by operating activities of €149,000. "
           "Prepare a reconciliation that explains the €38,000 difference, classify each reconciling item as a non-cash expense, a "
           "reclassification or a working capital movement, and write a four-line comment on what the two numbers each measure."),
         [A(BT(["Reconciling item", "€", "Type"], ["Net income"] + [""] * 7 + ["Net cash provided by operating activities"],
               w=(48, 18, 34))),
          L(4)])

SEC = SECTION(
    "K", "Statement of cash flows — indirect method",
    "The change-and-classification table, then the statement. This is the single most heavily examined topic in the course: "
    "Exercise Session 3 and Review Session 1 are nothing else.",
    [
        BLOCK("K.1", "The indirect method, from the comparative balance sheet",
              "Change and classification of every line, then the three sections and the cash check.", we1, [k1, k5]),
        BLOCK("K.2", "Disposals at a gain or a loss", "T-accounts for depreciation and purchases; where the gain and the proceeds go.", we2, [k2, k3]),
        BLOCK("K.3", "Income statement data and non-cash activities",
              "Deriving proceeds, purchases and dividends; the schedule of non-cash activities.", we3, [k6, k7]),
        BLOCK("K.4", "Accumulated depreciation, dividends and treasury shares", "The puzzles that unlock most cash flow questions.", we4, [k8, k9]),
        BLOCK("K.5", "Free cash flow and the net income reconciliation", "What is left after investing and dividends, and why profit is not cash.", we5, [k4, k10]),
    ],
)
