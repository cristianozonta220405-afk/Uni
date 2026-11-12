"""Screening universo titoli USA per lo SMG: indicatori fondamentali, momentum, revisioni stime."""
import yfinance as yf, pandas as pd, numpy as np, concurrent.futures as cf

UNIVERSE = """AAPL MSFT NVDA AVGO ORCL CRM ADBE AMD QCOM TXN MU AMAT LRCX KLAC ANET CSCO IBM NOW INTU PANW CRWD FTNT DELL HPE APH
GOOGL META NFLX DIS TMUS VZ T CMCSA
AMZN TSLA HD LOW MCD SBUX NKE TJX BKNG CMG ROST ORLY AZO GM DECK LULU
PG KO PEP WMT COST PM MO MDLZ CL KMB GIS KR
JPM BAC WFC C GS MS SCHW BLK AXP V MA PGR CB TRV MET AIG COF BK
UNH JNJ LLY ABBV MRK PFE TMO ABT DHR AMGN GILD VRTX REGN ISRG BSX SYK MDT CI ELV HCA MCK CVS
XOM CVX COP EOG SLB OXY PSX MPC VLO WMB
CAT DE HON GE RTX LMT NOC GD BA UPS UNP ETN PH EMR ITW WM URI PWR GEV
NEE DUK SO D AEP CEG VST SRE
LIN SHW APD FCX NEM NUE ECL
AMT PLD EQIX O SPG WELL PSA""".split()

def fetch(tk):
    try:
        t = yf.Ticker(tk); i = t.info
        row = dict(ticker=tk, nome=i.get('shortName'), settore=i.get('sector'), industria=i.get('industry'),
                   prezzo=i.get('currentPrice'), mkt_cap_mld=(i.get('marketCap') or 0)/1e9,
                   PE=i.get('trailingPE'), PE_fwd=i.get('forwardPE'), PB=i.get('priceToBook'),
                   PEG=i.get('trailingPegRatio'), ABR=i.get('recommendationMean'), n_analisti=i.get('numberOfAnalystOpinions'),
                   crescita_utili=i.get('earningsGrowth'), crescita_ricavi=i.get('revenueGrowth'),
                   ROE=i.get('returnOnEquity'), beta=i.get('beta'), target=i.get('targetMeanPrice'))
        try:  # revisioni stime: anno corrente, ultimi 30 giorni (base dell'"Agreement" Zacks)
            rv = t.eps_revisions; tr = t.eps_trend
            up = rv.loc['0y','upLast30days']; dn = rv.loc['0y','downLast30days']
            row['rev_su_30g'] = up; row['rev_giu_30g'] = dn
            row['var_stima_60g_%'] = (tr.loc['0y','current']/tr.loc['0y','60daysAgo']-1)*100
        except Exception: pass
        return row
    except Exception as e:
        return dict(ticker=tk, errore=str(e))

with cf.ThreadPoolExecutor(8) as ex: rows = list(ex.map(fetch, UNIVERSE))
df = pd.DataFrame(rows)
px = yf.download(UNIVERSE, period='1y', auto_adjust=True, progress=False)['Close']
df['mom_6m_%'] = df.ticker.map(((px.iloc[-1]/px.iloc[-126])-1)*100)
df['mom_3m_%'] = df.ticker.map(((px.iloc[-1]/px.iloc[-63])-1)*100)
df['upside_target_%'] = (df.target/df.prezzo-1)*100
df.to_csv('/home/user/Uni/SMG/dati/universo_screening.csv', index=False)
print(len(df), 'titoli; errori:', df.get('errore', pd.Series()).notna().sum())
