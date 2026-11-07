Crea in questa cartella un'automazione con **Google Apps Script** che, per ogni ordine Shopify **pagato** con **spedizione fuori dall'Unione Europea**, genera 4 documenti PDF per la spedizione con **FedEx** e li salva in una cartella Google Drive chiamata **"Fatture Estere"**. Vendo **cappelli** (settore abbigliamento). Uso già Fatture in Cloud per le fatture fiscali: questi documenti servono **solo per FedEx e la dogana**, quindi **non** va collegato Fatture in Cloud. Tutti i testi visibili (documenti, commenti, README, messaggi di log ed email) devono essere in **italiano**; i documenti PDF sono **bilingue italiano/inglese**.

## Struttura del progetto
```
shopify-fatture-estere/
├── README.md                     guida di installazione passo passo in italiano, per un non programmatore
├── .gitignore                    (ignora test/anteprime/)
├── apps-script/
│   ├── Configurazione.gs         UNICO file che l'utente modifica: oggetto globale CONFIG
│   ├── Codice.gs                 tutto il codice, l'utente non lo tocca
│   └── appsscript.json           timeZone Europe/Rome, runtime V8, scope OAuth espliciti
├── test/
│   ├── ordini-esempio.json       ordini finti nel formato della risposta GraphQL di Shopify
│   └── test.js                   test in Node che simulano i servizi Google e Shopify
└── esempi/                       PDF di esempio generati dalle anteprime
```
Solo due file `.gs`, così l'utente li incolla a mano nell'editor di script.google.com senza usare clasp.

## Configurazione.gs (oggetto `CONFIG`, ogni voce commentata in italiano)
- `AZIENDA`: ragione sociale, indirizzo, CAP, città, provincia, paese e codice paese, P.IVA, codice fiscale, EORI, REX (facoltativo), telefono, email, sito, nome/ruolo del firmatario, luogo della firma, `LOGO_DRIVE_FILE_ID` (facoltativo).
- `DRIVE`: `NOME_CARTELLA: 'Fatture Estere'`, `ID_CARTELLA` facoltativo (ha la precedenza), sottocartella per anno (sì/no), sottocartella per ordine (sì/no), nome del foglio registro `'Registro Fatture Estere'`.
- `SPEDIZIONE`: corriere `'FedEx'`, `INCOTERM: 'DAP'` (spiega DAP/DDP), motivo dell'export `'Vendita / Sale'`, peso imballo in kg (0,30), numero colli (1), `COPIE_FATTURA` (1 se si usa FedEx ETD, 3 se si stampa).
- `PRODOTTI`: valori di riserva quando il dato manca su Shopify: `HS_CODE_DEFAULT: '650500'` (commenta le alternative: 6504.00 paglia, 6505.00.30 cappellini con visiera, 6505.00.10 feltro di lana), `ORIGINE_DEFAULT: 'IT'`, peso unitario 0,15 kg, descrizione doganale `'Hat / Cappello'`, composizione predefinita; namespace/key dei metafield prodotto `custom.composizione` e `custom.descrizione_doganale`.
- `ORIGINE_PREFERENZIALE: false`, con un commento che spiega quando attivarla.
- `FATTURA`: `USA_NUMERO_ORDINE: false`, `PREFISSO: 'CI'`, clausola IVA "Operazione non imponibile IVA ai sensi dell'art. 8, comma 1, lett. a), D.P.R. 633/1972 – VAT exempt export…", note facoltative.
- `ORDINI`: `SOLO_PAGATI: true`, `AGGIUNGI_TAG: true`, `TAG: 'documenti-export-ok'`, `PAESI_BLOCCATI: ['RU','BY','KP','IR','SY']` (sanzioni UE; Reg. 833/2014 vieta beni di lusso > 300 € verso la Russia), `INTERVALLO_MINUTI: 15` (ammessi 1/5/10/15/30).
- `NOTIFICHE`: email in caso di errori o dati mancanti (sì), destinatario (vuoto = utente che esegue lo script), email di riepilogo (no).
- `SHOPIFY_API_VERSION` (una versione stabile recente, es. `'2026-07'`).
Le credenziali **non** vanno in CONFIG ma nelle **Proprietà script**: `SHOPIFY_NEGOZIO` (accetta `nome`, `nome.myshopify.com` o un URL completo e lo normalizza), `SHOPIFY_CLIENT_ID` + `SHOPIFY_CLIENT_SECRET`, oppure in alternativa `SHOPIFY_ACCESS_TOKEN` (shpat_ delle vecchie app personalizzate).

