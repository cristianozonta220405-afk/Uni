/**
 * ============================================================================
 *  Documenti di spedizione per ordini Shopify extra-UE → Google Drive
 * ============================================================================
 *
 *  NON serve modificare questo file: i dati vanno in Configurazione.gs.
 *
 *  Per ogni ordine pagato con spedizione fuori dall'Unione Europea genera:
 *    1. Fattura commerciale (Commercial Invoice) per FedEx / dogana
 *    2. Dichiarazione di origine della merce
 *    3. Dichiarazione di conformità del prodotto
 *    4. Dichiarazione di libera esportazione
 *  e salva i PDF nella cartella Drive "Fatture Estere", annotando tutto nel registro.
 *
 *  Funzioni da lanciare a mano dal menu "Esegui":
 *    setup()                     → prima installazione (una sola volta)
 *    processaNuoviOrdini()       → controllo manuale immediato (gira anche da solo)
 *    generaDocumentiOrdine()     → rigenera i documenti di un ordine specifico
 *    testConnessioneShopify()    → verifica che le credenziali funzionino
 *    disattivaAutomazione()      → ferma il controllo automatico
 */

// ============================================================================
//  COSTANTI
// ============================================================================

/** I 27 Stati membri UE + Monaco (territorio doganale UE tramite la Francia). */
var PAESI_UE = [
  'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE',
  'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'MC'
];

/**
 * Territori che fanno parte di uno Stato UE ma sono FUORI dal territorio doganale/IVA:
 * le spedizioni lì richiedono comunque i documenti di esportazione.
 * Chiave: codice paese → codici provincia Shopify.
 */
var TERRITORI_EXTRA_UE = {
  ES: ['GC', 'TF', 'CE', 'ML'] // Canarie (Las Palmas, S.C. Tenerife), Ceuta, Melilla
};

/** CAP italiani fuori dal territorio doganale UE (Livigno). */
var CAP_EXTRA_UE_IT = ['23041'];

var FUSO_ORARIO = 'Europe/Rome';
var PROP_ULTIMO_CONTROLLO = 'ULTIMO_CONTROLLO';
var PROP_TOKEN = 'SHOPIFY_TOKEN_CACHE';
var PROP_TOKEN_SCADENZA = 'SHOPIFY_TOKEN_SCADENZA';
var PROP_CARTELLA_ID = 'CARTELLA_ID';
var PROP_REGISTRO_ID = 'REGISTRO_ID';

var NOMI_PAESI = {
  AD: 'Andorra', AE: 'United Arab Emirates', AL: 'Albania', AR: 'Argentina', AU: 'Australia',
  BA: 'Bosnia and Herzegovina', BR: 'Brazil', BY: 'Belarus', CA: 'Canada', CH: 'Switzerland',
  CL: 'Chile', CN: 'China', CO: 'Colombia', EG: 'Egypt', GB: 'United Kingdom', GE: 'Georgia',
  GG: 'Guernsey', GI: 'Gibraltar', HK: 'Hong Kong', ID: 'Indonesia', IL: 'Israel', IN: 'India',
  IS: 'Iceland', JE: 'Jersey', JP: 'Japan', KR: 'South Korea', KW: 'Kuwait', LI: 'Liechtenstein',
  MA: 'Morocco', MD: 'Moldova', ME: 'Montenegro', MK: 'North Macedonia', MX: 'Mexico',
  MY: 'Malaysia', NO: 'Norway', NZ: 'New Zealand', PE: 'Peru', PH: 'Philippines', QA: 'Qatar',
  RS: 'Serbia', RU: 'Russia', SA: 'Saudi Arabia', SG: 'Singapore', SM: 'San Marino',
  TH: 'Thailand', TN: 'Tunisia', TR: 'Turkey', TW: 'Taiwan', UA: 'Ukraine', US: 'United States',
  VA: 'Vatican City', VN: 'Vietnam', ZA: 'South Africa',
  AT: 'Austria', BE: 'Belgium', BG: 'Bulgaria', HR: 'Croatia', CY: 'Cyprus', CZ: 'Czech Republic',
  DK: 'Denmark', EE: 'Estonia', FI: 'Finland', FR: 'France', DE: 'Germany', GR: 'Greece',
  HU: 'Hungary', IE: 'Ireland', IT: 'Italy', LV: 'Latvia', LT: 'Lithuania', LU: 'Luxembourg',
  MT: 'Malta', NL: 'Netherlands', PL: 'Poland', PT: 'Portugal', RO: 'Romania', SK: 'Slovakia',
  SI: 'Slovenia', ES: 'Spain', SE: 'Sweden', MC: 'Monaco'
};

// ============================================================================
//  FUNZIONI PRINCIPALI (da lanciare a mano)
// ============================================================================

/**
 * PRIMA INSTALLAZIONE. Lanciala una volta sola dopo aver compilato
 * Configurazione.gs e le Proprietà script. Crea cartella, registro e
 * attiva il controllo automatico degli ordini.
 */
function setup() {
  verificaConfigurazione_();
  var nomeNegozio = testConnessioneShopify();

  var cartella = cartellaPrincipale_();
  var registro = registro_();

  var props = PropertiesService.getScriptProperties();
  if (!props.getProperty(PROP_ULTIMO_CONTROLLO)) {
    // Si parte dagli ordini di oggi: quelli più vecchi si possono generare a mano
    // con generaDocumentiOrdine().
    var oggi = new Date();
    oggi.setHours(0, 0, 0, 0);
    props.setProperty(PROP_ULTIMO_CONTROLLO, oggi.toISOString());
  }

  installaTrigger_();

  var msg = 'Installazione completata.\n' +
    '• Negozio: ' + nomeNegozio + '\n' +
    '• Cartella Drive: ' + cartella.getUrl() + '\n' +
    '• Registro: ' + registro.getUrl() + '\n' +
    '• Controllo automatico ogni ' + intervalloMinuti_() + ' minuti, a partire dagli ordini del ' +
    formattaData_(new Date(props.getProperty(PROP_ULTIMO_CONTROLLO))) + '.';
  Logger.log(msg);
  return msg;
}

/**
 * Controlla i nuovi ordini pagati e genera i documenti per quelli extra-UE.
 * Viene eseguita automaticamente dal trigger; puoi lanciarla anche a mano.
 */
function processaNuoviOrdini() {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(10000)) {
    Logger.log('Un\'altra esecuzione è già in corso: salto questo giro.');
    return;
  }
  try {
    var props = PropertiesService.getScriptProperties();
    var inizioGiro = new Date();
    var ultimo = props.getProperty(PROP_ULTIMO_CONTROLLO);
    var da = ultimo ? new Date(ultimo) : new Date(inizioGiro.getTime() - 24 * 3600 * 1000);
    // margine di sicurezza di 10 minuti per non perdere ordini a cavallo dei giri
    da = new Date(da.getTime() - 10 * 60 * 1000);

    var query = ['updated_at:>=\'' + da.toISOString() + '\''];
    if (CONFIG.ORDINI.SOLO_PAGATI) query.push('financial_status:paid');
    if (CONFIG.ORDINI.AGGIUNGI_TAG && CONFIG.ORDINI.TAG) query.push('-tag:"' + CONFIG.ORDINI.TAG + '"');

    var ordini = shopifyCercaOrdini_(query.join(' '));
    var giaFatti = ordiniGiaRegistrati_();
    var esito = { generati: [], saltatiUe: 0, bloccati: [], errori: [] };

    ordini.forEach(function (o) {
      if (giaFatti[o.id]) return;
      try {
        var r = elaboraOrdine_(o, false);
        if (r.stato === 'generato') esito.generati.push(r);
        else if (r.stato === 'ue') esito.saltatiUe++;
        else if (r.stato === 'bloccato') esito.bloccati.push(r);
      } catch (e) {
        esito.errori.push({ ordine: o.name, errore: messaggioErrore_(e) });
        registraErrore_(o.name, e);
      }
    });

    // Se ci sono stati errori non avanzo il "segnalibro": al prossimo giro riprovo.
    if (esito.errori.length === 0) {
      props.setProperty(PROP_ULTIMO_CONTROLLO, inizioGiro.toISOString());
    }

    Logger.log('Ordini letti: %s | Documenti generati: %s | UE saltati: %s | Bloccati: %s | Errori: %s',
      ordini.length, esito.generati.length, esito.saltatiUe, esito.bloccati.length, esito.errori.length);

    notifica_(esito);
    return esito;
  } finally {
    lock.releaseLock();
  }
}

