"""Punteggio 'proxy Zacks' (revisioni stime) + classificazione per stile."""
import pandas as pd, numpy as np
df = pd.read_csv('dati/universo_screening.csv').dropna(subset=['settore'])
tot = (df.rev_su_30g + df.rev_giu_30g).replace(0, np.nan)
df['agreement'] = ((df.rev_su_30g - df.rev_giu_30g) / tot).fillna(0)          # -1..+1
df['magnitude'] = df['var_stima_60g_%'].clip(-20, 20)
z = lambda s: (s - s.mean()) / s.std()
df['score'] = (0.4*z(df.agreement) + 0.25*z(df.magnitude) + 0.2*z(-df.ABR.fillna(3))
               + 0.15*z(df['upside_target_%'].clip(-20, 60)))
def stile(r):
    if r['mom_6m_%'] > 20 and r['mom_3m_%'] > 5: return 'Momentum'
    if r.PE_fwd < 14 and 0 < r.PB < 3.5: return 'Value'
    if (r.crescita_utili or 0) > 0.25 and 0 < (r.PEG or 99) < 1.6: return 'Growth'
    return '-'
df['stile'] = df.apply(stile, axis=1)
df.sort_values('score', ascending=False).to_csv('dati/universo_classificato.csv', index=False)
c = ['ticker','settore','stile','score','agreement','var_stima_60g_%','ABR','PE_fwd','PB','PEG','mom_6m_%','crescita_utili']
d = df[df.stile != '-'].sort_values('score', ascending=False)
pd.set_option('display.width', 250)
for s in ['Value','Growth','Momentum']:
    print('\n==', s); print(d[d.stile == s][c].round(2).head(20).to_string(index=False))
