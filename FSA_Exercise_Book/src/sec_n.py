from lib import *

METHOD = RULE("Read the stem, cross out the options that are clearly wrong, choose, then justify in one line — the justification is what "
              "makes the answer stick, and on a true-or-false with reasoning it is worth the marks.", "Method")


def mcqs(items, start=1):
    """List of (question, options) → list of HTML chunks with answer boxes."""
    return [MCQ(start + i, q, o) for i, (q, o) in enumerate(items)]


# ------------------------------------------------------------------ N.1
we1 = WE(
    "Chapters 1–2: overview and reporting environment",
    METHOD,
    [
        ("Multiple choice",
         MCQ(1, "Which statement reports a company’s financial position at a point in time?",
             ["Income statement", "Balance sheet", "Statement of cash flows", "Statement of changes in equity"],
             answer="B", why="the other three cover a period")
         + MCQ(2, "The purpose of an external audit is to:",
               ["detect all fraud", "provide reasonable assurance that the statements are free of material misstatement",
                "guarantee the company’s solvency", "prepare the financial statements"],
               answer="B", why="assurance on fair presentation, not a guarantee; management prepares the statements")),
        ("True or false",
         TF(["Comparing a company’s figures across years is called horizontal analysis.",
             "Accrual accounting recognises revenue when cash is received."],
            answers=[("True", "year-to-year change and trend analysis compare the same company over time"),
                     ("False", "revenue is recognised when earned; cash timing is irrelevant")], title=None)),
    ],
)

n1 = EX("N1", "Chapter 1 — overview", "theory",
        mcqs([
            ("Which of the following is likely to be the most informative source if you were interested in a company’s business plan or strategy?",
             ["Auditor’s letter", "Management discussion and analysis", "Proxy statement", "Footnotes"]),
            ("Which of the following would not be considered a source of financing?",
             ["Notes receivable", "Common stockholders’ equity", "Retained earnings", "Debentures"]),
            ("The major reason for analysing a company’s financial statements, as stated in class, is to:",
             ["forecast the share price", "determine credit value", "satisfy the regulator", "compute the tax charge"]),
            ("A common-size income statement is prepared by dividing:",
             ["all items in year t by the corresponding value in year t−1", "all items in year t by the corresponding balance sheet accounts",
              "all items in year t by net income in year t", "all items in year t by sales in year t"]),
            ("Liquidity is generally defined as a measure of:",
             ["the ability to pay employees on time", "the ability to pay interest and principal on all debt",
              "the ability to pay dividends", "the ability to pay current liabilities"]),
            ("While determining the most profitable among a number of companies, which would be the best indicator of relative profitability?",
             ["Highest net income", "Highest retained earnings", "Highest return on equity", "Highest sales"]),
        ])
        + [TF(["Financial statement analysis is an exact science.",
               "The explanatory notes accompanying the financial statements are generally of little value to an analyst.",
               "Two popular techniques of comparative analysis are year-to-year change analysis and index-number trend analysis.",
               "In a common-size balance sheet, total assets are expressed as 100 per cent.",
               "In a common-size income statement, net income is expressed as 100 per cent.",
               "The income statement is the only one of the four basic statements that does not contain balances at a specific point in time."])],
        [])

n2 = EX("N2", "Chapter 2 — reporting environment", "theory",
        mcqs([
            ("If a company receives an unqualified audit opinion it means the auditors:",
             ["did not complete a full audit", "are providing assurance that the company will remain financially viable",
              "are providing assurance that the statements fairly present the company’s financial performance and position",
              "are guaranteeing that the statements are free from fraud"]),
            ("The Management Discussion and Analysis section of an annual report:",
             ["is required by the SEC", "is optional but normally included",
              "is required only if the company has suffered unfavourable trends", "is required only if the audit opinion is qualified"]),
            ("Which body sets IFRS?", ["The SEC", "The FASB", "The International Accounting Standards Board", "The AICPA"]),
            ("Which is not one of the three audit opinion outcomes named on the slide?", ["Clean", "Qualified", "Disclaimer", "Provisional"]),
            ("Accruals are the cornerstone of accounting because:",
             ["net income equals operating cash flow", "net income equals operating cash flow plus accruals",
              "accruals eliminate estimation error", "accruals are required only under IFRS"]),
            ("Recording the least optimistic information about uncertain events is the principle of:",
             ["materiality", "conservatism", "accrual accounting", "historical cost"]),
        ])
        + [TF(["Managers of companies are a major lobbyist on GAAP.",
               "Fair value accounting measures assets and liabilities at their values on the measurement date, approximately the date of the financial statements.",
               "Timeliness, frequency and forward-looking content are listed as desirable qualities of accounting information.",
               "A big bath is a strategy in which managers record huge write-offs in one period to relieve other periods of expenses.",
               "Income smoothing increases the volatility of reported income."])],
        [])

