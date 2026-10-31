"""Assemble the exercise book HTML and print it to PDF with Chromium."""
import importlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lib import render_section, _atom  # noqa: E402

ROOT = os.path.dirname(HERE)
OUT_HTML = os.path.join(HERE, "book.html")
OUT_PDF = os.path.join(ROOT, "FSA_5_-_Exercise_Book_with_space.pdf")

SECTION_MODULES = ["sec_a", "sec_b", "sec_c", "sec_d", "sec_e", "sec_f", "sec_g",
                   "sec_h", "sec_i", "sec_j", "sec_k", "sec_l", "sec_m", "sec_n", "sec_x"]

CSS = r"""
@font-face{font-family:"InterW";src:url("fonts/Inter-Regular.ttf");font-weight:400;font-style:normal}
@font-face{font-family:"InterW";src:url("fonts/Inter-Italic.ttf");font-weight:400;font-style:italic}
@font-face{font-family:"InterW";src:url("fonts/Inter-Medium.ttf");font-weight:500;font-style:normal}
@font-face{font-family:"InterW";src:url("fonts/Inter-SemiBold.ttf");font-weight:600;font-style:normal}
@font-face{font-family:"InterW";src:url("fonts/Inter-Bold.ttf");font-weight:700;font-style:normal}
@font-face{font-family:"InterW";src:url("fonts/Inter-ExtraBold.ttf");font-weight:800;font-style:normal}
:root{
  --bg:#0b0d12; --panel:#121722; --panel2:#0f141d; --text:#e6e9ef; --muted:#8e98aa; --dim:#5f697b;
  --amber:#f2b33d; --amber2:#ffd27a; --teal:#4fd6ab; --teal2:#9af0d2; --line:#2a3140; --line2:#20262f;
  --blank:#10151d; --grid:#1d2430; --gridb:#2b3342; --rule:#2f3847;
}
@page{size:A4;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--bg);color:var(--text);
  font-family:InterW,"DejaVu Sans",sans-serif;font-size:9.4pt;line-height:1.45;
  -webkit-print-color-adjust:exact;print-color-adjust:exact;font-feature-settings:"tnum" 1,"cv11" 1}
#src{position:absolute;left:0;top:0;width:178mm;visibility:hidden}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;background:var(--bg);break-after:page;page-break-after:always}
.page:last-child{break-after:auto}
.pc{position:absolute;top:14mm;left:16mm;width:178mm;height:266mm}
.pf{position:absolute;bottom:7.5mm;left:16mm;right:16mm;display:flex;justify-content:space-between;
  font-size:7pt;color:var(--dim);letter-spacing:.02em;border-top:0.5px solid var(--line2);padding-top:2mm}
.pf .pn{color:var(--muted);font-weight:600}
p{margin:0 0 1.6mm 0}
b,strong{font-weight:600}
em{color:var(--amber2);font-style:italic}
.atom{width:178mm;display:flow-root}
/* section header */
.sec-h{padding-top:1mm;padding-bottom:1mm}
.sec-k{font-size:8pt;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);font-weight:600}
h1{font-size:21pt;line-height:1.15;color:var(--amber);margin:1mm 0 2mm 0;font-weight:700;letter-spacing:-.01em}
.sec-i{color:var(--muted);font-size:8.8pt;margin-bottom:2mm}
/* type header */
.th{border-top:1px solid var(--line);padding-top:3.5mm}
.th-k{font-size:7.5pt;letter-spacing:.16em;text-transform:uppercase;color:var(--teal);font-weight:600}
h2{font-size:13pt;margin:.6mm 0 .8mm 0;color:var(--text);font-weight:700}
.th-d{color:var(--muted);font-size:8.6pt}
.th-p{margin-top:1.4mm;font-size:7.8pt;color:var(--dim)}
.th-p .pw{color:var(--teal)} .th-p .pe{color:var(--amber)}
/* worked example */
.we-box{background:var(--panel);border-left:2.5px solid var(--teal);padding:1.2mm 5mm 1.6mm 5mm}
.we-top{border-top-right-radius:2.5mm;padding-top:3.5mm}
.we-bot{border-bottom-right-radius:2.5mm;padding-bottom:4mm}
.we-label{font-size:7pt;letter-spacing:.18em;text-transform:uppercase;color:var(--teal);font-weight:700}
h4{margin:.6mm 0 1.8mm 0;font-size:11pt;color:var(--teal2);font-weight:700}
.step-h{color:var(--teal);font-weight:700;font-size:8.8pt;margin:1.2mm 0 1.2mm 0;
  border-top:0.5px dashed #2c4a44;padding-top:2.2mm}
.we-box .dt th{color:var(--teal2)}
.we-box .dt{background:var(--panel2)}
.ans{color:var(--teal2);font-weight:600}
/* exercise */
h3{font-size:10.8pt;margin:0 0 1.6mm 0;color:var(--amber);font-weight:700;display:flex;align-items:baseline;gap:2.2mm;flex-wrap:wrap}
h3 .exid{color:var(--amber);min-width:7mm}
h3 .tag{font-size:6.8pt;letter-spacing:.16em;color:var(--muted);font-weight:600;text-transform:uppercase}
h3 .todo{margin-left:auto;font-size:6.6pt;letter-spacing:.14em;text-transform:uppercase;color:var(--bg);
  background:var(--amber);border-radius:1.2mm;padding:.5mm 1.8mm;font-weight:700;align-self:center}
.ex p{color:var(--text)}
/* tables */
.dt{width:100%;border-collapse:collapse;margin:1.4mm 0 2mm 0;font-size:8.6pt}
.dt th,.dt td{border:0.6px solid var(--line);padding:1.25mm 2.2mm;vertical-align:middle;text-align:left}
.dt th{background:#151b26;color:var(--amber);font-weight:600}
.dt td.num,.dt th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.dt.ctr td.num,.dt.ctr th.num{text-align:center}
.dt tr.tot td{font-weight:700;background:#121823}
.dt tr.lab td{font-weight:600;color:var(--muted);background:#0f141c;font-size:8pt;letter-spacing:.04em}
.dt td.blank{background:var(--blank)}
.dt.tall td{height:8.6mm}
.dt.ans th{color:var(--amber)}
.dt.small{font-size:8pt}
.dt.small td,.dt.small th{padding:1mm 1.8mm}
/* calc table */
.calc{width:100%;border-collapse:collapse;margin:1mm 0 2mm 0;font-size:8.6pt}
.calc td{padding:1mm 2mm;border-bottom:0.5px solid #253041;vertical-align:top}
.calc td.wk{color:#c4cbd8;font-variant-numeric:tabular-nums}
.calc td.res{text-align:right;color:var(--teal2);font-weight:600;white-space:nowrap}
.calc tr.lab td{color:var(--muted);font-size:7.8pt;letter-spacing:.06em;text-transform:uppercase;border-bottom:none;padding-top:2mm}
/* required */
.req{border-left:2px solid var(--line);padding:.8mm 0 .6mm 4mm;margin:1.6mm 0 1.6mm 0}
.req-t{font-weight:700;margin-bottom:.8mm}
.req ol,ol.plain{margin:0;padding-left:5mm}
.req li,ol.plain li{margin:.5mm 0}
ul{margin:.6mm 0 1.6mm 0;padding-left:5mm} ul li{margin:.5mm 0}
.formula{margin:1.4mm 0 2mm 0;padding:1.6mm 3mm;background:#0e131b;border:0.6px solid var(--line);border-radius:1.5mm;
  font-size:9pt;color:var(--text)}
.rule{margin:1.6mm 0 2mm 0;padding:1.6mm 3mm;border:0.6px solid #2c4a44;border-radius:1.5mm;font-size:8.6pt;color:#cfe9df;background:#0f1a19}
.rule-t{color:var(--teal);font-weight:700;text-transform:uppercase;font-size:7pt;letter-spacing:.14em;margin-right:1.5mm}
.co{margin:1.6mm 0 .4mm 0}
.co-n{font-weight:700;letter-spacing:.06em}
.co-s{color:var(--muted);font-size:8.4pt}
/* mcq */
.mcq{margin:0 0 2.2mm 0;position:relative}
.mq{margin-bottom:1mm;padding-right:30mm}
.opts{padding-left:5mm}
.opt{margin:.6mm 0}
.abox{position:absolute;right:0;top:0;display:flex;align-items:center;gap:2mm;font-size:7pt;color:var(--muted);
  letter-spacing:.1em;text-transform:uppercase}
.abox i{display:inline-block;width:10mm;height:8mm;border:0.8px solid var(--gridb);border-radius:1.2mm;background:var(--blank)}
.mcq-sol{color:var(--teal2);font-size:8.6pt;margin:.6mm 0 1mm 5mm}
.mcq-sol b{color:var(--teal)}
.tf-t{font-weight:700;margin:2.4mm 0 1.4mm 0}
.tf{margin:0 0 1.6mm 0}
.tf-row{display:flex;align-items:center;gap:4mm}
.tf-s{flex:1}
.tfbox{display:flex;gap:1.5mm}
.tfbox span{width:8mm;height:7mm;border:0.8px solid var(--gridb);border-radius:1.2mm;background:var(--blank);
  display:flex;align-items:center;justify-content:center;font-size:7pt;color:var(--dim)}
.why{height:7.5mm;border-bottom:0.8px solid var(--rule);margin-left:5mm;margin-right:21mm}
/* workspace */
.wl{font-size:6.8pt;letter-spacing:.14em;text-transform:uppercase;color:var(--dim);margin:0 0 1mm 0;font-weight:600}
.wa{width:100%;position:relative}
.wa svg{position:absolute;left:0;top:0}
.ansatom .dt{margin-top:0}
/* cover / front matter */
.cover{padding:0}
.cv{position:absolute;inset:0;padding:70mm 18mm 0 18mm}
.cv-t{font-size:34pt;font-weight:800;color:var(--amber);letter-spacing:-.02em;line-height:1.05}
.cv-s{font-size:13pt;color:var(--amber2);margin-top:4mm}
.cv-bar{width:62mm;height:1.6mm;background:var(--amber);margin:9mm 0 8mm 0;border-radius:1mm}
.cv-m{color:var(--muted);font-size:9.4pt;line-height:1.7}
.cv-m em{color:var(--amber2)}
.cv-box{margin-top:16mm;border:0.6px solid var(--line);border-radius:2.5mm;padding:5mm 6mm;background:var(--panel);max-width:150mm}
.cv-box .k{font-size:7.5pt;letter-spacing:.16em;text-transform:uppercase;color:var(--teal);font-weight:700;margin-bottom:2mm}
.cv-box div.r{display:flex;gap:4mm;margin:1.6mm 0;align-items:center}
.sw{width:9mm;height:5mm;border-radius:1mm;flex:none}
.h-sub{font-size:13pt;color:var(--amber);font-weight:700;margin:0 0 2mm 0;padding-bottom:1.6mm;border-bottom:0.6px solid var(--line)}
.toc-s{display:flex;align-items:baseline;gap:3mm;padding:2.4mm 0 1mm 0;border-bottom:0.5px solid var(--line2)}
.toc-s .l{color:var(--amber);font-weight:800;width:5mm}
.toc-s a{color:var(--text);text-decoration:none;font-weight:600;flex:1}
.toc-t{display:flex;align-items:baseline;gap:3mm;padding:.7mm 0 .7mm 8mm;font-size:8.6pt}
.toc-t a{color:#c3cad6;text-decoration:none;flex:1}
.toc-t .c{color:var(--teal);width:9mm;font-size:7.8pt}
.toc-t .ids{color:var(--dim);font-size:7.8pt;width:22mm;text-align:right}
.pg{color:var(--muted);width:9mm;text-align:right;font-variant-numeric:tabular-nums}
.qh{margin:0 0 1.2mm 0;font-size:9.6pt;padding-left:2.5mm;border-left:2px solid var(--amber)}
.qh .mk{color:var(--muted);font-weight:500}
.legend{display:grid;grid-template-columns:1fr 1fr;gap:3mm 6mm;margin:2mm 0 3mm 0}
.lg{border:0.6px solid var(--line);border-radius:2mm;padding:3mm;background:var(--panel)}
.lg .k{font-weight:700;margin-bottom:1mm}
.lg .s{color:var(--muted);font-size:8.4pt}
"""