## Codice.gs – comportamento
**Funzioni pubbliche** (da lanciare dal menu Esegui):
- `setup()`: verifica la configurazione (errore se mancano i campi obbligatori, avviso nel log se ci sono ancora i dati di esempio), testa la connessione a Shopify, crea o trova la cartella e il registro, imposta il segnalibro `ULTIMO_CONTROLLO` a oggi alle 00:00 (solo se non esiste già), installa un trigger a tempo su `processaNuoviOrdini`. Si può rilanciare senza duplicare i trigger.
- `processaNuoviOrdini()`: usa LockService. Cerca gli ordini con `updated_at:>='<ultimo controllo − 10 minuti>'`, più `financial_status:paid` e `-tag:"<TAG>"` se attivi. Salta gli ordini già nel registro (per ID). Gestisce ogni ordine in un try/catch separato. Avanza il segnalibro **solo se non ci sono stati errori**. Scrive nel log un riepilogo e invia le notifiche.
- `generaDocumentiOrdine(numero)`: con un valore predefinito `'#1001'` modificabile nel codice; accetta `'1045'` o `'#1045'`. Rigenera anche se l'ordine è già stato fatto, **mantenendo lo stesso numero di fattura**, sovrascrivendo la riga del registro e spostando nel cestino i PDF vecchi.
- `testConnessioneShopify()`: interroga `shop { name myshopifyDomain currencyCode }`.
- `disattivaAutomazione()`: elimina il trigger.

**Shopify** – usa la GraphQL Admin API (non REST):
- Autenticazione: se c'è `SHOPIFY_ACCESS_TOKEN` usa quello. Altrimenti usa il **client credentials grant** delle app del Dev Dashboard: POST a `https://{negozio}/admin/oauth/access_token` con `grant_type=client_credentials`, `client_id` e `client_secret`. Il token dura 24 ore: va salvato nelle proprietà e rinnovato 30 minuti prima della scadenza, o dopo una risposta 401.
- Riprova con backoff in caso di 429, errori 5xx o errore GraphQL `THROTTLED`. Errori chiari in italiano negli altri casi.
- Query degli ordini con paginazione (25 per pagina, `sortKey: UPDATED_AT`). Campi: id, name, createdAt, email, phone, tags, customer, shippingAddress/billingAddress (name, firstName, lastName, company, address1, address2, city, province, provinceCode, zip, country, countryCodeV2, phone), currentTotalPriceSet, totalPriceSet, totalShippingPriceSet (shopMoney). Per i lineItems (first: 100): title, variantTitle, sku, quantity, currentQuantity, requiresShipping, originalUnitPriceSet, discountedUnitPriceSet, discountedUnitPriceAfterAllDiscountsSet, i metafield del prodotto con alias (`composizione:` e `descrizioneDoganale:`, con namespace/key passati come variabili), `variant.inventoryItem { harmonizedSystemCode countryCodeOfOrigin measurement { weight { unit value } } }`.
- Dopo la generazione aggiunge il tag con la mutation `tagsAdd`. Se fallisce (ad esempio per un permesso mancante) scrive solo nel log e non blocca nulla.

**Logica UE / extra-UE** (`isExtraUe_`): sono UE i 27 Stati membri più Monaco (`MC`). Sono **extra-UE** anche ES con provinceCode `GC`, `TF`, `CE`, `ML` (Canarie, Ceuta, Melilla) e IT con CAP `23041` (Livigno). Sono saltati gli ordini senza indirizzo di spedizione o senza articoli da spedire. Per i paesi in `PAESI_BLOCCATI` non genera nulla, registra un errore e manda un avviso.

**Normalizzazione dell'ordine**:
- Esclude le righe con quantità corrente pari a 0 o con `requiresShipping: false` (es. le gift card).
- Prezzo unitario = prezzo dopo tutti gli sconti (con fallback sui campi meno precisi).
- Converte il peso in kg da GRAMS, POUNDS, OUNCES o KILOGRAMS.
- Al codice HS toglie i caratteri non numerici. Se mancano HS, origine o peso usa i valori di riserva e aggiunge un **avviso** all'ordine. Aggiunge un avviso anche se manca il telefono del destinatario (FedEx lo richiede).
- Calcola totale merce, spedizione, totale, numero di pezzi, peso netto e peso lordo (= netto + imballo).
- Usa gli importi in valuta del negozio (shopMoney). Arrotonda correttamente a 2 decimali (3 per i pesi).

