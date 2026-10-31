from lib import *

PLAN_SL = ["Year", "Annual depreciation", "Accumulated depreciation", "Book value"]

# ------------------------------------------------------------------ B.1
we1 = WE(
    "A straight-line plan, then a disposal at the end of life",
    P("On 1 January Year 1, Pisani Spa buys a machine for €50,000. Useful life 4 years, residual value €6,000. "
      "(a) Prepare the straight-line depreciation plan. (b) At the end of Year 4 the machine is sold — in scenario (a) for "
      "€7,500, in scenario (b) for €4,200. Compute the gain or loss in each scenario."),
    [
        ("Step 1 — The annual charge",
         F("Annual depreciation = (Cost − Residual value) ÷ Useful life = (50,000 − 6,000) ÷ 4 = <span class='ans'>€11,000</span>")),
        ("Step 2 — The plan",
         T("""
^Year | Annual depreciation | Accumulated depreciation | Book value
1 Jan Year 1 | — | — | 50,000
Year 1 | 11,000 | 11,000 | 39,000
Year 2 | 11,000 | 22,000 | 28,000
Year 3 | 11,000 | 33,000 | 17,000
**Year 4 | 11,000 | 44,000 | 6,000
""", w=(25, 25, 25, 25), cls="small")),
        ("Step 3 — Disposal at the end of life",
         P("At the end of its life the book value equals the residual value, €6,000.")
         + CALC([("(a) Sold for €7,500", "7,500 − 6,000", "Gain €1,500"),
                 ("(b) Sold for €4,200", "4,200 − 6,000", "Loss €1,800")])),
    ],
    comment=P("Gain or loss = proceeds − book value. A gain means the residual value was estimated too low (depreciation was too high); "
              "a loss means the opposite. Neither is cash: the cash is the full proceeds."),
)

