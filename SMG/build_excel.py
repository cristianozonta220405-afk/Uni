"""Genera groupname_report2.xlsx: analisi del portafoglio iniziale (sezione 6.1) con formule visibili.
Convenzioni: blu = input, nero = formula, verde = collegamento ad altro foglio."""
import pandas as pd, datetime as dt, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.formula import ArrayFormula
from openpyxl.chart import LineChart, ScatterChart, PieChart, BarChart, Reference, Series
from openpyxl.chart.trendline import Trendline
from openpyxl.formatting.rule import ColorScaleRule, DataBarRule, CellIsRule
from openpyxl.workbook.defined_name import DefinedName

GROUP = os.environ.get('SMG_GROUP', 'groupname')
OUT = f'out/{GROUP}_report2.xlsx'
port = pd.read_csv('dati/portafoglio_iniziale.csv')
prices = pd.read_csv('dati/prezzi_lug_ott.csv', index_col=0, parse_dates=True)
tk = list(port.ticker); n = len(tk); T0 = len(prices); T = T0 - 1
SECTORS = sorted(port.settore.unique()); STYLES = ['Value', 'Growth', 'Momentum']

# ---------- stili ----------
NAVY, LIGHT, GREY = '1F3864', 'D9E1F2', 'F2F2F2'
F_IN, F_LINK, F_CALC = Font(name='Calibri', color='0000FF'), Font(name='Calibri', color='008000'), Font(name='Calibri', color='000000')
F_HEAD = Font(name='Calibri', bold=True, color='FFFFFF'); FILL_HEAD = PatternFill('solid', fgColor=NAVY)
FILL_SUB = PatternFill('solid', fgColor=LIGHT); FILL_KEY = PatternFill('solid', fgColor='FFF2CC')
thin = Side(style='thin', color='BFBFBF'); BOX = Border(top=thin, bottom=thin, left=thin, right=thin)
PCT, PCT4, NUM, USD, DATE = '0.00%', '0.0000%', '0.0000', '$#,##0.00', 'dd/mm/yyyy'

def title(ws, text, sub=None):
    ws['A1'] = text; ws['A1'].font = Font(name='Calibri', bold=True, size=14, color=NAVY)
    if sub: ws['A2'] = sub; ws['A2'].font = Font(name='Calibri', italic=True, color='595959')
    ws.sheet_view.showGridLines = False
def head(ws, row, col, vals):
    for j, v in enumerate(vals):
        c = ws.cell(row, col + j, v); c.font = F_HEAD; c.fill = FILL_HEAD; c.border = BOX
        c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
def put(ws, row, col, val, font=F_CALC, fmt=None, fill=None):
    c = ws.cell(row, col, val); c.font = font; c.border = BOX
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    return c
def widths(ws, d):
    for k, v in d.items(): ws.column_dimensions[k].width = v

wb = Workbook()
# ======================= INDICE =======================
ix = wb.active; ix.title = 'Indice'
title(ix, 'Stock Market Game 2026 - Analisi del portafoglio', f'Gruppo: {GROUP}  |  Corporate Finance & Financial Institutions 2')
head(ix, 4, 1, ['Foglio', 'Contenuto', 'Sezione istruzioni'])
SHEETS = [('Portafoglio', 'Composizione del portafoglio iniziale: azioni, prezzi, pesi, allocazione per settore e stile', 'B / 5.C'),
          ('Prezzi', 'Prezzi di chiusura giornalieri aggiustati per dividendi (30/06-31/10/2026) + S&P 500', '6.1'),
          ('Rendimenti', 'Rendimenti giornalieri dei titoli, del mercato e del portafoglio', '6.1.1 a-b'),
          ('Statistiche', 'Media aritmetica e geometrica, holding period return, varianza e deviazione standard', '6.1.1c, 6.1.2, 6.1.7'),
          ('Settori', 'Sotto-portafogli per settore: rendimenti giornalieri e statistiche', '6.1.3'),
          ('Stili', 'Sotto-portafogli per stile (value, growth, momentum)', '6.1.4'),
          ('Base100', 'Indici cumulati (base 100) per titoli, settori, stili, portafoglio e mercato', '6.1.5'),
          ('Grafici', 'Andamento nel tempo di titoli, settori, stili e portafoglio vs S&P 500', '6.1.5'),
          ('Eventi', 'Rendimenti anomali: giorni migliori e peggiori, rendimento in eccesso sul mercato', '6.1.6'),
          ('Cov_Beta', 'Matrice varianza-covarianza, beta dei titoli, beta di portafoglio, grafico beta-rendimento', '6.1.8, 6.1.9'),
          ('Correlazione', 'Matrice di correlazione tra titoli e mercato', '6.1.10'),
          ('Sharpe', 'Rendimenti mensili, annualizzazione e Sharpe ratio di portafoglio e mercato', '6.1.11, 6.1.12'),
          ('Controlli', 'Verifiche automatiche di coerenza (TRUE = ok)', '-')]
for i, (s, d, sec) in enumerate(SHEETS):
    c = put(ix, 5 + i, 1, s); c.hyperlink = f"#'{s}'!A1"; c.font = Font(color='0563C1', underline='single')
    put(ix, 5 + i, 2, d); put(ix, 5 + i, 3, sec)
