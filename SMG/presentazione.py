"""Presentazione della strategia SMG (pptx) per l'orale di gennaio."""
import os, pandas as pd
from pptx import Presentation
from pptx.util import Cm, Pt
from pptx.dml.color import RGBColor
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
GROUP = os.environ.get('SMG_GROUP', 'ZZ Capital')
NAVY, BLUE, GOLD, GREY, RED, GREEN = RGBColor(0x1F,0x38,0x64), RGBColor(0x2E,0x75,0xB6), RGBColor(0xC9,0x8B,0x1E), RGBColor(0x59,0x59,0x59), RGBColor(0xC0,0x39,0x2B), RGBColor(0x2E,0x8B,0x57)
p = pd.read_csv('dati/portafoglio_iniziale.csv'); p['cv'] = p.azioni*p.prezzo_acquisto; p['w'] = p.cv/p.cv.sum()
import numpy as np
_px = pd.read_csv('dati/prezzi_lug_ott.csv', index_col=0, parse_dates=True); _r = _px.pct_change().dropna()
_wv = pd.Series(p.w.values, index=p.ticker); _rp = _r[p.ticker] @ _wv
def _sh(rd, mprices):
    m = mprices.resample('ME').last(); rm = m.pct_change().dropna().mean(); return ((1+rm)**12-1-0.04)/(rd.std()*np.sqrt(250))
_mp = (_px[p.ticker].resample('ME').last().pct_change().dropna() @ _wv)
BT = dict(hpr=(1+_rp).prod()-1, spx=(1+_r.SPX).prod()-1, sh=((1+_mp.mean())**12-1-0.04)/(_rp.std()*np.sqrt(250)), shm=_sh(_r.SPX, _px.SPX),
          beta=float(sum(_wv[t]*_r[t].cov(_r.SPX) for t in p.ticker)/_r.SPX.var()), corr=(_r[p.ticker].corr().values.sum()-len(p))/(len(p)*(len(p)-1)))
INV = p.cv.sum()/1e6
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
tx(s, 2, 5, 30, 2.5, 'Buying rising earnings estimates', 44, True, RGBColor(255,255,255))
tx(s, 2, 7.8, 30, 1.5, 'Our strategy for the Stock Market Game 2026', 22, False, RGBColor(0xD9,0xE1,0xF2))
tx(s, 2, 11.5, 30, 3, [f'Group: {GROUP}', 'Cristiano Zonta (909123) and Mattia Zanrosso (909945)', 'Corporate Finance and Financial Institutions 2'], 16, False, RGBColor(0xD9,0xE1,0xF2))

# 2 tesi
s = slide('The strategy in one slide')
card(s, 1.2, 4.3, 10.2, 12.5, 'What we buy', ['US large caps whose analysts are raising their earnings estimates', 'Zacks (1979): estimate revisions move prices most over one to three months, about the length of the game'], BLUE, 17)
card(s, 11.8, 4.3, 10.2, 12.5, 'At what price', ['Median forward P/E of 13x, against 21.5x for the S&P 500', 'With the Fed raising rates we do not expect higher multiples, so prices have to follow earnings'], GOLD, 17)
card(s, 22.4, 4.3, 10.2, 12.5, 'How we combine them', ['Value, growth and momentum stocks', '19 stocks in 7 sectors, at most 25% per sector', f'Weights by conviction, from {p.w.min():.1%} to {p.w.max():.1%}', 'Technology at 19%, beta close to 1'], GREEN, 17)

# 3 macro
s = slide('The economic environment (November 2026)', 'What we expect for the next weeks and how it shaped the portfolio')
items = [('Fed raising rates', 'First hike in three years in September, and officials signal more. The 10-year Treasury yields about 4.9%.', RED),
         ('Inflation', 'Producer prices are rising at the fastest pace since 2022. 47% of fund managers expect stagflation.', RED),
         ('Oil', 'Brent went above $110 in October because of the conflict between the US and Iran. It now moves with news on talks.', GOLD),
         ('AI and chip stocks', 'Tech stocks lost more than $1 trillion of value in one week of October, and chip stocks keep falling.', GOLD),
         ('Valuations', 'The S&P 500 is up about 8% this year and trades at 21.5 times forward earnings.', BLUE),
         ('What we do', 'Buy rising estimates at low multiples, mix styles and sectors, and hold energy against an oil shock.', GREEN)]
