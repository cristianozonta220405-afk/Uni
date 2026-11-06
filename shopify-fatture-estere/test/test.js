/**
 * Test locale: esegue Codice.gs in Node simulando i servizi Google Apps Script
 * (Drive, Fogli, UrlFetch verso Shopify…) con gli ordini di ordini-esempio.json.
 *
 *   node test/test.js              → esegue i test
 *   node test/test.js --anteprime  → salva anche l'HTML dei documenti in test/anteprime/
 */
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');

const ROOT = path.join(__dirname, '..');
const ordiniEsempio = JSON.parse(fs.readFileSync(path.join(__dirname, 'ordini-esempio.json'), 'utf8'));
const salvaAnteprime = process.argv.includes('--anteprime');

// ---------------------------------------------------------------------------
//  Mock dei servizi Google
// ---------------------------------------------------------------------------
function creaAmbiente() {
  const props = {};
  const log = [];
  const richieste = [];
  const tagAggiunti = [];
  const email = [];
  let idSeq = 0;
  const nuovoId = () => 'id' + (++idSeq);

  function iteratore(arr) {
    let i = 0;
    return { hasNext: () => i < arr.length, next: () => arr[i++] };
  }

  const tuttiFile = {};
  function Cartella(nome, padre) {
    this.id = nuovoId(); this.nome = nome; this.padre = padre; this.cartelle = []; this.file = [];
  }
  Cartella.prototype = {
    getId() { return this.id; },
    getName() { return this.nome; },
    getUrl() { return 'https://drive.google.com/drive/folders/' + this.id; },
    getFoldersByName(n) { return iteratore(this.cartelle.filter(c => c.nome === n)); },
    getFilesByName(n) { return iteratore(this.file.filter(f => f.nome === n && !f.cestino)); },
    createFolder(n) { const c = new Cartella(n, this); this.cartelle.push(c); tutteCartelle[c.id] = c; return c; },
    createFile(blob) {
      const f = { id: nuovoId(), nome: blob.getName(), blob, cestino: false,
        getId() { return this.id; }, getName() { return this.nome; }, setTrashed(v) { this.cestino = v; },
        moveTo(c) { c.file.push(this); } };
      this.file.push(f); tuttiFile[f.id] = f; return f;
    },
    percorso() { return (this.padre ? this.padre.percorso() + '/' : '') + this.nome; }
  };
  const root = new Cartella('Il mio Drive', null);
  const tutteCartelle = { [root.id]: root };

  const fogli = {};
  function Foglio(nome) { this.nome = nome; this.righe = []; }
  Foglio.prototype = {
    setName(n) { this.nome = n; return this; },
    appendRow(r) { this.righe.push(r.slice()); return this; },
    getLastRow() { return this.righe.length; },
    getRange(r, c, nr, nc) {
      const self = this;
      nr = nr || 1; nc = nc || 1;
      return {
        getValues() {
          const out = [];
          for (let i = 0; i < nr; i++) { const riga = self.righe[r - 1 + i] || []; out.push(riga.slice(c - 1, c - 1 + nc)); }
          return out;
        },
        setValues(v) { v.forEach((riga, i) => { const t = self.righe[r - 1 + i]; riga.forEach((x, j) => { t[c - 1 + j] = x; }); }); return this; },
        setFontWeight() { return this; }, setBackground() { return this; }
      };
    },
    setFrozenRows() { return this; }
  };
  function Spreadsheet(nome) { this.id = nuovoId(); this.nome = nome; this.sheets = [new Foglio('Foglio1')]; }
  Spreadsheet.prototype = {
    getId() { return this.id; },
    getUrl() { return 'https://docs.google.com/spreadsheets/d/' + this.id; },
    getSheets() { return this.sheets; },
    getSheetByName(n) { return this.sheets.find(s => s.nome === n) || null; },
    insertSheet(n) { const s = new Foglio(n); this.sheets.push(s); return s; }
  };

  function blob(contenuto, tipo, nome) {
    return {
      contenuto, tipo, nome,
      getName() { return this.nome; }, setName(n) { this.nome = n; return this; },
      getAs(t) { return blob(this.contenuto, t, this.nome); },
      getContentType() { return this.tipo; }, getBytes() { return Buffer.from(this.contenuto); }
    };
  }

  function formatDate(d, tz, fmt) {
    const p = Object.fromEntries(new Intl.DateTimeFormat('en-GB', { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit' })
      .formatToParts(d).map(x => [x.type, x.value]));
    return fmt.replace('yyyy', p.year).replace('MM', p.month).replace('dd', p.day);
  }

  function rispostaShopify(payload) {
    const { query, variables } = JSON.parse(payload);
    richieste.push({ query, variables });
    if (query.includes('shop {')) return { data: { shop: { name: 'Negozio Test', myshopifyDomain: 'test.myshopify.com', currencyCode: 'EUR' } } };
    if (query.includes('tagsAdd')) { tagAggiunti.push(variables.id); return { data: { tagsAdd: { userErrors: [] } } }; }
    if (query.includes('orders(')) {
      let lista = ordiniEsempio;
      const m = /name:'(#\d+)'/.exec(variables.q);
      if (m) lista = lista.filter(o => o.name === m[1]);
      // paginazione: 2 ordini per pagina per esercitare il cursore
      const inizio = variables.cursor ? Number(variables.cursor) : 0;
      const pagina = lista.slice(inizio, inizio + 2);
      const prossimo = inizio + 2 < lista.length;
      return { data: { orders: { nodes: pagina, pageInfo: { hasNextPage: prossimo, endCursor: prossimo ? String(inizio + 2) : null } } } };
    }
    throw new Error('Query inattesa');
  }

  const ctx = {
    console,
    PropertiesService: { getScriptProperties: () => ({
      getProperty: k => (k in props ? props[k] : null), setProperty: (k, v) => { props[k] = String(v); } }) },
    Logger: { log: (...a) => log.push(a.join(' ')) },
    LockService: { getScriptLock: () => ({ tryLock: () => true, releaseLock() {} }) },
    Utilities: {
      formatDate, sleep() {}, base64Encode: b => Buffer.from(b).toString('base64'),
      newBlob: (c, t, n) => blob(c, t, n)
    },
    UrlFetchApp: {
      fetch(url, opz) {
        if (url.includes('/oauth/access_token')) {
          return { getResponseCode: () => 200, getContentText: () => JSON.stringify({ access_token: 'tok-123', expires_in: 86399 }) };
        }
        assert.ok(url.startsWith('https://test.myshopify.com/admin/api/'), 'URL Shopify: ' + url);
        assert.strictEqual(opz.headers['X-Shopify-Access-Token'], 'tok-123');
        const r = rispostaShopify(opz.payload);
        return { getResponseCode: () => 200, getContentText: () => JSON.stringify(r) };
      }
    },
    DriveApp: {
      getRootFolder: () => root,
      getFolderById: id => { if (!tutteCartelle[id]) throw new Error('non trovata'); return tutteCartelle[id]; },
      getFileById: id => {
        if (fogli[id]) return { moveTo(c) { c.file.push({ nome: fogli[id].nome, cestino: false, getId: () => id }); } };
        if (tuttiFile[id]) return tuttiFile[id];
        throw new Error('file non trovato');
      }
    },
    SpreadsheetApp: {
      create: n => { const s = new Spreadsheet(n); fogli[s.id] = s; return s; },
      openById: id => { if (!fogli[id]) throw new Error('non trovato'); return fogli[id]; }
    },
    ScriptApp: {
      _trigger: [],
      getProjectTriggers() { return this._trigger; },
      deleteTrigger(t) { this._trigger = this._trigger.filter(x => x !== t); },
      newTrigger(fn) {
        const self = this;
        return { timeBased: () => ({ everyMinutes: m => ({ create() { const t = { fn, m, getHandlerFunction: () => fn }; self._trigger.push(t); return t; } }) }) };
      }
    },
    MailApp: { sendEmail: (a, o, c) => email.push({ a, o, c }) },
    Session: { getEffectiveUser: () => ({ getEmail: () => 'titolare@example.com' }) }
  };
  vm.createContext(ctx);
  for (const f of ['Configurazione.gs', 'Codice.gs']) {
    vm.runInContext(fs.readFileSync(path.join(ROOT, 'apps-script', f), 'utf8'), ctx, { filename: f });
  }
  props.SHOPIFY_NEGOZIO = 'https://test.myshopify.com/';
  props.SHOPIFY_CLIENT_ID = 'cid';
  props.SHOPIFY_CLIENT_SECRET = 'secret';
  return { ctx, props, log, richieste, tagAggiunti, email, root, fogli, tutteCartelle };
}

// ---------------------------------------------------------------------------
//  Test
// ---------------------------------------------------------------------------
let ok = 0;
const piatto = x => JSON.parse(JSON.stringify(x));
function test(nome, fn) {
  try { fn(); ok++; console.log('  ✓ ' + nome); } catch (e) { console.error('  ✗ ' + nome + '\n    ' + e.stack); process.exitCode = 1; }
}

console.log('Filtro UE / extra-UE');
test('paesi UE, extra-UE e territori speciali', () => {
  const { ctx } = creaAmbiente();
  const f = ind => ctx.isExtraUe_(ind);
  assert.strictEqual(f({ codicePaese: 'DE' }), false);
  assert.strictEqual(f({ codicePaese: 'IT', cap: '20100' }), false);
  assert.strictEqual(f({ codicePaese: 'MC' }), false);
  assert.strictEqual(f({ codicePaese: 'US' }), true);
  assert.strictEqual(f({ codicePaese: 'GB' }), true);
  assert.strictEqual(f({ codicePaese: 'CH' }), true);
  assert.strictEqual(f({ codicePaese: 'NO' }), true);
  assert.strictEqual(f({ codicePaese: 'ES', codiceProvincia: 'GC' }), true);
  assert.strictEqual(f({ codicePaese: 'ES', codiceProvincia: 'M' }), false);
  assert.strictEqual(f({ codicePaese: 'IT', cap: '23041' }), true);
});

console.log('Normalizzazione ordine');
test('righe, prezzi scontati, pesi, valori di riserva', () => {
  const { ctx } = creaAmbiente();
  const o = ctx.normalizzaOrdine_(ordiniEsempio[0]);
  assert.strictEqual(o.righe.length, 2, 'la gift card non va in fattura');
  const [fedora, baseball] = o.righe;
  assert.strictEqual(fedora.prezzoUnitario, 71.1);
  assert.strictEqual(fedora.pesoUnitario, 0.18);
  assert.strictEqual(fedora.hs, '65050010');
  assert.strictEqual(baseball.hs, '650500');            // default
  assert.strictEqual(baseball.origine, 'IT');           // default
  assert.strictEqual(baseball.pesoUnitario, 0.15);      // default
  assert.strictEqual(baseball.totale, 42.9);
  assert.strictEqual(o.totaleMerce, 114);
  assert.strictEqual(o.costoSpedizione, 25);
  assert.strictEqual(o.totale, 139);
  assert.strictEqual(o.pezzi, 3);
  assert.strictEqual(o.pesoNetto, 0.48);
  assert.strictEqual(o.pesoLordo, 0.78);
  assert.strictEqual(o.avvisi.length, 3);
  const ch = ctx.normalizzaOrdine_(ordiniEsempio[4]);
  assert.strictEqual(ch.righe[0].hs, '65050030');
  assert.strictEqual(ch.righe[0].pesoUnitario, 0.113);  // 4 once
  assert.strictEqual(ch.totaleMerce, 1234.5);
});

console.log('Flusso completo');
let amb;
test('setup crea cartella, registro e trigger', () => {
  amb = creaAmbiente();
  amb.ctx.setup();
  const cartella = amb.root.cartelle.find(c => c.nome === 'Fatture Estere');
  assert.ok(cartella, 'cartella Fatture Estere creata');
  assert.ok(cartella.file.some(f => f.nome === 'Registro Fatture Estere'), 'registro nella cartella');
  assert.strictEqual(amb.ctx.ScriptApp._trigger.length, 1);
  assert.strictEqual(amb.ctx.ScriptApp._trigger[0].m, 15);
  amb.props.ULTIMO_CONTROLLO = '2026-11-01T00:00:00.000Z';
});

test('processaNuoviOrdini genera i documenti solo per gli extra-UE', () => {
  const esito = amb.ctx.processaNuoviOrdini();
  assert.deepStrictEqual(piatto(esito.generati.map(g => g.ordine)), ['#1001', '#1003', '#1005']);
  assert.strictEqual(esito.saltatiUe, 1);
  assert.deepStrictEqual(piatto(esito.bloccati.map(b => b.ordine)), ['#1004']);
  assert.strictEqual(esito.errori.length, 0);

  const q = amb.richieste.find(r => r.query.includes('orders(')).variables.q;
  assert.ok(q.includes("updated_at:>='2026-10-31T23:50:00.000Z'"), q);
  assert.ok(q.includes('financial_status:paid'));
  assert.ok(q.includes('-tag:"documenti-export-ok"'));

  const anno = amb.root.cartelle.find(c => c.nome === 'Fatture Estere').cartelle.find(c => c.nome === '2026');
  const nomi = anno.cartelle.map(c => c.nome);
  assert.deepStrictEqual(piatto(nomi), ['#1001 – John Smith (US)', '#1003 – Luis García (ES)', '#1005 – Sophie Keller (CH)']);
  const pdf = anno.cartelle[0].file.map(f => f.nome);
  assert.deepStrictEqual(piatto(pdf), [
    'CI-2026-0001_1001_1_Fattura_Commerciale.pdf',
    'CI-2026-0001_1001_2_Dichiarazione_Origine.pdf',
    'CI-2026-0001_1001_3_Dichiarazione_Conformita.pdf',
    'CI-2026-0001_1001_4_Dichiarazione_Libera_Esportazione.pdf'
  ]);
  anno.cartelle[0].file.forEach(f => assert.strictEqual(f.blob.tipo, 'application/pdf'));

  const registro = Object.values(amb.fogli)[0].getSheetByName('Registro').righe;
  assert.strictEqual(registro.length, 4);
  assert.deepStrictEqual(piatto(registro.slice(1).map(r => r[1])), ['CI-2026-0001', 'CI-2026-0002', 'CI-2026-0003']);
  assert.strictEqual(registro[1][9], 139);
  const errori = Object.values(amb.fogli)[0].getSheetByName('Errori').righe;
  assert.ok(errori.some(r => r[1] === '#1004' && /sanzioni/.test(r[2])));

  assert.deepStrictEqual(piatto(amb.tagAggiunti), ['gid://shopify/Order/1001', 'gid://shopify/Order/1003', 'gid://shopify/Order/1005']);
  assert.strictEqual(amb.email.length, 1, 'email con ordini da controllare');
  assert.ok(/BLOCCATO #1004/.test(amb.email[0].c));
  assert.ok(/DA CONTROLLARE #1001/.test(amb.email[0].c));
});

test('un secondo giro non duplica nulla', () => {
  const esito = amb.ctx.processaNuoviOrdini();
  assert.strictEqual(esito.generati.length, 0);
  const registro = Object.values(amb.fogli)[0].getSheetByName('Registro').righe;
  assert.strictEqual(registro.length, 4);
});

test('generaDocumentiOrdine rigenera mantenendo lo stesso numero', () => {
  const r = amb.ctx.generaDocumentiOrdine('1003');
  assert.strictEqual(r.stato, 'generato');
  assert.strictEqual(r.numero, 'CI-2026-0002');
  const registro = Object.values(amb.fogli)[0].getSheetByName('Registro').righe;
  assert.strictEqual(registro.length, 4, 'nessuna riga in più');
  const cartella = amb.root.cartelle.find(c => c.nome === 'Fatture Estere').cartelle[0].cartelle[1];
  assert.strictEqual(cartella.file.filter(f => !f.cestino).length, 4, 'i vecchi PDF vanno nel cestino');
});

console.log('Contenuto documenti');
test('fattura commerciale e dichiarazioni contengono i dati richiesti', () => {
  const { ctx } = creaAmbiente();
  const doc = { ordine: ctx.normalizzaOrdine_(ordiniEsempio[0]), numero: 'CI-2026-0001', data: new Date('2026-11-06T09:00:00Z'), azienda: ctx.CONFIG.AZIENDA, logo: '' };
  const fattura = ctx.htmlFatturaCommerciale_(doc);
  ['COMMERCIAL INVOICE', 'CI-2026-0001', '#1001', 'John Smith', '350 Fifth Avenue', '+1 212 555 0100', 'United States (US)',
    '6505.00.10', '6505.00', 'Wool felt fedora hat', '100% Cotone', '71,10', '42,90', '114,00', '25,00', '139,00',
    'DAP New York', 'art. 8, comma 1, lett. a)', 'EORI', 'FedEx', '0,780 kg'].forEach(t => assert.ok(fattura.includes(t), 'fattura: manca ' + t));
  assert.ok(!fattura.includes('Gift card'));
  assert.ok(!fattura.includes('preferential origin'), 'origine preferenziale disattivata di default');

  const origine = ctx.htmlDichiarazioneOrigine_(doc);
  ['DICHIARAZIONE DI ORIGINE', 'Italy (IT)', 'Reg. (UE) n. 952/2013', 'CI-2026-0001'].forEach(t => assert.ok(origine.includes(t), 'origine: manca ' + t));
  const conf = ctx.htmlDichiarazioneConformita_(doc);
  ['DICHIARAZIONE DI CONFORMITÀ', '2023/988', '1007/2011', 'REACH', '2016/425', '100% Lana'].forEach(t => assert.ok(conf.includes(t), 'conformità: manca ' + t));
  const lib = ctx.htmlLiberaEsportazione_(doc);
  ['LIBERA ESPORTAZIONE', '2021/821', '833/2014', '765/2006', '185', 'liberamente esportabili'].forEach(t => assert.ok(lib.includes(t), 'libera esp.: manca ' + t));

  ctx.CONFIG.ORIGINE_PREFERENZIALE = true;
  ctx.CONFIG.SPEDIZIONE.COPIE_FATTURA = 3;
  const f2 = ctx.htmlFatturaCommerciale_(doc);
  assert.ok(f2.includes('EU preferential origin'));
  assert.strictEqual((f2.match(/class="salto"/g) || []).length, 2);
  // origine non UE (Ecuador): niente dichiarazione preferenziale
  const docEc = Object.assign({}, doc, { ordine: ctx.normalizzaOrdine_(ordiniEsempio[2]) });
  assert.ok(!ctx.htmlFatturaCommerciale_(docEc).includes('EU preferential origin'));
  assert.ok(ctx.htmlDichiarazioneOrigine_(docEc).includes('non è applicabile'));
});

test('caratteri speciali vengono codificati', () => {
  const { ctx } = creaAmbiente();
  const o = JSON.parse(JSON.stringify(ordiniEsempio[0]));
  o.shippingAddress.name = '<script>alert(1)</script>';
  const doc = { ordine: ctx.normalizzaOrdine_(o), numero: 'X', data: new Date(), azienda: ctx.CONFIG.AZIENDA, logo: '' };
  assert.ok(!ctx.htmlFatturaCommerciale_(doc).includes('<script>'));
});

if (salvaAnteprime) {
  const { ctx } = creaAmbiente();
  const dir = path.join(__dirname, 'anteprime');
  fs.mkdirSync(dir, { recursive: true });
  [[0, 'US'], [4, 'CH']].forEach(([i, sigla]) => {
    const doc = { ordine: ctx.normalizzaOrdine_(ordiniEsempio[i]), numero: 'CI-2026-000' + (i + 1), data: new Date(), azienda: ctx.CONFIG.AZIENDA, logo: '' };
    fs.writeFileSync(path.join(dir, sigla + '_1_fattura.html'), ctx.htmlFatturaCommerciale_(doc));
    fs.writeFileSync(path.join(dir, sigla + '_2_origine.html'), ctx.htmlDichiarazioneOrigine_(doc));
    fs.writeFileSync(path.join(dir, sigla + '_3_conformita.html'), ctx.htmlDichiarazioneConformita_(doc));
    fs.writeFileSync(path.join(dir, sigla + '_4_libera_esportazione.html'), ctx.htmlLiberaEsportazione_(doc));
  });
  console.log('Anteprime HTML salvate in ' + dir);
}

console.log(process.exitCode ? '\nALCUNI TEST FALLITI' : '\nTutti i ' + ok + ' test superati.');