/**
 * Genera (o rigenera) i documenti di UN ordine, anche vecchio.
 * Modifica il numero qui sotto e lancia la funzione.
 * @param {string=} numeroOrdine es. '#1045' oppure '1045'
 */
function generaDocumentiOrdine(numeroOrdine) {
  numeroOrdine = numeroOrdine || '#1001'; // <-- cambia qui il numero d'ordine
  var nome = String(numeroOrdine).charAt(0) === '#' ? String(numeroOrdine) : '#' + numeroOrdine;
  var ordini = shopifyCercaOrdini_('name:\'' + nome + '\'');
  var ordine = ordini.filter(function (o) { return o.name === nome; })[0];
  if (!ordine) throw new Error('Ordine ' + nome + ' non trovato su Shopify.');
  var r = elaboraOrdine_(ordine, true);
  Logger.log(r.stato === 'generato' ? 'Documenti creati: ' + r.url : 'Esito: ' + r.stato + ' – ' + (r.motivo || ''));
  return r;
}

/** Verifica le credenziali Shopify e restituisce il nome del negozio. */
function testConnessioneShopify() {
  var dati = shopifyGraphql_('{ shop { name myshopifyDomain currencyCode } }', {});
  var s = dati.shop;
  Logger.log('Connessione OK: %s (%s), valuta %s', s.name, s.myshopifyDomain, s.currencyCode);
  return s.name;
}

/** Ferma il controllo automatico (i documenti già creati restano su Drive). */
function disattivaAutomazione() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'processaNuoviOrdini') ScriptApp.deleteTrigger(t);
  });
  Logger.log('Automazione disattivata.');
}

// ============================================================================
//  ELABORAZIONE ORDINE
// ============================================================================

/**
 * @param {Object} ordineShopify nodo ordine restituito da GraphQL
 * @param {boolean} forza rigenera anche se già registrato
 * @return {{stato:string, url?:string, motivo?:string, ordine:string}}
 */
function elaboraOrdine_(ordineShopify, forza) {
  var o = normalizzaOrdine_(ordineShopify);

  if (!o.spedizione.codicePaese) {
    return { stato: 'ue', ordine: o.nome, motivo: 'ordine senza indirizzo di spedizione' };
  }
  if (!isExtraUe_(o.spedizione)) {
    return { stato: 'ue', ordine: o.nome, motivo: 'spedizione in UE' };
  }
  if (CONFIG.ORDINI.PAESI_BLOCCATI.indexOf(o.spedizione.codicePaese) !== -1) {
    var motivo = 'Destinazione soggetta a sanzioni UE (' + o.spedizione.codicePaese +
      '): documenti NON generati. Verifica prima di spedire.';
    registraErrore_(o.nome, new Error(motivo));
    return { stato: 'bloccato', ordine: o.nome, motivo: motivo };
  }
  if (o.righe.length === 0) {
    return { stato: 'ue', ordine: o.nome, motivo: 'nessun articolo da spedire' };
  }

  var esistente = forza ? null : rigaRegistro_(o.id);
  if (esistente) return { stato: 'gia_fatto', ordine: o.nome, url: esistente.url };

  var numero = forza ? (numeroFatturaEsistente_(o.id) || nuovoNumeroFattura_(o)) : nuovoNumeroFattura_(o);
  var doc = { ordine: o, numero: numero, data: new Date(), azienda: CONFIG.AZIENDA, logo: logoDataUri_() };

  var cartella = cartellaOrdine_(o);
  var base = numero.replace(/[\/\\]/g, '-') + '_' + o.nome.replace('#', '');
  var files = [
    salvaPdf_(cartella, base + '_1_Fattura_Commerciale.pdf', htmlFatturaCommerciale_(doc)),
    salvaPdf_(cartella, base + '_2_Dichiarazione_Origine.pdf', htmlDichiarazioneOrigine_(doc)),
    salvaPdf_(cartella, base + '_3_Dichiarazione_Conformita.pdf', htmlDichiarazioneConformita_(doc)),
    salvaPdf_(cartella, base + '_4_Dichiarazione_Libera_Esportazione.pdf', htmlLiberaEsportazione_(doc))
  ];

  scriviRegistro_(o, numero, cartella.getUrl(), forza);

  if (CONFIG.ORDINI.AGGIUNGI_TAG && CONFIG.ORDINI.TAG) {
    try {
      shopifyAggiungiTag_(o.id, CONFIG.ORDINI.TAG);
    } catch (e) {
      // Non blocca nulla: i documenti sono già salvati e l'ordine è nel registro.
      Logger.log('Impossibile aggiungere il tag (manca il permesso write_orders?): ' + messaggioErrore_(e));
    }
  }

  return {
    stato: 'generato', ordine: o.nome, numero: numero, url: cartella.getUrl(),
    paese: o.spedizione.codicePaese, avvisi: o.avvisi, files: files.length
  };
}

/** Converte l'ordine GraphQL in una struttura semplice usata dai modelli. */
function normalizzaOrdine_(n) {
  var P = CONFIG.PRODOTTI;
  var avvisi = [];
  var valuta = soldi_(n.currentTotalPriceSet).valuta || soldi_(n.totalPriceSet).valuta || 'EUR';

  var righe = (n.lineItems && n.lineItems.nodes || []).filter(function (li) {
    var q = li.currentQuantity != null ? li.currentQuantity : li.quantity;
    return q > 0 && li.requiresShipping !== false;
  }).map(function (li) {
    var q = li.currentQuantity != null ? li.currentQuantity : li.quantity;
    var inv = li.variant && li.variant.inventoryItem || {};
    var prodotto = li.product || (li.variant && li.variant.product) || {};
    var titolo = li.title + (li.variantTitle ? ' – ' + li.variantTitle : '');

    var hs = (inv.harmonizedSystemCode || '').replace(/\D/g, '');
    if (!hs) { hs = P.HS_CODE_DEFAULT; avvisi.push('Codice HS mancante per "' + titolo + '": usato ' + P.HS_CODE_DEFAULT); }

    var origine = inv.countryCodeOfOrigin || '';
    if (!origine) { origine = P.ORIGINE_DEFAULT; avvisi.push('Paese di origine mancante per "' + titolo + '": usato ' + P.ORIGINE_DEFAULT); }

    var peso = pesoKg_(inv.measurement && inv.measurement.weight);
    if (!peso) { peso = P.PESO_UNITARIO_DEFAULT_KG; avvisi.push('Peso mancante per "' + titolo + '": usati ' + P.PESO_UNITARIO_DEFAULT_KG + ' kg'); }

    var prezzo = soldi_(li.discountedUnitPriceAfterAllDiscountsSet).importo;
    if (prezzo == null) prezzo = soldi_(li.discountedUnitPriceSet).importo;
    if (prezzo == null) prezzo = soldi_(li.originalUnitPriceSet).importo || 0;

    var composizione = (prodotto.composizione && prodotto.composizione.value) || P.COMPOSIZIONE_DEFAULT || '';
    var descrDoganale = (prodotto.descrizioneDoganale && prodotto.descrizioneDoganale.value) || P.DESCRIZIONE_DOGANALE_DEFAULT;

    return {
      titolo: titolo,
      sku: li.sku || '',
      descrizioneDoganale: descrDoganale,
      composizione: composizione,
      hs: hs,
      origine: origine.toUpperCase(),
      quantita: q,
      prezzoUnitario: arrotonda_(prezzo),
      totale: arrotonda_(prezzo * q),
      pesoUnitario: peso,
      pesoTotale: arrotonda_(peso * q, 3)
    };
  });

  var totaleMerce = arrotonda_(righe.reduce(function (s, r) { return s + r.totale; }, 0));
  var spedizione = arrotonda_(soldi_(n.totalShippingPriceSet).importo || 0);
  var pesoNetto = arrotonda_(righe.reduce(function (s, r) { return s + r.pesoTotale; }, 0), 3);

  var sped = indirizzo_(n.shippingAddress);
  var fatt = indirizzo_(n.billingAddress) || sped;
  var cliente = n.customer || {};
  if (sped) {
    sped.email = n.email || cliente.email || '';
    sped.telefono = sped.telefono || n.phone || cliente.phone || '';
    if (!sped.telefono) avvisi.push('Telefono del destinatario mancante: FedEx lo richiede per lo sdoganamento.');
  }

  return {
    id: n.id,
    nome: n.name,
    dataOrdine: new Date(n.createdAt),
    valuta: valuta,
    spedizione: sped || { codicePaese: '' },
    fatturazione: fatt,
    righe: righe,
    totaleMerce: totaleMerce,
    costoSpedizione: spedizione,
    totale: arrotonda_(totaleMerce + spedizione),
    pezzi: righe.reduce(function (s, r) { return s + r.quantita; }, 0),
    pesoNetto: pesoNetto,
    pesoLordo: arrotonda_(pesoNetto + (CONFIG.SPEDIZIONE.PESO_IMBALLO_KG || 0), 3),
    avvisi: avvisi
  };
}