JS = r"""
(async function(){
  await document.fonts.ready;
  const MM = 96/25.4;
  const CH = 266*MM - 2;              // usable content height (px)
  const MIN_WS = 28*MM;               // smallest writing chunk worth starting on a page
  const src = document.getElementById('src');
  const out = document.getElementById('out');
  const groups = [...src.querySelectorAll(':scope > .grp')].map(g => ({
    el: g, cover: g.dataset.cover === '1', newp: g.dataset.new === '1', sec: g.dataset.sec || '',
    atoms: [...g.querySelectorAll(':scope > .atom')].map(a => ({
      el: a, h: a.getBoundingClientRect().height, ws: a.classList.contains('ws'), kwn: a.classList.contains('kwn')
    }))
  }));
  const pages = []; let cur = null;
  function newPage(sec, cls){
    const p = document.createElement('div'); p.className = 'page' + (cls ? ' ' + cls : '');
    p.innerHTML = '<div class="pc"></div><div class="pf"><span class="bk">FSA Exercise Book · workbook edition</span><span class="rh"></span><span class="pn"></span></div>';
    out.appendChild(p);
    cur = {el: p, pc: p.firstChild, used: 0, sec: sec, atoms: []}; pages.push(cur); return cur;
  }
  const rem = () => CH - cur.used;
  function put(a, h){ cur.pc.appendChild(a.el); cur.used += h; cur.atoms.push(a); }
  function placeWS(a, sec){
    const area = a.el.querySelector('.wa');
    const over = a.h - area.getBoundingClientRect().height;   // label + padding
    let total = a.h;
    if (total <= rem()) { put(a, total); return; }
    if (rem() < MIN_WS || rem() < 0.5*total || total <= 60*MM) { newPage(sec); }
    if (total <= rem()) { put(a, total); return; }
    let first = true;
    while (total > 0){
      if (rem() < MIN_WS) newPage(sec);
      const take = Math.min(total, rem());
      const el = first ? a.el : a.el.cloneNode(true);
      if (!first){ const l = el.querySelector('.wl'); if (l) l.textContent = '✎ continued'; }
      el.querySelector('.wa').style.height = (take - over) + 'px';
      put({el: el, h: take, ws: true}, take);
      total -= take; first = false;
      if (total > 0 && total < MIN_WS) total = MIN_WS;
    }
  }
  for (const g of groups){
    if (g.cover){ newPage('', 'cover'); g.atoms.forEach(a => put(a, a.h)); cur = null; continue; }
    if (!cur || (g.newp && cur.atoms.length)) newPage(g.sec);
    if (!cur.sec) cur.sec = g.sec;
    const H = g.atoms.reduce((s, a) => s + a.h, 0);
    if (H <= rem()) { g.atoms.forEach(a => put(a, a.h)); continue; }
    if (H <= CH && cur.atoms.length) { newPage(g.sec); g.atoms.forEach(a => put(a, a.h)); continue; }
    // split the group across pages
    for (let i = 0; i < g.atoms.length; i++){
      const a = g.atoms[i];
      let need = 0, j = i;
      while (j < g.atoms.length && g.atoms[j].kwn){ need += g.atoms[j].h; j++; }
      if (j < g.atoms.length && j !== i) need += g.atoms[j].ws ? Math.min(g.atoms[j].h, MIN_WS) : g.atoms[j].h;
      else if (j === i) need = a.ws ? Math.min(a.h, MIN_WS) : a.h;
      if (need > CH) {   // chain cannot fit on any page: only keep this atom with the start of the next
        const nx = g.atoms[i + 1];
        need = (a.ws ? Math.min(a.h, MIN_WS) : a.h) + (a.kwn && nx ? Math.min(nx.h, 40*MM) : 0);
      }
      if (need > rem() && cur.atoms.length) newPage(g.sec);
      if (a.ws) placeWS(a, g.sec);
      else { if (a.h > rem() && cur.atoms.length) newPage(g.sec); put(a, a.h); }
    }
  }
  // stretch the last writing area of each page; otherwise add a notes area
  for (const p of pages){
    if (p.el.classList.contains('cover') || p.front) continue;
    const r = CH - p.used;
    const last = p.atoms[p.atoms.length - 1];
    if (!last) continue;
    if (last.ws){
      const area = last.el.querySelector('.wa');
      area.style.height = (area.getBoundingClientRect().height + r - 1) + 'px';
    } else if (r > 22*MM && !last.el.classList.contains('nofill')){
      const d = document.createElement('div');
      d.className = 'atom ws'; d.dataset.kind = 'grid'; d.style.paddingTop = '4mm';
      d.innerHTML = '<div class="wl">✎ Extra space</div><div class="wa grid"></div>';
      p.pc.appendChild(d);
      const over = d.getBoundingClientRect().height;
      d.querySelector('.wa').style.height = (r - over - 2) + 'px';
    }
  }
  // draw grids and ruled lines
  const NS = 'http://www.w3.org/2000/svg';
  for (const wa of document.querySelectorAll('#out .wa')){
    const w = wa.getBoundingClientRect().width, h = wa.getBoundingClientRect().height;
    const svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('width', w); svg.setAttribute('height', h); svg.setAttribute('viewBox', `0 0 ${w} ${h}`);
    let d = '';
    if (wa.classList.contains('grid')){
      const s = 5*MM;
      for (let x = s; x < w - 1; x += s) d += `M${x.toFixed(2)} 0V${h.toFixed(2)}`;
      for (let y = s; y < h - 1; y += s) d += `M0 ${y.toFixed(2)}H${w.toFixed(2)}`;
      svg.innerHTML = `<path d="${d}" stroke="#1b222d" stroke-width="0.6" fill="none"/>`+
        `<rect x="0.4" y="0.4" width="${(w-0.8).toFixed(2)}" height="${(h-0.8).toFixed(2)}" rx="6" fill="none" stroke="#2b3342" stroke-width="0.8"/>`;
    } else {
      const s = 8.5*MM;
      for (let y = s; y <= h + 0.5; y += s) d += `M0 ${y.toFixed(2)}H${w.toFixed(2)}`;
      svg.innerHTML = `<path d="${d}" stroke="#2f3847" stroke-width="0.8" fill="none"/>`;
    }
    wa.appendChild(svg);
  }
  // footers and page numbers
  pages.forEach((p, i) => {
    p.el.querySelector('.rh').textContent = p.sec;
    p.el.querySelector('.pn').textContent = (i + 1);
  });
  for (const s of document.querySelectorAll('[data-target]')){
    const t = document.getElementById(s.dataset.target);
    if (!t) continue;
    const pg = t.closest('.page');
    s.textContent = [...out.children].indexOf(pg) + 1;
  }
  window.__overflow = pages.map((p, i) => [i + 1, Math.round(p.pc.scrollHeight - p.pc.clientHeight)]).filter(x => x[1] > 1);
  src.remove();
  window.__pages = pages.length;
  window.__done = true;
})();
"""