r = 6 + len(SHEETS); ix.cell(r, 1, 'Legenda colori').font = Font(bold=True)
for k, (txt, f) in enumerate([('Valore inserito (input / dato scaricato)', F_IN), ('Formula di calcolo', F_CALC), ('Collegamento ad altro foglio', F_LINK)]):
    ix.cell(r + 1 + k, 1, 'Esempio 123').font = f; ix.cell(r + 1 + k, 2, txt)
ix.cell(r + 5, 1, 'Fonte dati: Yahoo Finance (Adjusted Close). Indice di mercato: S&P 500 (^GSPC). Risk-free: T-bill 12 mesi, 4% annuo.').font = Font(italic=True)
widths(ix, {'A': 16, 'B': 95, 'C': 22})

# ======================= PORTAFOGLIO =======================
pf = wb.create_sheet('Portafoglio')
title(pf, 'Portafoglio iniziale', 'Capitale iniziale $1.000.000 - acquisti eseguiti nella prima settimana di trading')
head(pf, 4, 1, ['Ticker', 'Società', 'Settore', 'Industria', 'Stile', 'Zacks Rank', 'N. azioni', 'Prezzo acquisto', 'Controvalore', 'Peso effettivo', 'Peso target'])
P0, P1 = 5, 5 + n - 1
for i, rw in port.iterrows():
    r = P0 + i
    for j, v in enumerate([rw.ticker, rw.nome, rw.settore, rw.industria, rw.stile]): put(pf, r, 1 + j, v, F_IN)
    put(pf, r, 6, None if pd.isna(rw.zacks_rank) else int(rw.zacks_rank), F_IN).alignment = Alignment(horizontal='center')
    put(pf, r, 7, int(rw.azioni), F_IN, '#,##0'); put(pf, r, 8, float(rw.prezzo_acquisto), F_IN, USD)
    put(pf, r, 9, f'=G{r}*H{r}', fmt=USD); put(pf, r, 10, f'=I{r}/$I${P1+1}', fmt=PCT); put(pf, r, 11, float(rw.peso_target), F_IN, PCT)
tr = P1 + 1
put(pf, tr, 1, 'Totale investito', fill=FILL_SUB).font = Font(bold=True)
put(pf, tr, 9, f'=SUM(I{P0}:I{P1})', fmt=USD, fill=FILL_SUB); put(pf, tr, 10, f'=SUM(J{P0}:J{P1})', fmt=PCT, fill=FILL_SUB)
put(pf, tr + 2, 8, 'Capitale iniziale'); put(pf, tr + 2, 9, 1_000_000, F_IN, USD)
put(pf, tr + 3, 8, 'Liquidità residua'); put(pf, tr + 3, 9, f'=I{tr+2}-I{tr}', fmt=USD)
put(pf, tr + 4, 8, '% capitale investito'); put(pf, tr + 4, 9, f'=I{tr}/I{tr+2}', fmt=PCT, fill=FILL_KEY)
put(pf, tr + 5, 8, 'N. società'); put(pf, tr + 5, 9, f'=COUNTA(A{P0}:A{P1})')
wb.defined_names['Pesi'] = DefinedName('Pesi', attr_text=f'Portafoglio!$J${P0}:$J${P1}')
# allocazione per settore e stile
sr = tr + 8; head(pf, sr, 2, ['Settore', 'N. titoli', 'Peso'])
for k, s in enumerate(SECTORS):
    put(pf, sr + 1 + k, 2, s); put(pf, sr + 1 + k, 3, f'=COUNTIF($C${P0}:$C${P1},B{sr+1+k})')
    put(pf, sr + 1 + k, 4, f'=SUMIF($C${P0}:$C${P1},B{sr+1+k},$J${P0}:$J${P1})', fmt=PCT)
yr = sr + len(SECTORS) + 3; head(pf, yr, 2, ['Stile', 'N. titoli', 'Peso'])
for k, s in enumerate(STYLES):
    put(pf, yr + 1 + k, 2, s); put(pf, yr + 1 + k, 3, f'=COUNTIF($E${P0}:$E${P1},B{yr+1+k})')
    put(pf, yr + 1 + k, 4, f'=SUMIF($E${P0}:$E${P1},B{yr+1+k},$J${P0}:$J${P1})', fmt=PCT)
for (r0, rows, ttl, anchor) in [(sr, len(SECTORS), 'Allocazione per settore', 'M4'), (yr, 3, 'Allocazione per stile', 'M22')]:
    pc = PieChart(); pc.title = ttl
    pc.add_data(Reference(pf, min_col=4, min_row=r0, max_row=r0 + rows), titles_from_data=True)
    pc.set_categories(Reference(pf, min_col=2, min_row=r0 + 1, max_row=r0 + rows)); pc.width, pc.height = 14, 8.5
    from openpyxl.chart.label import DataLabelList
    pc.dataLabels = DataLabelList(); pc.dataLabels.showPercent = True; pf.add_chart(pc, anchor)
widths(pf, {'A': 10, 'B': 32, 'C': 24, 'D': 30, 'E': 11, 'F': 8, 'G': 10, 'H': 13, 'I': 15, 'J': 10, 'K': 10})
pf.freeze_panes = 'B5'

