"""Relazione iniziale SMG: HTML -> PDF (Chromium), stile della presentazione. Limite 8.000 caratteri spazi esclusi."""
import os, base64, html, pandas as pd, numpy as np
import subprocess

GROUP = os.environ.get('SMG_GROUP', 'ZZ Capital')
MEMBERS = [('Cristiano Zonta', '909123', 'spokesperson'), ('Mattia Zanrosso', '909945', None)]
TRANCHE2_DONE = os.environ.get('SMG_TRANCHE2', '0') == '1'
p = pd.read_csv('dati/portafoglio_iniziale.csv'); wl = pd.read_csv('dati/watchlist.csv')
p['cv'] = p.azioni*p.prezzo_acquisto; p['w'] = p.cv/p.cv.sum(); inv = p.cv.sum()
has_z = p.zacks_rank.notna().any()
BG = {'CVX': 'Second-largest US integrated oil major', 'VLO': 'Largest independent US refiner', 'XOM': 'Largest US oil, gas and chemicals group',
      'COF': 'Credit-card issuer and consumer bank (owns Discover network)', 'C': 'Global bank, multi-year restructuring under way',
      'ELV': 'Health insurer (Anthem Blue Cross Blue Shield plans)', 'NUE': 'Largest US steelmaker (electric arc furnaces)',
      'TMUS': 'Leading US wireless carrier, 5G leader', 'MU': 'Memory chips (DRAM, NAND, HBM for AI servers)',
      'APH': 'Connectors and sensors, AI data-centre interconnect', 'MSFT': 'Software and Azure cloud, AI platforms',
      'PWR': 'Power-grid and utility infrastructure contractor', 'URI': 'World\'s largest equipment-rental company',
      'BLK': 'World\'s largest asset manager (iShares ETFs)', 'UNH': 'Largest US health insurer plus Optum services',
      'REGN': 'Biotech: Dupixent, Eylea, oncology pipeline', 'MCK': 'Largest US pharmaceutical distributor',
      'DHR': 'Life-science and diagnostics tools', 'MA': 'Global card-payment network'}
SHORT = {'Financial Services': 'Financials', 'Communication Services': 'Communication', 'Basic Materials': 'Materials', 'Consumer Cyclical': 'Cons. Discr.'}
TRIG = {'ANET': 'AI rebound', 'OXY': 'oil upside', 'PSX': 'refining margins', 'COP': 'oil upside', 'CVS': 'value health', 'CI': 'value health', 'AIG': 'rates', 'MET': 'rates',
        'CB': 'defensive insurer', 'AMD': 'AI rebound', 'AVGO': 'AI rebound', 'KLAC': 'chip capex', 'NVDA': 'AI rebound', 'GEV': 'grid capex', 'CEG': 'power demand',
        'TXN': 'chip cycle', 'TMO': 'health momentum', 'ISRG': 'health growth', 'V': 'payments', 'HCA': 'health momentum', 'TRV': 'insurance pricing',
        'ETN': 'grid capex', 'PH': 'industrial cycle', 'RTX': 'defence', 'ORLY': 'defensive retail'}
FONTS = os.path.abspath('assets/fonts')
f = lambda x, d=1: 'n.a.' if pd.isna(x) else f'{x:.{d}f}'
e = html.escape
def b64(path): return base64.b64encode(open(path, 'rb').read()).decode()
def table(head, rows, num_from, cls='', num_to=99):
    th = ''.join(f'<th class="{"r" if num_from <= j <= num_to else ""}">{h}</th>' for j, h in enumerate(head))
    tr = ''
    for row in rows:
        tds = ''
        for j, v in enumerate(row):
            c = ('r ' if num_from <= j <= num_to else '') + ('tk' if j == 0 else '')
            tds += f'<td class="{c}">{v}</td>'
        tr += f'<tr>{tds}</tr>'
    return f'<table class="{cls}"><tbody><tr class="h">{th}</tr>{tr}</tbody></table>'