def front_matter(sections):
    groups = []
    total_ex = sum(len(b["exs"]) for s in sections for b in s["blocks"])
    total_we = sum(1 for s in sections for b in s["blocks"])
    cover = f"""
<div class="cv">
  <h1 class="cv-t" id="cover">FSA Exercise Book</h1>
  <div class="cv-s">Workbook edition — with space to write and a worked example for every type</div>
  <div class="cv-bar"></div>
  <div class="cv-m">Financial Statement Analysis · Prof. Stefano Bianchi<br>
  {total_ex} exercises (128 by topic plus six full papers) · {total_we} new worked examples<br>
  Exercise numbers are unchanged: solutions in the companion file <em>FSA 6 — Exercise Solutions</em></div>
  <div class="cv-box">
    <div class="k">How every type is laid out</div>
    <div class="r"><span class="sw" style="background:var(--teal)"></span><span><b>① Worked example — solved.</b> New data, full method, every intermediate figure.</span></div>
    <div class="r"><span class="sw" style="background:var(--amber)"></span><span><b>② ③ Your turn.</b> Two exercises from the book, each followed by its own writing space.</span></div>
  </div>
</div>"""
    groups.append(({"cover": True}, [_atom(cover, pad=0)]))

    how = """
<div class="h-sub">How to use this book</div>
<p>Every exercise is written the way the exam writes it: a block of data, then <em>Required</em>. The book is now organised by
<b>type of exercise</b>. Each type opens with a <span class="ans">worked example</span> on new figures — read it, understand the
order of the steps — and then gives you <b>two exercises from the original book</b> to work on your own, in the space provided.
Only then open the solutions file.</p>
<p>Three rules carried over from the lecturer’s own answers, because they are worth marks on their own:</p>
<ul>
<li>When the question asks for a textbook ratio, name the substitution before computing — <em>“Operating profit margin (instead of Profit margin)”</em> — then the formula, then the assumptions, then the arithmetic.</li>
<li>State the tax rate you assumed (30 per cent unless the question gives one) and what you treated as operating.</li>
<li>If only one balance sheet date is given, write <em>“Can we calculate the average? No, we can’t”</em> and use the year-end figure.</li>
</ul>
<p>Use 360 days. Finish every quantitative answer with two or three lines of comment.</p>
<div class="h-sub" style="margin-top:5mm">The writing space</div>
<div class="legend">
 <div class="lg"><div class="k">Grid</div><div class="s">For calculations, schedules and statements. Draw your own columns; one square is 5 mm.</div></div>
 <div class="lg"><div class="k">Ruled lines</div><div class="s">For comments, explanations and written answers. The number of lines is the length the question asks for.</div></div>
 <div class="lg"><div class="k">Blank tables</div><div class="s">Pre-drawn answer tables (plans, ratios, horizontal and common-size columns): fill in the empty cells.</div></div>
 <div class="lg"><div class="k">Answer boxes</div><div class="s">Multiple choice and true/false: write the letter, or tick T or F.</div></div>
</div>
<p class="muted" style="color:var(--muted)">The space is sized to the question — two lines for a one-line answer, most of a page for a statement of cash flows.
Whatever is left at the bottom of a page is added to the last exercise on it, so you always have room to finish.</p>
"""
    groups.append(({"new": True, "sec": "How to use this book"}, [_atom(how, pad=0, cls="nofill")]))

    toc_atoms = [_atom('<div class="h-sub">Contents</div>', pad=0, kwn=True)]
    for s in sections:
        L_ = s["letter"]
        ids = [e["id"] for b in s["blocks"] for e in b["exs"]]
        toc_atoms.append(_atom(
            f'<div class="toc-s"><span class="l">{L_}</span><a href="#sec-{L_}">{s["title"]}</a>'
            f'<span class="pg" data-target="sec-{L_}"></span></div>', pad=0, kwn=True))
        for b in s["blocks"]:
            tid = "type-" + b["code"].replace(".", "-")
            exids = " · ".join(e["id"] for e in b["exs"])
            toc_atoms.append(_atom(
                f'<div class="toc-t"><span class="c">{b["code"]}</span><a href="#{tid}">{b["name"]}</a>'
                f'<span class="ids">{exids}</span><span class="pg" data-target="{tid}"></span></div>', pad=0))
    toc_atoms[-1] = toc_atoms[-1].replace('class="atom"', 'class="atom nofill"', 1)
    groups.append(({"new": True, "sec": "Contents", "split": True}, toc_atoms))
    return groups