# ======================= PREZZI =======================
pr = wb.create_sheet('Prezzi'); cols = tk + ['SPX']
title(pr, 'Prezzi di chiusura giornalieri aggiustati (Adjusted Close)', 'Fonte: Yahoo Finance. 30/06/2026 = prezzo base per il rendimento del 1° luglio')
head(pr, 3, 1, ['Data'] + cols); R0 = 4; RN = R0 + T0 - 1
for i, (d, row) in enumerate(prices.iterrows()):
    put(pr, R0 + i, 1, d.to_pydatetime(), F_IN, DATE)
    for j, c in enumerate(cols): put(pr, R0 + i, 2 + j, round(float(row[c]), 4), F_IN, '#,##0.00')
pr.freeze_panes = 'B4'; widths(pr, {'A': 12})

# ======================= RENDIMENTI =======================
re = wb.create_sheet('Rendimenti'); SPXc = n + 2; PFc = n + 3
title(re, 'Rendimenti giornalieri  r(t) = (P(t) - P(t-1)) / P(t-1)', 'Portafoglio: R(p,t) = Σ w(i) · r(i,t)  con pesi del portafoglio iniziale')
put(re, 3, 1, 'Ticker', F_HEAD, fill=FILL_HEAD); put(re, 4, 1, 'Peso', fill=FILL_SUB); put(re, 5, 1, 'Settore', fill=FILL_SUB); put(re, 6, 1, 'Stile', fill=FILL_SUB)
for j in range(n):
    c = 2 + j; pfr = P0 + j
    put(re, 3, c, f'=Prezzi!{L(c)}3', F_HEAD, fill=FILL_HEAD)
    put(re, 4, c, f'=Portafoglio!J{pfr}', F_LINK, PCT); put(re, 5, c, f'=Portafoglio!C{pfr}', F_LINK); put(re, 6, c, f'=Portafoglio!E{pfr}', F_LINK)
put(re, 3, SPXc, 'SPX', F_HEAD, fill=FILL_HEAD); put(re, 3, PFc, 'Portafoglio', F_HEAD, fill=FILL_HEAD)
put(re, 7, 1, 'Data', F_HEAD, fill=FILL_HEAD)
D0 = 8; DN = D0 + T - 1; S, E = L(2), L(n + 1)
for t in range(T):
    r = D0 + t; p = R0 + 1 + t
    put(re, r, 1, f'=Prezzi!A{p}', F_LINK, DATE)
    for j in range(n + 1):
        c = L(2 + j); put(re, r, 2 + j, f'=(Prezzi!{c}{p}-Prezzi!{c}{p-1})/Prezzi!{c}{p-1}', fmt=PCT)
    put(re, r, PFc, f'=SUMPRODUCT(${S}$4:${E}$4,{S}{r}:{E}{r})', fmt=PCT, fill=FILL_KEY)
re.freeze_panes = 'B8'; widths(re, {'A': 12})
def RR(col): return f'Rendimenti!${L(col)}${D0}:${L(col)}${DN}'

# ======================= STATISTICHE =======================
st = wb.create_sheet('Statistiche')
title(st, 'Statistiche descrittive dei rendimenti giornalieri (01/07-31/10/2026)', 'Geometrica = [Π(1+r)]^(1/T) - 1   |   HPR = Π(1+r) - 1   |   Varianza e dev. std campionarie (VAR.S, STDEV.S)')
head(st, 4, 1, ['Titolo', 'Settore', 'Stile', 'N. osservazioni', 'Media aritmetica', 'Media geometrica', 'Holding period return', 'Varianza', 'Dev. std giornaliera', 'Dev. std annua (√250)', 'Rank rischio (1 = più rischioso)'])
names = tk + ['Portafoglio', 'SPX']; colmap = {**{t: 2 + j for j, t in enumerate(tk)}, 'Portafoglio': PFc, 'SPX': SPXc}
ST0 = 5
for i, nm in enumerate(names):
    r = ST0 + i; rg = RR(colmap[nm]); stock = i < n
    put(st, r, 1, nm, F_CALC if not stock else F_LINK, fill=None if stock else FILL_SUB).font = Font(bold=not stock, color='000000' if not stock else '008000')
    if stock: put(st, r, 1, f'=Portafoglio!A{P0+i}', F_LINK); put(st, r, 2, f'=Portafoglio!C{P0+i}', F_LINK); put(st, r, 3, f'=Portafoglio!E{P0+i}', F_LINK)
    else:
        for cc in (2, 3): put(st, r, cc, '-', fill=FILL_SUB)
    put(st, r, 4, f'=COUNT({rg})'); put(st, r, 5, f'=AVERAGE({rg})', fmt=PCT4)
    st.cell(r, 7).value = ArrayFormula(f'G{r}', f'=PRODUCT(1+{rg})-1'); st.cell(r, 7).number_format = PCT; st.cell(r, 7).border = BOX
    put(st, r, 6, f'=(1+G{r})^(1/D{r})-1', fmt=PCT4); put(st, r, 8, f'=VAR.S({rg})', fmt='0.000000')
    put(st, r, 9, f'=SQRT(H{r})', fmt=PCT); put(st, r, 10, f'=I{r}*SQRT(250)', fmt=PCT)
    if stock: put(st, r, 11, f'=RANK(I{r},$I${ST0}:$I${ST0+n-1},0)')
