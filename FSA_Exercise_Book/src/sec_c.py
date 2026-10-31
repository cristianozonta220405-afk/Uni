from lib import *

# ------------------------------------------------------------------ C.1
we1 = WE(
    "FIFO, LIFO and weighted average on three cost layers",
    P("Merli Trading, Year 3 (periodic system). Opening inventory 40 units at €10; purchase in May of 60 units at €12; purchase in "
      "October of 20 units at €15. During the year 90 units were sold at €20 each.")
    + REQ(["Compute cost of goods sold and ending inventory under FIFO, LIFO and weighted average.",
           "Compute gross profit under each method and comment."]),
    [
        ("Step 1 — Goods available for sale: the total every method must split",
         T("""
^Layer | Units | Unit cost | Cost
Opening inventory | 40 | 10 | 400
May purchase | 60 | 12 | 720
October purchase | 20 | 15 | 300
**Available for sale | 120 | | 1,420
""", w=(40, 20, 20, 20), cls="small")
         + P("Units sold 90, so units in ending inventory = 120 − 90 = 30.")),
        ("Step 2 — Assign the 90 units sold",
         CALC([("FIFO — oldest first", "COGS = 40 × 10 + 50 × 12 = 400 + 600", "1,000"),
               ("", "Ending inventory = 10 × 12 + 20 × 15 = 120 + 300", "420"),
               ("LIFO — newest first", "COGS = 20 × 15 + 60 × 12 + 10 × 10 = 300 + 720 + 100", "1,120"),
               ("", "Ending inventory = 30 × 10", "300"),
               ("Weighted average", "Average cost = 1,420 ÷ 120 = €11.833", ""),
               ("", "COGS = 90 × 11.833", "1,065"),
               ("", "Ending inventory = 30 × 11.833", "355")], w=(24, 56, 20))),
        ("Step 3 — Gross profit, and the check",
         T("""
^Method | Revenue | COGS | Gross profit | Ending inventory | COGS + EI
FIFO | 1,800 | 1,000 | 800 | 420 | 1,420
LIFO | 1,800 | 1,120 | 680 | 300 | 1,420
Weighted average | 1,800 | 1,065 | 735 | 355 | 1,420
""", w=(22, 14, 14, 16, 18, 16), cls="small")),
    ],
    comment=P("With rising prices FIFO gives the highest gross profit and the most current inventory on the balance sheet; LIFO "
              "gives the most current cost of goods sold in the income statement and the lowest profit; weighted average sits between."),
)

METH = ["FIFO", "LIFO", "Weighted average"]

c1 = EX("C1", "FIFO, LIFO and weighted average", "inventory",
        P("Vasco Trading reports the following for Year 2. Opening inventory 50 units at €20; purchase on 12 April of 30 units at "
          "€24; purchase on 3 October of 20 units at €30. During the year 70 units were sold at €38 each.")
        + REQ(["Compute cost of goods sold and ending inventory under FIFO, LIFO and the weighted average method.",
               "Compute gross profit under each method.", "Comment in two lines."]),
        [G(55),
         A(BT(["Method", "Revenue", "COGS", "Ending inventory", "Gross profit"], METH, w=(28, 18, 18, 18, 18)), "Summary"),
         L(2)])

c2 = EX("C2", "Four cost layers", "inventory",
        P("Pelmar Srl, Year 4. Opening inventory 100 units at €12; purchases of 150 units at €14 in March, 200 units at €15 in "
          "July and 50 units at €18 in November. 380 units were sold during the year.")
        + REQ(["Compute cost of goods sold and ending inventory under FIFO, LIFO and weighted average.",
               "State which method gives the most current balance sheet value for inventory, and which gives the most current income statement."]),
        [G(62),
         A(BT(["Method", "Cost of goods sold", "Ending inventory", "Check: COGS + EI"], METH, w=(28, 24, 24, 24)), "Summary"),
         L(2)])

