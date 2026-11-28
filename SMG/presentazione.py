"""Presentazione strategia SMG - stile 'steel blue / pixel' (riferimento grafico dell'utente)."""
import os, numpy as np, pandas as pd
from pptx import Presentation
from pptx.util import Cm, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree

GROUP = os.environ.get('SMG_GROUP', 'ZZ Capital')
p = pd.read_csv('dati/portafoglio_iniziale.csv'); p['cv'] = p.azioni*p.prezzo_acquisto; p['w'] = p.cv/p.cv.sum(); INV = p.cv.sum()/1e6
_px = pd.read_csv('dati/prezzi_lug_ott.csv', index_col=0, parse_dates=True); _r = _px.pct_change().dropna()
_wv = pd.Series(p.w.values, index=p.ticker); _rp = _r[p.ticker] @ _wv
_mp = _px[p.ticker].resample('ME').last().pct_change().dropna() @ _wv
_mm = _px.SPX.resample('ME').last().pct_change().dropna()
BT = dict(hpr=(1+_rp).prod()-1, spx=(1+_r.SPX).prod()-1, sh=((1+_mp.mean())**12-1-0.04)/(_rp.std()*np.sqrt(250)),
          shm=((1+_mm.mean())**12-1-0.04)/(_r.SPX.std()*np.sqrt(250)), beta=float(sum(_wv[t]*_r[t].cov(_r.SPX) for t in p.ticker)/_r.SPX.var()),
          corr=(_r[p.ticker].corr().values.sum()-len(p))/(len(p)*(len(p)-1)))
SHORT = {'Financial Services': 'Financials', 'Communication Services': 'Communication', 'Basic Materials': 'Materials'}

# ---------------- stile ----------------
HEAD, BODY, MONO = 'Aptos Display', 'Aptos', 'Aptos Mono'
INK, INK2, WHITE = RGBColor(0x0F,0x1B,0x2A), RGBColor(0x4A,0x58,0x68), RGBColor(0xF2,0xF5,0xF8)
MUTED_D, ACC_D, ACC_L = RGBColor(0xA9,0xBC,0xCB), RGBColor(0x9F,0xC6,0xE6), RGBColor(0x3D,0x6A,0x8E)
BLACK = RGBColor(0x0B,0x0F,0x14); LINE_L = RGBColor(0xC9,0xD0,0xDB)
SW, SH = Cm(33.867), Cm(19.05); M = 1.9  # margine
prs = Presentation(); prs.slide_width, prs.slide_height = SW, SH; BL = prs.slide_layouts[6]

def alpha(shape_fill_el, a):
    """Imposta trasparenza (a = opacità 0-1) sul solidFill dello shape."""
    sf = shape_fill_el.find(qn('a:solidFill')); clr = sf[0]
    for old in clr.findall(qn('a:alpha')): clr.remove(old)
    e = etree.SubElement(clr, qn('a:alpha')); e.set('val', str(int(a*100000)))
def T(s, x, y, w, h, text, size=14, color=INK, font=BODY, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=1.0, after=0, bold=False):
    tb = s.shapes.add_textbox(Cm(x), Cm(y), Cm(w), Cm(h)); tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    lines = text if isinstance(text, list) else [text]
    for i, line in enumerate(lines):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); para.alignment = align; para.line_spacing = spacing; para.space_after = Pt(after)
        parts = line if isinstance(line, list) else [(line, color)]
        for txt, c in parts:
            r = para.add_run(); r.text = txt; f = r.font; f.size = Pt(size); f.color.rgb = c; f.name = font; f.bold = bold
    return tb
