from lib import *

PV = F("Price = Coupon × [1 − (1 + r)<sup>−n</sup>] ÷ r &nbsp;+&nbsp; Face × (1 + r)<sup>−n</sup> "
       "&nbsp;&nbsp;— r = required rate per period, n = periods <b>remaining</b>")

# ------------------------------------------------------------------ M.1
we1 = WE(
    "Pricing a bond with annual coupons — at a discount and at a premium",
    P("<b>(a)</b> An 8-year bond, face value €1,000, coupon 6 per cent paid at the end of each year, is priced at the end of its third year, "
      "when the required rate is 8 per cent. <b>(b)</b> A 10-year bond, face €1,000, coupon 9 per cent annual, is priced at the beginning of "
      "its seventh year, when the required rate is 7 per cent. Compute both prices."),
    [
        ("Step 1 — Count the periods that are left",
         PV + CALC([("(a) End of year 3 of 8", "8 − 3", "n = 5"),
                    ("(b) Beginning of year 7 = end of year 6", "10 − 6", "n = 4")], w=(40, 44, 16))),
        ("Step 2 — Discount the coupons and the face value",
         CALC([("(a) Annuity factor 8%, 5", "(1 − 1.08<sup>−5</sup>) ÷ 0.08", "3.992710"),
               ("(a) PV factor 8%, 5", "1.08<sup>−5</sup>", "0.680583"),
               ("(a) Price", "60 × 3.992710 + 1,000 × 0.680583 = 239.563 + 680.583", "€920.15"),
               ("(b) Annuity factor 7%, 4", "(1 − 1.07<sup>−4</sup>) ÷ 0.07", "3.387211"),
               ("(b) PV factor 7%, 4", "1.07<sup>−4</sup>", "0.762895"),
               ("(b) Price", "90 × 3.387211 + 1,000 × 0.762895 = 304.849 + 762.895", "€1,067.74")], w=(26, 56, 18))),
    ],
    comment=P("(a) Coupon 6 per cent below the 8 per cent required → the bond sells at a <b>discount</b>. (b) Coupon 9 per cent above the 7 per "
              "cent required → <b>premium</b>. The sign of the gap tells you the answer before you compute: use it as a check."),
)

m1 = EX("M1", "Priced at a discount", "bonds",
        P("Compute the present value of a 10-year bond with a face value of $100 and a contract (coupon) rate of 10 per cent "
          "per annum, payable at the end of each year, priced at the end of its fifth year, when the effective (required) interest "
          "rate is 14 per cent per annum."),
        [G(52)])

m2 = EX("M2", "Priced at a premium", "bonds",
        P("Compute the present value of a 14-year bond with a face value of $1,000 and a contract rate of 8 per cent per "
          "annum, payable at the end of each year, priced at the beginning of its tenth year, when the required rate is 6 per cent per annum."),
        [G(52)])

# ------------------------------------------------------------------ M.2
we2 = WE(
    "Semiannual coupons; pricing a purchase at two required rates",
    P("<b>(a)</b> Reprice bond (b) of the previous example assuming the coupon is paid semiannually. "
      "<b>(b)</b> You consider buying $5,000 of 6 per cent bonds due in 5 years, interest paid semiannually. Price them at a required rate of "
      "8 per cent and of 4 per cent, rounded to the nearest dollar."),
    [
        ("Step 1 — Halve the rates, double the periods",
         CALC([("(a) Per period", "coupon 90 ÷ 2 = 45; rate 7% ÷ 2 = 3.5%; n = 4 × 2 = 8", ""),
               ("(a) Price", "45 × 6.873956 + 1,000 × 0.759412 = 309.328 + 759.412", "€1,068.74")], w=(18, 64, 18))
         + P("Slightly higher than with annual coupons (€1,067.74): half of each coupon arrives six months earlier, and money received "
             "earlier is worth more.")),
        ("Step 2 — (b) One bond, two required rates",
         CALC([("Coupon per period", "$5,000 × 6% ÷ 2", "$150"),
               ("At 8% → 4% × 10 periods", "150 × 8.110896 + 5,000 × 0.675564 = 1,216.63 + 3,377.82", "$4,594"),
               ("At 4% → 2% × 10 periods", "150 × 8.982585 + 5,000 × 0.820348 = 1,347.39 + 4,101.74", "$5,449")], w=(26, 58, 16))),
    ],
    comment=P("Risk — the chance that interest or principal is not paid in full and on time — is priced through the required rate: the riskier "
              "you judge the issuer, the higher the rate you require and the lower the price you are willing to pay."),
)