# ------------------------------------------------------------------ N.2
we2 = WE(
    "Chapters 3–4: financing and investing activities",
    METHOD,
    [
        ("Multiple choice",
         MCQ(1, "A provision for product warranties is:",
             ["an asset", "an operating liability", "a financing liability", "part of equity"],
             answer="B", why="it arises from selling goods, carries no interest and is not borrowed money")
         + MCQ(2, "Which method assigns the most recent costs to ending inventory?",
               ["FIFO", "LIFO", "Weighted average", "None of them"],
               answer="A", why="first in, first out: the oldest costs go to cost of goods sold, the newest stay in inventory")),
        ("True or false",
         TF(["Goodwill is amortised over a maximum of 40 years under IFRS.",
             "Retained earnings are part of earned capital."],
            answers=[("False", "goodwill is not amortised; it is tested for impairment at least annually"),
                     ("True", "contributed capital is paid in by shareholders; retained earnings are earned and kept")], title=None)),
    ],
)

n3 = EX("N3", "Chapter 3 — financing activities", "theory",
        mcqs([
            ("Which is an operating liability?", ["Bonds payable", "Accounts payable", "Current portion of long-term debt", "Finance lease obligation"]),
            ("Treasury stock is:", ["an asset", "a contra-equity account", "a current liability", "a non-current liability"]),
            ("A spin-off differs from a split-off in that in a spin-off:",
             ["subsidiary stock is distributed to shareholders as a dividend", "subsidiary stock is exchanged for the company’s own shares",
              "the subsidiary is sold for cash", "the subsidiary is liquidated"]),
            ("To record a contingent liability, the loss must be:",
             ["possible and estimable", "probable and reasonably estimable", "remote but disclosed", "certain"]),
            ("A lease must be accounted for as a capital lease if, at inception, it meets:",
             ["all four criteria", "any one of four criteria", "at least three of four criteria", "none of the criteria"]),
            ("Which is not listed as a transaction sometimes used for off-balance-sheet financing?",
             ["Take-or-pay arrangements", "Through-put agreements", "Issuing ordinary shares at a premium",
              "Selling receivables with recourse and recording them as sales"]),
        ])
        + [TF(["A contingent asset is recorded as soon as realisation is probable.",
               "Loss reserves alter a company’s risk exposure and have cash flow consequences.",
               "A lease whose term is 75 per cent or more of the asset’s estimated economic life is a capital lease.",
               "Paid-in capital in excess of par is part of contributed capital."])],
        [])

n4 = EX("N4", "Chapter 4 — investing activities", "theory",
        mcqs([
            ("In a period of rising prices, which method produces the highest ending inventory?", ["LIFO", "FIFO", "Weighted average", "They are equal"]),
            ("The LIFO reserve is:",
             ["the difference between FIFO and weighted average inventory",
              "the amount by which current cost exceeds the reported cost of LIFO inventories",
              "a liability for future inventory purchases", "the gain on a LIFO liquidation"]),
            ("Receivables are reported at:", ["gross invoice value", "net realisable value", "replacement cost", "present value"]),
            ("A securitisation of receivables with recourse requires the seller to:",
             ["remove the receivables from the balance sheet", "record both an asset and a compensating liability for the amount factored",
              "recognise a gain equal to the discount", "do nothing until the receivables are collected"]),
            ("Impairment is recognised when:",
             ["market value falls below cost", "expected undiscounted cash flows are less than carrying value",
              "the asset is fully depreciated", "the useful life is revised"]),
            ("Average age of plant assets is measured as:",
             ["gross plant ÷ depreciation expense", "accumulated depreciation ÷ depreciation expense",
              "net plant ÷ depreciation expense", "accumulated depreciation ÷ gross plant"]),
        ])
        + [TF(["Capitalising a cost means reporting it in the period when it is incurred.",
               "The double-declining-balance method ignores salvage value in computing the annual charge.",
               "Acquisition cost of a plant asset includes financing charges.",
               "In a period of rising prices, FIFO gross profit contains a holding gain as well as an economic profit."])],
        [])

# ------------------------------------------------------------------ N.3
we3 = WE(
    "Chapters 7–8: cash flow and return on invested capital",
    METHOD,
    [
        ("Multiple choice",
         MCQ(1, "Dividends paid to shareholders are classified as:", ["operating", "investing", "financing", "non-cash"],
             answer="C", why="a distribution to capital providers; dividends <i>received</i> are operating")
         + MCQ(2, "If NOA is 800 and equity is 500, net financial obligations are:", ["1,300", "300", "−300", "500"],
               answer="B", why="NOA = NFO + Equity, so NFO = 800 − 500")),
        ("True or false",
         TF(["Under the indirect method a decrease in accounts receivable is added to net income.",
             "RNOA changes when the company replaces equity with debt."],
            answers=[("True", "customers paid more than the period’s sales: cash above income"),
                     ("False", "RNOA = NOPAT ÷ NOA is independent of financing; the effect of debt shows in LEV × Spread")], title=None)),
    ],
)