def rect(s, x, y, w, h, fill=None, line=None, radius=0.06, a=None, la=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    sh = s.shapes.add_shape(shape, Cm(x), Cm(y), Cm(w), Cm(h))
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE: sh.adjustments[0] = radius
    if fill is None: sh.fill.background()
    else:
        sh.fill.solid(); sh.fill.fore_color.rgb = fill
        if a is not None: alpha(sh._element.spPr, a)
    if line is None: sh.line.fill.background()
    else:
        sh.line.color.rgb = line; sh.line.width = Pt(0.75)
        if la is not None: alpha(sh._element.spPr.find(qn('a:ln')), la)
    sh.shadow.inherit = False; sh.text_frame.text = ''
    return sh
def pic(s, path, x, y, w, h, rounded=None):
    pc = s.shapes.add_picture(path, Cm(x), Cm(y), Cm(w), Cm(h))
    if rounded is not None: pc.auto_shape_type = MSO_SHAPE.ROUNDED_RECTANGLE; pc._element.spPr.find(qn('a:prstGeom')).find(qn('a:avLst')).append(etree.fromstring(f'<a:gd xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="adj" fmla="val {int(rounded*100000)}"/>'))
    return pc
def pill(s, x, y, label, num, dark):
    c = WHITE if dark else INK
    w = 0.35 + len(label) * 0.2 + 0.9
    rect(s, x, y, w, 0.62, None, WHITE if dark else INK2, 0.5, la=0.5 if dark else 0.6)
    T(s, x + 0.3, y + 0.12, w - 1, 0.4, label, 8, c, MONO)
    rect(s, x + w - 0.62, y + 0.08, 0.46, 0.46, WHITE if dark else INK, None, 0.2)
    T(s, x + w - 0.62, y + 0.15, 0.46, 0.35, num, 7, INK if dark else WHITE, MONO, PP_ALIGN.CENTER)
def slide(dark, tag, num, bgimg=None, cubes=False):
    s = prs.slides.add_slide(BL)
    pic(s, bgimg or ('assets/bg_dark.png' if dark else 'assets/bg_light.png'), 0, 0, 33.867, 19.05)
    if cubes: pic(s, 'assets/cubes.png', 25.6, -1.0, 8.6, 8.6)
    pill(s, M, 1.5, tag, f'{len(prs.slides):02d}', dark)
    T(s, M, 18.0, 15, 0.5, f'{GROUP}  /  Stock Market Game 2026', 7.5, MUTED_D if dark else INK2, MONO)
    T(s, 33.867 - M - 3, 18.0, 3, 0.5, f'{len(prs.slides):02d}', 7.5, MUTED_D if dark else INK2, MONO, PP_ALIGN.RIGHT)
    return s
def title(s, x, y, w, parts, size=34, dark=False):
    base = WHITE if dark else INK; acc = ACC_D if dark else ACC_L
    lines = []
    for line in parts: lines.append([(t, acc if hl else base) for t, hl in line])
    return T(s, x, y, w, 4, lines, size, base, HEAD, spacing=0.95)
def card(s, x, y, w, h, kind, head, body, num=None, hsize=19, bsize=9.5):
    if kind == 'grad': pic(s, 'assets/card_grad.png', x, y, w, h, rounded=0.05); hc, bc, ic = WHITE, RGBColor(0xDD,0xE6,0xEE), WHITE
    elif kind == 'imgdark': pic(s, 'assets/card_dark.png', x, y, w, h, rounded=0.05); hc, bc, ic = WHITE, RGBColor(0xDD,0xE6,0xEE), WHITE
    elif kind == 'black': rect(s, x, y, w, h, BLACK, None, 0.05); hc, bc, ic = WHITE, MUTED_D, WHITE
    elif kind == 'white': rect(s, x, y, w, h, RGBColor(0xFA,0xFB,0xFD), None, 0.05); hc, bc, ic = INK, INK2, INK
    elif kind == 'glass': rect(s, x, y, w, h, RGBColor(0xFF,0xFF,0xFF), RGBColor(0xFF,0xFF,0xFF), 0.06, a=0.07, la=0.18); hc, bc, ic = WHITE, MUTED_D, WHITE
    if num:
        rect(s, x + 0.55, y + 0.55, 0.75, 0.75, RGBColor(0xFF,0xFF,0xFF) if kind != 'white' else INK, None, 0.2, a=0.18 if kind != 'white' else None)
        T(s, x + 0.55, y + 0.72, 0.75, 0.4, num, 8, ic if kind != 'white' else WHITE, MONO, PP_ALIGN.CENTER)
    BODY_H = 1.9 if body else 0
    head_lines = head.count('\n') + 1; head_h = hsize * 0.036 * head_lines
    T(s, x + 0.55, y + h - 0.6 - BODY_H - 0.5 - head_h, w - 1.1, head_h + 0.3, head.split('\n'), hsize, hc, HEAD, spacing=0.95)
    if body: T(s, x + 0.55, y + h - 0.6 - BODY_H, w - 1.1, BODY_H, body, bsize, bc, MONO, spacing=1.08)

# ================= 01 copertina =================
s = slide(True, 'ZZ Capital', '01')
title(s, M, 6.2, 22, [[('Buying ', False), ('rising earnings', True)], [('estimates at a fair price', False)]], 46, True)
T(s, M, 10.6, 18, 1, 'Our strategy for the Stock Market Game 2026', 15, MUTED_D, BODY)
T(s, M, 15.2, 10, 1.6, ['Cristiano Zonta  909123  (spokesperson)', 'Mattia Zanrosso  909945'], 9, WHITE, MONO, spacing=1.3)
T(s, 14.2, 15.2, 10, 1.6, ['Corporate Finance and', 'Financial Institutions 2'], 9, WHITE, MONO, spacing=1.3)
T(s, 24.2, 15.2, 8, 1.6, ['Ca\' Foscari University', 'November 2026'], 9, WHITE, MONO, spacing=1.3)

# ================= 02 strategia =================
s = slide(False, 'Strategy', '02', cubes=True)
title(s, M, 2.9, 22, [[('The strategy in one slide', False)]], 34)
cw = (33.867 - 2*M - 2*0.5) / 3
card(s, M, 6.2, cw, 10.8, 'grad', 'What\nwe buy', 'US large caps whose analysts are raising their earnings estimates. Zacks (1979): revisions move prices most over one to three months.', '01')
card(s, M + cw + 0.5, 6.2, cw, 10.8, 'black', 'At what\nprice', 'Median forward P/E of 13x, against 21.5x for the S&P 500. With the Fed raising rates, prices have to follow earnings.', '02')
card(s, M + 2*(cw + 0.5), 6.2, cw, 10.8, 'white', 'How we\ncombine them', f'Value, growth and momentum stocks. 19 holdings in 7 sectors, at most 25% each. Weights by conviction, {p.w.min():.1%} to {p.w.max():.1%}.', '03')

# ================= 03 macro =================
s = slide(True, 'Market', '03')
title(s, M, 2.9, 13.5, [[('Where the', False)], [('market stands', True)], [('in November 2026', False)]], 36, True)
T(s, M, 14.6, 12.5, 2.6, 'What we do about it: buy rising estimates at low multiples, mix styles and sectors, and hold energy against an oil shock.', 10, WHITE, MONO, spacing=1.15)
items = [('Fed raising rates', 'First hike in three years in September; officials signal more. 10-year Treasury at about 4.9%.'),
         ('Inflation', 'Producer prices rise at the fastest pace since 2022. 47% of fund managers expect stagflation.'),
         ('Oil', 'Brent above $110 in October because of the US and Iran conflict; now moving with news on talks.'),
         ('AI and chip stocks', 'More than $1 trillion of tech value lost in one week of October; chip stocks still falling.'),
         ('Valuations', 'S&P 500 up about 8% this year, at 21.5 times forward earnings.')]
x0, w0, h0 = 17.2, 33.867 - M - 17.2, 2.72
for i, (h_, b_) in enumerate(items):
    y_ = 2.9 + i * (h0 + 0.25); rect(s, x0, y_, w0, h0, RGBColor(0x0B,0x15,0x22), RGBColor(0xFF,0xFF,0xFF), 0.08, a=0.5, la=0.16)
    T(s, x0 + 0.55, y_ + 0.35, 8, 0.4, f'{i+1:02d}', 7.5, MUTED_D, MONO)
    T(s, x0 + 0.55, y_ + 0.85, w0 - 1.1, 0.7, h_, 15, WHITE, HEAD)
    T(s, x0 + 0.55, y_ + 1.6, w0 - 1.1, 1, b_, 8.5, MUTED_D, MONO, spacing=1.05)

# ================= 04 metodo =================
s = slide(False, 'Method', '04', cubes=True)
title(s, M, 2.9, 20, [[('How we picked ', False), ('the stocks', True)], [('Zacks criteria on 151 US large caps', False)]], 32)
crit = [('40%', 'Agreement', 'Share of upward EPS revisions in the last 30 days; Zacks weighs it most'), ('25%', 'Magnitude', 'Change in the consensus EPS estimate over 60 days'),
        ('20%', 'Broker opinion', 'Average Broker Recommendation, 1 = Strong Buy'), ('15%', 'Upside', 'Analysts\' price target against the current price'), ('Check', 'Surprise', 'Average EPS surprise over the last four quarters')]
for i, (wgt, h_, b_) in enumerate(crit):
    y_ = 7.0 + i * 2.1; rect(s, M, y_, 17.6, 1.85, RGBColor(0xFA,0xFB,0xFD), None, 0.12)
    T(s, M + 0.55, y_ + 0.38, 2.6, 1, wgt, 20 if wgt != 'Check' else 14, ACC_L, HEAD, anchor=MSO_ANCHOR.MIDDLE)
    T(s, M + 3.5, y_ + 0.3, 13.5, 0.6, h_, 13, INK, HEAD); T(s, M + 3.5, y_ + 1.0, 13.5, 0.6, b_, 8.5, INK2, MONO)
fun = [('151', 'large caps screened'), ('38', 'candidates: positive revisions, ABR 2.5 or better'), ('19', 'stocks in the portfolio'), ('25', 'stocks in the watch list')]
for i, (v, l) in enumerate(fun):
    x_ = 20.4 + (i % 2) * 5.85; y_ = 7.0 + (i // 2) * 5.2
    rect(s, x_, y_, 5.55, 4.95, BLACK if i == 2 else RGBColor(0xFA,0xFB,0xFD), None, 0.07)
    T(s, x_ + 0.5, y_ + 0.6, 4.6, 1.6, v, 36, WHITE if i == 2 else INK, HEAD)
    T(s, x_ + 0.5, y_ + 3.3, 4.6, 1.4, l, 8.5, MUTED_D if i == 2 else INK2, MONO, spacing=1.05)
T(s, M, 17.4, 30, 0.4, 'Then we checked the price: forward P/E, P/B and PEG (slide 8). Limit: the signal works over a short horizon of one to three months.', 7.5, INK2, MONO)

# ================= 05 regole =================
s = slide(True, 'Screening', '05', bgimg='assets/bg_dark2.png')
title(s, M, 2.9, 24, [[('Three styles, ', False), ('one screen', True)]], 34, True)
sty = p.groupby('stile').w.sum()
rules = [('Value', f'{sty["Value"]:.0%}', ['Forward P/E below 14', 'P/B below 3.5'], 'Oil, banks, health insurers, steel, telecom. They gain from oil prices and higher rates.'),
         ('Growth', f'{sty["Growth"]:.0%}', ['EPS growth above 25%', 'PEG below 1.6'], 'AI hardware, grid contractors, asset management. Earnings already growing.'),
         ('Momentum', f'{sty["Momentum"]:.0%}', ['6-month return above 20%', '3-month return above 5%'], 'Healthcare leaders and payments. Rising prices and rising estimates.')]
for i, (n_, pct, rl, d_) in enumerate(rules):
    x_ = M + i * (cw + 0.5); rect(s, x_, 5.6, cw, 8.6, RGBColor(0x0B,0x15,0x22), RGBColor(0xFF,0xFF,0xFF), 0.05, a=0.45, la=0.16)
    T(s, x_ + 0.6, 6.1, cw - 1.2, 0.5, f'{i+1:02d}  /  share of portfolio', 7.5, MUTED_D, MONO)
    T(s, x_ + 0.6, 6.9, cw - 1.2, 1.8, pct, 40, ACC_D, HEAD); T(s, x_ + 0.6, 8.9, cw - 1.2, 0.8, n_, 20, WHITE, HEAD)
    T(s, x_ + 0.6, 10.3, cw - 1.2, 1.2, rl, 9.5, WHITE, MONO, spacing=1.2)
    T(s, x_ + 0.6, 12.0, cw - 1.2, 1.8, d_, 8.5, MUTED_D, MONO, spacing=1.1)
rect(s, M, 14.8, 33.867 - 2*M, 2.5, BLACK, None, 0.12, a=0.55)
T(s, M + 0.6, 15.25, 30, 0.4, 'Portfolio constraints', 7.5, MUTED_D, MONO)
T(s, M + 0.6, 15.85, 29.5, 1.2, f'At most 25% per sector and three technology stocks. 19 holdings (rules allow 10 to 30). {INV:.1%} invested after the first purchase (minimum 95%). No utilities, real estate or consumer discretionary, which suffer most from higher rates and weak spending.', 9.5, WHITE, MONO, spacing=1.15)

# ================= 06 portafoglio =================
s = slide(False, 'Portfolio', '06')
title(s, M, 2.9, 20, [[('The initial portfolio', False)]], 30)
T(s, 33.867 - M - 12, 3.35, 12, 0.5, 'Market orders executed 24/11/2026, fill prices', 8, INK2, MONO, PP_ALIGN.RIGHT)
cols = ['Ticker', 'Company', 'Sector', 'Style', 'Shares', 'Fill price', 'Weight']; cwid = [2.4, 9.0, 5.6, 3.6, 2.8, 3.6, 3.07]
rows = [[r.ticker, r.nome.replace('ExxonMobil Holdings Corporation', 'Exxon Mobil Corporation')[:34], SHORT.get(r.settore, r.settore), r.stile, f'{r.azioni:,}', f'${r.prezzo_acquisto:,.2f}', f'{r.w:.1%}'] for _, r in p.sort_values('w', ascending=False).iterrows()]
y_ = 5.0; rh = 0.6
xs = np.cumsum([M] + cwid)
for j, c in enumerate(cols): T(s, xs[j] + 0.25, y_, cwid[j] - 0.5, 0.4, c, 7.5, INK2, MONO, PP_ALIGN.RIGHT if j >= 4 else PP_ALIGN.LEFT)
rect(s, M, y_ + 0.55, sum(cwid), 0.02, INK2, None, shape=MSO_SHAPE.RECTANGLE)
for i, row in enumerate(rows):
    yy = y_ + 0.72 + i * rh
    if i % 2 == 0: rect(s, M, yy - 0.06, sum(cwid), rh, RGBColor(0xFA,0xFB,0xFD), None, shape=MSO_SHAPE.RECTANGLE)
    for j, v in enumerate(row): T(s, xs[j] + 0.25, yy + 0.06, cwid[j] - 0.5, 0.45, v, 9, INK if j != 0 else ACC_L, MONO if j in (0, 4, 5, 6) else BODY, PP_ALIGN.RIGHT if j >= 4 else PP_ALIGN.LEFT, bold=(j == 0))
yy = y_ + 0.72 + len(rows) * rh + 0.1
rect(s, M, yy, sum(cwid), 0.02, INK2, None, shape=MSO_SHAPE.RECTANGLE)
T(s, M + 0.25, yy + 0.15, 20, 0.45, f'Total invested ${p.cv.sum():,.0f} of $1,000,000  /  cash {1-INV:.1%}', 8.5, INK, MONO)
T(s, xs[6] + 0.25, yy + 0.15, cwid[6] - 0.5, 0.45, f'{INV:.1%}', 8.5, INK, MONO, PP_ALIGN.RIGHT)

# ================= 07 diversificazione =================
s = slide(False, 'Diversification', '07', cubes=True)
title(s, M, 2.9, 22, [[('Weights and ', False), ('diversification', True)]], 32)
sec = p.groupby('settore').w.sum().sort_values(ascending=False); styw = p.groupby('stile').w.sum().reindex(['Value', 'Growth', 'Momentum'])
rect(s, M, 6.0, 18.4, 11.4, RGBColor(0xFA,0xFB,0xFD), None, 0.04); rect(s, M + 18.9, 6.0, 33.867 - 2*M - 18.9, 11.4, BLACK, None, 0.04)
T(s, M + 0.6, 6.5, 10, 0.4, 'Weight by sector', 7.5, INK2, MONO); T(s, M + 19.5, 6.5, 10, 0.4, 'Weight by style', 7.5, MUTED_D, MONO)
for k, (nm, v) in enumerate(sec.items()):
    yy = 7.4 + k * 1.38; T(s, M + 0.6, yy + 0.12, 4.6, 0.5, SHORT.get(nm, nm), 10, INK, BODY)
    rect(s, M + 5.3, yy + 0.18, 10.5, 0.42, RGBColor(0xE2,0xE6,0xEE), None, 0.5)
    rect(s, M + 5.3, yy + 0.18, max(0.42, 10.5 * v / 0.25), 0.42, ACC_L if k else INK, None, 0.5)
    T(s, M + 16.1, yy + 0.12, 1.8, 0.5, f'{v:.0%}', 10, INK, MONO, PP_ALIGN.RIGHT)
cd = CategoryChartData(); cd.categories = list(styw.index); cd.add_series('Weight', [round(v, 4) for v in styw.values])
gf = s.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT, Cm(M + 19.4), Cm(7.2), Cm(6.6), Cm(6.6), cd); ch = gf.chart
ch.has_legend = False; ch.has_title = False; pl = ch.plots[0]
for i, c in enumerate([RGBColor(0x9F,0xC6,0xE6), RGBColor(0x5E,0x80,0x9C), RGBColor(0xE8,0xEE,0xF3)]):
    pt = pl.series[0].points[i]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = c; pt.format.line.color.rgb = BLACK
for i, (nm, v) in enumerate(styw.items()):
    yy = 7.6 + i * 2.0; rect(s, M + 26.6, yy + 0.18, 0.4, 0.4, [RGBColor(0x9F,0xC6,0xE6), RGBColor(0x5E,0x80,0x9C), RGBColor(0xE8,0xEE,0xF3)][i], None, 0.2)
    T(s, M + 27.3, yy, 3, 0.6, nm, 11, WHITE, HEAD); T(s, M + 27.3, yy + 0.65, 3, 0.5, f'{v:.0%}', 9, MUTED_D, MONO)
T(s, M + 19.5, 14.2, 10.5, 2.9, f'Weights by conviction: 5% plus or minus 2.5 points with the score, from {p.w.min():.1%} to {p.w.max():.1%}. Equal weights would ignore the signal; value weights would load up on the largest tech names.', 8.5, WHITE, MONO, spacing=1.15)

# ================= 08 profilo valutativo (bento) =================
s = slide(False, 'Valuation', '08')
title(s, M, 2.9, 22, [[('Selection parameters, ', False), ('portfolio medians', True)]], 32)
up = p.rev_su_30g.sum() / (p.rev_su_30g.sum() + p.rev_giu_30g.sum())
k = [(f'{p.PE_fwd.median():.1f}x', 'median forward P/E', 'S&P 500 at 21.5x'), (f'{up:.0%}', 'of EPS revisions in the last 30 days are upward', None),
     (f'{p.ABR.median():.2f}', 'median broker rating', '1 = Strong Buy'), (f'+{p["surprise_4q_%"].median():.1f}%', 'median EPS surprise, last four quarters', None)]
pos = [(M, 6.0, 6.2, 5.4), (M, 11.9, 6.2, 5.5), (M + 18.1, 6.0, 6.0, 5.4), (M + 18.1, 11.9, 6.0, 5.5)]
for (v, l, sub), (x_, y_, w_, h_) in zip(k, pos):
    rect(s, x_, y_, w_, h_, RGBColor(0xFA,0xFB,0xFD), None, 0.06)
    T(s, x_ + 0.55, y_ + 0.6, w_ - 1.1, 1.6, v, 34, INK, HEAD)
    T(s, x_ + 0.55, y_ + h_ - 1.75, w_ - 1.1, 1.2, l, 8.5, INK2, MONO, spacing=1.05)
    if sub: T(s, x_ + 0.55, y_ + 2.35, w_ - 1.1, 0.5, sub, 8, ACC_L, MONO)
card(s, M + 6.6, 6.0, 11.1, 11.4, 'imgdark', 'Lower price,\nrising estimates', None, hsize=28)
T(s, M + 7.15, 6.6, 10, 0.5, 'Portfolio profile', 7.5, WHITE, MONO)
x_ = M + 24.5; w_ = 33.867 - M - x_
rect(s, x_, 6.0, w_, 11.4, BLACK, None, 0.04)
T(s, x_ + 0.55, 6.6, w_ - 1.1, 0.5, 'Reading', 7.5, MUTED_D, MONO)
T(s, x_ + 0.55, 10.6, w_ - 1.1, 6, 'Analysts are raising estimates on almost all our stocks, and we pay about 13 times expected earnings, against 21.5 for the S&P 500.', 10, WHITE, HEAD, spacing=1.1)

# ================= watch list (D) =================
s = slide(False, 'Watch list', '09', cubes=True)
title(s, M, 2.9, 20, [[('Monitoring list', False)], [('25 stocks, same screen', True)]], 32)
wl = [('Energy', 'OXY  COP  PSX'), ('Technology', 'ANET  AMD  NVDA  AVGO  KLAC  TXN'), ('Industrials and power', 'GEV  ETN  CEG  PH  RTX'),
      ('Healthcare', 'CVS  CI  TMO  ISRG  HCA'), ('Financials', 'AIG  MET  CB  TRV  V'), ('Consumer', 'ORLY')]
for i, (h_, b_) in enumerate(wl):
    x_ = M + (i % 3) * (cw + 0.5); y_ = 7.2 + (i // 3) * 4.4
    rect(s, x_, y_, cw, 4.0, BLACK if i == 1 else RGBColor(0xFA,0xFB,0xFD), None, 0.07)
    T(s, x_ + 0.6, y_ + 0.5, cw - 1.2, 0.4, f'{i+1:02d}', 7.5, MUTED_D if i == 1 else INK2, MONO)
    T(s, x_ + 0.6, y_ + 1.2, cw - 1.2, 0.8, h_, 16, WHITE if i == 1 else INK, HEAD)
    T(s, x_ + 0.6, y_ + 2.5, cw - 1.2, 1.0, b_, 11, ACC_D if i == 1 else ACC_L, MONO)
T(s, M, 16.3, 30, 1, 'Selected with the same parameters as the portfolio. We use them to replace holdings whose estimates start to be cut. The full table is in the report and in the Excel file.', 9, INK2, MONO, spacing=1.1)

# ================= trading =================
s = slide(True, 'Trading', '10', bgimg='assets/bg_dark2.png')
title(s, M, 2.9, 13.5, [[('Trading until', False)], [('18 December', True)]], 36, True)
T(s, M, 14.2, 12.5, 3, 'Game rules: at least 5 trades, 10 to 30 stocks at all times, no short selling or margin.', 10, WHITE, MONO, spacing=1.15)
rules = [('Sell', 'a stock when analysts start cutting its estimates'), ('Replace', 'it with the best stock of the same style from the watch list'),
         ('Trim', 'any position that grows above 10% of the portfolio'), ('Spread', 'the trades over the period, not all in the last days')]
for i, (h_, b_) in enumerate(rules):
    y_ = 2.9 + i * 3.7; rect(s, x0, y_, w0, 3.4, RGBColor(0x0B,0x15,0x22), RGBColor(0xFF,0xFF,0xFF), 0.08, a=0.5, la=0.16)
    T(s, x0 + 0.6, y_ + 0.45, 8, 0.4, f'{i+1:02d}', 7.5, MUTED_D, MONO)
    T(s, x0 + 0.6, y_ + 1.0, w0 - 1.2, 0.9, h_, 18, WHITE, HEAD)
    T(s, x0 + 0.6, y_ + 2.05, w0 - 1.2, 1, b_, 9.5, MUTED_D, MONO)

# ================= 09 back-test =================
s = slide(True, 'Back-test', '09')
title(s, M, 2.9, 22, [[('First analysis: ', False)], [('July to October 2026', True)]], 34, True)
T(s, 33.867 - M - 12, 5.0, 12, 0.5, 'Daily dividend-adjusted closes, S&P 500 as the market, risk-free rate 4%', 8, MUTED_D, MONO, PP_ALIGN.RIGHT)
vals = [(f'{BT["hpr"]:+.1%}', 'portfolio holding-period return', True), (f'{BT["spx"]:+.1%}', 'S&P 500 holding-period return', False), (f'{BT["sh"]:.2f}', 'portfolio Sharpe ratio', True),
        (f'{BT["shm"]:.2f}'.replace('-', '−'), 'S&P 500 Sharpe ratio', False), (f'{BT["beta"]:.2f}', 'portfolio beta', False), (f'{BT["corr"]:.2f}', 'average correlation between pairs of stocks', False)]
gw = (33.867 - 2*M - 2*0.4) / 3
for i, (v, l, hl) in enumerate(vals):
    x_ = M + (i % 3) * (gw + 0.4); y_ = 6.6 + (i // 3) * 3.6
    rect(s, x_, y_, gw, 3.3, RGBColor(0x0B,0x15,0x22), RGBColor(0xFF,0xFF,0xFF), 0.07, a=0.45, la=0.16)
    T(s, x_ + 0.6, y_ + 0.45, gw - 1.2, 1.6, v, 32, ACC_D if hl else WHITE, HEAD); T(s, x_ + 0.6, y_ + 2.3, gw - 1.2, 0.6, l, 8.5, MUTED_D, MONO)
rect(s, M, 14.15, 33.867 - 2*M, 3.2, BLACK, None, 0.08, a=0.6)
T(s, M + 0.6, 14.6, 10, 0.4, 'Note', 7.5, ACC_D, MONO)
T(s, M + 0.6, 15.2, 29.5, 1.8, 'This is the initial portfolio tested on the four months before the game, as the assignment asks (section 6.1). Part of the selection data comes from the same period, so the result looks better than it would in real time.', 9.5, WHITE, MONO, spacing=1.15)

# ================= 12 formule =================
s = slide(False, 'Excel', '12')
title(s, M, 2.9, 22, [[('Formulas used ', False), ('in the Excel file', True)]], 32)
fm = [('Daily return', 'r(t) = (P(t) − P(t−1)) / P(t−1)'), ('Portfolio return', 'R(p,t) = Σ w(i) · r(i,t)'), ('Geometric mean and HPR', '[Π(1 + r(t))]^(1/T) − 1     HPR = Π(1 + r(t)) − 1'),
      ('Risk', 'sample variance VAR.S, standard deviation STDEV.S'), ('Beta', 'β(i) = Cov(r(i), R(m)) / Var(R(m))     β(p) = Σ w(i) · β(i)'), ('Sharpe ratio', '(R(annual) − Rf) / σ(annual)     R(annual) = (1 + R(monthly))^12 − 1     σ(annual) = σ(daily) · √250')]
fw = (33.867 - 2*M - 0.5) / 2
for i, (h_, f_) in enumerate(fm):
    x_ = M + (i % 2) * (fw + 0.5); y_ = 6.0 + (i // 2) * 3.8
    rect(s, x_, y_, fw, 3.5, BLACK if i == 5 else RGBColor(0xFA,0xFB,0xFD), None, 0.07)
    T(s, x_ + 0.6, y_ + 0.5, fw - 1.2, 0.4, f'{i+1:02d}  /  {h_}', 7.5, MUTED_D if i == 5 else INK2, MONO)
    T(s, x_ + 0.6, y_ + 1.4, fw - 1.2, 1.8, f_, 13 if i != 5 else 10.5, WHITE if i == 5 else INK, MONO, spacing=1.1)

os.makedirs('out', exist_ok=True); prs.save('out/presentazione_strategia.pptx'); print('ok', len(prs.slides))
