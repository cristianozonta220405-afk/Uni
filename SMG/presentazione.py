"""Presentazione della strategia SMG (pptx) per l'orale di gennaio."""
import os, pandas as pd
from pptx import Presentation
from pptx.util import Cm, Pt
from pptx.dml.color import RGBColor
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
GROUP = os.environ.get('SMG_GROUP', '[GROUP NAME]')
NAVY, BLUE, GOLD, GREY, RED, GREEN = RGBColor(0x1F,0x38,0x64), RGBColor(0x2E,0x75,0xB6), RGBColor(0xC9,0x8B,0x1E), RGBColor(0x59,0x59,0x59), RGBColor(0xC0,0x39,0x2B), RGBColor(0x2E,0x8B,0x57)
p = pd.read_csv('dati/portafoglio_iniziale.csv'); p['cv'] = p.azioni*p.prezzo_acquisto; p['w'] = p.cv/p.cv.sum()
SHORT = {'Financial Services': 'Financials', 'Communication Services': 'Communication', 'Basic Materials': 'Materials'}
prs = Presentation(); prs.slide_width, prs.slide_height = Cm(33.867), Cm(19.05); BL = prs.slide_layouts[6]
def tx(s, x, y, w, h, text, size=16, bold=False, color=GREY, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tb = s.shapes.add_textbox(Cm(x), Cm(y), Cm(w), Cm(h)); tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    for i, line in enumerate(text if isinstance(text, list) else [text]):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); para.alignment = align
        r = para.add_run(); r.text = line; r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color; r.font.name = 'Calibri'; para.space_after = Pt(6)
    return tb
def slide(title, sub=None):
    s = prs.slides.add_slide(BL); bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Cm(2.6)); bar.fill.solid(); bar.fill.fore_color.rgb = NAVY; bar.line.fill.background()
    tx(s, 1.2, 0.45, 30, 1.6, title, 26, True, RGBColor(255,255,255), anchor=MSO_ANCHOR.MIDDLE)
    if sub: tx(s, 1.2, 2.9, 31, 1, sub, 14, False, BLUE)
    tx(s, 1.2, 18.0, 25, 0.8, f'Stock Market Game 2026  |  {GROUP}', 9, color=GREY); tx(s, 30.5, 18.0, 2.5, 0.8, str(len(prs.slides)), 9, color=GREY, align=PP_ALIGN.RIGHT)
    return s
def card(s, x, y, w, h, head, body, col=BLUE, size=13):
    b = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Cm(x), Cm(y), Cm(w), Cm(h)); b.fill.solid(); b.fill.fore_color.rgb = RGBColor(0xF2,0xF5,0xFA); b.line.color.rgb = col; b.adjustments[0] = 0.06
    tx(s, x + 0.4, y + 0.3, w - 0.8, 1.2, head, 15, True, col); tx(s, x + 0.4, y + 1.4, w - 0.8, h - 1.6, body, size)
def kpi(s, x, y, w, val, lab, col=NAVY):
    tx(s, x, y, w, 1.8, val, 34, True, col, PP_ALIGN.CENTER); tx(s, x, y + 1.9, w, 1.2, lab, 12, False, GREY, PP_ALIGN.CENTER)

# 1 titolo
s = prs.slides.add_slide(BL); bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height); bg.fill.solid(); bg.fill.fore_color.rgb = NAVY; bg.line.fill.background()
tx(s, 2, 5, 30, 2.5, 'Riding Earnings Revisions', 44, True, RGBColor(255,255,255))
tx(s, 2, 7.8, 30, 1.5, 'A multi-style, valuation-disciplined strategy for an uncertain market', 22, False, RGBColor(0xD9,0xE1,0xF2))
tx(s, 2, 11.5, 30, 3, [f'Group: {GROUP}', 'Stock Market Game 2026 – Corporate Finance and Financial Institutions 2'], 16, False, RGBColor(0xD9,0xE1,0xF2))