n5 = EX("N5", "Chapter 7 — cash flow", "theory",
        mcqs([
            ("Interest paid is classified in the statement of cash flows as:", ["operating", "investing", "financing", "non-cash"]),
            ("Which section always appears first?", ["Investing", "Financing", "Operating", "Non-cash"]),
            ("Under the indirect method, a gain on the sale of equipment is:",
             ["added to net income", "deducted from net income", "ignored", "shown in financing"]),
            ("An increase in accounts payable is:",
             ["a cash outflow in operating", "a cash inflow in operating", "a financing inflow", "a non-cash item"]),
            ("The purchase of equipment financed in full by a note issued to the seller is:",
             ["an investing outflow and a financing inflow", "an investing outflow only", "disclosed as a non-cash activity", "ignored entirely"]),
            ("Free cash flow is:",
             ["cash from operations", "cash from operations less capital expenditures less cash dividends",
              "net income plus depreciation", "the net increase in cash"]),
        ])
        + [TF(["Both the direct and the indirect method give the same cash from operations.",
               "Cash from operations is a measure of profitability.",
               "An increase in inventory is added to net income in the operating section.",
               "Depreciation is a source of cash."])],
        [])

n6 = EX("N6", "Chapter 8 — return on invested capital", "theory",
        mcqs([
            ("NOPAT is:", ["net income plus interest", "operating income × (1 − tax rate)", "net income × (1 − tax rate)", "pretax income less tax"]),
            ("Net operating assets equal:",
             ["total assets", "total assets less total liabilities", "operating assets less operating liabilities", "operating assets less financial liabilities"]),
            ("RNOA can be decomposed as:", ["margin + turnover", "margin × turnover", "margin ÷ turnover", "turnover − margin"]),
            ("In the expression ROCE = RNOA + (LEV × Spread), Spread is:", ["RNOA − NFR", "NFR − RNOA", "RNOA − LEV", "NFE ÷ NFO"]),
            ("Net financial obligations are computed as:", ["total liabilities", "NOA − equity", "equity − NOA", "current liabilities + bonds"]),
            ("If RNOA is below the net financial rate, additional leverage:", ["raises ROCE", "lowers ROCE", "leaves ROCE unchanged", "raises RNOA"]),
        ])
        + [TF(["Invested capital is usually computed on average balances.",
               "Operating liabilities leverage increases RNOA.",
               "ROCE excludes preferred dividends from the numerator and preferred stock from the denominator.",
               "Two companies with the same RNOA must have the same margin."])],
        [])

# ------------------------------------------------------------------ N.4
we4 = WE(
    "Chapter 10 and the marking conventions",
    METHOD,
    [
        ("Multiple choice",
         MCQ(1, "The cash ratio is:",
             ["cash ÷ current assets", "(cash + marketable securities) ÷ current liabilities", "cash ÷ total liabilities",
              "(cash + receivables) ÷ current liabilities"],
             answer="B", why="the strictest liquidity measure: only cash and near-cash against current liabilities")
         + MCQ(2, "The total debt ratio is:",
               ["total liabilities ÷ equity", "total liabilities ÷ total assets", "long-term debt ÷ equity", "current liabilities ÷ total liabilities"],
               answer="B", why="A is debt to equity, C long-term debt to equity, D short-term to total debt")),
        ("True or false",
         TF(["A company whose current ratio is below 1 has negative working capital.",
             "The collection period is computed on year-end receivables."],
            answers=[("True", "current assets below current liabilities means CA − CL is negative"),
                     ("False", "collection period = 360 ÷ turnover on average receivables; days’ sales in receivables uses the closing balance")], title=None)),
    ],
)

n7 = EX("N7", "Chapter 10 — credit analysis", "theory",
        mcqs([
            ("Working capital is:", ["current assets", "current assets ÷ current liabilities", "current assets − current liabilities", "total assets − total liabilities"]),
            ("The acid-test ratio excludes:", ["cash", "accounts receivable", "marketable securities", "inventory and prepaid expenses"]),
            ("Days’ sales in inventory is:",
             ["inventory ÷ sales × 360", "inventory ÷ cost of goods sold × 360", "cost of goods sold ÷ inventory", "360 ÷ inventory"]),
            ("The rule-of-thumb current ratio named on the slide is:", ["1:1", "1.5:1", "2:1", "3:1"]),
            ("Times interest earned is potentially misleading because:",
             ["it uses net income", "it ignores taxes", "it treats interest as the only fixed charge", "it uses an average balance"]),
            ("Window dressing a current ratio of 1.5 by paying down payables with cash will:",
             ["raise it", "lower it", "leave it unchanged", "leave working capital changed"]),
        ])
        + [TF(["Solvency concerns long-run financial viability.",
               "Loan covenants define default and the remedies available.",
               "The short-term debt to total debt ratio measures reliance on short-term financing.",
               "A current ratio of 4:1 is unambiguously better than 2:1.",
               "Liquidity depends mainly on the level of cash rather than on prospective cash flows."])],
        [])