# ------------------------------------------------------------------ C.2
we2 = WE(
    "What the method does to the ratios, and restating LIFO to FIFO",
    P("<b>(a)</b> Use the Merli data of the previous example. Opening inventory was €400 under either method; other current assets "
      "are €1,000 and current liabilities €900. Compute inventory turnover and the current ratio under FIFO and LIFO.")
    + P("<b>(b)</b> Sirmione Spa reports inventories of €1,500 thousand on a LIFO basis and a LIFO reserve of €400 thousand; tax rate "
        "30 per cent. Restate inventory to FIFO and show the balancing adjustments."),
    [
        ("Step 1 — (a) Ratios under each method",
         CALC([("Inventory turnover, FIFO", "COGS ÷ avg inventory = 1,000 ÷ [(400 + 420) ÷ 2 = 410]", "2.44x"),
               ("Inventory turnover, LIFO", "1,120 ÷ [(400 + 300) ÷ 2 = 350]", "3.20x"),
               ("Current ratio, FIFO", "(1,000 + 420) ÷ 900", "1.58"),
               ("Current ratio, LIFO", "(1,000 + 300) ÷ 900", "1.44")], w=(30, 52, 18))
         + P("LIFO makes the company look <b>more efficient</b> (higher turnover) and <b>less liquid</b> (lower current ratio) — "
             "without anything real having changed. A creditor should put both companies on the same basis before comparing.")),
        ("Step 2 — (b) Restate with the LIFO reserve",
         T("""
^Adjustment | € 000
Inventory, LIFO | 1,500
Add LIFO reserve | +400
**Inventory, FIFO | 1,900
##The two balancing adjustments
Deferred tax liability (30% × 400) | +120
Retained earnings (70% × 400) | +280
""", w=(75, 25), cls="small")),
    ],
    comment=P("Assets rise by 400; the financing side rises by 120 of tax and 280 of equity. The restated balance sheet still balances."),
)

c3 = EX("C3", "Which method, and what it does to the ratios", "inventory",
        P("Use the Pelmar data of exercise C2. Opening inventory was €1,200 under either method. Other current assets are "
          "€3,200 and current liabilities are €2,900.")
        + REQ(["Compute the inventory turnover and the current ratio under FIFO and under LIFO.",
               "Comment on what the choice of method does to a creditor’s view of the company."]),
        [G(32),
         A(BT(["Ratio", "FIFO", "LIFO"], ["Inventory turnover", "Current ratio"], w=(40, 30, 30))),
         L(3)])

c5 = EX("C5", "Restating LIFO inventory to FIFO", "inventory",
        P("Oristan Group reports inventories of €2,400 thousand on a LIFO basis and discloses a LIFO reserve of €600 "
          "thousand. The tax rate is 30 per cent. Restate the inventory to a FIFO basis and show the two balancing adjustments."),
        [A(BT(["Adjustment", "€ 000"], ["Inventory, LIFO", "LIFO reserve", "Inventory, FIFO", "Balancing adjustment 1:", "Balancing adjustment 2:"],
              w=(70, 30)), "Restatement"),
         G(22)])

# ------------------------------------------------------------------ C.3
we3 = WE(
    "Holding gains, and a LIFO liquidation",
    P("<b>(a)</b> Bruni Spa began the year with 20 units at €100 and bought 30 units at €130. It sold 25 units at €200. Split FIFO gross "
      "profit into economic profit and holding gain.")
    + P("<b>(b)</b> Gaeta Srl carries LIFO inventory in two layers: 1,000 units at €4 (old) and 2,000 units at €7. This year it buys "
        "3,000 units at €10 and sells 4,500 units at €16. Compute COGS and gross profit, and the effect of the liquidation."),
    [
        ("Step 1 — (a) FIFO profit contains a holding gain",
         CALC([("Revenue", "25 × 200", "5,000"),
               ("FIFO COGS", "20 × 100 + 5 × 130", "2,650"),
               ("FIFO gross profit", "5,000 − 2,650", "2,350"),
               ("Economic profit", "Revenue − current cost = 5,000 − 25 × 130", "1,750"),
               ("Holding gain", "20 old units × (130 − 100)", "600"),
               ("Check", "FIFO GP − holding gain = 2,350 − 600 = LIFO GP (25 × 130 at current cost)", "1,750 ✓")], w=(24, 58, 18))),
        ("Step 2 — (b) Selling more than you buy digs into old layers",
         CALC([("Units", "3,000 opening + 3,000 bought − 4,500 sold", "1,500 left"),
               ("LIFO COGS", "3,000 × 10 + 1,500 × 7", "40,500"),
               ("Gross profit", "4,500 × 16 − 40,500 = 72,000 − 40,500", "31,500"),
               ("COGS had it bought 4,500", "4,500 × 10", "45,000"),
               ("Liquidation profit", "1,500 × (10 − 7) = 45,000 − 40,500", "+4,500")], w=(28, 54, 18))),
    ],
    comment=P("Both effects are one-off and come from old, cheap costs, not from selling better. The analyst removes them when "
              "judging sustainable margins; the liquidation also brings forward tax on the old layers."),
)

c4 = EX("C4", "Economic profit and holding gain", "inventory",
        P("Tellaro Spa began the year with 50 units at €400 and purchased 70 units at €480 during the year. It sold 40 units at "
          "€650 each. Compute the gross profit under FIFO, split it into economic profit and holding gain, and show that the "
          "FIFO gross profit less the holding gain equals the LIFO gross profit."),
        [G(72)])