# ---------------- contenuto ----------------
w = p.w; sec = p.groupby('settore').w.sum().sort_values(ascending=False); sty = p.groupby('stile').w.sum()
zline = ('The Zacks Rank (table in C.b) is a second check: eight holdings are rated Strong Buy or Buy, eleven Hold and none Sell. ' if has_z else '')
tranche = ('' if TRANCHE2_DONE else f'The first purchase used {inv/1e6:.1%} of the capital. On 30/11 we will add the remaining cash, less a $1,500 buffer, in equal amounts to '
           'COF, VLO, PWR and APH, the highest-scoring holdings outside healthcare, so the 25% cap still holds.')
members = '; '.join(f'{n}, student ID {i}' + (f' ({r})' if r else '') for n, i, r in MEMBERS)

t_port = table(['Ticker', 'Company', 'Industry', 'Shares', 'Price', 'Weight', 'Background'],
    [[r.ticker, e(r.nome.replace('ExxonMobil Holdings Corporation', 'Exxon Mobil Corp.')), e(r.industria), f'{r.azioni:,}', f'${r.prezzo_acquisto:,.2f}', f'{r.w:.1%}', e(BG[r.ticker])] for _, r in p.iterrows()]
    + [['', '<b>Total invested</b>', '', '', '', f'<b>{inv/1e6:.1%}</b>', f'${inv:,.0f} of $1,000,000; cash {1-inv/1e6:.1%}']], 3, 'port', 5)
hdr = ['Ticker', 'Style', 'Fwd P/E', 'P/B', 'PEG', 'ABR', 'Rev. up/down 30d', 'EPS est. change 60d', 'Surprise 4Q', 'Score'] + (['Zacks Rank'] if has_z else [])
rows = [[r.ticker, r.stile, f(r.PE_fwd), f(r.PB), f(r.PEG, 2), f(r.ABR, 2), f'{r.rev_su_30g:.0f} / {r.rev_giu_30g:.0f}', f'{r["var_stima_60g_%"]:+.1f}%',
         f'{r["surprise_4q_%"]:+.1f}%', f(r.score, 2)] + ([f(r.zacks_rank, 0)] if has_z else []) for _, r in p.iterrows()]
rows.append(['<b>Median</b>', '', f(p.PE_fwd.median()), f(p.PB[p.PB > 0].median()), f(p.PEG.median(), 2), f(p.ABR.median(), 2), '', f'{p["var_stima_60g_%"].median():+.1f}%',
             f'{p["surprise_4q_%"].median():+.1f}%', f(p.score.median(), 2)] + ([''] if has_z else []))
t_par = table(hdr, rows, 2, 'par')
t_wl = table(['Ticker', 'Sector', 'Style', 'Fwd P/E', 'PEG', 'ABR', 'Rev. up/down', 'EPS est. 60d', 'Score', 'Buy if'],
    [[r.ticker, SHORT.get(r.settore, r.settore), r.stile, f(r.PE_fwd), f(r.PEG, 2), f(r.ABR, 2), f'{r.rev_su_30g:.0f} / {r.rev_giu_30g:.0f}', f'{r["var_stima_60g_%"]:+.1f}%', f(r.score, 2), TRIG[r.ticker]] for _, r in wl.iterrows()], 3, 'wl', 8)

