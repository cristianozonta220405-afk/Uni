"""Relazione iniziale SMG (PDF, <= 8.000 caratteri spazi esclusi)."""
import os, pandas as pd, numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

GROUP = os.environ.get('SMG_GROUP', '[GROUP NAME]')
MEMBERS = os.environ.get('SMG_MEMBERS', '[Name Surname, student ID] (spokesperson); [Name Surname, ID]; [Name Surname, ID]; [Name Surname, ID]')
p = pd.read_csv('dati/portafoglio_iniziale.csv'); wl = pd.read_csv('dati/watchlist.csv')
p['cv'] = p.azioni*p.prezzo_acquisto; p['w'] = p.cv/p.cv.sum(); inv = p.cv.sum()
has_z = p.zacks_rank.notna().any()
BG = {'CVX': 'Second-largest US integrated oil major', 'VLO': 'Largest independent US refiner', 'XOM': 'Largest US integrated oil & gas and chemicals group',
      'COF': 'Credit-card issuer and consumer bank (owns Discover network)', 'C': 'Global bank, multi-year restructuring under way',
      'ELV': 'Health insurer (Anthem Blue Cross Blue Shield plans)', 'NUE': 'Largest US steelmaker (electric arc furnaces)',
      'TMUS': 'Leading US wireless carrier, 5G leader', 'MU': 'Memory chips (DRAM, NAND, HBM for AI servers)',
      'APH': 'Connectors and sensors, AI data-centre interconnect', 'MSFT': 'Software and Azure cloud, AI platforms',
      'PWR': 'Power-grid and utility infrastructure contractor', 'URI': 'World\'s largest equipment-rental company',
      'BLK': 'World\'s largest asset manager (iShares ETFs)', 'UNH': 'Largest US health insurer plus Optum services',
      'REGN': 'Biotech: Dupixent, Eylea, oncology pipeline', 'MCK': 'Largest US pharmaceutical distributor',
      'DHR': 'Life-science and diagnostics tools', 'MA': 'Global card-payment network'}
SHORT = {'Financial Services': 'Financials', 'Communication Services': 'Communication', 'Basic Materials': 'Materials', 'Consumer Cyclical': 'Cons. Discr.'}

ss = getSampleStyleSheet()
H1 = ParagraphStyle('h1', parent=ss['Title'], fontSize=15, spaceAfter=2, textColor=colors.HexColor('#1F3864'))
H2 = ParagraphStyle('h2', parent=ss['Heading2'], fontSize=11, spaceBefore=7, spaceAfter=3, textColor=colors.HexColor('#1F3864'))
B = ParagraphStyle('b', parent=ss['BodyText'], fontSize=9, leading=11.5, alignment=4, spaceAfter=3)
SM = ParagraphStyle('sm', parent=B, fontSize=7, leading=8.5, textColor=colors.HexColor('#404040'))
TC = ParagraphStyle('tc', parent=B, fontSize=7, leading=8, alignment=0, spaceAfter=0)
def table(data, widths, num_from=None):
    t = Table(data, colWidths=widths, repeatRows=1)
    st = [('FONT', (0, 0), (-1, -1), 'Helvetica', 7), ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 7),
          ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F3864')), ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
          ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#EEF2F8')]),
          ('GRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#BFBFBF')), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
          ('TOPPADDING', (0, 0), (-1, -1), 1.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5)]
    if num_from is not None: st.append(('ALIGN', (num_from, 1), (-1, -1), 'RIGHT'))
    t.setStyle(TableStyle(st)); return t
f = lambda x, d=1: '–' if pd.isna(x) else f'{x:.{d}f}'
el = []
el += [Paragraph('Stock Market Game 2026 – Initial Report', H1), Paragraph(f'Corporate Finance and Financial Institutions 2', SM), Spacer(1, 4)]
el += [Paragraph('A. Group name and composition', H2), Paragraph(f'<b>Group:</b> {GROUP} (Investopedia username: {GROUP}). <b>Members:</b> {MEMBERS}.', B)]