c6 = EX("C6", "LIFO liquidation", "inventory",
        P("Brienno Spa carries LIFO inventory in two layers: 2,000 units at €6, acquired years ago, and 3,000 units at €9. During "
          "the current year it purchases 4,000 units at €12 and sells 5,000 units at €20.")
        + REQ(["Compute cost of goods sold and gross profit for the year.",
               "Compute what cost of goods sold would have been had the company purchased 5,000 units instead of 4,000, and quantify the effect of the liquidation on pretax income.",
               "Comment."]),
        [G(62), L(3)])

# ------------------------------------------------------------------ C.4
we4 = WE(
    "The cost of goods sold equation, and product versus period costs",
    P("<b>(a)</b> Ferla Ltd shows opening inventory of €60,000, closing inventory of €75,000 and cost of goods sold of €395,000. "
      "Compute net purchases; then show the effect of closing inventory overstated by €5,000 (tax rate 30 per cent).")
    + P("<b>(b)</b> Classify as product or period cost: factory rent; depreciation of delivery vans; import duties on goods bought; "
        "chief executive’s salary; packaging of the product; interest on a working-capital loan."),
    [
        ("Step 1 — (a) One equation, solved for the unknown",
         F("Opening inventory + Net purchases − Closing inventory = Cost of goods sold")
         + CALC([("Net purchases", "395,000 + 75,000 − 60,000", "410,000"),
                 ("COGS if closing is overstated by 5,000", "60,000 + 410,000 − 80,000", "390,000"),
                 ("Effect", "COGS −5,000 → pretax income +5,000 → net income +3,500", "overstated")], w=(34, 50, 16))
         + P("Next year the error reverses: opening inventory is overstated, so next year’s COGS is overstated by the same 5,000.")),
        ("Step 2 — (b) Is the cost needed to bring the goods to saleable condition?",
         T("""
^Cost | Classification
Factory rent | <span class="ans">Product</span> — manufacturing overhead
Depreciation of delivery vans | <span class="ans">Period</span> — selling expense
Import duties on goods bought | <span class="ans">Product</span> — part of purchase cost
Chief executive’s salary | <span class="ans">Period</span> — administrative
Packaging of the product | <span class="ans">Product</span>
Interest on a working-capital loan | <span class="ans">Period</span> — financing
""", w=(50, 50), cls="small")),
    ],
    comment=P("If a product cost is wrongly expensed as a period cost, it leaves cost of goods sold, so <b>gross profit is overstated</b>; "
              "but the part that belonged to closing inventory is charged now, so <b>operating profit and inventory are understated</b>."),
)

c7 = EX("C7", "The cost of goods sold equation", "inventory",
        P("Filled in from a damaged file, Canova Ltd shows opening inventory of €85,000, closing inventory of €97,000 and cost "
          "of goods sold of €640,000. Compute net purchases for the year. Then show what cost of goods sold would have "
          "been if closing inventory had been overstated by €9,000, and what that would do to reported net income."),
        [G(45), L(2)])

c8 = EX("C8", "Expensing or capitalising inventory costs", "inventory",
        P("For each cost below, say whether it is treated as a product cost (capitalised into inventory) or a period cost (expensed "
          "as incurred), and state the effect on the current year’s gross profit of getting it wrong in the direction of expensing everything.")
        + T("""
^Cost | Product or period
Direct labour in the factory | __
Office supplies at head office | __
Freight-in on raw materials | __
Advertising campaign | __
Factory overhead allocated to units produced | __
Sales commissions | __
""", w=(62, 38), tall=True),
        [L(3, "Effect on gross profit of expensing everything")])

SEC = SECTION(
    "C", "Inventory valuation",
    "FIFO, LIFO, weighted average, the LIFO reserve and the liquidation effect. Chapter 4 covers all of this and the lecturer "
    "never set an exercise on it — which is a reason to be ready, not a reason to skip it.",
    [
        BLOCK("C.1", "FIFO, LIFO and weighted average",
              "Goods available for sale, split between cost of goods sold and ending inventory.", we1, [c1, c2]),
        BLOCK("C.2", "The method and the ratios; restating LIFO to FIFO",
              "Turnover and current ratio under each method, and the LIFO reserve adjustment.", we2, [c3, c5]),
        BLOCK("C.3", "Holding gains and LIFO liquidations",
              "The part of profit that comes from old costs rather than from trading.", we3, [c4, c6]),
        BLOCK("C.4", "The cost of goods sold equation; product and period costs",
              "Solving the inventory identity, and what an error does to profit.", we4, [c7, c8]),
    ],
)