def ensure_fonts():
    """Inter ships as CFF (.otf), which Chromium embeds as Type 3; convert once to TrueType."""
    fdir = os.path.join(HERE, "fonts")
    if not os.path.exists(os.path.join(fdir, "Inter-Regular.ttf")):
        os.makedirs(fdir, exist_ok=True)
        subprocess.run([sys.executable, os.path.join(HERE, "otf2ttf.py"), fdir], check=True)


def main():
    ensure_fonts()
    sections = []
    for m in SECTION_MODULES:
        try:
            mod = importlib.import_module(m)
        except ModuleNotFoundError as e:
            if e.name == m:
                continue
            raise
        sections.append(mod.SEC)
    groups = front_matter(sections)
    for s in sections:
        groups += render_section(s)
    parts = []
    for attrs, atoms in groups:
        da = ""
        if attrs.get("cover"):
            da += ' data-cover="1"'
        if attrs.get("new"):
            da += ' data-new="1"'
        if attrs.get("sec"):
            da += f' data-sec="{attrs["sec"]}"'
        parts.append(f'<div class="grp"{da}>' + "".join(atoms) + "</div>")
    html = ("<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\"><title>FSA Exercise Book — workbook edition</title>"
            f"<style>{CSS}</style></head><body><div id=\"out\"></div><div id=\"src\">{''.join(parts)}</div>"
            f"<script>{JS}</script></body></html>")
    with open(OUT_HTML, "w") as f:
        f.write(html)
    n_ex = sum(len(b["exs"]) for s in sections for b in s["blocks"])
    n_we = sum(len(s["blocks"]) for s in sections)
    print(f"sections={len(sections)} worked_examples={n_we} exercises={n_ex}")
    out = sys.argv[1] if len(sys.argv) > 1 else OUT_PDF
    subprocess.run(["node", os.path.join(HERE, "render.js"), OUT_HTML, out], check=True)


if __name__ == "__main__":
    main()