STN = ST0 + n - 1
st.conditional_formatting.add(f'J{ST0}:J{STN}', DataBarRule(start_type='min', end_type='max', color='F4B183'))
st.conditional_formatting.add(f'G{ST0}:G{STN}', ColorScaleRule(start_type='min', start_color='F8696B', mid_type='num', mid_value=0, mid_color='FFFFFF', end_type='max', end_color='63BE7B'))
k = STN + 5; put(st, k, 1, 'Titolo più rischioso'); put(st, k, 2, f'=INDEX($A${ST0}:$A${STN},MATCH(MAX($I${ST0}:$I${STN}),$I${ST0}:$I${STN},0))', fill=FILL_KEY)
put(st, k + 1, 1, 'Titolo meno rischioso'); put(st, k + 1, 2, f'=INDEX($A${ST0}:$A${STN},MATCH(MIN($I${ST0}:$I${STN}),$I${ST0}:$I${STN},0))', fill=FILL_KEY)
put(st, k + 2, 1, 'Miglior HPR'); put(st, k + 2, 2, f'=INDEX($A${ST0}:$A${STN},MATCH(MAX($G${ST0}:$G${STN}),$G${ST0}:$G${STN},0))', fill=FILL_KEY)
put(st, k + 3, 1, 'Peggior HPR'); put(st, k + 3, 2, f'=INDEX($A${ST0}:$A${STN},MATCH(MIN($G${ST0}:$G${STN}),$G${ST0}:$G${STN},0))', fill=FILL_KEY)
bc = BarChart(); bc.type = 'bar'; bc.title = 'Holding period return per titolo'; bc.height, bc.width = 11, 16
bc.add_data(Reference(st, min_col=7, min_row=4, max_row=STN + 2), titles_from_data=True); bc.set_categories(Reference(st, min_col=1, min_row=5, max_row=STN + 2)); bc.legend = None
st.add_chart(bc, 'M4')
widths(st, {'A': 13, 'B': 22, 'C': 11, 'D': 10, 'E': 12, 'F': 12, 'G': 13, 'H': 11, 'I': 12, 'J': 12, 'K': 13}); st.freeze_panes = 'B5'

# ======================= SETTORI / STILI =======================
def subport(name, groups, row_key, stitle):
    ws = wb.create_sheet(name)
    title(ws, stitle, 'Rendimento giornaliero del sotto-portafoglio = Σ w(i)·r(i,t) / Σ w(i), per i titoli del gruppo (pesi del portafoglio iniziale)')
    head(ws, 4, 1, ['Data'] + groups); G0 = 5
    kr = f'Rendimenti!${S}${row_key}:${E}${row_key}'; wr = f'Rendimenti!${S}$4:${E}$4'
    for t in range(T):
        r = G0 + t; put(ws, r, 1, f'=Rendimenti!A{D0+t}', F_LINK, DATE)
        for j in range(len(groups)):
            c = L(2 + j); put(ws, r, 2 + j, f'=SUMPRODUCT(({kr}={c}$4)*{wr}*Rendimenti!${S}{D0+t}:${E}{D0+t})/SUMIF({kr},{c}$4,{wr})', fmt=PCT)
    GN = G0 + T - 1; sc = len(groups) + 3
    head(ws, 4, sc, ['Gruppo', 'N. titoli', 'Peso', 'Media aritm.', 'Media geom.', 'HPR', 'Dev. std giorn.', 'Dev. std annua'])
    for j, g in enumerate(groups):
        r = 5 + j; c = L(2 + j); rg = f'{c}${G0}:{c}${GN}'; x = lambda k: L(sc + k)
        put(ws, r, sc, g); put(ws, r, sc + 1, f'=COUNTIF({kr},{x(0)}{r})'); put(ws, r, sc + 2, f'=SUMIF({kr},{x(0)}{r},{wr})', fmt=PCT)
        put(ws, r, sc + 3, f'=AVERAGE({rg})', fmt=PCT4); ws.cell(r, sc + 5).value = ArrayFormula(f'{x(5)}{r}', f'=PRODUCT(1+{rg})-1')
        ws.cell(r, sc + 5).number_format = PCT; ws.cell(r, sc + 5).border = BOX; ws.cell(r, sc + 5).fill = FILL_KEY
        put(ws, r, sc + 4, f'=(1+{x(5)}{r})^(1/COUNT({rg}))-1', fmt=PCT4); put(ws, r, sc + 6, f'=STDEV.S({rg})', fmt=PCT); put(ws, r, sc + 7, f'={x(6)}{r}*SQRT(250)', fmt=PCT)
    rr = 5 + len(groups); put(ws, rr, sc, 'Portafoglio', fill=FILL_SUB); put(ws, rr, sc + 5, f"=Statistiche!G{ST0+n}", F_LINK, PCT); put(ws, rr, sc + 6, f"=Statistiche!I{ST0+n}", F_LINK, PCT)
    put(ws, rr + 1, sc, 'S&P 500', fill=FILL_SUB); put(ws, rr + 1, sc + 5, f"=Statistiche!G{ST0+n+1}", F_LINK, PCT); put(ws, rr + 1, sc + 6, f"=Statistiche!I{ST0+n+1}", F_LINK, PCT)
    bc = BarChart(); bc.title = f'HPR per {name.lower()[:-1]}o vs portafoglio e mercato'; bc.height, bc.width = 8, 16; bc.legend = None
    bc.add_data(Reference(ws, min_col=sc + 5, min_row=4, max_row=rr + 1), titles_from_data=True); bc.set_categories(Reference(ws, min_col=sc, min_row=5, max_row=rr + 1))
    ws.add_chart(bc, f'{L(sc)}{rr + 4}')
    ws.freeze_panes = 'B5'; ws.column_dimensions['A'].width = 12; ws.column_dimensions[L(sc)].width = 24
    for j in range(len(groups)): ws.column_dimensions[L(2 + j)].width = 13
    return G0, GN