# 2 tesi
s = slide('Our investment thesis in one slide')
card(s, 1.2, 4.3, 10.2, 12.5, '1 · What we buy', ['US large caps whose analysts are RAISING earnings estimates', 'Zacks: estimate revisions are the strongest short-term driver of prices (1–3 months = length of the game)'], BLUE, 17)
card(s, 11.8, 4.3, 10.2, 12.5, '2 · At what price', ['Only at reasonable multiples', 'Median forward P/E ≈ 13x vs ≈ 21.5x for the S&P 500', 'Returns must come from earnings, not from re-rating, when the Fed is hiking'], GOLD, 17)
card(s, 22.4, 4.3, 10.2, 12.5, '3 · How we combine', ['Three styles: Value · Growth (GARP) · Momentum', '19 stocks, 7 sectors, max 25% per sector', 'Conviction weights (2.7%–8.1%)', 'Beta ≈ 1, technology underweight'], GREEN, 17)

# 3 macro
s = slide('The economic environment (November 2026)', 'Why a defensive, earnings-driven approach makes sense now')
items = [('Hawkish Fed', 'First hike in three years in September; officials lean towards more hikes. 10-year Treasury ≈ 4.9%.', RED),
         ('Sticky inflation', 'Producer prices rising at the fastest pace since 2022; 47% of fund managers see stagflation.', RED),
         ('Oil shock', 'US–Iran conflict: Brent above $110 in October, now volatile on diplomacy hopes.', GOLD),
         ('AI / chip selloff', 'More than $1 trillion of tech value lost in one week in October; semiconductors still under pressure.', GOLD),
         ('Rich valuations', 'S&P 500 up ≈ 8% YTD at ≈ 21.5x forward earnings.', BLUE),
         ('Our answer', 'Rising estimates + low multiples + style and sector diversification + energy as an inflation hedge.', GREEN)]