m3 = EX("M3", "The same bond, semiannual interest", "bonds",
        P("Recompute exercise M2 assuming the bond interest is payable in equal semiannual amounts. Explain why the answer differs."),
        [G(44), L(2, "Why the answer differs")])

m4 = EX("M4", "Pricing a purchase", "bonds",
        P("On 1 January Year 1 you are considering the purchase of $10,000 of Colvin Company’s 8 per cent bonds. The bonds "
          "are due in 10 years, with interest payable semiannually on 30 June and 31 December. Based on your analysis of "
          "Colvin you determine that a 6 per cent required interest rate is appropriate.")
        + REQ(["Compute the price you will pay for the bonds using the present value model, rounded to the nearest dollar.",
               "Recompute the price if your required rate of return is 10 per cent.",
               "Describe risk and explain how it is reflected in your required rate of return."]),
        [G(36, "1."), G(32, "2."), L(3, "3.")])

# ------------------------------------------------------------------ M.3
we3 = WE(
    "Working back to the required rate; a bond issued at a discount",
    P("<b>(a)</b> A 2-year bond, face €1,000, annual coupon 8 per cent, is quoted at €965.29. Find the required rate. "
      "<b>(b)</b> Lario Spa issues €200,000 of 5-year bonds with a 4 per cent annual coupon when the market requires 6 per cent. Before the "
      "issue: total assets €1,000,000, total liabilities €400,000, operating income €150,000, interest expense €20,000. Compute the proceeds, "
      "the discount, and the effect on the total debt ratio and times interest earned."),
    [
        ("Step 1 — (a) Trial and error, guided by the price",
         P("Price below par → the required rate is above the 8 per cent coupon. Try 10 per cent:")
         + CALC([("At 10%", "80 ÷ 1.10 + 1,080 ÷ 1.10<sup>2</sup> = 72.73 + 892.56", "965.29 ✓")])
         + P("The market requires 10 per cent, 2 points above the coupon: it sees the issuer as riskier than when the bond was issued, or rates have risen.")),
        ("Step 2 — (b) Proceeds and discount",
         CALC([("Proceeds", "8,000 × 4.212364 + 200,000 × 0.747258 = 33,699 + 149,452", "€183,151"),
               ("Discount", "200,000 − 183,151", "€16,849")])
         + P("The discount is extra interest: investors accept a 4 per cent coupon only if they pay less today; it is amortised over five years, "
             "so interest expense (6% × carrying amount) exceeds the coupon.")),
        ("Step 3 — (b) Effect on the ratios",
         CALC([("Total debt ratio before", "400,000 ÷ 1,000,000", "40.0%"),
               ("Total debt ratio after", "(400,000 + 183,151) ÷ (1,000,000 + 183,151)", "49.3%"),
               ("TIE before", "150,000 ÷ 20,000", "7.5x"),
               ("TIE after (effective interest)", "150,000 ÷ (20,000 + 6% × 183,151 = 10,989)", "4.84x"),
               ("TIE on the coupon only", "150,000 ÷ (20,000 + 8,000) — overstated", "5.36x")], w=(30, 54, 16))),
    ],
)

m5 = EX("M5", "Working backwards to the required rate", "bonds",
        P("A three-year bond with a face value of €1,000 and an annual coupon of 10 per cent is quoted at €951.96. The coupon "
          "is paid at the end of each year. Determine the required rate implied by that price, showing your reasoning, and say "
          "what it tells you about the market’s view of the issuer."),
        [G(58), L(2)])

