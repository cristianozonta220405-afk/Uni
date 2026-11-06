# Documenti export automatici: Shopify extra-UE → Google Drive

Per ogni **ordine pagato con spedizione fuori dall'Unione Europea** l'automazione crea 4 PDF e li salva su Google Drive nella cartella **Fatture Estere**:

| # | Documento | A cosa serve |
|---|-----------|--------------|
| 1 | **Fattura commerciale / Commercial Invoice** (IT/EN) | Da dare a FedEx per lo sdoganamento |
| 2 | **Dichiarazione di origine della merce** | Paese di origine di ogni articolo (+ origine preferenziale UE, se la attivi) |
| 3 | **Dichiarazione di conformità del prodotto** | Conformità alle norme UE sull'abbigliamento: GPSR, etichettatura tessile, REACH, non-DPI |
| 4 | **Dichiarazione di libera esportazione** | Merce non a duplice uso, non soggetta a sanzioni o licenze, liberamente esportabile |

Struttura su Drive:

```
Fatture Estere/
├── Registro Fatture Estere      ← foglio Google con tutti gli ordini elaborati + scheda "Errori"
└── 2026/
    └── #1045 – John Smith (US)/
        ├── CI-2026-0001_1045_1_Fattura_Commerciale.pdf
        ├── CI-2026-0001_1045_2_Dichiarazione_Origine.pdf
        ├── CI-2026-0001_1045_3_Dichiarazione_Conformita.pdf
        └── CI-2026-0001_1045_4_Dichiarazione_Libera_Esportazione.pdf
```

Nella cartella [`esempi/`](esempi/) trovi i PDF di prova di due ordini (USA e Svizzera) per vedere come escono i documenti.

### Come funziona
È un **Google Apps Script**: un programma gratuito che gira sui server di Google e non richiede un tuo server. Ogni 15 minuti:
1. chiede a Shopify gli ordini pagati nuovi o modificati;
2. tiene solo quelli con indirizzo di spedizione fuori UE (gestisce anche Canarie, Ceuta, Melilla e Livigno, che sono "extra-UE" per la dogana);
3. genera i 4 PDF, li salva su Drive e scrive una riga nel registro con un numero progressivo (`CI-2026-0001`, `CI-2026-0002`, …);
4. aggiunge all'ordine su Shopify il tag `documenti-export-ok`;
5. se manca un dato (codice HS, telefono del cliente…) o la destinazione è sotto sanzioni (Russia, Bielorussia…) **ti manda un'email**.

Un ordine non viene mai elaborato due volte.

---

## Installazione (circa 20 minuti, una volta sola)

### Passo 1 – Crea l'app su Shopify (per dare allo script il permesso di leggere gli ordini)