for i, (h, b, c) in enumerate(items): card(s, 1.2 + (i % 3)*10.6, 4.4 + (i // 3)*6.6, 10.2, 6.2, h, b, c, 16)

# 4 metodo
s = slide('Methodology: rebuilding the Zacks Rank', 'Revision score computed for 151 US large caps')
crit = [('Agreement · 40%', 'Share of upward EPS revisions in the last 30 days (the most important Zacks criterion)'), ('Magnitude · 25%', 'Change of the consensus EPS estimate over 60 days'),
        ('Broker view · 20%', 'Average Broker Recommendation (ABR, 1 = Strong Buy)'), ('Upside · 15%', 'Analysts\' price target vs current price'),
        ('Surprise · check', 'Average EPS surprise over the last 4 quarters')]
for i, (h, b) in enumerate(crit): card(s, 1.2, 4.3 + i*2.6, 15.5, 2.4, h, b, BLUE, 11)
fun = [('151', 'large caps screened'), ('38', 'candidates with positive revisions and ABR ≤ 2.5'), ('19', 'stocks in the portfolio'), ('25', 'stocks in the watch list')]
for i, (v, l) in enumerate(fun):
    w = 14 - i*2; x = 17.5 + (15 - w)/2; b = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Cm(x), Cm(4.4 + i*3.3), Cm(w), Cm(2.9)); b.fill.solid(); b.fill.fore_color.rgb = [NAVY, BLUE, GREEN, GOLD][i]; b.line.fill.background()
    tx(s, x, 4.5 + i*3.3, w, 2.8, [v, l], 13, True, RGBColor(255,255,255), PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
tx(s, 1.2, 17.15, 31, 0.8, 'Score = 0.40·z(Agreement) + 0.25·z(Magnitude) + 0.20·z(−ABR) + 0.15·z(Upside). Zacks Rank used as confirmation, aware of its limits (short horizon, size and industry biases).', 10, color=GREY)

# 5 regole di stile
s = slide('Screening rules by investment style')
card(s, 1.2, 4.0, 10.2, 8.2, 'Value  (44%)', ['Forward P/E < 14', 'P/B < 3.5', 'Energy, banks, managed care, steel, telecom', 'Benefit from oil prices and higher rates'], BLUE, 16)
card(s, 11.8, 4.0, 10.2, 8.2, 'Growth at a reasonable price  (40%)', ['EPS growth > 25%', 'PEG < 1.6', 'AI hardware, grid infrastructure, asset management', 'Real earnings behind the story'], GOLD, 16)
card(s, 22.4, 4.0, 10.2, 8.2, 'Momentum  (16%)', ['6-month return > 20%', '3-month return > 5%', 'Healthcare leaders and payments', 'Trend + rising estimates'], GREEN, 16)
card(s, 1.2, 12.7, 31.4, 4.6, 'Portfolio constraints', ['Max 25% per sector  ·  max 3 technology names  ·  10–30 stocks (we hold 19)  ·  ≥ 95% invested (we invest ≈ 96.6%)  ·  no utilities, real estate, consumer discretionary (rate- and stagflation-sensitive)'], NAVY, 13)

# 6 portafoglio
s = slide('The initial portfolio'); tx(s, 22, 2.75, 11, 0.5, 'Market orders of 24/11/2026 – preview prices, fills pending', 9, color=GREY, align=PP_ALIGN.RIGHT)
rows = [['Ticker', 'Company', 'Sector', 'Style', 'Shares', 'Weight']] + [[r.ticker, r.nome.replace('ExxonMobil Holdings Corporation', 'Exxon Mobil Corp.')[:28], SHORT.get(r.settore, r.settore), r.stile, f'{r.azioni:,}', f'{r.w:.1%}'] for _, r in p.sort_values('w', ascending=False).iterrows()]
t = s.shapes.add_table(len(rows), 6, Cm(1.2), Cm(3.1), Cm(31.4), Cm(14.6)).table
for j, wdt in enumerate([3, 10, 6.4, 4.5, 3.5, 4]): t.columns[j].width = Cm(wdt)
for i, row in enumerate(rows):
    for j, v in enumerate(row):
        c = t.cell(i, j); c.text = v; para = c.text_frame.paragraphs[0]; para.runs[0].font.size = Pt(10.5); para.runs[0].font.bold = i == 0
        if j >= 4: para.alignment = PP_ALIGN.RIGHT
        c.margin_top = c.margin_bottom = Cm(0.02)
        if i == 0: c.fill.solid(); c.fill.fore_color.rgb = NAVY
        else: c.fill.solid(); c.fill.fore_color.rgb = RGBColor(0xEE,0xF2,0xF8) if i % 2 else RGBColor(255,255,255); para.runs[0].font.color.rgb = RGBColor(0x26,0x26,0x26)
    t.rows[i].height = Cm(0.72)

# 7 allocazione
s = slide('Diversification: sectors and styles')
sec = p.groupby('settore').w.sum().sort_values(ascending=False); sty = p.groupby('stile').w.sum().reindex(['Value', 'Growth', 'Momentum'])
for (ser, x, ttl, typ) in [(sec, 1.2, 'Weight by sector', XL_CHART_TYPE.BAR_CLUSTERED), (sty, 17.5, 'Weight by style', XL_CHART_TYPE.DOUGHNUT)]:
    cd = CategoryChartData(); cd.categories = [SHORT.get(k, k) for k in ser.index]; cd.add_series('Weight', [round(v, 4) for v in ser.values])
    ch = s.shapes.add_chart(typ, Cm(x), Cm(3.2), Cm(15.5), Cm(13.5), cd).chart; ch.has_title = True; ch.chart_title.text_frame.text = ttl
    pl = ch.plots[0]; pl.has_data_labels = True; pl.data_labels.number_format = '0%'; pl.data_labels.number_format_is_linked = False; pl.data_labels.font.size = Pt(12)
    if typ == XL_CHART_TYPE.BAR_CLUSTERED: ch.has_legend = False; ch.value_axis.visible = False; ch.category_axis.reverse_order = True; ch.value_axis.has_major_gridlines = False; pl.series[0].format.fill.solid(); pl.series[0].format.fill.fore_color.rgb = BLUE
    else: ch.has_legend = True; ch.legend.position = XL_LEGEND_POSITION.BOTTOM; ch.legend.include_in_layout = False
tx(s, 1.2, 16.9, 31, 1, 'Technology 19% vs ≈ 33% in the S&P 500 · energy as a natural hedge against the oil-driven inflation shock · healthcare as the defensive core', 12, color=NAVY)

# 8 parametri
s = slide('Valuation and revision profile of the portfolio')
kp = [(f'{p.PE_fwd.median():.1f}x', 'median forward P/E\n(S&P 500 ≈ 21.5x)'), (f'{p.PEG.median():.2f}', 'median PEG'), (f'{p.ABR.median():.2f}', 'median ABR\n(1 = Strong Buy)'),
      (f'{(p.rev_su_30g.sum()/(p.rev_su_30g.sum()+p.rev_giu_30g.sum())):.0%}', 'of EPS revisions in the\nlast 30 days are upward'), (f'+{p["surprise_4q_%"].median():.1f}%', 'median EPS surprise\nlast 4 quarters')]
for i, (v, l) in enumerate(kp): kpi(s, 1.2 + i*6.3, 4.5, 6.0, v, l)
card(s, 1.2, 10.3, 31.4, 6.8, 'How to read it', ['Analysts are raising estimates on almost all our names, the companies keep beating expectations, and we pay well below the market multiple.',
     'That is exactly the combination Zacks research associates with outperformance over a 1–3 month horizon.'], NAVY, 17)

# 9 backtest
s = slide('Back-test of the initial portfolio: July–October 2026', 'Same weights, daily dividend-adjusted closes, market = S&P 500')
for i, (v, l, c) in enumerate([('+14.3%', 'portfolio holding-period return', GREEN), ('+1.1%', 'S&P 500 return', GREY), ('3.38', 'portfolio Sharpe ratio (Rf = 4%)', GREEN), ('−0.06', 'S&P 500 Sharpe ratio', GREY), ('0.71', 'portfolio beta (vs S&P 500)', NAVY), ('0.05', 'average pairwise correlation', NAVY)]):
    kpi(s, 1.2 + (i % 3)*10.6, 4.6 + (i // 3)*4.2, 10.2, v, l, c)
card(s, 1.2, 13.3, 31.4, 4.2, 'Honest caveat (look-ahead bias)', ['Momentum and revisions measured today partly reflect July–October performance, so the back-test flatters the strategy. The real test is the trading period (24/11–18/12).'], RED, 13)

# 10 piano trading
s = slide('Trading plan for 24 November – 18 December')
card(s, 1.2, 4.0, 15.5, 13.3, 'Rules for our (≥ 5) trades', ['SELL when estimates start being cut (Agreement < 0) or the Zacks Rank falls to 4–5', 'SELL / TRIM after a −10% drawdown not explained by the market', 'TRIM any position above 10% of the portfolio', 'BUY from the watch list the best-scoring replacement in the same style', 'Trades spread over the period (not all in the last days) to measure their effect'], BLUE, 16)
card(s, 17.1, 4.0, 15.5, 13.3, 'Watch list (25 stocks) and triggers', ['Oil upside: OXY, COP, PSX', 'AI rebound: ANET, AMD, NVDA, AVGO, KLAC, TXN', 'Grid and power: GEV, ETN, CEG', 'Defensive health: CVS, CI, TMO, ISRG, HCA', 'Rates and insurance: AIG, MET, CB, TRV, V', 'Others: PH, RTX, ORLY'], GOLD, 16)

# 11 rischi
s = slide('Main risks and how we manage them')
rk = [('Oil price collapse (peace deal)', '≈ 19% in energy; refiners less exposed to crude prices; OXY/COP not bought.'), ('Further Fed hikes', 'Low multiples, banks and insurers benefit from higher rates; no utilities or REITs.'),
      ('Deeper AI / chip selloff', 'Only 3 tech names (19%); MU bought at ≈ 3x forward earnings.'), ('Policy risk on managed care', 'Healthcare capped at 25%, split between insurers, biotech, distribution and tools.'),
      ('Model risk (Zacks limits)', 'Revisions are a short-term signal; combined with valuation and diversification, reviewed weekly.')]
for i, (h, b) in enumerate(rk): card(s, 1.2, 3.9 + i*2.8, 31.4, 2.6, h, b, [RED, RED, GOLD, GOLD, BLUE][i], 12)

# 12 formule
s = slide('Key formulas we use in the Excel analysis')
fm = ['Daily return:  r(t) = (P(t) − P(t−1)) / P(t−1)', 'Portfolio return:  R(p,t) = Σ w(i)·r(i,t)', 'Geometric mean:  [Π(1 + r(t))]^(1/T) − 1;   HPR = Π(1 + r(t)) − 1',
      'Risk:  sample variance VAR.S and standard deviation STDEV.S of returns', 'Beta:  β(i) = Cov(r(i), R(m)) / Var(R(m));   β(p) = Σ w(i)·β(i)',
      'Sharpe:  (R(p,annual) − Rf) / σ(p,annual),  R(annual) = (1 + R(monthly))^12 − 1,  σ(annual) = σ(daily)·√250']
for i, f_ in enumerate(fm): tx(s, 1.5, 4.0 + i*2.25, 31, 2, '•  ' + f_, 17, False, NAVY)

os.makedirs('out', exist_ok=True); prs.save('out/presentazione_strategia.pptx'); print('ok', len(prs.slides))
