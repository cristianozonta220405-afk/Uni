"""Portafoglio iniziale DEFINITIVO + watchlist. Regole:
1) universo 151 large cap USA; 2) revisioni stime positive (agreement>0) e ABR<=2.5;
3) classificazione per stile (regole in classifica.py); 4) migliori punteggi per stile con limiti:
   max 25% per settore, max 3 titoli tech/semis (contesto Fed restrittiva + correzione AI);
5) pesi per convinzione 5% +/- 2.5% in base al punteggio, normalizzati; investito ~97% del capitale."""
import pandas as pd, numpy as np, yfinance as yf, concurrent.futures as cf
PORT = {'Value': 'CVX VLO XOM COF C ELV NUE TMUS', 'Growth': 'MU APH MSFT PWR URI BLK UNH', 'Momentum': 'REGN MCK DHR MA'}
WATCH = 'ANET OXY PSX COP CVS CI AIG MET CB AMD AVGO KLAC NVDA GEV CEG TXN TMO ISRG V HCA TRV ETN PH RTX ORLY'.split()
u = pd.read_csv('dati/universo_classificato.csv').set_index('ticker')
def surprise(tk):  # sorpresa media sugli utili ultimi 4 trimestri (4° criterio Zacks)
    try:
        h = yf.Ticker(tk).earnings_history; return tk, float(h['surprisePercent'].tail(4).mean()*100)
    except Exception: return tk, np.nan
allt = [t for v in PORT.values() for t in v.split()] + WATCH
with cf.ThreadPoolExecutor(8) as ex: sur = dict(ex.map(surprise, allt))
cols = ['nome','settore','industria','prezzo','mkt_cap_mld','PE','PE_fwd','PB','PEG','ABR','n_analisti','rev_su_30g','rev_giu_30g',
        'var_stima_60g_%','upside_target_%','mom_3m_%','mom_6m_%','beta','score']
def tab(tks, style=None):
    d = u.loc[tks, cols].copy(); d.insert(0, 'ticker', tks); d['surprise_4q_%'] = d.ticker.map(sur)
    d['stile'] = style if style else u.loc[tks, 'stile'].replace('-', 'Blend').values; d['zacks_rank'] = np.nan; return d
p = pd.concat([tab(v.split(), s) for s, v in PORT.items()], ignore_index=True)
z = ((p.score - p.score.mean())/p.score.std()).clip(-1, 1); w = 0.05 + 0.025*z
w = w/w.sum()
for _ in range(20):  # limite 25% per settore: riduce il settore in eccesso e redistribuisce sugli altri
    sec = w.groupby(p.settore).sum(); over = sec[sec > 0.25]
    if over.empty: break
    for s_ in over.index:
        m = p.settore == s_; ex = w[m].sum() - 0.25; w[m] *= 0.25/w[m].sum(); w[~m] += ex*w[~m]/w[~m].sum()
p['peso_target'] = w.round(4)
p['prezzo_acquisto'] = p.prezzo.round(2)
p['azioni'] = np.floor(p.peso_target*970_000/p.prezzo_acquisto).astype(int)
p.to_csv('dati/portafoglio_iniziale.csv', index=False)
wl = tab(WATCH); wl.to_csv('dati/watchlist.csv', index=False)
inv = (p.azioni*p.prezzo_acquisto).sum()
print(p[['ticker','settore','stile','score','peso_target','prezzo_acquisto','azioni','surprise_4q_%','beta']].round(3).to_string(index=False))
print('Investito', round(inv), 'beta medio pond.', round((p.beta*p.peso_target).sum(), 2))
print(p.groupby('settore').peso_target.sum().round(3).to_string()); print(p.groupby('stile').peso_target.sum().round(3).to_string())