body = f'''
<header class="hero">
  <div class="pill"><span>{e(GROUP)}</span><i>01</i></div>
  <h1>Stock Market Game 2026: <em>Initial Report</em></h1>
  <div class="sub">Corporate Finance and Financial Institutions 2</div>
</header>

<section><h2><b>A</b>Group name and composition</h2>
<p><span class="lab">Group:</span> {e(GROUP)}<br><span class="lab">Members:</span> {e(members)}</p></section>

<section><h2><b>B</b>Strategy adopted</h2>
<p class="lead">We buy US large caps whose earnings estimates are being raised, only at moderate valuations, and spread them across value, growth and momentum stocks.</p>
<h3>Why earnings revisions</h3><p>Leonard Zacks (1979) found that changes in analysts' earnings estimates move stock prices more than any other factor over one to three months,
which is about the length of the game. We rebuilt his ranking from analyst data for 151 large caps. Each stock gets a revision score made of the share of upward EPS revisions in the last
30 days (Agreement, weight 40%), the change in the consensus EPS estimate over 60 days (Magnitude, 25%), the Average Broker Recommendation (20%) and the gap between the analysts' price
target and the price (Upside, 15%). The average EPS surprise of the last four quarters is used as a check. {zline}We keep the limits of this signal in mind: it works over a short horizon
and favours smaller companies and whichever industry is in fashion.</p>
<h3>Why now</h3><p>In September 2026 the Fed raised rates for the first time in three years, and its officials are signalling more hikes. US producer prices are rising at
the fastest pace since 2022, and 47% of fund managers expect stagflation. Brent crude went above $110 in October because of the conflict between the US and Iran, and AI and chip stocks have
fallen sharply since. With the S&amp;P 500 at about 21.5 times forward earnings, we do not expect valuations to rise further, so prices will have to follow earnings. This is why we buy
companies with rising estimates and a median forward P/E of about 13. No style has a clear lead in this market, so we mix them. Our value stocks (oil companies and banks) gain from high oil
prices and higher rates. Our growth stocks supply AI data centres and the power grid and already report growing earnings. Our momentum stocks are mostly healthcare companies, which have led
the market as a defensive sector. Technology is 19% of the portfolio against about 33% of the S&amp;P 500. We hold no utilities, real estate or consumer discretionary stocks, which suffer
most from rising rates and weak consumer spending.</p></section>

<section class="pb"><h2><b>C</b>Initial portfolio composition</h2>
<h3>a. Companies and shares held</h3><p>Market orders executed on 24/11/2026 at the prices below, with no commission.</p>
{t_port}
<div class="pb"></div><h3>b. Selection parameters and criteria</h3><p>We kept stocks with more upward than downward estimate revisions (Agreement above 0) and an ABR of 2.5 or better, then
sorted them by style. Value: forward P/E below 14 and P/B below 3.5. Growth: EPS growth above 25% and PEG below 1.6. Momentum: 6-month return above 20% and 3-month return above 5%.
Within each style we took the highest scores, subject to the sector limits in point d.</p>
{t_par}
<p class="note">MCK has negative book value because of share buybacks, so its P/B is not meaningful. Data: Yahoo Finance, 23/11/2026{'; Zacks Rank: zacks.com, 27/11/2026.' if has_z else '.'}</p>
<h3>c. Weighting criterion</h3><p>Weights follow conviction. Each stock starts at 5% and moves up or down by up to 2.5 points with its standardised revision score; the
weights are then normalised and capped at 25% per sector, which gives a range from {w.min():.1%} to {w.max():.1%}. Equal weights would ignore the differences in signal strength. Value weights
would put most of the money into the largest companies and raise the technology share we want to keep low. {tranche}</p>
<h3>d. Diversification</h3><p>By sector: {', '.join(f'{SHORT.get(k, k)} {v:.0%}' for k, v in sec.items())}. By style: {', '.join(f'{k} {sty[k]:.0%}' for k in ['Value', 'Growth', 'Momentum'])}.
No sector is above 25% and we hold only three technology stocks. We picked sectors that offset each other. Energy gains when oil spikes, the shock that hurts technology and consumers most,
while healthcare holds up in a slowdown. From July to October 2026 the average correlation between pairs of our stocks was 0.05, and the weighted 5-year beta of the portfolio is 0.97.</p></section>

<section class="pb"><h2><b>D</b>Monitoring list</h2>
<p>These 25 stocks pass the same screen and would replace holdings whose estimates start to be cut.</p>
{t_wl}</section>
'''
css = f'''
@font-face {{ font-family: InterD; font-weight: 300; src: url("file://{FONTS}/InterDisplay-Light.ttf"); }}
@font-face {{ font-family: InterD; font-weight: 400; src: url("file://{FONTS}/InterDisplay-Regular.ttf"); }}
@font-face {{ font-family: Inter; font-weight: 400; src: url("file://{FONTS}/Inter-Regular.ttf"); }}
@font-face {{ font-family: Inter; font-weight: 500; src: url("file://{FONTS}/Inter-Medium.ttf"); }}
@font-face {{ font-family: Inter; font-weight: 600; src: url("file://{FONTS}/Inter-SemiBold.ttf"); }}
@font-face {{ font-family: Mono; src: url("file:///usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf"); }}
@page {{ size: A4; margin: 18mm 18mm 16mm 18mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family: Inter; font-size: 9.6pt; line-height: 1.55; color: #2B3643; margin: 0; font-feature-settings: "tnum" 1; }}
.hero {{ background: #0F1B2A url(data:image/png;base64,{b64('assets/bg_dark.png')}) center/cover; border-radius: 12px; padding: 22px 26px 22px; margin-bottom: 26px; color: #F2F5F8; }}
.pill {{ display: inline-flex; align-items: center; gap: 8px; border: 0.6pt solid rgba(255,255,255,.55); border-radius: 20px; padding: 3px 4px 3px 11px; font: 7pt Mono; }}
.pill i {{ font-style: normal; background: #F2F5F8; color: #0F1B2A; border-radius: 5px; padding: 1px 5px; }}
h1 {{ font-family: InterD; font-weight: 300; font-size: 25pt; line-height: 1.12; margin: 34px 0 8px; letter-spacing: -0.3px; }}
h1 em {{ font-style: normal; color: #9FC6E6; }}
.sub {{ font-family: Inter; font-size: 9pt; color: #C3D2DE; }}
h2 {{ font-family: InterD; font-weight: 400; font-size: 15.5pt; color: #0F1B2A; margin: 26px 0 12px; display: flex; align-items: center; gap: 10px; letter-spacing: -0.1px; }}
h2:first-child {{ margin-top: 0; }}
h2 b {{ font: 500 8pt Inter; background: #0F1B2A; color: #F2F5F8; border-radius: 5px; width: 20px; height: 20px; display: inline-flex; align-items: center; justify-content: center; }}
h3 {{ font-family: Inter; font-weight: 600; font-size: 10pt; color: #0F1B2A; margin: 18px 0 6px; }}
p {{ margin: 0 0 10px; text-align: left; hyphens: none; }}
p.lead {{ font-family: InterD; font-weight: 300; font-size: 13pt; line-height: 1.4; color: #0F1B2A; margin: 0 0 16px; }}
.lab {{ font-weight: 600; color: #0F1B2A; }}
.note {{ font-size: 7.6pt; color: #66727F; margin: 6px 0 0; }}
.pb {{ break-before: page; }}
table {{ width: 100%; border-collapse: collapse; margin: 10px 0 4px; font-size: 8pt; line-height: 1.35; break-inside: avoid; }}
tr.h th {{ font-family: Inter; font-weight: 500; font-size: 7pt; color: #66727F; text-transform: uppercase; letter-spacing: 0.4px; text-align: left; padding: 0 7px 7px; border-bottom: 1pt solid #0F1B2A; vertical-align: bottom; }}
td {{ padding: 5.2px 7px; border-bottom: 0.5pt solid #E1E5EC; vertical-align: top; }}
td.tk {{ font-weight: 600; color: #3D6A8E; }}
.r {{ text-align: right; white-space: nowrap; }}
tr.h th.r {{ text-align: right; }}
table.port td:nth-child(2) {{ color: #0F1B2A; font-weight: 500; }}
table.port td:last-child, table.port td:nth-child(3) {{ color: #55616E; }}
table.port tbody tr:last-child td, table.par tbody tr:last-child td {{ border-top: 1pt solid #0F1B2A; border-bottom: none; font-weight: 600; color: #0F1B2A; }}
table.wl td:last-child {{ color: #55616E; }}
'''
doc = f'<!DOCTYPE html><html><head><meta charset="utf-8"><title>SMG Initial Report - {e(GROUP)}</title><style>{css}</style></head><body>{body}</body></html>'
os.makedirs('out', exist_ok=True); hp = os.path.abspath('out/_report1.html'); open(hp, 'w').write(doc)
out = f"out/{GROUP.replace(' ', '_')}_report1.pdf"
js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();"
      f"await p.goto('file://{hp}');await p.waitForTimeout(400);await p.pdf({{path:'{os.path.abspath(out)}',format:'A4',printBackground:true,preferCSSPageSize:true}});await b.close();}})();")
subprocess.run(['node', '-e', js], check=True)
os.remove(hp); print(out)