1. Vai su **[dev.shopify.com](https://dev.shopify.com)** e accedi con l'account del negozio. Dall'admin di Shopify ci arrivi da *Impostazioni → App → Sviluppa app → Crea app nel Dev Dashboard*.
2. **Crea app** → *Avvia da Dev Dashboard*. Chiamala ad esempio `Documenti Export`.
3. Nella sezione **Versioni → Accesso** seleziona questi permessi (*scopes*):
   - `read_orders` (legge gli ordini)
   - `read_products` (legge composizione e descrizione doganale)
   - `read_inventory` (legge codice HS, paese di origine e peso)
   - `write_orders` (serve solo per aggiungere il tag all'ordine)
   - *facoltativo:* `read_all_orders`, solo se vuoi generare documenti per ordini più vecchi di 60 giorni
4. Sempre nell'app, alla voce **Dati protetti dei clienti**, abilita l'accesso a **nome, email, telefono e indirizzo**. Senza questo passaggio Shopify nasconde gli indirizzi e i documenti escono vuoti.
5. **Rilascia** la versione, poi **Installa** l'app sul tuo negozio.
6. In **Impostazioni** dell'app copia il **Client ID** e il **Client secret**.

> Hai già una vecchia "app personalizzata" creata dall'admin, con un token che inizia per `shpat_`? Puoi usare quella: al punto 3 del passo successivo inserisci `SHOPIFY_ACCESS_TOKEN` al posto di client ID e secret.

### Passo 2 – Crea lo script Google

1. Vai su **[script.google.com](https://script.google.com)** con l'account Google che usa la cartella Drive e clicca **Nuovo progetto**. Rinominalo `Documenti Export Shopify`.
2. Crea i file del codice:
   - c'è già un file `Codice.gs`: cancellane il contenuto e incolla tutto il file [`apps-script/Codice.gs`](apps-script/Codice.gs);
   - clicca **+ → Script**, chiamalo `Configurazione` e incolla il file [`apps-script/Configurazione.gs`](apps-script/Configurazione.gs).
3. Inserisci le credenziali: ⚙️ **Impostazioni progetto** → in fondo **Proprietà script → Aggiungi proprietà**:

   | Proprietà | Valore |
   |-----------|--------|
   | `SHOPIFY_NEGOZIO` | `tuonegozio.myshopify.com` |
   | `SHOPIFY_CLIENT_ID` | il Client ID copiato al passo 1 |
   | `SHOPIFY_CLIENT_SECRET` | il Client secret copiato al passo 1 |

4. Sempre in ⚙️ Impostazioni progetto imposta il **Fuso orario** su `(GMT+01:00) Roma`.
   *Facoltativo:* spunta "Mostra il file manifest appsscript.json" e incolla il contenuto di [`apps-script/appsscript.json`](apps-script/appsscript.json).

### Passo 3 – Compila i tuoi dati

Apri `Configurazione.gs` e sostituisci i dati di esempio con:
- **ragione sociale, indirizzo, P.IVA, EORI** (di solito `IT` seguito dalla partita IVA) e **chi firma**;
- il **logo** (facoltativo): caricalo su Drive e incolla l'ID del file;
- **Incoterm**: `DAP` se i dazi li paga il cliente, che è il caso normale, oppure `DDP` se li paghi tu;
- **copie della fattura**: 1 se usi FedEx ETD (fattura elettronica), 3 se stampi i documenti e li attacchi al pacco.

Poi salva con Ctrl+S.

### Passo 4 – Avvia

1. In alto seleziona la funzione **`setup`** e clicca **▶ Esegui**.
2. Google ti chiede le autorizzazioni (Drive, Fogli, connessione esterna, email). Clicca *Consenti*. Se compare "App non verificata", scegli *Avanzate → Vai a Documenti Export Shopify*: è normale per gli script personali.
3. Nel registro di esecuzione deve comparire **"Installazione completata"** con il link alla cartella.

Da questo momento l'automazione controlla gli ordini ogni 15 minuti, a partire da quelli di oggi.

### Passo 5 – Prova con un ordine vero

Apri `Codice.gs`, cerca `generaDocumentiOrdine` e sostituisci `'#1001'` con il numero di un ordine extra-UE già esistente. Seleziona la funzione `generaDocumentiOrdine` ed esegui: in Drive trovi i 4 PDF. **Controllali bene la prima volta.**

---

## Dati da completare su Shopify (importante per la dogana)

Per ogni prodotto, nella **variante → sezione "Spedizione / Dogana"**:

| Campo | Esempio per cappelli |
|-------|----------------------|
| **Codice HS** (sistema armonizzato) | `6505.00.30` cappellino con visiera · `6505.00.90` berretto o cappello in tessuto o maglia · `6505.00.10` feltro di lana · `6504.00` paglia o intrecciato · `6506.99` altri materiali (es. pelle) |
| **Paese di origine** | dove è stato **prodotto** il cappello, non da dove lo spedisci |
| **Peso** | peso del singolo cappello |

Se un campo manca, lo script usa i valori di riserva di `Configurazione.gs` e ti avvisa via email.

**Consigliati: composizione e descrizione per la dogana.** Su Shopify vai in *Impostazioni → Dati personalizzati → Prodotti → Aggiungi definizione* e crea due campi testo:
- `custom.composizione` → es. `100% Cotone / 100% Cotton`
- `custom.descrizione_doganale` → es. `Cotton baseball cap / Cappellino in cotone con visiera`

La dogana vuole una descrizione chiara del tipo "berretto da baseball in cotone", non il nome commerciale del prodotto. Il nome commerciale viene comunque riportato sotto, più in piccolo.

---

## Funzioni utili (menu ▶ Esegui)

| Funzione | Cosa fa |
|----------|---------|
| `setup` | Prima installazione (si può rilanciare senza problemi) |
| `processaNuoviOrdini` | Controlla subito i nuovi ordini senza aspettare i 15 minuti |
| `generaDocumentiOrdine` | Genera o rigenera i documenti di un ordine specifico, anche vecchio o già fatto: mantiene lo stesso numero e sostituisce i PDF |
| `testConnessioneShopify` | Verifica che le credenziali funzionino |
| `disattivaAutomazione` | Ferma il controllo automatico |

---

## Note fiscali e doganali

- **Questi documenti servono alla spedizione e alla dogana, non sono la fattura fiscale.** La fattura elettronica resta quella di Fatture in Cloud. Per questo la numerazione è separata (`CI-` = Commercial Invoice). Se preferisci usare il numero d'ordine Shopify, imposta `USA_NUMERO_ORDINE: true`.
- **Clausola IVA:** "Operazione non imponibile ai sensi dell'art. 8, comma 1, lett. a) DPR 633/72". Vale quando il trasporto lo organizzi tu tramite FedEx. Per avere la non imponibilità serve la **prova di uscita** della merce: conserva la bolletta doganale o l'MRN che ti manda FedEx insieme ai PDF.
- **Origine preferenziale** (`ORIGINE_PREFERENZIALE: true`): aggiunge la dichiarazione ufficiale "*…these products are of EU preferential origin*", che permette al cliente di pagare dazi ridotti o zero in paesi con un accordo UE (UK, Svizzera, Canada, Giappone, Corea…). **Attivala solo se i cappelli rispettano davvero le regole di origine.** Sopra 6.000 € a spedizione serve anche il numero **REX**. Se un articolo non è di origine UE, la dichiarazione viene esclusa in automatico.
- **Sanzioni:** gli ordini verso Russia, Bielorussia, Corea del Nord, Iran e Siria **non vengono elaborati** e ricevi un avviso. Per la Russia è vietato esportare capi d'abbigliamento sopra i 300 € (Reg. UE 833/2014).
- **Dichiarazione di conformità:** cita GPSR (Reg. UE 2023/988), etichettatura tessile (Reg. UE 1007/2011), REACH, POP e Codice del Consumo, e specifica che i cappelli non sono dispositivi di protezione individuale (niente marcatura CE). **Verifica che sia vero per i tuoi prodotti**, cioè che abbiano etichetta di composizione e dati del produttore. Se vendi cappelli per bambini negli USA servono anche i test CPSIA, che qui non sono coperti.
- Nella fattura il valore è quello **effettivamente pagato** dal cliente (dopo gli sconti), che è il valore richiesto dalla dogana. Le gift card e i prodotti senza spedizione sono esclusi.
- Le firme vanno apposte a mano o con firma digitale. Se usi FedEx ETD puoi caricare un'immagine della firma nel profilo FedEx.

> Testi e riferimenti normativi sono un modello standard per il settore abbigliamento. **Falli controllare una volta al tuo commercialista o spedizioniere doganale** prima di usarli in produzione.

---

## Problemi frequenti

| Problema | Soluzione |
|----------|-----------|
| `Impossibile ottenere il token Shopify` | L'app non è installata sul negozio, oppure il Client ID o il secret sono sbagliati |
| Indirizzi vuoti nei PDF | Manca l'accesso ai **Dati protetti dei clienti** (passo 1.4) |
| `Shopify ha risposto 403` | Manca uno dei permessi del passo 1.3: aggiungilo, rilascia una nuova versione e reinstalla l'app |
| Un ordine non viene elaborato | Controlla che sia **pagato** e che abbia un indirizzo di spedizione extra-UE. Guarda la scheda *Errori* del registro |
| Voglio i documenti di ordini passati | Usa `generaDocumentiOrdine` con il numero d'ordine |

---

## Per sviluppatori: test

```bash
node test/test.js              # simula Shopify e Google Drive e controlla tutto il flusso
node test/test.js --anteprime  # salva anche l'HTML dei documenti in test/anteprime/
```