function indirizzo_(a) {
  if (!a) return null;
  var nome = a.name || [a.firstName, a.lastName].filter(Boolean).join(' ');
  return {
    nome: nome,
    azienda: a.company || '',
    riga1: a.address1 || '',
    riga2: a.address2 || '',
    citta: a.city || '',
    provincia: a.provinceCode || a.province || '',
    codiceProvincia: a.provinceCode || '',
    cap: a.zip || '',
    paese: a.country || NOMI_PAESI[a.countryCodeV2] || a.countryCodeV2 || '',
    codicePaese: (a.countryCodeV2 || '').toUpperCase(),
    telefono: a.phone || ''
  };
}

/** true se la destinazione è fuori dal territorio doganale UE. */
function isExtraUe_(ind) {
  var paese = (ind.codicePaese || '').toUpperCase();
  if (!paese) return false;
  var eccezioni = TERRITORI_EXTRA_UE[paese];
  if (eccezioni && eccezioni.indexOf((ind.codiceProvincia || '').toUpperCase()) !== -1) return true;
  if (paese === 'IT' && CAP_EXTRA_UE_IT.indexOf(String(ind.cap || '').trim()) !== -1) return true;
  return PAESI_UE.indexOf(paese) === -1;
}

// ============================================================================
//  SHOPIFY
// ============================================================================

var QUERY_ORDINI_ =
  'query Ordini($q: String!, $cursor: String, $nsComp: String!, $keyComp: String!, $nsDesc: String!, $keyDesc: String!) {' +
  '  orders(first: 25, after: $cursor, query: $q, sortKey: UPDATED_AT) {' +
  '    pageInfo { hasNextPage endCursor }' +
  '    nodes {' +
  '      id name createdAt email phone tags' +
  '      customer { firstName lastName email phone }' +
  '      shippingAddress { name firstName lastName company address1 address2 city province provinceCode zip country countryCodeV2 phone }' +
  '      billingAddress { name firstName lastName company address1 address2 city province provinceCode zip country countryCodeV2 phone }' +
  '      currentTotalPriceSet { shopMoney { amount currencyCode } }' +
  '      totalPriceSet { shopMoney { amount currencyCode } }' +
  '      totalShippingPriceSet { shopMoney { amount currencyCode } }' +
  '      lineItems(first: 100) {' +
  '        nodes {' +
  '          title variantTitle sku quantity currentQuantity requiresShipping' +
  '          originalUnitPriceSet { shopMoney { amount currencyCode } }' +
  '          discountedUnitPriceSet { shopMoney { amount currencyCode } }' +
  '          discountedUnitPriceAfterAllDiscountsSet { shopMoney { amount currencyCode } }' +
  '          product {' +
  '            composizione: metafield(namespace: $nsComp, key: $keyComp) { value }' +
  '            descrizioneDoganale: metafield(namespace: $nsDesc, key: $keyDesc) { value }' +
  '          }' +
  '          variant { inventoryItem { harmonizedSystemCode countryCodeOfOrigin measurement { weight { unit value } } } }' +
  '        }' +
  '      }' +
  '    }' +
  '  }' +
  '}';

/** Cerca ordini con la sintassi di ricerca Shopify, gestendo la paginazione. */
function shopifyCercaOrdini_(query) {
  var P = CONFIG.PRODOTTI;
  var risultati = [];
  var cursor = null;
  var pagine = 0;
  do {
    var dati = shopifyGraphql_(QUERY_ORDINI_, {
      q: query, cursor: cursor,
      nsComp: P.METAFIELD_COMPOSIZIONE.namespace, keyComp: P.METAFIELD_COMPOSIZIONE.key,
      nsDesc: P.METAFIELD_DESCRIZIONE_DOGANALE.namespace, keyDesc: P.METAFIELD_DESCRIZIONE_DOGANALE.key
    });
    risultati = risultati.concat(dati.orders.nodes);
    cursor = dati.orders.pageInfo.hasNextPage ? dati.orders.pageInfo.endCursor : null;
    pagine++;
  } while (cursor && pagine < 40);
  return risultati;
}

function shopifyAggiungiTag_(idOrdine, tag) {
  var dati = shopifyGraphql_(
    'mutation Tag($id: ID!, $tags: [String!]!) { tagsAdd(id: $id, tags: $tags) { userErrors { field message } } }',
    { id: idOrdine, tags: [tag] });
  var err = dati.tagsAdd.userErrors;
  if (err && err.length) throw new Error(err.map(function (e) { return e.message; }).join('; '));
}

/** Esegue una chiamata GraphQL Admin API con retry su limiti di velocità. */
function shopifyGraphql_(query, variabili) {
  var negozio = dominioNegozio_();
  var url = 'https://' + negozio + '/admin/api/' + CONFIG.SHOPIFY_API_VERSION + '/graphql.json';
  var tentativi = 0;
  while (true) {
    tentativi++;
    var risposta = UrlFetchApp.fetch(url, {
      method: 'post',
      contentType: 'application/json',
      headers: { 'X-Shopify-Access-Token': tokenShopify_(tentativi > 1) },
      payload: JSON.stringify({ query: query, variables: variabili || {} }),
      muteHttpExceptions: true
    });
    var codice = risposta.getResponseCode();
    var testo = risposta.getContentText();

    if ((codice === 429 || codice >= 500) && tentativi < 5) {
      Utilities.sleep(1000 * Math.pow(2, tentativi));
      continue;
    }
    if (codice === 401 && tentativi < 2 && usaClientCredentials_()) {
      continue; // token scaduto: al secondo giro ne chiede uno nuovo
    }
    if (codice !== 200) {
      throw new Error('Shopify ha risposto ' + codice + ': ' + testo.substring(0, 500));
    }
    var json = JSON.parse(testo);
    if (json.errors && json.errors.length) {
      var throttled = json.errors.some(function (e) { return e.extensions && e.extensions.code === 'THROTTLED'; });
      if (throttled && tentativi < 5) { Utilities.sleep(2000 * tentativi); continue; }
      throw new Error('Errore GraphQL Shopify: ' + json.errors.map(function (e) { return e.message; }).join('; '));
    }
    return json.data;
  }
}