SE0, SEN = subport('Settori', SECTORS, 5, 'Rendimenti per settore')
SY0, SYN = subport('Stili', STYLES, 6, 'Rendimenti per stile di investimento')

# ======================= BASE 100 =======================
bz = wb.create_sheet('Base100')
title(bz, 'Indici cumulati base 100:  I(t) = I(t-1) · (1 + r(t)),  I(30/06) = 100')
series = [(t, 'Rendimenti', 2 + j) for j, t in enumerate(tk)] + [('Portafoglio', 'Rendimenti', PFc), ('SPX', 'Rendimenti', SPXc)] \
         + [(s, 'Settori', 2 + j) for j, s in enumerate(SECTORS)] + [(s, 'Stili', 2 + j) for j, s in enumerate(STYLES)]
head(bz, 3, 1, ['Data'] + [s[0] for s in series]); B0 = 4
put(bz, B0, 1, f'=Prezzi!A{R0}', F_LINK, DATE)
for j, (nm, sh, col) in enumerate(series):
    put(bz, B0, 2 + j, 100, F_IN, '0.00')
    off = (D0 if sh == 'Rendimenti' else 5)
    for t in range(T):
        r = B0 + 1 + t; put(bz, r, 2 + j, f'={L(2+j)}{r-1}*(1+{sh}!{L(col)}{off+t})', fmt='0.00')
for t in range(T): put(bz, B0 + 1 + t, 1, f'=Rendimenti!A{D0+t}', F_LINK, DATE)
BN = B0 + T; bz.freeze_panes = 'B4'; bz.column_dimensions['A'].width = 12

# ======================= GRAFICI =======================
gr = wb.create_sheet('Grafici'); title(gr, 'Andamento nel tempo (base 100 = 30/06/2026)')
def line(ttl, cols_idx, anchor, w=24, h=10):
    ch = LineChart(); ch.title = ttl; ch.y_axis.title = 'Indice (base 100)'; ch.width, ch.height = w, h
    ch.x_axis.number_format = 'dd/mm'; ch.x_axis.majorTimeUnit = 'months'
    for ci in cols_idx:
        s = Series(Reference(bz, min_col=ci, min_row=B0, max_row=BN), title_from_data=False, title=None)
        s.tx = None; ch.series.append(s)
        from openpyxl.chart.series import SeriesLabel; from openpyxl.chart.data_source import StrRef
        s.tx = SeriesLabel(strRef=StrRef(f"'Base100'!${L(ci)}$3")); s.smooth = False; s.graphicalProperties.line.width = 15000
    ch.set_categories(Reference(bz, min_col=1, min_row=B0, max_row=BN)); ch.legend.position = 'b'
    lo, hi = YR(cols_idx); ch.y_axis.scaling.min, ch.y_axis.scaling.max = lo, hi; gr.add_chart(ch, anchor)
import math
_r = prices.pct_change().dropna(); _w = (port.azioni*port.prezzo_acquisto); _w = pd.Series((_w/_w.sum()).values, index=tk)
_ser = {t: _r[t] for t in tk + ['SPX']}; _ser['Portafoglio'] = _r[tk] @ _w
for col_, groups_ in (('settore', SECTORS), ('stile', STYLES)):
    for g in groups_:
        m_ = list(port.ticker[port[col_] == g]); _ser[g] = _r[m_] @ (_w[m_]/_w[m_].sum())
def YR(cols_idx):  # min/max dell'asse Y calcolati dai dati (solo per la scala del grafico)
    vals = [v for ci in cols_idx for v in 100*(1+_ser[series[ci-2][0]]).cumprod()] + [100]
    return math.floor(min(vals)/5)*5, math.ceil(max(vals)/5)*5
idx = {nm: 2 + j for j, (nm, _, _) in enumerate(series)}
line('Portafoglio vs S&P 500', [idx['Portafoglio'], idx['SPX']], 'A3')
line('Sotto-portafogli per settore vs S&P 500', [2 + n + 2 + k for k in range(len(SECTORS))] + [idx['SPX']], 'A25')
line('Sotto-portafogli per stile vs S&P 500', [2 + n + 2 + len(SECTORS) + k for k in range(3)] + [idx['SPX']], 'A47')
for k, s in enumerate(STYLES):
    line(f'Titoli {s}', [2 + j for j, t in enumerate(tk) if port.stile[j] == s], f'A{69 + 22*k}')