n8 = EX("N8", "The conventions used when marking", "theory",
        mcqs([
            ("Which formula does this course use for the operating profit margin?",
             ["Net income ÷ sales", "Operating income ÷ sales", "NOPAT ÷ sales", "Gross profit ÷ sales"]),
            ("Which denominator belongs in the operating asset turnover?",
             ["Average total assets", "Average net operating assets", "Average equity", "Year-end total assets"]),
            ("Which days convention is used throughout this course?", ["365", "360", "252", "350"]),
            ("Which default tax rate does the lecturer assume when the exercise does not give one?", ["20%", "25%", "30%", "40%"]),
            ("Which items does he treat as financial rather than operating when the balance sheet shows them separately?",
             ["Inventory and receivables", "Prepaid expenses", "Short-term investments, marketable securities and long-term investments", "Accounts payable"]),
        ]),
        [])

# ------------------------------------------------------------------ N.5
we5 = WE(
    "Rapid classification and mixed true or false",
    METHOD,
    [
        ("Rapid classification",
         T("""
^Item | Classification
Income tax payable | <span class="ans">Current liability (operating)</span>
Patents | <span class="ans">Non-current asset (intangible)</span>
Share premium | <span class="ans">Equity (contributed capital)</span>
Allowance for doubtful accounts | <span class="ans">Contra-asset (reduces receivables)</span>
Bonds due in 8 years | <span class="ans">Non-current liability (financing)</span>
Prepaid insurance | <span class="ans">Current asset</span>
""", w=(44, 56), cls="small")),
        ("Mixed true or false",
         TF(["Depreciation is added back under the indirect method because it is a source of cash.",
             "A positive spread means that more leverage raises ROCE."],
            answers=[("False", "it is added back because it is a non-cash expense already deducted in net income"),
                     ("True", "ROCE = RNOA + LEV × Spread: with Spread > 0, a higher LEV adds to ROCE")], title=None)),
    ],
)

n9 = EX("N9", "Rapid-fire classification", "theory",
        P("Classify each item. Allow yourself thirty seconds for the whole list.")
        + T("""
^Item | Classification
Current portion of long-term borrowings | __
Advances received from customers | __
Treasury shares | __
Accumulated depreciation | __
Deferred tax liabilities, long-term | __
Goodwill | __
Marketable securities | __
Notes payable due in eight months | __
Construction in progress | __
Provisions | __
Unearned revenue | __
Bank overdraft | __
""", w=(52, 48), tall=True),
        [])

n10 = EX("N10", "Mixed true or false", "theory",
         [TF(["Investing equals financing is another statement of the balance sheet identity.",
              "A gain on the sale of an asset increases cash from operations.",
              "Index-number trend percentages can be compared between two companies with different base years.",
              "Operating profit is measured before interest expense.",
              "If only one balance sheet date is given you should still compute an average.",
              "A company can report rising net income and negative cash from operations for several years."]),
          TF(["The allowance for doubtful accounts is a liability.",
              "LIFO raises inventory turnover and lowers the current ratio in a period of rising prices.",
              "Depreciation expense is a financing activity.",
              "The net trade cycle equals days in inventory plus days in receivables less days in payables.",
              "A negative spread means the company is unprofitable.",
              "Common-size analysis removes the effect of size, so a small and a large company can be compared directly."],
             start=7, title=None)],
         [])

SEC = SECTION(
    "N", "Multiple choice and true or false",
    "Modelled on the chapter 1 question file on the course page, extended to every chapter covered. These are the cheap marks: "
    "answer them in two minutes and spend the time saved on the computational part.",
    [
        BLOCK("N.1", "Chapters 1 and 2", "Overview of analysis and the reporting environment.", we1, [n1, n2]),
        BLOCK("N.2", "Chapters 3 and 4", "Financing and investing activities.", we2, [n3, n4]),
        BLOCK("N.3", "Chapters 7 and 8", "Cash flow, and return on invested capital.", we3, [n5, n6]),
        BLOCK("N.4", "Chapter 10 and the marking conventions", "Credit analysis, and the conventions the lecturer marks against.", we4, [n7, n8]),
        BLOCK("N.5", "Rapid classification and mixed true or false", "Speed drills across the course.", we5, [n9, n10]),
    ],
)
