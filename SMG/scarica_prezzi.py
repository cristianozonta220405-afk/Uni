"""Scarica chiusure giornaliere aggiustate (dividendi/split) 30/06-31/10/2026 di portafoglio + S&P 500."""
import pandas as pd, yfinance as yf
p = pd.read_csv('dati/portafoglio_iniziale.csv')
tk = list(p.ticker) + ['^GSPC']
d = yf.download(tk, start='2026-06-30', end='2026-11-01', auto_adjust=True, progress=False)['Close'][tk]
d = d.rename(columns={'^GSPC':'SPX'}).dropna(how='all'); d.index = d.index.date
d.to_csv('dati/prezzi_lug_ott.csv'); print(d.shape, d.index[0], d.index[-1], 'NaN:', int(d.isna().sum().sum()))