el += [Paragraph('B. Strategy adopted', H2)]
el += [Paragraph('<b>Multi-style earnings-revision strategy with valuation discipline and a defensive tilt.</b> We select US large caps whose analysts are '
    '<i>raising</i> their earnings estimates, buy them only at reasonable multiples, and spread them across value, growth and momentum styles and seven sectors.', B)]
el += [Paragraph('<b>Rationale.</b> Leonard Zacks showed that earnings-estimate revisions are the strongest short-term driver of stock prices (1–3 month horizon, '
    'matching the length of the game). We rebuilt the four Zacks criteria from analyst data and computed a revision score for 151 large caps: '
    'Agreement (share of upward revisions in the last 30 days, weight 40%), Magnitude (change of the consensus EPS estimate over 60 days, 25%), '
    'broker opinion (ABR, 20%) and Upside (analysts\' target vs price, 15%); Surprise (average EPS surprise of the last four quarters) is used as a check. '
    'The Zacks Rank is used as confirmation, aware of its limits (short horizon, small/mid-cap and industry biases).', B)]
el += [Paragraph('<b>Why it should work now.</b> The macro picture in November 2026 is uncertain: the Fed hiked in September for the first time in three years and '
    'officials lean towards further hikes; producer inflation is the highest since 2022 and 47% of fund managers describe the outlook as stagflation; the 10-year '
    'Treasury yields about 4.9%. Oil is volatile because of the US–Iran conflict (Brent above $110 in October), and AI and semiconductor stocks have sold off '
    'sharply. With the S&P 500 at about 21.5x forward earnings, returns are unlikely to come from rising multiples, so we want companies whose <i>earnings</i> are '
    'being revised up, bought at moderate valuations (median forward P/E of the portfolio about 13x). Since no single style is guaranteed to lead in this '
    'regime, we combine: <b>value</b> (energy, banks: helped by oil prices and higher rates), <b>growth at a reasonable price</b> (AI and grid-infrastructure '
    'names with real earnings support) and <b>momentum</b> (healthcare, which leads the market as a defensive sector). We underweight technology (19% vs about '
    '33% in the S&P 500) and avoid utilities, real estate and consumer discretionary, which suffer from rising rates and stagflation.', B)]

el += [Paragraph('C. Initial portfolio composition', H2), Paragraph(f'<b>a. Companies and shares held</b> (orders of 24/11/2026; market orders, $0 commission; prices are order-preview estimates, to be replaced by fill prices).', B)]
rows = [['Ticker', 'Company', 'Industry', 'Shares', 'Weight', 'Background']]
for _, r in p.iterrows():
    rows.append([r.ticker, Paragraph(r.nome.replace('ExxonMobil Holdings Corporation', 'Exxon Mobil Corp.'), TC), Paragraph(r.industria, TC), f'{r.azioni:,}', f'{r.w:.1%}', Paragraph(BG[r.ticker], TC)])
rows.append(['', 'Total invested', '', '', f'{inv/1e6:.1%}', f'${inv:,.0f} of $1,000,000; cash {1-inv/1e6:.1%}'])
el += [table(rows, [1.1*cm, 3.3*cm, 3.3*cm, 1.2*cm, 1.2*cm, 7.2*cm], num_from=3)]

el += [Spacer(1, 4), Paragraph('<b>b. Selection parameters and criteria.</b> Screening rules: (1) liquid US large caps; (2) positive revision balance '
    '(Agreement &gt; 0) and ABR ≤ 2.5; (3) style by rules – <i>value</i>: forward P/E &lt; 14 and P/B &lt; 3.5; <i>growth</i>: EPS growth &gt; 25% and PEG &lt; 1.6; '
    '<i>momentum</i>: 6-month return &gt; 20% and 3-month return &gt; 5%; (4) highest scores within each style, subject to the sector limits below.', B)]
hdr = ['Ticker', 'Style', 'Fwd P/E', 'P/B', 'PEG', 'ABR', 'Rev. up/down 30d', 'ΔEPS est. 60d', 'Surprise 4Q', 'Score'] + (['Zacks Rank'] if has_z else [])
rows = [hdr]
for _, r in p.iterrows():
    rows.append([r.ticker, r.stile, f(r.PE_fwd), f(r.PB), f(r.PEG, 2), f(r.ABR, 2), f'{r.rev_su_30g:.0f} / {r.rev_giu_30g:.0f}', f'{r["var_stima_60g_%"]:+.1f}%',
                 f'{r["surprise_4q_%"]:+.1f}%', f(r.score, 2)] + ([f(r.zacks_rank, 0)] if has_z else []))