function dominioNegozio_() {
  var d = PropertiesService.getScriptProperties().getProperty('SHOPIFY_NEGOZIO');
  if (!d) throw new Error('Manca la proprietà script SHOPIFY_NEGOZIO (es. tuonegozio.myshopify.com).');
  d = d.trim().replace(/^https?:\/\//, '').replace(/\/.*$/, '');
  if (d.indexOf('.') === -1) d += '.myshopify.com';
  return d;
}

function usaClientCredentials_() {
  var p = PropertiesService.getScriptProperties();
  return !p.getProperty('SHOPIFY_ACCESS_TOKEN') && !!p.getProperty('SHOPIFY_CLIENT_ID');
}

/**
 * Restituisce il token di accesso.
 *  - App creata nel Dev Dashboard (dal 2026): SHOPIFY_CLIENT_ID + SHOPIFY_CLIENT_SECRET,
 *    il token (valido 24 ore) viene richiesto e rinnovato in automatico.
 *  - App personalizzata "vecchia" creata dall'admin: SHOPIFY_ACCESS_TOKEN (shpat_...).
 */
function tokenShopify_(forzaRinnovo) {
  var p = PropertiesService.getScriptProperties();
  var statico = p.getProperty('SHOPIFY_ACCESS_TOKEN');
  if (statico) return statico.trim();

  var clientId = p.getProperty('SHOPIFY_CLIENT_ID');
  var secret = p.getProperty('SHOPIFY_CLIENT_SECRET');
  if (!clientId || !secret) {
    throw new Error('Credenziali Shopify mancanti: imposta SHOPIFY_CLIENT_ID e SHOPIFY_CLIENT_SECRET ' +
      '(oppure SHOPIFY_ACCESS_TOKEN) nelle Proprietà script.');
  }
  var cache = p.getProperty(PROP_TOKEN);
  var scadenza = Number(p.getProperty(PROP_TOKEN_SCADENZA) || 0);
  if (!forzaRinnovo && cache && Date.now() < scadenza) return cache;

  var r = UrlFetchApp.fetch('https://' + dominioNegozio_() + '/admin/oauth/access_token', {
    method: 'post',
    payload: { grant_type: 'client_credentials', client_id: clientId.trim(), client_secret: secret.trim() },
    muteHttpExceptions: true
  });
  if (r.getResponseCode() !== 200) {
    throw new Error('Impossibile ottenere il token Shopify (' + r.getResponseCode() + '): ' +
      r.getContentText().substring(0, 300) + '. L\'app è installata sul negozio?');
  }
  var json = JSON.parse(r.getContentText());
  var durata = (json.expires_in || 86399) * 1000;
  p.setProperty(PROP_TOKEN, json.access_token);
  p.setProperty(PROP_TOKEN_SCADENZA, String(Date.now() + durata - 30 * 60 * 1000)); // rinnova 30 min prima
  return json.access_token;
}

// ============================================================================
//  GOOGLE DRIVE E REGISTRO
// ============================================================================

function cartellaPrincipale_() {
  var props = PropertiesService.getScriptProperties();
  var id = CONFIG.DRIVE.ID_CARTELLA || props.getProperty(PROP_CARTELLA_ID);
  if (id) {
    try { return DriveApp.getFolderById(id); } catch (e) { /* cartella cancellata: la ricreo */ }
  }
  var trovate = DriveApp.getRootFolder().getFoldersByName(CONFIG.DRIVE.NOME_CARTELLA);
  var cartella = trovate.hasNext() ? trovate.next() : DriveApp.getRootFolder().createFolder(CONFIG.DRIVE.NOME_CARTELLA);
  props.setProperty(PROP_CARTELLA_ID, cartella.getId());
  return cartella;
}

function sottocartella_(padre, nome) {
  var it = padre.getFoldersByName(nome);
  return it.hasNext() ? it.next() : padre.createFolder(nome);
}

function cartellaOrdine_(o) {
  var c = cartellaPrincipale_();
  if (CONFIG.DRIVE.SOTTOCARTELLA_PER_ANNO) c = sottocartella_(c, Utilities.formatDate(o.dataOrdine, FUSO_ORARIO, 'yyyy'));
  if (CONFIG.DRIVE.SOTTOCARTELLA_PER_ORDINE) {
    var nome = o.nome + ' – ' + (o.spedizione.nome || 'Cliente') + ' (' + o.spedizione.codicePaese + ')';
    c = sottocartella_(c, nome.replace(/[\/\\]/g, '-'));
  }
  return c;
}

/** Converte l'HTML in PDF e lo salva (sostituendo un eventuale file con lo stesso nome). */
function salvaPdf_(cartella, nomeFile, html) {
  var vecchi = cartella.getFilesByName(nomeFile);
  while (vecchi.hasNext()) vecchi.next().setTrashed(true);
  var pdf = Utilities.newBlob(html, 'text/html', nomeFile.replace(/\.pdf$/, '.html'))
    .getAs('application/pdf')
    .setName(nomeFile);
  return cartella.createFile(pdf);
}

var INTESTAZIONE_REGISTRO_ = ['Data creazione', 'N. fattura commerciale', 'Ordine Shopify', 'Data ordine',
  'Cliente', 'Paese', 'Pezzi', 'Valore merce', 'Spedizione', 'Totale', 'Valuta', 'Peso lordo kg',
  'Cartella Drive', 'Avvisi', 'ID ordine'];

var registroCache_ = null;

function registro_() {
  if (registroCache_) return registroCache_;
  var props = PropertiesService.getScriptProperties();
  var id = props.getProperty(PROP_REGISTRO_ID);
  if (id) {
    try { registroCache_ = SpreadsheetApp.openById(id); return registroCache_; } catch (e) { /* ricreo */ }
  }
  var cartella = cartellaPrincipale_();
  var esistenti = cartella.getFilesByName(CONFIG.DRIVE.NOME_REGISTRO);
  var ss;
  if (esistenti.hasNext()) {
    ss = SpreadsheetApp.openById(esistenti.next().getId());
  } else {
    ss = SpreadsheetApp.create(CONFIG.DRIVE.NOME_REGISTRO);
    DriveApp.getFileById(ss.getId()).moveTo(cartella);
    var foglio = ss.getSheets()[0].setName('Registro');
    foglio.appendRow(INTESTAZIONE_REGISTRO_);
    foglio.getRange(1, 1, 1, INTESTAZIONE_REGISTRO_.length).setFontWeight('bold').setBackground('#e8eef7');
    foglio.setFrozenRows(1);
    var err = ss.insertSheet('Errori');
    err.appendRow(['Data', 'Ordine', 'Errore']);
    err.getRange(1, 1, 1, 3).setFontWeight('bold').setBackground('#fde8e8');
    err.setFrozenRows(1);
  }
  props.setProperty(PROP_REGISTRO_ID, ss.getId());
  registroCache_ = ss;
  return ss;
}

function foglioRegistro_() { return registro_().getSheetByName('Registro'); }

/** Mappa { idOrdine: true } degli ordini già registrati. */
function ordiniGiaRegistrati_() {
  var f = foglioRegistro_();
  var mappa = {};
  if (f.getLastRow() < 2) return mappa;
  var col = INTESTAZIONE_REGISTRO_.indexOf('ID ordine') + 1;
  f.getRange(2, col, f.getLastRow() - 1, 1).getValues().forEach(function (r) { if (r[0]) mappa[r[0]] = true; });
  return mappa;
}

function rigaRegistro_(idOrdine) {
  var f = foglioRegistro_();
  if (f.getLastRow() < 2) return null;
  var valori = f.getRange(2, 1, f.getLastRow() - 1, INTESTAZIONE_REGISTRO_.length).getValues();
  var cId = INTESTAZIONE_REGISTRO_.indexOf('ID ordine');
  for (var i = 0; i < valori.length; i++) {
    if (valori[i][cId] === idOrdine) {
      return { riga: i + 2, numero: valori[i][1], url: valori[i][INTESTAZIONE_REGISTRO_.indexOf('Cartella Drive')] };
    }
  }
  return null;
}

function numeroFatturaEsistente_(idOrdine) {
  var r = rigaRegistro_(idOrdine);
  return r ? String(r.numero) : null;
}

/** Numero progressivo per anno: PREFISSO-2026-0001 (o numero d'ordine se configurato). */
function nuovoNumeroFattura_(o) {
  if (CONFIG.FATTURA.USA_NUMERO_ORDINE) return o.nome.replace('#', '');
  var anno = Utilities.formatDate(new Date(), FUSO_ORARIO, 'yyyy');
  var prefisso = (CONFIG.FATTURA.PREFISSO || 'CI') + '-' + anno + '-';
  var f = foglioRegistro_();
  var max = 0;
  if (f.getLastRow() >= 2) {
    f.getRange(2, 2, f.getLastRow() - 1, 1).getValues().forEach(function (r) {
      var v = String(r[0]);
      if (v.indexOf(prefisso) === 0) max = Math.max(max, parseInt(v.substring(prefisso.length), 10) || 0);
    });
  }
  return prefisso + ('000' + (max + 1)).slice(-4);
}

function scriviRegistro_(o, numero, url, sovrascrivi) {
  var f = foglioRegistro_();
  var riga = [
    new Date(), numero, o.nome, o.dataOrdine, o.spedizione.nome, o.spedizione.codicePaese, o.pezzi,
    o.totaleMerce, o.costoSpedizione, o.totale, o.valuta, o.pesoLordo, url, o.avvisi.join(' | '), o.id
  ];
  var esistente = sovrascrivi ? rigaRegistro_(o.id) : null;
  if (esistente) f.getRange(esistente.riga, 1, 1, riga.length).setValues([riga]);
  else f.appendRow(riga);
}

function registraErrore_(ordine, e) {
  try {
    registro_().getSheetByName('Errori').appendRow([new Date(), ordine, messaggioErrore_(e)]);
  } catch (x) {
    Logger.log('Impossibile scrivere nel foglio Errori: ' + x);
  }
  Logger.log('Errore ordine %s: %s', ordine, messaggioErrore_(e));
}

// ============================================================================
//  TRIGGER, CONTROLLI, NOTIFICHE
// ============================================================================

function intervalloMinuti_() {
  var consentiti = [1, 5, 10, 15, 30];
  var m = Number(CONFIG.ORDINI.INTERVALLO_MINUTI) || 15;
  return consentiti.indexOf(m) !== -1 ? m : 15;
}

function installaTrigger_() {
  disattivaAutomazione();
  ScriptApp.newTrigger('processaNuoviOrdini').timeBased().everyMinutes(intervalloMinuti_()).create();
}

function verificaConfigurazione_() {
  var a = CONFIG.AZIENDA;
  var mancanti = [];
  ['RAGIONE_SOCIALE', 'INDIRIZZO', 'CITTA', 'PARTITA_IVA', 'EORI', 'FIRMATARIO_NOME'].forEach(function (k) {
    if (!a[k]) mancanti.push('AZIENDA.' + k);
  });
  if (mancanti.length) throw new Error('Compila in Configurazione.gs: ' + mancanti.join(', '));
  if (a.RAGIONE_SOCIALE === 'Nome Azienda S.r.l.' || a.PARTITA_IVA === 'IT00000000000') {
    Logger.log('ATTENZIONE: in Configurazione.gs ci sono ancora i dati di esempio dell\'azienda.');
  }
  dominioNegozio_();
}

function notifica_(esito) {
  var N = CONFIG.NOTIFICHE;
  var email = N.EMAIL || Session.getEffectiveUser().getEmail();
  if (!email) return;
  var problemi = esito.errori.length || esito.bloccati.length ||
    esito.generati.some(function (g) { return g.avvisi && g.avvisi.length; });

  if (N.EMAIL_ERRORI && problemi) {
    var righe = [];
    esito.errori.forEach(function (e) { righe.push('ERRORE ' + e.ordine + ': ' + e.errore); });
    esito.bloccati.forEach(function (b) { righe.push('BLOCCATO ' + b.ordine + ': ' + b.motivo); });
    esito.generati.forEach(function (g) {
      if (g.avvisi && g.avvisi.length) righe.push('DA CONTROLLARE ' + g.ordine + ' (' + g.url + '):\n  - ' + g.avvisi.join('\n  - '));
    });
    MailApp.sendEmail(email, 'Documenti export Shopify: ci sono ordini da controllare', righe.join('\n\n') +
      '\n\nRegistro: ' + registro_().getUrl());
  } else if (N.EMAIL_RIEPILOGO && esito.generati.length) {
    MailApp.sendEmail(email, 'Documenti export pronti: ' + esito.generati.length + ' ordini',
      esito.generati.map(function (g) { return g.ordine + ' (' + g.paese + ') → ' + g.url; }).join('\n'));
  }
}

// ============================================================================
//  UTILITÀ
// ============================================================================

function soldi_(set) {
  if (!set || !set.shopMoney) return { importo: null, valuta: null };
  return { importo: Number(set.shopMoney.amount), valuta: set.shopMoney.currencyCode };
}

function pesoKg_(w) {
  if (!w || w.value == null) return 0;
  var v = Number(w.value);
  switch (String(w.unit).toUpperCase()) {
    case 'GRAMS': return arrotonda_(v / 1000, 3);
    case 'POUNDS': return arrotonda_(v * 0.45359237, 3);
    case 'OUNCES': return arrotonda_(v * 0.028349523, 3);
    default: return arrotonda_(v, 3); // KILOGRAMS
  }
}

function arrotonda_(n, decimali) {
  var f = Math.pow(10, decimali == null ? 2 : decimali);
  return Math.round((Number(n) + Number.EPSILON) * f) / f;
}

function formattaData_(d) { return Utilities.formatDate(d, FUSO_ORARIO, 'dd/MM/yyyy'); }

function formattaImporto_(n) {
  var parti = arrotonda_(n).toFixed(2).split('.');
  parti[0] = parti[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  return parti.join(',');
}

function formattaPeso_(n) { return arrotonda_(n, 3).toFixed(3).replace('.', ','); }

function formattaHs_(hs) {
  hs = String(hs || '');
  if (hs.length <= 4) return hs;
  return hs.substring(0, 4) + '.' + hs.substring(4, 6) + (hs.length > 6 ? '.' + hs.substring(6) : '');
}

function nomePaese_(codice) { return NOMI_PAESI[codice] ? NOMI_PAESI[codice] + ' (' + codice + ')' : codice; }

function esc_(s) {
  return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function messaggioErrore_(e) { return e && e.message ? e.message : String(e); }

function logoDataUri_() {
  var id = CONFIG.AZIENDA.LOGO_DRIVE_FILE_ID;
  if (!id) return '';
  try {
    var blob = DriveApp.getFileById(id).getBlob();
    return 'data:' + blob.getContentType() + ';base64,' + Utilities.base64Encode(blob.getBytes());
  } catch (e) {
    Logger.log('Logo non trovato su Drive: ' + messaggioErrore_(e));
    return '';
  }
}

// ============================================================================
//  MODELLI DEI DOCUMENTI (HTML → PDF)
//  Layout a tabelle e CSS semplice: il convertitore PDF di Google supporta
//  solo un sottoinsieme di CSS (niente flexbox/grid).
// ============================================================================

var CSS_ =
  '@page { size: A4; margin: 14mm 12mm; }' +
  'body { font-family: Arial, Helvetica, sans-serif; font-size: 9.5pt; color: #1a1a1a; margin: 0; }' +
  'table { border-collapse: collapse; width: 100%; }' +
  'td, th { vertical-align: top; }' +
  '.testata td { padding: 0; }' +
  '.titolo { font-size: 17pt; font-weight: bold; color: #0f2b4c; margin: 0; }' +
  '.sottotitolo { font-size: 9pt; color: #555; margin-top: 2px; }' +
  '.box { border: 1px solid #9aa7b8; padding: 6px 8px; }' +
  '.etichetta { font-size: 7.5pt; text-transform: uppercase; color: #4a5a70; font-weight: bold; letter-spacing: .3px; }' +
  '.dati td { padding: 3px 6px; border: 1px solid #9aa7b8; font-size: 8.5pt; }' +
  '.dati td.k { background: #eef2f7; font-weight: bold; width: 34%; }' +
  '.righe th { background: #0f2b4c; color: #fff; font-size: 7.5pt; padding: 5px 4px; text-align: left; border: 1px solid #0f2b4c; }' +
  '.righe td { border: 1px solid #9aa7b8; padding: 4px; font-size: 8.5pt; }' +
  '.righe tr.alt td { background: #f6f8fb; }' +
  '.n { text-align: right; white-space: nowrap; }' +
  '.c { text-align: center; }' +
  '.piccolo { font-size: 7.5pt; color: #555; }' +
  '.totali td { padding: 3px 6px; font-size: 9pt; }' +
  '.totali tr.grande td { font-size: 11pt; font-weight: bold; border-top: 2px solid #0f2b4c; }' +
  '.clausola { border-left: 3px solid #0f2b4c; background: #f3f6fa; padding: 6px 8px; font-size: 8.5pt; margin-top: 8px; }' +
  '.testo { font-size: 10pt; line-height: 1.45; text-align: justify; }' +
  '.testo p { margin: 0 0 8px 0; }' +
  '.elenco td { padding: 4px 6px; font-size: 9.5pt; border-bottom: 1px solid #dde3ea; }' +
  '.firma { margin-top: 26px; }' +
  '.linea-firma { border-top: 1px solid #333; width: 230px; margin-top: 38px; padding-top: 3px; font-size: 8.5pt; }' +
  '.salto { page-break-before: always; }';

function pagina_(titoloDoc, corpo) {
  return '<!DOCTYPE html><html><head><meta charset="utf-8"><title>' + esc_(titoloDoc) + '</title>' +
    '<style>' + CSS_ + '</style></head><body>' + corpo + '</body></html>';
}

function testata_(doc, titolo, sottotitolo) {
  var a = doc.azienda;
  var logo = doc.logo ? '<img src="' + doc.logo + '" style="max-height:48px;max-width:170px;margin-bottom:4px;"><br>' : '';
  return '<table class="testata"><tr>' +
    '<td style="width:55%">' + logo +
    '<b style="font-size:11pt">' + esc_(a.RAGIONE_SOCIALE) + '</b><br>' +
    esc_(a.INDIRIZZO) + '<br>' + esc_(a.CAP + ' ' + a.CITTA + (a.PROVINCIA ? ' (' + a.PROVINCIA + ')' : '')) + ' – ' + esc_(a.PAESE) + '<br>' +
    '<span class="piccolo">P.IVA/VAT ' + esc_(a.PARTITA_IVA) + ' · EORI ' + esc_(a.EORI) +
    (a.REX ? ' · REX ' + esc_(a.REX) : '') + '<br>' +
    esc_([a.TELEFONO, a.EMAIL, a.SITO].filter(Boolean).join(' · ')) + '</span>' +
    '</td>' +
    '<td style="width:45%;text-align:right">' +
    '<div class="titolo">' + titolo + '</div>' +
    '<div class="sottotitolo">' + sottotitolo + '</div>' +
    '</td></tr></table><div style="height:10px"></div>';
}

function bloccoIndirizzo_(etichetta, ind, conContatti) {
  if (!ind) return '<div class="box"><div class="etichetta">' + etichetta + '</div>—</div>';
  var righe = [
    '<b>' + esc_(ind.nome) + '</b>',
    ind.azienda ? esc_(ind.azienda) : '',
    esc_(ind.riga1),
    ind.riga2 ? esc_(ind.riga2) : '',
    esc_([ind.cap, ind.citta, ind.provincia].filter(Boolean).join(' ')),
    '<b>' + esc_(nomePaese_(ind.codicePaese)) + '</b>'
  ];
  if (conContatti) {
    righe.push('<span class="piccolo">Tel: ' + esc_(ind.telefono || '—') + (ind.email ? ' · ' + esc_(ind.email) : '') + '</span>');
  }
  return '<div class="box"><div class="etichetta">' + etichetta + '</div>' +
    righe.filter(Boolean).join('<br>') + '</div>';
}

function firma_(doc, etichetta) {
  var a = doc.azienda;
  return '<table class="firma"><tr>' +
    '<td style="width:50%">' + esc_(a.LUOGO_FIRMA || a.CITTA) + ', ' + formattaData_(doc.data) + '</td>' +
    '<td style="width:50%;text-align:right">' +
    '<div style="display:inline-block;text-align:left">' +
    '<div class="piccolo">' + (etichetta || 'Timbro e firma / Stamp and signature') + '</div>' +
    '<div class="linea-firma">' + esc_(a.FIRMATARIO_NOME) + ' – ' + esc_(a.FIRMATARIO_RUOLO) + '<br>' +
    esc_(a.RAGIONE_SOCIALE) + '</div></div>' +
    '</td></tr></table>';
}

function riferimenti_(doc) {
  var o = doc.ordine;
  return '<table class="dati">' +
    '<tr><td class="k">Fattura comm. / Commercial invoice n.</td><td>' + esc_(doc.numero) + ' del ' + formattaData_(doc.data) + '</td></tr>' +
    '<tr><td class="k">Ordine / Order</td><td>' + esc_(o.nome) + ' del ' + formattaData_(o.dataOrdine) + '</td></tr>' +
    '<tr><td class="k">Destinatario / Consignee</td><td>' + esc_(o.spedizione.nome) + ' – ' + esc_(nomePaese_(o.spedizione.codicePaese)) + '</td></tr>' +
    '</table>';
}

function descrizioneRiga_(r) {
  return '<b>' + esc_(r.descrizioneDoganale) + '</b>' +
    (r.composizione ? '<br>' + esc_(r.composizione) : '') +
    '<br><span class="piccolo">' + esc_(r.titolo) + (r.sku ? ' · SKU ' + esc_(r.sku) : '') + '</span>';
}

function originiUe_(o) {
  return o.righe.every(function (r) { return PAESI_UE.indexOf(r.origine) !== -1; });
}

/** Testo standard della dichiarazione di origine su fattura (Allegato 22-07 Reg. UE 2015/2447). */
function testoOriginePreferenziale_(doc) {
  var a = doc.azienda;
  return 'The exporter of the products covered by this document (Customs Authorisation or REX No. ' +
    (a.REX ? esc_(a.REX) : '……………') + ') declares that, except where otherwise clearly indicated, ' +
    'these products are of EU preferential origin.<br>' +
    '<span class="piccolo">L\'esportatore delle merci contemplate nel presente documento dichiara che, salvo indicazione ' +
    'contraria, le merci sono di origine preferenziale UE.</span><br>' +
    esc_(a.LUOGO_FIRMA || a.CITTA) + ', ' + formattaData_(doc.data) + ' – ' + esc_(a.FIRMATARIO_NOME);
}

// ---------------------------------------------------------------------------
//  1. FATTURA COMMERCIALE
// ---------------------------------------------------------------------------
function htmlFatturaCommerciale_(doc) {
  var copie = Math.max(1, Number(CONFIG.SPEDIZIONE.COPIE_FATTURA) || 1);
  var corpo = '';
  for (var i = 0; i < copie; i++) {
    corpo += (i > 0 ? '<div class="salto"></div>' : '') + corpoFattura_(doc, i + 1, copie);
  }
  return pagina_('Commercial Invoice ' + doc.numero, corpo);
}

function corpoFattura_(doc, copia, totaleCopie) {
  var o = doc.ordine;
  var S = CONFIG.SPEDIZIONE;
  var v = esc_(o.valuta);

  var righe = o.righe.map(function (r, i) {
    return '<tr' + (i % 2 ? ' class="alt"' : '') + '>' +
      '<td class="c">' + (i + 1) + '</td>' +
      '<td>' + descrizioneRiga_(r) + '</td>' +
      '<td class="c">' + esc_(formattaHs_(r.hs)) + '</td>' +
      '<td class="c">' + esc_(r.origine) + '</td>' +
      '<td class="n">' + r.quantita + '</td>' +
      '<td class="n">' + formattaPeso_(r.pesoTotale) + '</td>' +
      '<td class="n">' + formattaImporto_(r.prezzoUnitario) + '</td>' +
      '<td class="n">' + formattaImporto_(r.totale) + '</td>' +
      '</tr>';
  }).join('');

  var origine = CONFIG.ORIGINE_PREFERENZIALE && originiUe_(o)
    ? '<div class="clausola"><div class="etichetta">Dichiarazione di origine / Origin declaration</div>' + testoOriginePreferenziale_(doc) + '</div>'
    : '';

  return testata_(doc, 'COMMERCIAL INVOICE',
      'Fattura commerciale' + (totaleCopie > 1 ? ' · copia ' + copia + '/' + totaleCopie : '') + '<br>' +
      '<b style="font-size:11pt;color:#1a1a1a">N. ' + esc_(doc.numero) + '</b><br>' +
      'Data / Date: ' + formattaData_(doc.data)) +

    '<table><tr>' +
    '<td style="width:50%;padding-right:5px">' + bloccoIndirizzo_('Destinatario / Consignee (Ship to)', o.spedizione, true) + '</td>' +
    '<td style="width:50%;padding-left:5px">' + bloccoIndirizzo_('Acquirente / Buyer (Bill to)', o.fatturazione, false) + '</td>' +
    '</tr></table><div style="height:8px"></div>' +

    '<table><tr><td style="width:50%;padding-right:5px"><table class="dati">' +
    '<tr><td class="k">Ordine / Order no.</td><td>' + esc_(o.nome) + ' (' + formattaData_(o.dataOrdine) + ')</td></tr>' +
    '<tr><td class="k">Motivo / Reason for export</td><td>' + esc_(S.MOTIVO_EXPORT) + '</td></tr>' +
    '<tr><td class="k">Incoterms® 2020</td><td>' + esc_(S.INCOTERM) + ' ' + esc_(o.spedizione.citta) + '</td></tr>' +
    '<tr><td class="k">Pagamento / Payment</td><td>Prepagato / Prepaid</td></tr>' +
    '</table></td><td style="width:50%;padding-left:5px"><table class="dati">' +
    '<tr><td class="k">Corriere / Carrier</td><td>' + esc_(S.CORRIERE) + '</td></tr>' +
    '<tr><td class="k">AWB / Tracking no.</td><td>&nbsp;</td></tr>' +
    '<tr><td class="k">Paese di destinazione</td><td>' + esc_(nomePaese_(o.spedizione.codicePaese)) + '</td></tr>' +
    '<tr><td class="k">Valuta / Currency</td><td>' + v + '</td></tr>' +
    '</table></td></tr></table><div style="height:10px"></div>' +

    '<table class="righe"><tr>' +
    '<th class="c" style="width:4%">#</th>' +
    '<th style="width:38%">Descrizione merce / Description of goods</th>' +
    '<th class="c" style="width:11%">HS code</th>' +
    '<th class="c" style="width:7%">Origine Origin</th>' +
    '<th class="n" style="width:6%">Q.tà Qty</th>' +
    '<th class="n" style="width:10%">Peso netto kg Net wt.</th>' +
    '<th class="n" style="width:11%">Prezzo unit. Unit value (' + v + ')</th>' +
    '<th class="n" style="width:13%">Totale Total (' + v + ')</th>' +
    '</tr>' + righe + '</table>' +

    '<table style="margin-top:8px"><tr>' +
    '<td style="width:55%;padding-right:10px"><table class="dati">' +
    '<tr><td class="k">N. colli / Packages</td><td>' + (S.NUMERO_COLLI || 1) + '</td></tr>' +
    '<tr><td class="k">N. pezzi / Total units</td><td>' + o.pezzi + '</td></tr>' +
    '<tr><td class="k">Peso netto / Net weight</td><td>' + formattaPeso_(o.pesoNetto) + ' kg</td></tr>' +
    '<tr><td class="k">Peso lordo / Gross weight</td><td>' + formattaPeso_(o.pesoLordo) + ' kg</td></tr>' +
    '</table></td>' +
    '<td style="width:45%"><table class="totali">' +
    '<tr><td>Valore merce / Goods value</td><td class="n">' + formattaImporto_(o.totaleMerce) + ' ' + v + '</td></tr>' +
    '<tr><td>Trasporto / Freight</td><td class="n">' + formattaImporto_(o.costoSpedizione) + ' ' + v + '</td></tr>' +
    '<tr><td>IVA / VAT</td><td class="n">0,00 ' + v + '</td></tr>' +
    '<tr class="grande"><td>TOTALE / TOTAL</td><td class="n">' + formattaImporto_(o.totale) + ' ' + v + '</td></tr>' +
    '</table></td></tr></table>' +

    '<div class="clausola"><b>IVA / VAT:</b> ' + esc_(CONFIG.FATTURA.CLAUSOLA_IVA) + '</div>' +
    origine +
    '<div class="clausola">I hereby certify that the information on this invoice is true and correct and that the contents ' +
    'of this shipment are as stated above.<br><span class="piccolo">Si dichiara che le informazioni riportate nella presente ' +
    'fattura sono veritiere e corrette e che il contenuto della spedizione corrisponde a quanto indicato.</span></div>' +
    (CONFIG.FATTURA.NOTE ? '<div class="piccolo" style="margin-top:6px">' + esc_(CONFIG.FATTURA.NOTE) + '</div>' : '') +
    '<div class="piccolo" style="margin-top:6px">Documento commerciale per la spedizione e lo sdoganamento. ' +
    'Commercial document for shipping and customs clearance purposes.</div>' +
    firma_(doc);
}

// ---------------------------------------------------------------------------
//  2. DICHIARAZIONE DI ORIGINE DELLA MERCE
// ---------------------------------------------------------------------------
function htmlDichiarazioneOrigine_(doc) {
  var o = doc.ordine;
  var a = doc.azienda;

  var righe = o.righe.map(function (r, i) {
    return '<tr' + (i % 2 ? ' class="alt"' : '') + '>' +
      '<td class="c">' + (i + 1) + '</td><td>' + descrizioneRiga_(r) + '</td>' +
      '<td class="c">' + esc_(formattaHs_(r.hs)) + '</td><td class="n">' + r.quantita + '</td>' +
      '<td><b>' + esc_(nomePaese_(r.origine)) + '</b></td></tr>';
  }).join('');

  var paesi = {};
  o.righe.forEach(function (r) { paesi[r.origine] = true; });
  var elencoPaesi = Object.keys(paesi).map(nomePaese_).join(', ');

  var preferenziale = '';
  if (CONFIG.ORIGINE_PREFERENZIALE) {
    preferenziale = originiUe_(o)
      ? '<div class="clausola"><div class="etichetta">Origine preferenziale / Preferential origin</div>' + testoOriginePreferenziale_(doc) + '</div>'
      : '<div class="clausola">Non tutte le merci sono di origine UE: la dichiarazione di origine preferenziale non è applicabile. ' +
        '<span class="piccolo">Not all goods are of EU origin: preferential origin statement not applicable.</span></div>';
  }

  var corpo = testata_(doc, 'DICHIARAZIONE DI ORIGINE', 'Declaration of origin of goods<br>' +
      'Rif. / Ref.: ' + esc_(doc.numero)) +
    riferimenti_(doc) + '<div style="height:12px"></div>' +
    '<div class="testo">' +
    '<p>Il/La sottoscritto/a <b>' + esc_(a.FIRMATARIO_NOME) + '</b>, in qualità di ' + esc_(a.FIRMATARIO_RUOLO) +
    ' della società <b>' + esc_(a.RAGIONE_SOCIALE) + '</b>, con sede in ' + esc_(a.INDIRIZZO + ', ' + a.CAP + ' ' + a.CITTA) +
    ', P.IVA ' + esc_(a.PARTITA_IVA) + ', EORI ' + esc_(a.EORI) + ',</p>' +
    '<p style="text-align:center"><b>DICHIARA</b></p>' +
    '<p>sotto la propria responsabilità che le merci di seguito elencate, oggetto della fattura commerciale n. <b>' +
    esc_(doc.numero) + '</b> del ' + formattaData_(doc.data) + ' e spedite a ' + esc_(o.spedizione.nome) + ' (' +
    esc_(nomePaese_(o.spedizione.codicePaese)) + '), sono originarie di: <b>' + esc_(elencoPaesi) + '</b>, ' +
    'ai sensi delle norme sull\'origine non preferenziale di cui agli artt. 59-63 del Reg. (UE) n. 952/2013 ' +
    '(Codice Doganale dell\'Unione).</p>' +
    '<p class="piccolo">The undersigned, acting on behalf of the exporter named above, hereby declares that the goods listed ' +
    'below, covered by commercial invoice no. ' + esc_(doc.numero) + ', originate in: ' + esc_(elencoPaesi) +
    ', in accordance with the non-preferential rules of origin of Articles 59-63 of Regulation (EU) No 952/2013 (Union Customs Code).</p>' +
    '</div>' +
    '<table class="righe" style="margin-top:6px"><tr>' +
    '<th class="c" style="width:5%">#</th><th style="width:50%">Merce / Goods</th><th class="c" style="width:13%">HS code</th>' +
    '<th class="n" style="width:8%">Q.tà Qty</th><th style="width:24%">Paese di origine / Country of origin</th></tr>' +
    righe + '</table>' +
    preferenziale +
    '<div class="testo" style="margin-top:10px"><p class="piccolo">Il dichiarante si impegna a fornire, su richiesta delle ' +
    'autorità doganali, la documentazione a supporto della presente dichiarazione. / The declarant undertakes to provide, at the ' +
    'request of the customs authorities, any supporting documentation for this declaration.</p></div>' +
    firma_(doc);
  return pagina_('Dichiarazione di origine ' + doc.numero, corpo);
}

// ---------------------------------------------------------------------------
//  3. DICHIARAZIONE DI CONFORMITÀ DEL PRODOTTO (abbigliamento – cappelli)
// ---------------------------------------------------------------------------
function htmlDichiarazioneConformita_(doc) {
  var o = doc.ordine;
  var a = doc.azienda;

  var prodotti = o.righe.map(function (r, i) {
    return '<tr' + (i % 2 ? ' class="alt"' : '') + '><td class="c">' + (i + 1) + '</td><td>' + descrizioneRiga_(r) + '</td>' +
      '<td class="c">' + esc_(formattaHs_(r.hs)) + '</td><td>' + esc_(r.composizione || '—') + '</td>' +
      '<td class="n">' + r.quantita + '</td></tr>';
  }).join('');

  var norme = [
    ['Reg. (UE) 2023/988', 'Sicurezza generale dei prodotti (GPSR) / General Product Safety Regulation'],
    ['Reg. (UE) n. 1007/2011', 'Denominazione delle fibre tessili ed etichettatura della composizione / Textile fibre names and labelling'],
    ['Reg. (CE) n. 1907/2006 (REACH)', 'Restrizioni dell\'Allegato XVII (es. coloranti azoici, nichel, formaldeide, ftalati, PFAS soggetti a restrizione); ' +
      'nessuna sostanza SVHC della Candidate List in concentrazione > 0,1% p/p / REACH Annex XVII restrictions; no SVHC above 0.1% w/w'],
    ['Reg. (UE) 2019/1021', 'Inquinanti organici persistenti (POP) / Persistent organic pollutants'],
    ['D.Lgs. 206/2005', 'Codice del Consumo – informazioni al consumatore / Italian Consumer Code']
  ];
  var elencoNorme = norme.map(function (n) {
    return '<tr><td style="width:32%"><b>' + esc_(n[0]) + '</b></td><td>' + esc_(n[1]) + '</td></tr>';
  }).join('');

  var corpo = testata_(doc, 'DICHIARAZIONE DI CONFORMITÀ', 'Product declaration of conformity<br>' +
      'Rif. / Ref.: ' + esc_(doc.numero)) +
    riferimenti_(doc) + '<div style="height:12px"></div>' +
    '<div class="testo">' +
    '<p>Il/La sottoscritto/a <b>' + esc_(a.FIRMATARIO_NOME) + '</b>, in qualità di ' + esc_(a.FIRMATARIO_RUOLO) +
    ' della società <b>' + esc_(a.RAGIONE_SOCIALE) + '</b> (P.IVA ' + esc_(a.PARTITA_IVA) + '), in qualità di fabbricante/fornitore, ' +
    'dichiara sotto la propria esclusiva responsabilità che i prodotti di seguito elencati:</p>' +
    '</div>' +
    '<table class="righe"><tr><th class="c" style="width:5%">#</th><th style="width:45%">Prodotto / Product</th>' +
    '<th class="c" style="width:12%">HS code</th><th style="width:28%">Composizione / Composition</th>' +
    '<th class="n" style="width:10%">Q.tà Qty</th></tr>' + prodotti + '</table>' +
    '<div class="testo" style="margin-top:10px">' +
    '<p>sono conformi ai requisiti della seguente normativa dell\'Unione Europea e nazionale applicabile agli articoli di abbigliamento e accessori tessili:</p>' +
    '</div>' +
    '<table class="elenco">' + elencoNorme + '</table>' +
    '<div class="testo" style="margin-top:10px">' +
    '<p>Si dichiara inoltre che:</p>' +
    '<p>• i prodotti sono accessori di abbigliamento (cappelli) per uso civile e <b>non sono dispositivi di protezione individuale</b> ' +
    'ai sensi del Reg. (UE) 2016/425, pertanto non sono soggetti a marcatura CE;<br>' +
    '• i prodotti sono etichettati con l\'indicazione della composizione fibrosa ai sensi del Reg. (UE) n. 1007/2011 e con le ' +
    'informazioni di identificazione e tracciabilità del fabbricante previste dal Reg. (UE) 2023/988;<br>' +
    '• i prodotti non contengono materiali di origine animale appartenenti a specie protette dalla Convenzione CITES (Reg. CE 338/97).</p>' +
    '<p class="piccolo">The undersigned declares under sole responsibility that the products listed above comply with the EU legislation ' +
    'listed above applicable to textile apparel and accessories. The products are fashion headwear for civil use and are not personal ' +
    'protective equipment under Regulation (EU) 2016/425, therefore no CE marking applies. The products are labelled with their fibre ' +
    'composition and do not contain materials from CITES-protected species.</p>' +
    '</div>' +
    firma_(doc);
  return pagina_('Dichiarazione di conformità ' + doc.numero, corpo);
}

// ---------------------------------------------------------------------------
//  4. DICHIARAZIONE DI LIBERA ESPORTAZIONE
// ---------------------------------------------------------------------------
function htmlLiberaEsportazione_(doc) {
  var o = doc.ordine;
  var a = doc.azienda;

  var hsUnici = {};
  o.righe.forEach(function (r) { hsUnici[formattaHs_(r.hs)] = true; });

  var punti = [
    ['non rientrano tra i <b>prodotti a duplice uso</b> elencati nell\'Allegato I del Reg. (UE) 2021/821 e successive modifiche;',
      'are not dual-use items listed in Annex I to Regulation (EU) 2021/821, as amended;'],
    ['non sono soggette a divieti o autorizzazioni previsti dai regolamenti UE concernenti <b>misure restrittive (sanzioni)</b>, ' +
      'in particolare il Reg. (UE) n. 833/2014 e il Reg. (UE) n. 269/2014 (Russia) e il Reg. (CE) n. 765/2006 (Bielorussia), ' +
      'e che il destinatario non è una persona o entità designata;',
      'are not subject to prohibitions or authorisations under EU restrictive measures (sanctions), in particular Regulations ' +
      '(EU) No 833/2014 and No 269/2014 (Russia) and (EC) No 765/2006 (Belarus), and the consignee is not a designated person or entity;'],
    ['non sono <b>materiali d\'armamento</b> ai sensi della Legge 9 luglio 1990 n. 185, né armi da fuoco ai sensi del Reg. (UE) n. 258/2012;',
      'are not military equipment under Italian Law 185/1990, nor firearms under Regulation (EU) No 258/2012;'],
    ['non rientrano tra le merci di cui al Reg. (UE) 2019/125 (<b>beni utilizzabili per la pena di morte o la tortura</b>);',
      'are not goods covered by Regulation (EU) 2019/125 (goods which could be used for capital punishment or torture);'],
    ['non sono <b>beni culturali</b> ai sensi del Reg. (CE) n. 116/2009 e del D.Lgs. 42/2004;',
      'are not cultural goods under Regulation (EC) No 116/2009 and Italian Legislative Decree 42/2004;'],
    ['non contengono esemplari o parti di <b>specie protette CITES</b> (Reg. CE n. 338/97);',
      'do not contain specimens or parts of CITES-protected species (Regulation (EC) No 338/97);'],
    ['non sono soggette a <b>licenza di esportazione</b> e sono pertanto <b>liberamente esportabili</b>.',
      'are not subject to export licensing and may therefore be freely exported.']
  ];
  var elenco = punti.map(function (p, i) {
    return '<tr><td style="width:4%"><b>' + String.fromCharCode(97 + i) + ')</b></td><td>' + p[0] +
      '<br><span class="piccolo">' + p[1] + '</span></td></tr>';
  }).join('');

  var corpo = testata_(doc, 'DICHIARAZIONE DI LIBERA ESPORTAZIONE', 'Free export declaration<br>' +
      'Rif. / Ref.: ' + esc_(doc.numero)) +
    '<table class="dati">' +
    '<tr><td class="k">Esportatore / Exporter</td><td>' + esc_(a.RAGIONE_SOCIALE) + ' – P.IVA ' + esc_(a.PARTITA_IVA) + ' – EORI ' + esc_(a.EORI) + '</td></tr>' +
    '<tr><td class="k">Destinatario / Consignee</td><td>' + esc_(o.spedizione.nome) + ', ' +
    esc_([o.spedizione.riga1, o.spedizione.cap, o.spedizione.citta].filter(Boolean).join(' ')) + ' – ' + esc_(nomePaese_(o.spedizione.codicePaese)) + '</td></tr>' +
    '<tr><td class="k">Fattura comm. / Commercial invoice</td><td>' + esc_(doc.numero) + ' del ' + formattaData_(doc.data) + ' – ordine ' + esc_(o.nome) + '</td></tr>' +
    '<tr><td class="k">Merce / Goods</td><td>Cappelli e copricapi (abbigliamento) / Hats and headwear (apparel) – HS ' +
    esc_(Object.keys(hsUnici).join(', ')) + '</td></tr>' +
    '<tr><td class="k">Colli · Pezzi · Peso lordo</td><td>' + (CONFIG.SPEDIZIONE.NUMERO_COLLI || 1) + ' · ' + o.pezzi + ' · ' + formattaPeso_(o.pesoLordo) + ' kg</td></tr>' +
    '<tr><td class="k">Valore / Value</td><td>' + formattaImporto_(o.totaleMerce) + ' ' + esc_(o.valuta) + '</td></tr>' +
    '<tr><td class="k">Corriere / Carrier</td><td>' + esc_(CONFIG.SPEDIZIONE.CORRIERE) + '</td></tr>' +
    '</table><div style="height:12px"></div>' +
    '<div class="testo">' +
    '<p>Il/La sottoscritto/a <b>' + esc_(a.FIRMATARIO_NOME) + '</b>, in qualità di ' + esc_(a.FIRMATARIO_RUOLO) +
    ' della società esportatrice sopra indicata, consapevole delle responsabilità previste dalla normativa doganale, ' +
    '<b>DICHIARA</b> che le merci sopra descritte:</p>' +
    '<p class="piccolo">The undersigned, on behalf of the exporter named above, aware of the responsibilities under customs law, ' +
    'DECLARES that the goods described above:</p>' +
    '</div>' +
    '<table class="elenco">' + elenco + '</table>' +
    '<div class="testo" style="margin-top:10px"><p>Si dichiara infine che le merci sono destinate a uso civile e personale ' +
    'del destinatario finale e che non saranno riesportate verso Paesi soggetti a embargo.<br>' +
    '<span class="piccolo">The goods are intended for civil and personal use by the final consignee and will not be re-exported ' +
    'to embargoed countries.</span></p></div>' +
    firma_(doc);
  return pagina_('Dichiarazione di libera esportazione ' + doc.numero, corpo);
}
