/**
 * ============================================================================
 *  CONFIGURAZIONE – Documenti di spedizione per ordini Shopify extra-UE
 * ============================================================================
 *
 *  Questo è l'UNICO file da modificare. Compila i dati della tua azienda qui
 *  sotto. Le credenziali di Shopify NON vanno scritte qui: si inseriscono in
 *  "Impostazioni progetto → Proprietà script" (vedi README).
 *
 *  Dopo ogni modifica: salva (Ctrl+S). Non serve rilanciare setup().
 */
var CONFIG = {

  // ---------------------------------------------------------------------------
  // DATI AZIENDA (mittente / esportatore) – compaiono su tutti i documenti
  // ---------------------------------------------------------------------------
  AZIENDA: {
    RAGIONE_SOCIALE: 'Nome Azienda S.r.l.',
    INDIRIZZO: 'Via Roma 1',
    CAP: '00100',
    CITTA: 'Roma',
    PROVINCIA: 'RM',
    PAESE: 'Italia',
    PAESE_CODICE: 'IT',
    PARTITA_IVA: 'IT00000000000',
    CODICE_FISCALE: '00000000000',
    EORI: 'IT00000000000',            // di solito "IT" + partita IVA
    REX: '',                          // n. esportatore registrato (solo se lo hai, serve oltre 6.000 €)
    TELEFONO: '+39 000 0000000',
    EMAIL: 'info@tuosito.it',
    SITO: 'www.tuosito.it',

    // Chi firma le dichiarazioni (legale rappresentante o delegato)
    FIRMATARIO_NOME: 'Mario Rossi',
    FIRMATARIO_RUOLO: 'Legale rappresentante',
    LUOGO_FIRMA: 'Roma',

    // Logo (facoltativo): carica il logo su Drive e incolla qui l'ID del file
    // (la parte della URL tra /d/ e /view). Lascia '' per non usarlo.
    LOGO_DRIVE_FILE_ID: ''
  },

  // ---------------------------------------------------------------------------
  // GOOGLE DRIVE
  // ---------------------------------------------------------------------------
  DRIVE: {
    // Nome della cartella principale. Se non esiste viene creata in "Il mio Drive".
    NOME_CARTELLA: 'Fatture Estere',
    // In alternativa puoi indicare direttamente l'ID della cartella (ha la precedenza).
    ID_CARTELLA: '',
    // Crea sottocartelle per anno (Fatture Estere/2026/...)
    SOTTOCARTELLA_PER_ANNO: true,
    // Una sottocartella per ogni ordine con i 4 PDF dentro
    SOTTOCARTELLA_PER_ORDINE: true,
    // Nome del foglio Google che fa da registro (creato nella cartella principale)
    NOME_REGISTRO: 'Registro Fatture Estere'
  },

  // ---------------------------------------------------------------------------
  // SPEDIZIONE / DOGANA
  // ---------------------------------------------------------------------------
  SPEDIZIONE: {
    CORRIERE: 'FedEx',
    // DAP = dazi e tasse a carico del destinatario (il caso più comune per l'e-commerce)
    // DDP = dazi e tasse pagati da te
    INCOTERM: 'DAP',
    MOTIVO_EXPORT: 'Vendita / Sale',
    // Peso dell'imballo (scatola, carta…) da aggiungere al peso netto, in kg
    PESO_IMBALLO_KG: 0.30,
    NUMERO_COLLI: 1,
    // Copie della fattura commerciale nello stesso PDF (FedEx ne chiede di solito 3
    // se non usi l'invio elettronico ETD). Metti 1 se usi FedEx ETD.
    COPIE_FATTURA: 1
  },

  // ---------------------------------------------------------------------------
  // VALORI DI RISERVA – usati se il prodotto su Shopify non ha il dato compilato
  // (conviene compilarli in Shopify: Prodotto → Variante → "Dogana")
  // ---------------------------------------------------------------------------
  PRODOTTI: {
    // 6505.00 = cappelli a maglia o confezionati con tessuto (cotone, poliestere…)
    // Varianti utili: 6504.00 cappelli di paglia/intrecciati, 6505.00.30 cappellini con visiera,
    // 6505.00.10 cappelli di feltro di lana. Meglio impostarlo prodotto per prodotto su Shopify.
    HS_CODE_DEFAULT: '650500',
    ORIGINE_DEFAULT: 'IT',
    PESO_UNITARIO_DEFAULT_KG: 0.15,
    DESCRIZIONE_DOGANALE_DEFAULT: 'Hat / Cappello',
    COMPOSIZIONE_DEFAULT: '',          // es. '100% Cotone / 100% Cotton'

    // Metafield prodotto (facoltativi) da cui leggere i dati per singolo prodotto.
    // Creali in Shopify: Impostazioni → Dati personalizzati → Prodotti.
    METAFIELD_COMPOSIZIONE: { namespace: 'custom', key: 'composizione' },
    METAFIELD_DESCRIZIONE_DOGANALE: { namespace: 'custom', key: 'descrizione_doganale' }
  },

  // ---------------------------------------------------------------------------
  // ORIGINE PREFERENZIALE
  // Metti true SOLO se i cappelli sono prodotti in Italia/UE rispettando le regole
  // di origine degli accordi UE (chiedi conferma al tuo spedizioniere/commercialista).
  // Se true, sulla fattura e sulla dichiarazione di origine compare la "dichiarazione
  // di origine su fattura" che permette al cliente (es. UK, Svizzera, Canada, Giappone)
  // di pagare dazi ridotti o zero. Sopra i 6.000 € serve anche il numero REX.
  // ---------------------------------------------------------------------------
  ORIGINE_PREFERENZIALE: false,

  // ---------------------------------------------------------------------------
  // FATTURA COMMERCIALE
  // ---------------------------------------------------------------------------
  FATTURA: {
    // Numerazione: PREFISSO-ANNO-0001. In alternativa usa il numero d'ordine Shopify.
    USA_NUMERO_ORDINE: false,
    PREFISSO: 'CI',
    // Clausola IVA per le esportazioni (art. 8, c.1, lett. a: trasporto a cura del cedente)
    CLAUSOLA_IVA: 'Operazione non imponibile IVA ai sensi dell\'art. 8, comma 1, lett. a), D.P.R. 633/1972 – ' +
                  'VAT exempt export (Art. 8(1)(a) Italian Presidential Decree 633/1972)',
    // Nota a piè di pagina facoltativa
    NOTE: ''
  },

  // ---------------------------------------------------------------------------
  // QUALI ORDINI ELABORARE
  // ---------------------------------------------------------------------------
  ORDINI: {
    // Elabora solo ordini con pagamento completato
    SOLO_PAGATI: true,
    // Aggiunge un tag all'ordine su Shopify quando i documenti sono pronti
    // (richiede il permesso write_orders). Comodo per vedere a colpo d'occhio cosa è pronto.
    AGGIUNGI_TAG: true,
    TAG: 'documenti-export-ok',
    // Paesi verso cui NON generare nulla e mandare un avviso (sanzioni UE: per Russia e
    // Bielorussia è vietato esportare beni di lusso, inclusi capi d'abbigliamento > 300 €).
    PAESI_BLOCCATI: ['RU', 'BY', 'KP', 'IR', 'SY'],
    // Ogni quanti minuti controllare i nuovi ordini (1, 5, 10, 15 o 30)
    INTERVALLO_MINUTI: 15
  },

  // ---------------------------------------------------------------------------
  // NOTIFICHE
  // ---------------------------------------------------------------------------
  NOTIFICHE: {
    // Ti manda una email se un ordine non va a buon fine o se mancano dati
    EMAIL_ERRORI: true,
    // Email di destinazione ('' = l'account Google che esegue lo script)
    EMAIL: '',
    // Email di riepilogo ogni volta che vengono generati nuovi documenti
    EMAIL_RIEPILOGO: false
  },

  // Versione delle API Shopify (aggiornala una volta l'anno, es. '2027-01')
  SHOPIFY_API_VERSION: '2026-07'
};