for i, (h, b, c) in enumerate(items): card(s, 1.2 + (i % 3)*10.6, 4.4 + (i // 3)*6.6, 10.2, 6.2, h, b, c, 16)

# 4 metodo
s = slide('Methodology: rebuilding the Zacks Rank', 'Revision score computed for 151 US large caps')
crit = [('Agreement, 40%', 'Share of upward EPS revisions in the last 30 days. Zacks weighs this criterion most'), ('Magnitude, 25%', 'Change of the consensus EPS estimate over 60 days'),
        ('Broker opinion, 20%', 'Average Broker Recommendation (ABR, 1 = Strong Buy)'), ('Upside, 15%', 'Analysts\' price target vs current price'),
        ('Surprise, used as a check', 'Average EPS surprise over the last 4 quarters')]
for i, (h, b) in enumerate(crit): card(s, 1.2, 4.3 + i*2.6, 15.5, 2.4, h, b, BLUE, 11)
fun = [('151', 'large caps screened'), ('38', 'candidates with positive revisions and ABR ≤ 2.5'), ('19', 'stocks in the portfolio'), ('25', 'stocks in the watch list')]
for i, (v, l) in enumerate(fun):
    w = 14 - i*2; x = 17.5 + (15 - w)/2; b = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Cm(x), Cm(4.4 + i*3.3), Cm(w), Cm(2.9)); b.fill.solid(); b.fill.fore_color.rgb = [NAVY, BLUE, GREEN, GOLD][i]; b.line.fill.background()
    tx(s, x, 4.5 + i*3.3, w, 2.8, [v, l], 13, True, RGBColor(255,255,255), PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
tx(s, 1.2, 17.15, 31, 0.8, 'Score = 0.40·z(Agreement) + 0.25·z(Magnitude) + 0.20·z(−ABR) + 0.15·z(Upside). The signal works over a short horizon and favours smaller companies and fashionable industries.', 10, color=GREY)

# 5 regole di stile
s = slide('Screening rules by investment style')
card(s, 1.2, 4.0, 10.2, 8.2, 'Value  (44%)', ['Forward P/E < 14', 'P/B < 3.5', 'Energy, banks, managed care, steel, telecom', 'Gain from oil prices and higher rates'], BLUE, 16)
card(s, 11.8, 4.0, 10.2, 8.2, 'Growth at a reasonable price  (40%)', ['EPS growth > 25%', 'PEG < 1.6', 'AI hardware, grid infrastructure, asset management', 'Earnings already growing'], GOLD, 16)
card(s, 22.4, 4.0, 10.2, 8.2, 'Momentum  (16%)', ['6-month return > 20%', '3-month return > 5%', 'Healthcare leaders and payments', 'Rising prices and rising estimates'], GREEN, 16)
card(s, 1.2, 12.7, 31.4, 4.6, 'Portfolio constraints', [f'At most 25% per sector and three technology stocks. 19 stocks (the rules allow 10 to 30). {INV:.1%} invested after the first purchase (minimum 95%). No utilities, real estate or consumer discretionary, which suffer most from higher rates and weak spending.'], NAVY, 13)

# 6 portafoglio
s = slide('The initial portfolio'); tx(s, 22, 2.75, 11, 0.5, 'Market orders executed on 24/11/2026 at the prices shown in the Excel file', 9, color=GREY, align=PP_ALIGN.RIGHT)
rows = [['Ticker', 'Company', 'Sector', 'Style', 'Shares', 'Weight']] + [[r.ticker, r.nome.replace('ExxonMobil Holdings Corporation', 'Exxon Mobil Corp.')[:28], SHORT.get(r.settore, r.settore), r.stile, f'{r.azioni:,}', f'{r.w:.1%}'] for _, r in p.sort_values('w', ascending=False).iterrows()]
t = s.shapes.add_table(len(rows), 6, Cm(1.2), Cm(3.4), Cm(31.4), Cm(14.0)).table
for j, wdt in enumerate([3, 10, 6.4, 4.5, 3.5, 4]): t.columns[j].width = Cm(wdt)
for i, row in enumerate(rows):
    for j, v in enumerate(row):
        c = t.cell(i, j); c.text = v; para = c.text_frame.paragraphs[0]; para.runs[0].font.size = Pt(10.5); para.runs[0].font.bold = i == 0
        if j >= 4: para.alignment = PP_ALIGN.RIGHT
        c.margin_top = c.margin_bottom = Cm(0.02)
        if i == 0: c.fill.solid(); c.fill.fore_color.rgb = NAVY
        else: c.fill.solid(); c.fill.fore_color.rgb = RGBColor(0xEE,0xF2,0xF8) if i % 2 else RGBColor(255,255,255); para.runs[0].font.color.rgb = RGBColor(0x26,0x26,0x26)
    t.rows[i].height = Cm(0.69)

# 7 allocazione
s = slide('Diversification: sectors and styles')
sec = p.groupby('settore').w.sum().sort_values(ascending=False); sty = p.groupby('stile').w.sum().reindex(['Value', 'Growth', 'Momentum'])
for (ser, x, ttl, typ) in [(sec, 1.2, 'Weight by sector', XL_CHART_TYPE.BAR_CLUSTERED), (sty, 17.5, 'Weight by style', XL_CHART_TYPE.DOUGHNUT)]:
    cd = CategoryChartData(); cd.categories = [SHORT.get(k, k) for k in ser.index]; cd.add_series('Weight', [round(v, 4) for v in ser.values])
    ch = s.shapes.add_chart(typ, Cm(x), Cm(3.2), Cm(15.5), Cm(13.5), cd).chart; ch.has_title = True; ch.chart_title.text_frame.text = ttl
    pl = ch.plots[0]; pl.has_data_labels = True; pl.data_labels.number_format = '0%'; pl.data_labels.number_format_is_linked = False; pl.data_labels.font.size = Pt(12)
    if typ == XL_CHART_TYPE.BAR_CLUSTERED: ch.has_legend = False; ch.value_axis.visible = False; ch.category_axis.reverse_order = True; ch.value_axis.has_major_gridlines = False; pl.series[0].format.fill.solid(); pl.series[0].format.fill.fore_color.rgb = BLUE
    else: ch.has_legend = True; ch.legend.position = XL_LEGEND_POSITION.BOTTOM; ch.legend.include_in_layout = False
tx(s, 1.2, 16.9, 31, 1, 'Technology is 19% of the portfolio against about 33% of the S&P 500. Energy offsets an oil shock; healthcare holds up in a slowdown.', 12, color=NAVY)

# 8 parametri
s = slide('Valuation and revision profile of the portfolio')
kp = [(f'{p.PE_fwd.median():.1f}x', 'median forward P/E\n(S&P 500 ≈ 21.5x)'), (f'{p.PEG.median():.2f}', 'median PEG'), (f'{p.ABR.median():.2f}', 'median ABR\n(1 = Strong Buy)'),
      (f'{(p.rev_su_30g.sum()/(p.rev_su_30g.sum()+p.rev_giu_30g.sum())):.0%}', 'of EPS revisions in the\nlast 30 days are upward'), (f'+{p["surprise_4q_%"].median():.1f}%', 'median EPS surprise\nlast 4 quarters')]
for i, (v, l) in enumerate(kp): kpi(s, 1.2 + i*6.3, 4.5, 6.0, v, l)
card(s, 1.2, 10.3, 31.4, 6.8, 'What the numbers say', ['Analysts raised estimates on almost every holding in the last month, the companies beat their last four earnings forecasts by a median of 9%, and we pay about 13 times expected earnings against 21.5 for the market.'], NAVY, 17)

# 9 backtest
s = slide('Back-test of the initial portfolio, July to October 2026', 'Same weights, daily dividend-adjusted closes, S&P 500 as the market')
for i, (v, l, c) in enumerate([(f'{BT["hpr"]:+.1%}', 'portfolio holding-period return', GREEN), (f'{BT["spx"]:+.1%}', 'S&P 500 return', GREY), (f'{BT["sh"]:.2f}', 'portfolio Sharpe ratio (Rf = 4%)', GREEN), (f'{BT["shm"]:.2f}'.replace('-', '−'), 'S&P 500 Sharpe ratio', GREY), (f'{BT["beta"]:.2f}', 'portfolio beta against the S&P 500', NAVY), (f'{BT["corr"]:.2f}', 'average correlation between pairs of stocks', NAVY)]):
    kpi(s, 1.2 + (i % 3)*10.6, 4.6 + (i // 3)*4.2, 10.2, v, l, c)
card(s, 1.2, 13.3, 31.4, 4.2, 'Look-ahead bias', ['We chose the stocks with momentum and revisions measured in November, which partly reflect July to October. The back-test therefore overstates the strategy; the trading period from 24/11 to 18/12 is the real test.'], RED, 13)

# 10 piano trading
s = slide('Trading plan, 24 November to 18 December')
card(s, 1.2, 4.0, 15.5, 13.3, 'Rules for our trades (at least 5)', ['Sell when estimates start to be cut (Agreement below 0) or the Zacks Rank falls to 4 or 5', 'Sell or reduce after a 10% fall that the market does not explain', 'Reduce any position above 10% of the portfolio', 'Replace it with the best-scoring watch-list stock of the same style', 'Spread trades over the period so their effect can be measured'], BLUE, 16)
card(s, 17.1, 4.0, 15.5, 13.3, 'Watch list (25 stocks) and what would make us buy', ['Oil upside: OXY, COP, PSX', 'AI rebound: ANET, AMD, NVDA, AVGO, KLAC, TXN', 'Grid and power: GEV, ETN, CEG', 'Defensive health: CVS, CI, TMO, ISRG, HCA', 'Rates and insurance: AIG, MET, CB, TRV, plus V', 'Others: PH, RTX, ORLY'], GOLD, 16)

# 11 rischi
s = slide('Main risks and how we manage them')
rk = [('Oil price collapse after a peace deal', 'Energy is 19% of the portfolio. Refiners depend less on crude prices, and we did not buy OXY or COP.'), ('More Fed hikes', 'Our multiples are low, banks earn more with higher rates, and we hold no utilities or REITs.'),
      ('A deeper fall in AI and chip stocks', 'We hold three technology stocks (19%). MU cost about 3 times expected earnings.'), ('Policy risk for health insurers', 'Healthcare is capped at 25% and split between insurers, biotech, drug distribution and lab tools.'),
      ('Model risk', 'Revisions are a short-term signal. We check them every week and rely on valuation and diversification too.')]
for i, (h, b) in enumerate(rk): card(s, 1.2, 3.9 + i*2.8, 31.4, 2.6, h, b, [RED, RED, GOLD, GOLD, BLUE][i], 12)

# 12 formule
s = slide('Formulas used in the Excel analysis')
fm = ['Daily return:  r(t) = (P(t) − P(t−1)) / P(t−1)', 'Portfolio return:  R(p,t) = Σ w(i)·r(i,t)', 'Geometric mean:  [Π(1 + r(t))]^(1/T) − 1;   HPR = Π(1 + r(t)) − 1',
      'Risk:  sample variance VAR.S and standard deviation STDEV.S of returns', 'Beta:  β(i) = Cov(r(i), R(m)) / Var(R(m));   β(p) = Σ w(i)·β(i)',
      'Sharpe:  (R(p,annual) − Rf) / σ(p,annual),  R(annual) = (1 + R(monthly))^12 − 1,  σ(annual) = σ(daily)·√250']
for i, f_ in enumerate(fm): tx(s, 1.5, 4.0 + i*2.25, 31, 2, '•  ' + f_, 17, False, NAVY)

os.makedirs('out', exist_ok=True); prs.save('out/presentazione_strategia.pptx'); print('ok', len(prs.slides))