b1 = EX("B1", "Straight-line depreciation plan", "depreciation",
        P("On 1 January Year 1, Rendo Spa buys a machine for €96,000. The expected useful life is 5 years and the estimated "
          "residual value is €6,000. Prepare the full depreciation plan under the straight-line method, showing annual expense, "
          "accumulated depreciation and book value."),
        [G(18, "Annual charge"),
         A(BT(PLAN_SL, ["1 Jan Year 1", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"], w=(25, 25, 25, 25)), "Plan")])

b2 = EX("B2", "Straight-line plan and disposal at the end of life", "disposal",
        P("Use the machine of exercise B1. At the end of Year 5 Rendo sells it, in scenario (a) for €9,500 and in scenario (b) for "
          "€3,800. Compute the gain or loss on disposal in each scenario."),
        [G(32), L(2)])

# ------------------------------------------------------------------ B.2
we2 = WE(
    "Double-declining-balance and units-of-activity",
    P("<b>(a)</b> Sala Ltd buys equipment for €40,000, useful life 4 years, residual value €4,000. Prepare the double-declining-balance plan. "
      "<b>(b)</b> A truck costs €62,000, residual value €2,000, expected total use 300,000 km. Actual use: Year 1 80,000 km, Year 2 100,000 km, "
      "Year 3 70,000 km, Year 4 50,000 km. Prepare the units-of-activity plan."),
    [
        ("Step 1 — (a) DDB: double the straight-line rate, applied to the opening book value",
         F("Rate = 2 × (1 ÷ 4) = 50% · the residual value is <b>ignored</b> in the rate but is the floor for the book value")
         + T("""
^Year | Opening book value | Rate | Depreciation | Accumulated | Closing book value
Year 1 | 40,000 | 50% | 20,000 | 20,000 | 20,000
Year 2 | 20,000 | 50% | 10,000 | 30,000 | 10,000
Year 3 | 10,000 | 50% | 5,000 | 35,000 | 5,000
**Year 4 | 5,000 | plug | 1,000 | 36,000 | 4,000
""", w=(14, 19, 10, 17, 19, 21), cls="small")
         + P("Year 4 at 50% would give 2,500 and a book value of 2,500, below the residual value: the last charge is the plug "
             "5,000 − 4,000 = <span class='ans'>1,000</span>.")),
        ("Step 2 — (b) Units of activity: a rate per kilometre",
         F("Rate = (62,000 − 2,000) ÷ 300,000 km = <span class='ans'>€0.20 per km</span>")
         + T("""
^Year | Kilometres | × Rate | Depreciation | Accumulated | Book value
Year 1 | 80,000 | 0.20 | 16,000 | 16,000 | 46,000
Year 2 | 100,000 | 0.20 | 20,000 | 36,000 | 26,000
Year 3 | 70,000 | 0.20 | 14,000 | 50,000 | 12,000
**Year 4 | 50,000 | 0.20 | 10,000 | 60,000 | 2,000
""", w=(14, 18, 12, 18, 18, 20), cls="small")),
    ],
    comment=P("DDB front-loads the expense; units of activity follows use. Both end at the residual value: check the last book value."),
)

b3 = EX("B3", "Double-declining-balance plan", "depreciation",
        P("Vandel Ltd buys equipment for €80,000 with a 5-year useful life and an estimated residual value of €5,000. Prepare "
          "the depreciation plan under the double-declining-balance method."),
        [G(14, "Rate"),
         A(BT(["Year", "Opening book value", "Rate", "Depreciation", "Accumulated", "Closing book value"],
              ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"], w=(14, 19, 10, 17, 19, 21)), "Plan")])

b4 = EX("B4", "Units-of-activity method", "depreciation",
        P("A delivery fleet costs €150,000, has an estimated residual value of €10,000 and an expected total output of 400,000 "
          "kilometres. Actual use is Year 1: 95,000 km, Year 2: 110,000 km, Year 3: 80,000 km, Year 4: 70,000 km, Year 5: 45,000 km. "
          "Prepare the depreciation plan under the units-of-activity method."),
        [G(14, "Rate per km"),
         A(BT(["Year", "Kilometres", "× Rate", "Depreciation", "Accumulated", "Book value"],
              ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"], w=(14, 18, 12, 18, 18, 20)), "Plan")])

# ------------------------------------------------------------------ B.3
we3 = WE(
    "Gain or loss from cost and accumulated depreciation",
    P("<b>(a)</b> Equipment that cost €30,000, with accumulated depreciation of €17,500, is sold for €10,000. "
      "<b>(b)</b> Equipment that cost €45,000, with accumulated depreciation of €41,000, is sold for €6,200. Compute the gain or loss."),
    [
        ("Step 1 — Book value first, then compare with the proceeds",
         F("Book value = Cost − Accumulated depreciation · Gain (loss) = Proceeds − Book value")
         + CALC([("(a) Book value", "30,000 − 17,500", "12,500"),
                 ("(a) Result", "10,000 − 12,500", "Loss €2,500"),
                 ("(b) Book value", "45,000 − 41,000", "4,000"),
                 ("(b) Result", "6,200 − 4,000", "Gain €2,200")])),
    ],
    comment=P("A nearly fully depreciated asset (b) easily produces a gain: the gain is not a sign of good management, only that "
              "past depreciation was heavier than the actual loss of value."),
)

b5 = EX("B5", "Gain or loss from cost and accumulated depreciation", "disposal",
        P("During the year equipment was sold for €11,400 cash. The cost of the equipment was €26,000 originally and it had "
          "accumulated depreciation of €13,100 at the time of sale. Compute the gain or loss on the sale."),
        [G(30)])

b6 = EX("B6", "Gain on a nearly fully depreciated asset", "disposal",
        P("Old equipment with an original cost of €64,000 and accumulated depreciation of €58,500 was sold for €14,200 cash. "
          "Compute the gain or loss."),
        [G(30)])

# ------------------------------------------------------------------ B.4
we4 = WE(
    "Working backwards through the disposal identity",
    P("<b>(a)</b> Equipment costing €36,000 with a book value of €14,000 is sold for €15,500. Compute the accumulated depreciation "
      "and the gain or loss. <b>(b)</b> Equipment costing €60,000 is sold for €21,000, producing a loss of €3,000. Compute the book "
      "value at the date of sale and the accumulated depreciation."),
    [
        ("Step 1 — Two identities, three unknowns at most",
         F("Book value = Cost − Accumulated depreciation &nbsp;&nbsp;·&nbsp;&nbsp; Proceeds − Book value = Gain (+) or Loss (−)")),
        ("Step 2 — Solve",
         CALC([("(a) Accumulated depreciation", "36,000 − 14,000", "22,000"),
               ("(a) Gain or loss", "15,500 − 14,000", "Gain €1,500"),
               ("(b) Book value", "Proceeds + loss = 21,000 + 3,000", "24,000"),
               ("(b) Accumulated depreciation", "60,000 − 24,000", "36,000")])),
    ],
    comment=P("With a <b>gain</b> the book value is proceeds − gain; with a <b>loss</b> it is proceeds + loss. Write the identity "
              "first, then substitute — it avoids the sign error."),
)

b7 = EX("B7", "Work backwards to accumulated depreciation", "disposal",
        P("Old equipment costing €47,500 with a book value of €18,000 was sold for €12,750 cash. Compute the accumulated "
          "depreciation at the date of sale and the gain or loss."),
        [G(32)])

b8 = EX("B8", "Work backwards from the gain", "disposal",
        P("Old equipment costing €52,000 was sold for €16,900, producing a gain of €6,400. Compute the book value at the "
          "date of sale and the accumulated depreciation."),
        [G(32)])

# ------------------------------------------------------------------ B.5
we5 = WE(
    "A mid-year disposal, and the plant asset age measures",
    P("<b>(a)</b> Corti Srl bought a machine on 1 January Year 1 for €90,000, straight-line over 6 years, residual value €6,000. "
      "On 31 March Year 3 it is sold for €58,000. Compute the Year 3 depreciation to the date of sale, the accumulated depreciation "
      "at that date and the gain or loss.")
    + P("<b>(b)</b> Fenni Group reports gross plant and equipment of €600,000, accumulated depreciation of €240,000 and depreciation "
        "expense for the year of €50,000. Compute the average total life span, average age and average remaining life."),
    [
        ("Step 1 — (a) Depreciate up to the date of sale, by months",
         CALC([("Annual charge", "(90,000 − 6,000) ÷ 6", "14,000"),
               ("Year 3, 1 Jan – 31 Mar", "14,000 × 3/12", "3,500"),
               ("Accumulated at date of sale", "14,000 × 2 + 3,500", "31,500"),
               ("Book value", "90,000 − 31,500", "58,500"),
               ("Gain or loss", "58,000 − 58,500", "Loss €500")])),
        ("Step 2 — (b) Every age measure divides by the depreciation expense",
         CALC([("Average total life span", "Gross PP&amp;E ÷ Dep. expense = 600,000 ÷ 50,000", "12.0 years"),
               ("Average age", "Accumulated dep. ÷ Dep. expense = 240,000 ÷ 50,000", "4.8 years"),
               ("Average remaining life", "Net PP&amp;E ÷ Dep. expense = 360,000 ÷ 50,000", "7.2 years"),
               ("Consistency check", "4.8 + 7.2", "12.0 ✓")], w=(28, 50, 22))),
    ],
    comment=P("The plant is 40 per cent through its life (4.8 ÷ 12): heavy replacement spending is about seven years away. The "
              "measures assume straight-line depreciation and exclude land, which is not depreciated."),
)

b9 = EX("B9", "Partial-year depreciation and a mid-year disposal", "disposal",
        P("Sarnico Srl owns a machine bought on 1 January Year 1 for €120,000, depreciated straight-line over 8 years with a "
          "residual value of €8,000. On 30 September Year 4 the machine is sold for €74,000. Compute (a) the depreciation to be "
          "recorded in Year 4 up to the date of disposal, (b) the accumulated depreciation at the date of disposal and (c) the gain "
          "or loss on the sale."),
        [G(58)])

b10 = EX("B10", "Plant asset age measures", "analysis",
         P("Teoro Group reports gross plant and equipment of €860,000, accumulated depreciation of €344,000 and a current "
           "year depreciation expense of €86,000. Compute the average total life span, the average age and the average "
           "remaining life, check that they are consistent, and comment in two lines."),
         [A(BT(["Measure", "Formula", "Computation", "Result"],
               ["Average total life span", "Average age", "Average remaining life", "Check"], w=(26, 28, 30, 16))),
          L(2)])

SEC = SECTION(
    "B", "Depreciation, amortisation and disposals",
    "The depreciation-method spreadsheet of Exercise Session 1 in four shapes, plus the plans and the age measures from chapter 4.",
    [
        BLOCK("B.1", "Straight-line plans and disposal at the end of life",
              "Annual charge, the plan table, and gain or loss when the asset is sold at the end.", we1, [b1, b2]),
        BLOCK("B.2", "Double-declining-balance and units-of-activity plans",
              "Accelerated and usage-based depreciation, and the residual value as the floor.", we2, [b3, b4]),
        BLOCK("B.3", "Gain or loss on disposal",
              "Book value from cost and accumulated depreciation, then compare with the proceeds.", we3, [b5, b6]),
        BLOCK("B.4", "Working backwards from the disposal",
              "Recovering book value or accumulated depreciation from the gain or loss.", we4, [b7, b8]),
        BLOCK("B.5", "Mid-year disposals and plant asset age",
              "Depreciation by months to the date of sale; total life, age and remaining life.", we5, [b9, b10]),
    ],
)