m6 = EX("M6", "A bond issued at a discount", "bonds",
        P("Nera Spa issues €500,000 of ten-year bonds carrying a 5 per cent annual coupon at a time when the market requires "
          "7 per cent on debt of this quality.")
        + REQ(["Compute the cash proceeds of the issue.",
               "State the discount and explain what it represents.",
               "State the effect of the issue on the total debt ratio and on times interest earned, given that before the issue the "
               "company had total assets of €4,000,000, total liabilities of €1,600,000, operating income of €600,000 and interest expense of €96,000."]),
        [G(62), L(2)])

# ------------------------------------------------------------------ M.4
we4 = WE(
    "Discount, premium or par without computing; bonds in the statements",
    P("<b>(a)</b> Without computing, say whether each bond prices at a discount, premium or par: coupon 5% / required 5%; 8% / 6%; 3% / 6%; "
      "zero coupon / 4%; 6% / 6% but the issuer is upgraded the next day. "
      "<b>(b)</b> Answer: (1) where does a bond issued at a premium appear and what happens to it over its life? (2) A bond is redeemed early "
      "at a loss — where do the cash paid and the loss go in the cash flow statement?"),
    [
        ("Step 1 — (a) Compare the coupon with the required rate",
         T("""
^Coupon / required | Price | Reason
5% / 5% | <span class="ans">Par</span> | the coupon pays exactly what the market requires
8% / 6% | <span class="ans">Premium</span> | coupon above the required rate: investors pay more for it
3% / 6% | <span class="ans">Discount</span> | coupon below the required rate
Zero coupon / 4% | <span class="ans">Discount</span> | all the return comes from buying below face
6% / 6%, then upgraded | <span class="ans">Premium</span> | lower risk → lower required rate → price rises above par
""", w=(22, 16, 62), cls="small")),
        ("Step 2 — (b) Bonds inside the statements",
         UL(["(1) A <b>non-current liability</b> at its carrying amount = face value + unamortised premium. The premium is amortised each year, "
             "so the carrying amount falls to face value at maturity and interest expense is lower than the coupon paid.",
             "(2) The <b>cash paid</b> to redeem is a financing outflow; the <b>loss</b> is a non-cash item inside net income, added back in the "
             "operating section."])),
    ],
)

m7 = EX("M7", "Discount, premium or par", "bonds",
        P("For each bond, state without computing whether it prices at a discount, at a premium or at par, and give the one-line reason.")
        + T("""
^Bond | Coupon rate | Required rate | Discount / premium / par | Reason
A | 6% | 6% | __ | __
B | 9% | 5% | __ | __
C | 4% | 7% | __ | __
D | 7% | 7%, but the issuer is downgraded the next day | __ | __
E | 0% (zero coupon) | 5% | __ | __
""", w=(7, 14, 22, 19, 38), tall=True),
        [L(1, "Notes")])

m8 = EX("M8", "Bonds inside the financial statements", "bonds",
        P("Answer in three or four lines each.")
        + OL(["Where does a bond issued at a discount appear on the balance sheet, and what happens to that figure over the life of the bond?",
              "Why does the cash flow statement show the proceeds of a bond issue in financing, while the interest paid on the "
              "same bond sits in operating?",
              "Two companies have identical operating businesses. One issued its debt at par at 8 per cent; the other issued at a "
              "deep discount with a 2 per cent coupon and the same 8 per cent effective rate. Which reports the higher times "
              "interest earned if both use the coupon rate to measure interest expense, and what should the analyst do?"]),
        [L(4, "1."), L(4, "2."), L(4, "3.")])

SEC = SECTION(
    "M", "Bonds and present value",
    "Exercises 1-13 and 1-14 of the Subramanyam chapter 1 problem set, which the lecturer listed for Exercise Session 2 and never solved in class.",
    [
        BLOCK("M.1", "Pricing a bond with annual coupons", "Periods remaining, annuity factor, discount factor — and the sanity check.", we1, [m1, m2]),
        BLOCK("M.2", "Semiannual coupons and the required rate", "Halve the rate, double the periods; risk in the required rate.", we2, [m3, m4]),
        BLOCK("M.3", "The implied rate and bonds issued at a discount", "Working back from a price; proceeds, discount and the ratios.", we3, [m5, m6]),
        BLOCK("M.4", "Discount, premium, par — and bonds in the statements", "Answers without computing, and where bonds sit in the statements.", we4, [m7, m8]),
    ],
)
