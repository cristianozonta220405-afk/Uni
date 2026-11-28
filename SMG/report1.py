"""Relazione iniziale SMG (PDF, <= 8.000 caratteri spazi esclusi)."""
import os, pandas as pd, numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

GROUP = os.environ.get('SMG_GROUP', 'ZZ Capital')
MEMBERS = os.environ.get('SMG_MEMBERS', 'Cristiano Zonta, student ID 909123 (spokesperson); Mattia Zanrosso, student ID 909945')
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
          ('TOPPADDING', (0, 0), (-1, -1), 1.2), ('BOTTOMPADDING', (0, 0), (-1, -1), 1.2)]
    if num_from is not None: st.append(('ALIGN', (num_from, 1), (-1, -1), 'RIGHT'))
    t.setStyle(TableStyle(st)); return t
f = lambda x, d=1: 'n.a.' if pd.isna(x) else f'{x:.{d}f}'
el = []
el += [Paragraph('Stock Market Game 2026: Initial Report', H1), Paragraph('Corporate Finance and Financial Institutions 2', SM), Spacer(1, 4)]
el += [Paragraph('A. Group name and composition', H2), Paragraph(f'<b>Group:</b> {GROUP} (Investopedia username: {GROUP}). <b>Members:</b> {MEMBERS}.', B)]

el += [Paragraph('B. Strategy adopted', H2)]
el += [Paragraph('<b>We buy US large caps whose earnings estimates are being raised, only at moderate valuations, and spread them across value, growth and '
    'momentum stocks.</b>', B)]
zline = ('The Zacks Rank of each holding, reported in the table in C.b, confirms the score. ' if has_z else '')
el += [Paragraph('<b>Why earnings revisions.</b> Leonard Zacks (1979) found that changes in analysts\' earnings estimates move stock prices more than any '
    'other factor over one to three months, which is about the length of the game. We rebuilt his ranking from analyst data for 151 large caps. '
    'Each stock gets a revision score made of the share of upward EPS revisions in the last 30 days (Agreement, weight 40%), the change in the consensus '
    'EPS estimate over 60 days (Magnitude, 25%), the Average Broker Recommendation (20%) and the gap between the analysts\' price target and the price '
    '(Upside, 15%). The average EPS surprise of the last four quarters is used as a check. ' + zline +
    'We keep the limits of this signal in mind: it works over a short horizon and favours smaller companies and whichever industry is in fashion.', B)]
el += [Paragraph('<b>Why now.</b> In September 2026 the Fed raised rates for the first time in three years, and its officials are signalling more hikes. '
    'US producer prices are rising at the fastest pace since 2022, and 47% of fund managers expect stagflation. '
    'Brent crude went above $110 in October because of the conflict between the US and Iran, and AI and chip stocks have fallen sharply since. '
    'With the S&amp;P 500 at about 21.5 times forward earnings, we do not expect valuations to rise further, so prices will have to follow earnings. '
    'This is why we buy companies with rising estimates and a median forward P/E of about 13. No style has a clear lead in this market, so we mix them. '
    'Our value stocks (oil companies and banks) gain from high oil prices and higher rates. Our growth stocks supply AI data centres and the power grid '
    'and already report growing earnings. Our momentum stocks are mostly healthcare companies, which have led the market as a defensive sector. '
    'Technology is 19% of the portfolio against about 33% of the S&amp;P 500. We hold no utilities, real estate or consumer discretionary stocks, '
    'which suffer most from rising rates and weak consumer spending.', B)]

el += [Paragraph('C. Initial portfolio composition', H2), Paragraph('<b>a. Companies and shares held.</b> Market orders executed on 24/11/2026 at the prices below, with no commission.', B)]
rows = [['Ticker', 'Company', 'Industry', 'Shares', 'Price', 'Weight', 'Background']]
for _, r in p.iterrows():
    rows.append([r.ticker, Paragraph(r.nome.replace('ExxonMobil Holdings Corporation', 'Exxon Mobil Corp.'), TC), Paragraph(r.industria, TC), f'{r.azioni:,}', f'${r.prezzo_acquisto:,.2f}', f'{r.w:.1%}', Paragraph(BG[r.ticker], TC)])
rows.append(['', 'Total invested', '', '', '', f'{inv/1e6:.1%}', f'${inv:,.0f} of $1,000,000; cash {1-inv/1e6:.1%}'])
el += [table(rows, [1.1*cm, 3.1*cm, 3.0*cm, 1.1*cm, 1.5*cm, 1.1*cm, 6.4*cm], num_from=3)]

el += [Spacer(1, 4), Paragraph('<b>b. Selection parameters and criteria.</b> We kept stocks with more upward than downward estimate revisions (Agreement above 0) '
    'and an ABR of 2.5 or better, then sorted them by style. Value: forward P/E below 14 and P/B below 3.5. Growth: EPS growth above 25% and PEG below 1.6. '
    'Momentum: 6-month return above 20% and 3-month return above 5%. Within each style we took the highest scores, subject to the sector limits in point d.', B)]