# ======================= EVENTI =======================
ev = wb.create_sheet('Eventi')
title(ev, 'Rendimenti anomali (6.1.6)', 'Rend. in eccesso = r(i,t) - r(SPX,t). Evidenziati i movimenti oltre ±2 deviazioni standard del titolo')
head(ev, 4, 1, ['Titolo', 'Giorno migliore', 'Data', 'Giorno peggiore', 'Data', 'Max rend. in eccesso vs SPX', 'Data', 'N. giorni oltre ±2σ', 'Causa / notizia (da ricerca)'])
spx = RR(SPXc)
for j, t in enumerate(tk + ['SPX']):
    r = 5 + j; col = 2 + j if j < n else SPXc; rg = RR(col); dates = f'Rendimenti!$A${D0}:$A${DN}'
    put(ev, r, 1, f'=Rendimenti!{L(col)}3', F_LINK)
    put(ev, r, 2, f'=MAX({rg})', fmt=PCT); put(ev, r, 3, f'=INDEX({dates},MATCH(B{r},{rg},0))', fmt=DATE)
    put(ev, r, 4, f'=MIN({rg})', fmt=PCT); put(ev, r, 5, f'=INDEX({dates},MATCH(D{r},{rg},0))', fmt=DATE)
    if j < n:
        ev.cell(r, 6).value = ArrayFormula(f'F{r}', f'=MAX({rg}-{spx})'); ev.cell(r, 6).number_format = PCT; ev.cell(r, 6).border = BOX
        ev.cell(r, 7).value = ArrayFormula(f'G{r}', f'=INDEX({dates},MATCH(F{r},{rg}-{spx},0))'); ev.cell(r, 7).number_format = DATE; ev.cell(r, 7).border = BOX
        ev.cell(r, 8).value = ArrayFormula(f'H{r}', f'=SUM(--(ABS({rg}-AVERAGE({rg}))>2*STDEV.S({rg})))'); ev.cell(r, 8).border = BOX
    put(ev, r, 9, '', F_IN)
widths(ev, {'A': 10, 'B': 12, 'C': 12, 'D': 12, 'E': 12, 'F': 14, 'G': 12, 'H': 11, 'I': 70})

# ======================= COV / BETA =======================
cv = wb.create_sheet('Cov_Beta'); allc = [2 + j for j in range(n)] + [SPXc]; m = len(allc)
title(cv, 'Matrice varianza-covarianza dei rendimenti giornalieri (COVARIANCE.S) e Beta', 'Beta(i) = Cov(r(i), R(m)) / Var(R(m)), mercato = S&P 500')
head(cv, 4, 1, [''] + tk + ['SPX'])
for a in range(m):
    put(cv, 5 + a, 1, f'=Rendimenti!{L(allc[a])}3', F_HEAD, fill=FILL_HEAD)
    for b in range(m):
        f = f'=VAR.S({RR(allc[a])})' if a == b else f'=COVARIANCE.S({RR(allc[a])},{RR(allc[b])})'
        put(cv, 5 + a, 2 + b, f, fmt='0.000000', fill=FILL_SUB if a == b else None)
CN = 5 + m - 1; mc = L(1 + m)
cv.conditional_formatting.add(f'B5:{mc}{CN}', ColorScaleRule(start_type='min', start_color='FFFFFF', end_type='max', end_color='F4B183'))
b0 = CN + 3; head(cv, b0, 1, ['Titolo', 'Cov(i, SPX)', 'Var(SPX)', 'Beta', 'Peso', 'Peso × Beta', 'Media aritm. giorn.', 'Interpretazione'])
for j in range(n):
    r = b0 + 1 + j
    put(cv, r, 1, f'=A{5+j}', F_CALC); put(cv, r, 2, f'={mc}{5+j}', fmt='0.000000'); put(cv, r, 3, f'=${mc}${CN}', fmt='0.000000')
    put(cv, r, 4, f'=B{r}/C{r}', fmt='0.00', fill=FILL_KEY); put(cv, r, 5, f'=Portafoglio!J{P0+j}', F_LINK, PCT); put(cv, r, 6, f'=D{r}*E{r}', fmt='0.0000')
    put(cv, r, 7, f'=Statistiche!E{ST0+j}', F_LINK, PCT4); put(cv, r, 8, f'=IF(D{r}>1,"Più rischioso del mercato (aggressivo)",IF(D{r}<1,"Meno rischioso del mercato (difensivo)","Come il mercato"))')
BE = b0 + n; rb = BE + 1
put(cv, rb, 1, 'SPX', fill=FILL_SUB); put(cv, rb, 4, f'={mc}{CN}/{mc}{CN}', fmt='0.00', fill=FILL_SUB)
put(cv, rb + 2, 1, 'BETA DI PORTAFOGLIO  β(p) = Σ w(i)·β(i)').font = Font(bold=True); put(cv, rb + 2, 4, f'=SUMPRODUCT(E{b0+1}:E{BE},D{b0+1}:D{BE})', fmt='0.00', fill=FILL_KEY)
wb.defined_names['BetaPortafoglio'] = DefinedName('BetaPortafoglio', attr_text=f'Cov_Beta!$D${rb+2}')
put(cv, rb + 3, 1, 'Rendimento medio giornaliero portafoglio'); put(cv, rb + 3, 4, f'=Statistiche!E{ST0+n}', F_LINK, PCT4)
put(cv, rb + 4, 1, 'Rendimento medio giornaliero S&P 500'); put(cv, rb + 4, 4, f'=Statistiche!E{ST0+n+1}', F_LINK, PCT4)
put(cv, rb + 5, 1, 'Correlazione beta - rendimento medio (titoli)'); put(cv, rb + 5, 4, f'=CORREL(D{b0+1}:D{BE},G{b0+1}:G{BE})', fmt='0.00')
sc_ = ScatterChart(); sc_.title = 'Beta vs rendimento medio giornaliero'; sc_.style = 13; sc_.x_axis.title = 'Beta'; sc_.y_axis.title = 'Rendimento medio giornaliero'
s = Series(Reference(cv, min_col=7, min_row=b0 + 1, max_row=BE), Reference(cv, min_col=4, min_row=b0 + 1, max_row=BE), title='Titoli')
s.marker.symbol = 'circle'; s.marker.size = 8; s.graphicalProperties.line.noFill = True; s.trendline = Trendline(trendlineType='linear', dispRSqr=True)
sc_.series.append(s); sc_.y_axis.number_format = '0.00%'; sc_.width, sc_.height = 18, 11; cv.add_chart(sc_, f'J{b0}')
cv.column_dimensions['A'].width = 14; cv.freeze_panes = 'B5'
for j in range(2, m + 2): cv.column_dimensions[L(j)].width = 11

