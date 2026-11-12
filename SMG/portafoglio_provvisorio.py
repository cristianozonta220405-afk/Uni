"""Portafoglio iniziale PROVVISORIO (pesi per convinzione dal punteggio proxy). Da aggiornare con Zacks Rank."""
import pandas as pd, numpy as np, yfinance as yf
sel = {'Value':'CVX OXY COF CVS NUE C TMUS','Growth':'MU NVDA APH PWR UNH BLK URI','Momentum':'REGN PSX AMD MSFT DHR MET'}
u = pd.read_csv('dati/universo_classificato.csv').set_index('ticker')
rows = [dict(ticker=t, nome=u.loc[t,'nome'], settore=u.loc[t,'settore'], industria=u.loc[t,'industria'], stile=s,
             score=u.loc[t,'score'], zacks_rank=np.nan) for s,ts in sel.items() for t in ts.split()]
p = pd.DataFrame(rows)
# Pesi per convinzione: base 5% +/- 3% in funzione del punteggio (z-score troncato a [-1,1]), poi normalizzati
z = ((p.score - p.score.mean())/p.score.std()).clip(-1,1)
w = 0.05 + 0.03*z; p['peso_target'] = (w/w.sum()).round(4)
px = yf.download(list(p.ticker), period='5d', auto_adjust=False, progress=False)['Close'].iloc[-1]
p['prezzo_acquisto'] = p.ticker.map(px).round(2)
p['azioni'] = np.floor(p.peso_target*980_000/p.prezzo_acquisto).astype(int)
p.drop(columns='score').to_csv('dati/portafoglio_iniziale.csv', index=False)
print(p[['ticker','settore','stile','peso_target','prezzo_acquisto','azioni']].to_string(index=False))
print('Investito:', (p.azioni*p.prezzo_acquisto).sum().round(0))