rows.append(['Median', '', f(p.PE_fwd.median()), f(p.PB[p.PB > 0].median()), f(p.PEG.median(), 2), f(p.ABR.median(), 2), '', f'{p["var_stima_60g_%"].median():+.1f}%', f'{p["surprise_4q_%"].median():+.1f}%', f(p.score.median(), 2)] + ([''] if has_z else []))
el += [table(rows, None, num_from=2)]
el += [Paragraph('MCK has negative book value (buybacks), so P/B is not meaningful. Source: Yahoo Finance and Zacks, 23/11/2026.', SM)]

el += [Paragraph('<b>c. Weighting criterion.</b> We built a <b>conviction-weighted</b> portfolio: weight = 5% ± 2.5% according to the standardised revision score, '
    'then normalised, with a 25% cap per sector (weights from 2.7% to 8.1%). We rejected equal weights because our signals differ in strength, and value '
    'weights because they would concentrate the portfolio in mega caps and technology, against our strategy. About 3.4% stays in cash as a buffer for price '
    'moves (minimum invested 95%).', B)]
sec = p.groupby('settore').w.sum().sort_values(ascending=False); sty = p.groupby('stile').w.sum()
el += [Paragraph('<b>d. Diversification.</b> 19 stocks in 7 sectors: ' + ', '.join(f'{SHORT.get(k, k)} {v:.0%}' for k, v in sec.items()) +
    '; styles: ' + ', '.join(f'{k} {sty[k]:.0%}' for k in ['Value', 'Growth', 'Momentum']) + '. No sector exceeds 25% and technology is limited to three names. '
    'Sectors were chosen to offset each other: energy gains when oil spikes, the shock that hurts technology and consumers most, while healthcare and insurers are '
    'defensive. Over July–October 2026 the average pairwise correlation of our stocks was only 0.05, and the weighted 5-year beta is about 0.97, close to the market.', B)]

el += [Paragraph('D. Monitoring list', H2), Paragraph('Twenty-five stocks consistent with the strategy, screened with the same parameters, to replace holdings whose estimates start to be cut.', B)]
TRIG = {'ANET': 'AI rebound', 'OXY': 'oil upside', 'PSX': 'refining margins', 'COP': 'oil upside', 'CVS': 'value health', 'CI': 'value health', 'AIG': 'rates', 'MET': 'rates',
        'CB': 'defensive insurer', 'AMD': 'AI rebound', 'AVGO': 'AI rebound', 'KLAC': 'chip capex', 'NVDA': 'AI rebound', 'GEV': 'grid capex', 'CEG': 'power demand',
        'TXN': 'chip cycle', 'TMO': 'health momentum', 'ISRG': 'health growth', 'V': 'payments', 'HCA': 'health momentum', 'TRV': 'insurance pricing',
        'ETN': 'grid capex', 'PH': 'industrial cycle', 'RTX': 'defence', 'ORLY': 'defensive retail'}
rows = [['Ticker', 'Sector', 'Style', 'Fwd P/E', 'PEG', 'ABR', 'Rev. up/down', 'ΔEPS 60d', 'Score', 'Trigger']]
for _, r in wl.iterrows():
    rows.append([r.ticker, SHORT.get(r.settore, r.settore), r.stile, f(r.PE_fwd), f(r.PEG, 2), f(r.ABR, 2), f'{r.rev_su_30g:.0f} / {r.rev_giu_30g:.0f}', f'{r["var_stima_60g_%"]:+.1f}%', f(r.score, 2), TRIG[r.ticker]])
el += [table(rows, None, num_from=3)]

out = f'out/{GROUP if GROUP[0] != "[" else "groupname"}_report1.pdf'
SimpleDocTemplate(out, pagesize=A4, leftMargin=1.6*cm, rightMargin=1.6*cm, topMargin=1.3*cm, bottomMargin=1.3*cm, title='SMG Initial Report').build(el)
print(out)