hdr = ['Ticker', 'Style', 'Fwd P/E', 'P/B', 'PEG', 'ABR', 'Rev. up/down 30d', 'EPS est. change 60d', 'Surprise 4Q', 'Score'] + (['Zacks Rank'] if has_z else [])
rows = [hdr]
for _, r in p.iterrows():
    rows.append([r.ticker, r.stile, f(r.PE_fwd), f(r.PB), f(r.PEG, 2), f(r.ABR, 2), f'{r.rev_su_30g:.0f} / {r.rev_giu_30g:.0f}', f'{r["var_stima_60g_%"]:+.1f}%',
                 f'{r["surprise_4q_%"]:+.1f}%', f(r.score, 2)] + ([f(r.zacks_rank, 0)] if has_z else []))
rows.append(['Median', '', f(p.PE_fwd.median()), f(p.PB[p.PB > 0].median()), f(p.PEG.median(), 2), f(p.ABR.median(), 2), '', f'{p["var_stima_60g_%"].median():+.1f}%', f'{p["surprise_4q_%"].median():+.1f}%', f(p.score.median(), 2)] + ([''] if has_z else []))
el += [table(rows, None, num_from=2)]
el += [Paragraph('MCK has negative book value because of share buybacks, so its P/B is not meaningful. '
    'Data: Yahoo Finance' + (' and Zacks' if has_z else '') + ', 23/11/2026.', SM)]

w = p.w
el += [Paragraph(f'<b>c. Weighting criterion.</b> Weights follow conviction. Each stock starts at 5% and moves up or down by up to 2.5 points with its standardised '
    f'revision score; the weights are then normalised and capped at 25% per sector, which gives a range from {w.min():.1%} to {w.max():.1%}. Equal weights would ignore '
    'the differences in signal strength. Value weights would put most of the money into the largest companies and raise the technology share '
    f'we want to keep low. The first purchase used {inv/1e6:.1%} of the capital. On 30/11 we will add the remaining cash, less a $1,500 buffer, in equal amounts to '
    'COF, VLO, PWR and APH, the highest-scoring holdings outside healthcare, so the 25% cap still holds.', B)]
sec = p.groupby('settore').w.sum().sort_values(ascending=False); sty = p.groupby('stile').w.sum()
el += [Paragraph('<b>d. Diversification.</b> By sector: ' + ', '.join(f'{SHORT.get(k, k)} {v:.0%}' for k, v in sec.items()) +
    '. By style: ' + ', '.join(f'{k} {sty[k]:.0%}' for k in ['Value', 'Growth', 'Momentum']) + '. No sector is above 25% and we hold only three technology stocks. '
    'We picked sectors that offset each other. Energy gains when oil spikes, the shock that hurts technology and consumers most, while healthcare holds up in a slowdown. '
    'From July to October 2026 the average correlation between pairs of our stocks was 0.05, and the weighted 5-year beta of the portfolio is 0.97.', B)]

el += [Paragraph('D. Monitoring list', H2), Paragraph('These 25 stocks pass the same screen and would replace holdings whose estimates start to be cut.', B)]
TRIG = {'ANET': 'AI rebound', 'OXY': 'oil upside', 'PSX': 'refining margins', 'COP': 'oil upside', 'CVS': 'value health', 'CI': 'value health', 'AIG': 'rates', 'MET': 'rates',
        'CB': 'defensive insurer', 'AMD': 'AI rebound', 'AVGO': 'AI rebound', 'KLAC': 'chip capex', 'NVDA': 'AI rebound', 'GEV': 'grid capex', 'CEG': 'power demand',
        'TXN': 'chip cycle', 'TMO': 'health momentum', 'ISRG': 'health growth', 'V': 'payments', 'HCA': 'health momentum', 'TRV': 'insurance pricing',
        'ETN': 'grid capex', 'PH': 'industrial cycle', 'RTX': 'defence', 'ORLY': 'defensive retail'}
rows = [['Ticker', 'Sector', 'Style', 'Fwd P/E', 'PEG', 'ABR', 'Rev. up/down', 'EPS est. 60d', 'Score', 'Buy if']]
for _, r in wl.iterrows():
    rows.append([r.ticker, SHORT.get(r.settore, r.settore), r.stile, f(r.PE_fwd), f(r.PEG, 2), f(r.ABR, 2), f'{r.rev_su_30g:.0f} / {r.rev_giu_30g:.0f}', f'{r["var_stima_60g_%"]:+.1f}%', f(r.score, 2), TRIG[r.ticker]])
el += [table(rows, None, num_from=3)]

out = f"out/{GROUP.replace(' ', '_')}_report1.pdf"
SimpleDocTemplate(out, pagesize=A4, leftMargin=1.6*cm, rightMargin=1.6*cm, topMargin=1.0*cm, bottomMargin=0.9*cm, title='SMG Initial Report').build(el)
print(out)