**Drive e registro**:
- Cartella principale per ID (da config o da proprietà salvata); altrimenti la cerca per nome in "Il mio Drive" e, se non esiste, la crea.
- Percorso: `Fatture Estere/<anno>/<#ordine> – <nome cliente> (<codice paese>)/`.
- Nomi dei file: `<numero>_<ordine senza #>_1_Fattura_Commerciale.pdf`, `_2_Dichiarazione_Origine.pdf`, `_3_Dichiarazione_Conformita.pdf`, `_4_Dichiarazione_Libera_Esportazione.pdf`.
- PDF generati da HTML con `Utilities.newBlob(html,'text/html').getAs('application/pdf')`. Se esiste già un file con lo stesso nome, quello vecchio va nel cestino.
- Il foglio Google "Registro Fatture Estere" va creato dentro la cartella, con due schede:
  - **Registro**, colonne: Data creazione, N. fattura commerciale, Ordine Shopify, Data ordine, Cliente, Paese, Pezzi, Valore merce, Spedizione, Totale, Valuta, Peso lordo kg, Cartella Drive, Avvisi, ID ordine;
  - **Errori**: Data, Ordine, Errore.
  Intestazioni in grassetto e bloccate. Tieni in cache il foglio durante l'esecuzione.
- Numerazione: `CI-<anno>-0001` progressiva per anno, calcolata dal registro; in alternativa il numero d'ordine se `USA_NUMERO_ORDINE`.

**Notifiche via email** (MailApp): un'unica email se ci sono errori, ordini bloccati o ordini generati con avvisi ("DA CONTROLLARE #1001 (link): - …"), con il link al registro. Email di riepilogo facoltativa.

## I 4 documenti (HTML → PDF)
Usa solo CSS semplice a tabelle (niente flexbox o grid, il convertitore di Google è limitato), Arial, `@page A4`, colore principale blu scuro `#0f2b4c`. L'**escape HTML** va applicato a tutti i dati dinamici. Ogni documento ha:
- intestazione con logo facoltativo (scaricato da Drive e inserito in base64), dati dell'azienda (P.IVA, EORI, REX se presente, contatti), titolo e riferimenti a destra;
- in fondo luogo, data e spazio per timbro e firma con nome e ruolo del firmatario.

Date nel formato gg/mm/aaaa (fuso Europe/Rome), importi `1.234,50`, pesi `0,780`, codice HS formattato `6505.00.30`, paesi come "United States (US)".

1. **COMMERCIAL INVOICE / Fattura commerciale**:
   - Riquadri Destinatario (spedizione, con telefono ed email) e Acquirente (fatturazione).
   - Tabelle con ordine, motivo dell'export, "Incoterms® 2020" + Incoterm + città di destinazione, pagamento "Prepagato / Prepaid", corriere, AWB vuoto da compilare, paese di destinazione, valuta.
   - Tabella degli articoli: #, descrizione doganale in grassetto + composizione + titolo/variante/SKU in piccolo, HS, origine, quantità, peso netto, prezzo unitario, totale.
   - Colli, pezzi, peso netto e lordo; totali (merce, trasporto, IVA 0,00, TOTALE).
   - Clausola IVA, dichiarazione di veridicità in inglese e italiano, nota "documento commerciale per spedizione e sdoganamento".
   - Se `ORIGINE_PREFERENZIALE` è attiva e **tutte** le origini sono UE, aggiunge la dichiarazione di origine su fattura dell'Allegato 22-07 del Reg. UE 2015/2447 ("The exporter of the products covered by this document (Customs Authorisation or REX No. …) declares that, except where otherwise clearly indicated, these products are of EU preferential origin.").
   - Ripete la fattura `COPIE_FATTURA` volte nello stesso PDF con interruzione di pagina, indicando "copia n/N".
2. **DICHIARAZIONE DI ORIGINE**:
   - Tabella di riferimento (fattura, ordine, destinatario).
   - Testo "Il/La sottoscritto/a … DICHIARA che le merci … sono originarie di: …", con riferimento all'origine non preferenziale degli artt. 59-63 del Reg. (UE) 952/2013 (CDU), e versione inglese.
   - Tabella con articoli, HS, quantità e paese di origine.
   - Blocco sull'origine preferenziale se attiva, oppure la nota "non applicabile" se ci sono origini non UE.
   - Impegno a fornire documentazione su richiesta della dogana.
3. **DICHIARAZIONE DI CONFORMITÀ** (abbigliamento/cappelli):
   - Tabella dei prodotti con composizione.
   - Conformità a: Reg. (UE) 2023/988 GPSR, Reg. (UE) 1007/2011 sull'etichettatura delle fibre tessili, REACH 1907/2006 (Allegato XVII, nessuna SVHC sopra lo 0,1%), Reg. (UE) 2019/1021 POP, D.Lgs. 206/2005.
   - Dichiarazioni aggiuntive: i prodotti non sono DPI ai sensi del Reg. (UE) 2016/425, quindi niente marcatura CE; sono etichettati con la composizione e la tracciabilità; non contengono specie protette CITES (Reg. CE 338/97).
   - Riassunto in inglese.