# ======================= CORRELAZIONE =======================
co = wb.create_sheet('Correlazione'); title(co, 'Matrice di correlazione dei rendimenti giornalieri (CORREL)')
head(co, 4, 1, [''] + tk + ['SPX'])
for a in range(m):
    put(co, 5 + a, 1, f'=Rendimenti!{L(allc[a])}3', F_HEAD, fill=FILL_HEAD)
    for b in range(m): put(co, 5 + a, 2 + b, f'=CORREL({RR(allc[a])},{RR(allc[b])})', fmt='0.00')
co.conditional_formatting.add(f'B5:{mc}{CN}', ColorScaleRule(start_type='num', start_value=-1, start_color='5B9BD5', mid_type='num', mid_value=0, mid_color='FFFFFF', end_type='num', end_value=1, end_color='F8696B'))
k = CN + 3; sn = L(n + 1)
put(co, k, 1, 'Correlazione media tra coppie di titoli'); put(co, k, 5, f'=(SUM(B5:{sn}{4+n})-{n})/({n}*({n}-1))', fmt='0.00', fill=FILL_KEY)
put(co, k + 1, 1, 'Correlazione massima tra due titoli'); co.cell(k + 1, 5).value = ArrayFormula(f'E{k+1}', f'=MAX(IF(B5:{sn}{4+n}<0.9999,B5:{sn}{4+n}))'); co.cell(k + 1, 5).number_format = '0.00'
put(co, k + 2, 1, 'Correlazione minima tra due titoli'); put(co, k + 2, 5, f'=MIN(B5:{sn}{4+n})', fmt='0.00')
put(co, k + 3, 1, 'Correlazione media titoli - S&P 500'); put(co, k + 3, 5, f'=AVERAGE({mc}5:{mc}{4+n})', fmt='0.00')
co.column_dimensions['A'].width = 14; co.freeze_panes = 'B5'
for j in range(2, m + 2): co.column_dimensions[L(j)].width = 7

# ======================= SHARPE =======================
sh = wb.create_sheet('Sharpe')
title(sh, 'Rendimento corretto per il rischio: Sharpe ratio = (R(p, annuo) - Rf) / σ(p, annuo)', 'R annuo = (1 + media aritmetica mensile)^12 - 1   |   σ annua = σ giornaliera · √250   |   prezzi di fine mese')
head(sh, 4, 1, ['Fine mese'] + cols); M0 = 5
for k in range(5):
    r = M0 + k; put(sh, r, 1, f'=EOMONTH(DATE(2026,6,1),{k})', fmt=DATE)
    for j in range(n + 1):
        c = L(2 + j); put(sh, r, 2 + j, f'=INDEX(Prezzi!{c}${R0}:{c}${RN},MATCH($A{r},Prezzi!$A${R0}:$A${RN},1))', F_LINK, '#,##0.00')
r1 = M0 + 6; head(sh, r1, 1, ['Rend. mensile'] + cols + ['Portafoglio'])
for k in range(4):
    r = r1 + 1 + k; put(sh, r, 1, f'=TEXT(A{M0+1+k},"mmm yyyy")')
    for j in range(n + 1):
        c = L(2 + j); put(sh, r, 2 + j, f'=({c}{M0+1+k}-{c}{M0+k})/{c}{M0+k}', fmt=PCT)
    put(sh, r, n + 3, f'=SUMPRODUCT(Portafoglio!$J${P0}:$J${P1},TRANSPOSE(B{r}:{L(n+1)}{r}))', fmt=PCT, fill=FILL_KEY)
    sh.cell(r, n + 3).value = ArrayFormula(f'{L(n+3)}{r}', f'=SUMPRODUCT(Portafoglio!$J${P0}:$J${P1},TRANSPOSE(B{r}:{L(n+1)}{r}))')
r2 = r1 + 7; head(sh, r2, 1, ['Indicatore', 'Portafoglio', 'S&P 500'])
pc, mk = L(n + 3), L(n + 2); MR = f'{r1+1}:{{c}}{r1+4}'
rows_ = [('Rendimento medio mensile (aritm.)', f'=AVERAGE({pc}{r1+1}:{pc}{r1+4})', f'=AVERAGE({mk}{r1+1}:{mk}{r1+4})', PCT),
         ('Rendimento annuo  (1+Rm)^12 - 1', f'=(1+B{r2+1})^12-1', f'=(1+C{r2+1})^12-1', PCT),
         ('Dev. std giornaliera', f'=Statistiche!I{ST0+n}', f'=Statistiche!I{ST0+n+1}', PCT),
         ('Dev. std annua  σ·√250', f'=B{r2+3}*SQRT(250)', f'=C{r2+3}*SQRT(250)', PCT),
         ('Risk-free (T-bill 12 mesi)', 0.04, f'=B{r2+5}', PCT),
         ('SHARPE RATIO', f'=(B{r2+2}-B{r2+5})/B{r2+4}', f'=(C{r2+2}-C{r2+5})/C{r2+4}', '0.00'),
         ('Beta', '=BetaPortafoglio', 1, '0.00')]