4. **DICHIARAZIONE DI LIBERA ESPORTAZIONE**:
   - Tabella con esportatore, destinatario, fattura e ordine, merce ("Cappelli e copricapi – HS …"), colli/pezzi/peso lordo, valore, corriere.
   - Elenco a)–g), ognuno in italiano con la traduzione inglese:
     - a) non sono beni a duplice uso (Reg. UE 2021/821);
     - b) non sono soggetti a sanzioni (Reg. UE 833/2014 e 269/2014 per la Russia, Reg. CE 765/2006 per la Bielorussia) e il destinatario non è un soggetto designato;
     - c) non sono materiale d'armamento (L. 185/1990) né armi da fuoco (Reg. UE 258/2012);
     - d) non rientrano nel Reg. UE 2019/125 (tortura);
     - e) non sono beni culturali (Reg. CE 116/2009, D.Lgs. 42/2004);
     - f) non contengono specie CITES;
     - g) non sono soggetti a licenza e sono liberamente esportabili.
   - Chiusura: uso civile e personale, nessuna riesportazione verso paesi sotto embargo.

## Test (Node, senza dipendenze)
`test/test.js` carica `Configurazione.gs` e `Codice.gs` in un contesto `vm`, con mock in memoria di PropertiesService, Logger, LockService, Utilities (formatDate con Intl e fuso orario, newBlob/getAs, base64Encode, sleep), UrlFetchApp (finto token OAuth e finte risposte GraphQL con paginazione a 2 ordini per pagina, query shop, tagsAdd), DriveApp (cartelle e file con cestino), SpreadsheetApp, ScriptApp (trigger), MailApp e Session. Attenzione: gli array che arrivano dal contesto vm vanno convertiti con JSON prima di usare `deepStrictEqual`.

Ordini di esempio:
- **#1001 USA**: fedora con HS, origine e peso in grammi, prezzo scontato; baseball cap senza HS, origine e peso (devono scattare i valori di riserva); gift card da escludere.
- **#1002 Germania**: deve essere saltato.
- **#1003 Canarie** (ES/GC): cappello di paglia con origine Ecuador.
- **#1004 Russia**: deve essere bloccato.
- **#1005 Svizzera**: 30 coppole, HS scritto `6505.00.30`, peso in once.

Da verificare:
- filtro UE / extra-UE e territori speciali;
- calcoli (totali 114 + 25 = 139, peso lordo 0,78);
- flusso completo: setup, primo giro (generati #1001, #1003 e #1005 con numeri CI-2026-0001…0003, 1 ordine UE saltato, #1004 bloccato e registrato tra gli errori, tag aggiunti, una sola email con "BLOCCATO" e "DA CONTROLLARE");
- un secondo giro senza duplicati;
- la rigenerazione mantiene il numero e sposta nel cestino i PDF vecchi;
- contenuto dei 4 HTML: dati chiave, normative, origine preferenziale accesa/spenta, copie multiple, escape di `<script>`.

Con `--anteprime` il test salva l'HTML dei documenti in `test/anteprime/`. Poi genera i PDF in `esempi/` con Playwright, guarda gli screenshot per controllare l'impaginazione e correggi quello che non va.

## README.md (in italiano, per un non programmatore)
Deve contenere:
- tabella dei 4 documenti e albero delle cartelle su Drive;
- come funziona;
- installazione passo passo:
  1. app nel Shopify Dev Dashboard con gli scope `read_orders`, `read_products`, `read_inventory`, `write_orders` (`read_all_orders` facoltativo), accesso ai **dati protetti dei clienti** (nome, email, telefono, indirizzo), rilascio, installazione, Client ID e secret;
  2. script.google.com: nuovo progetto, incollare i file, Proprietà script, fuso orario Roma, manifest facoltativo;
  3. compilare la configurazione;
  4. eseguire `setup` e accettare le autorizzazioni, anche l'avviso "app non verificata";
  5. provare con `generaDocumentiOrdine`;
- quali campi compilare su Shopify per ogni variante (HS con esempi per tipo di cappello, origine, peso) e come creare i metafield `custom.composizione` e `custom.descrizione_doganale`;
- tabella delle funzioni;
- note fiscali e doganali: non è la fattura fiscale; art. 8 lett. a) e prova di uscita (MRN/bolletta da conservare); quando attivare l'origine preferenziale e il REX sopra 6.000 €; sanzioni; verificare la dichiarazione di conformità, CPSIA esclusa; valore pagato dopo gli sconti; firme; farli controllare al commercialista;
- tabella dei problemi frequenti;
- come lanciare i test.

## Come procedere
Scrivi i file, esegui `node test/test.js --anteprime` finché tutti i test passano, genera e controlla i PDF di esempio, poi fai un commit con un messaggio descrittivo in italiano. Alla fine dimmi in breve cosa devo fare io per installarlo.