for i, (lab, a, b, fm) in enumerate(rows_):
    r = r2 + 1 + i; key = lab == 'SHARPE RATIO'
    put(sh, r, 1, lab, fill=FILL_KEY if key else None).font = Font(bold=key)
    put(sh, r, 2, a, F_IN if isinstance(a, float) else (F_LINK if 'Statistiche' in str(a) or 'Beta' in str(a) else F_CALC), fm, FILL_KEY if key else None)
    put(sh, r, 3, b, F_LINK if 'Statistiche' in str(b) else F_CALC, fm, FILL_KEY if key else None)
wb.defined_names['Rf'] = DefinedName('Rf', attr_text=f'Sharpe!$B${r2+5}')
put(sh, r2 + 9, 1, 'Esito'); put(sh, r2 + 9, 2, f'=IF(B{r2+6}>C{r2+6},"Il portafoglio ha battuto il mercato in termini di rendimento corretto per il rischio","Il mercato ha offerto un rendimento corretto per il rischio superiore al portafoglio")')
bc = BarChart(); bc.title = 'Sharpe ratio: portafoglio vs S&P 500'; bc.height, bc.width = 7, 12; bc.legend = None
bc.add_data(Reference(sh, min_col=2, max_col=3, min_row=r2 + 6), from_rows=True, titles_from_data=False)
bc.set_categories(Reference(sh, min_col=2, max_col=3, min_row=r2)); sh.add_chart(bc, f'E{r2}')
widths(sh, {'A': 34, 'B': 14, 'C': 14}); sh.freeze_panes = 'B5'

# ======================= CONTROLLI =======================
ck = wb.create_sheet('Controlli'); title(ck, 'Controlli automatici di coerenza'); head(ck, 3, 1, ['Controllo', 'Valore', 'Esito'])
checks = [('Somma dei pesi = 100%', f'=Portafoglio!J{tr}', f'=ABS(B4-1)<0.000001'),
          ('N. società tra 10 e 30', f'=Portafoglio!I{tr+5}', '=AND(B5>=10,B5<=30)'),
          ('Capitale investito ≥ 95%', f'=Portafoglio!I{tr+4}', '=B6>=0.95'),
          ('N. rendimenti = N. prezzi - 1', f'=Statistiche!D{ST0}', f'=B7=COUNT(Prezzi!B{R0}:B{RN})-1'),
          ('Beta del mercato = 1', f'=Cov_Beta!D{rb}', '=ABS(B8-1)<0.000001'),
          ('Matrice di covarianza simmetrica', f'=Cov_Beta!C5-Cov_Beta!B6', '=ABS(B9)<1E-12'),
          ('Diagonale correlazione = 1', '=Correlazione!B5', '=ABS(B10-1)<0.000001'),
          ('Varianza in matrice = VAR.S in Statistiche', f'=Cov_Beta!B5-Statistiche!H{ST0}', '=ABS(B11)<1E-12'),
          ('HPR coerente con i prezzi', f'=Statistiche!G{ST0}-(Prezzi!B{RN}/Prezzi!B{R0}-1)', '=ABS(B12)<0.000001')]
for i, (a, b, c) in enumerate(checks):
    put(ck, 4 + i, 1, a); put(ck, 4 + i, 2, b, F_LINK, '0.0000'); put(ck, 4 + i, 3, c, fill=FILL_SUB)
ck.conditional_formatting.add(f'C4:C{3+len(checks)}', CellIsRule(operator='equal', formula=['TRUE'], fill=PatternFill('solid', fgColor='C6EFCE')))
ck.conditional_formatting.add(f'C4:C{3+len(checks)}', CellIsRule(operator='equal', formula=['FALSE'], fill=PatternFill('solid', fgColor='FFC7CE')))
put(ck, 5 + len(checks), 1, 'TUTTI I CONTROLLI SUPERATI', fill=FILL_KEY).font = Font(bold=True); put(ck, 5 + len(checks), 3, f'=AND(C4:C{3+len(checks)})', fill=FILL_KEY)
widths(ck, {'A': 44, 'B': 14, 'C': 12})

for ws in wb.worksheets: ws.sheet_properties.tabColor = {'Indice': NAVY, 'Controlli': '70AD47'}.get(ws.title, '8EA9DB')
for ws in wb.worksheets:
    for ch in ws._charts:
        for ax in ('x_axis', 'y_axis'):
            if hasattr(ch, ax): getattr(ch, ax).delete = False
# prefisso _xlfn per le funzioni statistiche moderne (altrimenti #NAME?)
import re
FIX = re.compile(r'(?<![\w.])(VAR\.S|STDEV\.S|COVARIANCE\.S)\(')
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            v = c.value
            if isinstance(v, str) and v.startswith('='): c.value = FIX.sub(r'_xlfn.\1(', v)
            elif isinstance(v, ArrayFormula): v.text = FIX.sub(r'_xlfn.\1(', v.text)
os.makedirs('out', exist_ok=True); wb.save(OUT); print('Salvato', OUT)
