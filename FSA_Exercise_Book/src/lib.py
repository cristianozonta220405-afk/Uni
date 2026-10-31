"""Building blocks for the FSA exercise book (dark theme, with workspace).

Content modules (sec_a.py ... sec_x.py) describe sections with SECTION/BLOCK/WE/EX.
build.py turns them into one HTML file; a small paginator running in Chromium
lays the atoms out on A4 pages, stretches writing areas to fill each page,
and the page is then printed to PDF.
"""
import re

# ---------------------------------------------------------------- tables

_NUM = re.compile(
    r"^[+\-−]?\s*[€$]?\s*\(?\s*[+\-−]?\s*[€$]?\s*\d[\d,\.]*\s*\)?\s*"
    r"(%|x|×|days|pts|years|p\.p\.)?\s*✓?$"
)


def _strip(c):
    return re.sub(r"<[^>]+>", "", c).strip()


def _isnum(c):
    s = _strip(c)
    if s in ("?", "—", "–", "n.m.", "n/a", "0"):
        return True
    return bool(_NUM.match(s))


def _parse(spec):
    rows = []
    for line in spec.strip("\n").split("\n"):
        line = line.strip()
        if not line:
            continue
        kind = "row"
        if line.startswith("^"):
            kind, line = "head", line[1:]
        elif line.startswith("**"):
            kind, line = "total", line[2:]
        elif line.startswith("##"):
            kind, line = "label", line[2:]
        cells = [c.strip() for c in line.split("|")]
        rows.append((kind, cells))
    return rows


def T(spec, w=None, cls="", add=None, tall=False, center=False):
    """Data table from a compact spec.

    '^a | b'   header row          '**a | b'  total row (bold)
    '##Label'  label row (spans)   '__'       blank answer cell
    add=[..]   extra blank answer columns appended to every row
    """
    rows = _parse(spec)
    if add:
        new = []
        for kind, cells in rows:
            if kind == "head":
                new.append((kind, cells + list(add)))
            elif kind == "label":
                new.append((kind, cells))
            else:
                new.append((kind, cells + ["__"] * len(add)))
        rows = new
    ncols = max(len(c) for k, c in rows if k != "label")
    # per-column numeric detection (body rows)
    colnum = []
    for j in range(ncols):
        vals = [c[j] for k, c in rows if k in ("row", "total") and j < len(c)]
        vals = [v for v in vals if v not in ("", "__")]
        colnum.append(bool(vals) and sum(_isnum(v) for v in vals) >= len(vals) * 0.6)
    out = [f'<table class="dt {cls}{" tall" if tall else ""}{" ctr" if center else ""}">']
    if w:
        out.append("<colgroup>" + "".join(f'<col style="width:{x}%">' for x in w) + "</colgroup>")
    for kind, cells in rows:
        if kind == "label":
            out.append(f'<tr class="lab"><td colspan="{ncols}">{cells[0]}</td></tr>')
            continue
        tag = "th" if kind == "head" else "td"
        trc = ' class="tot"' if kind == "total" else ""
        tds = []
        for j, c in enumerate(cells):
            cl = []
            if c == "__":
                cl.append("blank")
                c = ""
            elif j > 0 and (_isnum(c) if kind != "head" else colnum[j]):
                cl.append("num")
            if kind == "head" and j > 0 and colnum[j]:
                cl.append("num")
            ca = f' class="{" ".join(dict.fromkeys(cl))}"' if cl else ""
            tds.append(f"<{tag}{ca}>{c}</{tag}>")
        # pad short rows
        for j in range(len(cells), ncols):
            tds.append(f"<{tag}></{tag}>")
        out.append(f"<tr{trc}>" + "".join(tds) + "</tr>")
    out.append("</table>")
    return "".join(out)


def BT(headers, labels, w=None, blanks=None, cls=""):
    """Blank answer table: headers + row labels, other cells blank (tall rows)."""
    n = len(headers)
    lines = ["^" + " | ".join(headers)]
    for lab in labels:
        if isinstance(lab, (list, tuple)):
            cells = list(lab) + ["__"] * (n - len(lab))
        else:
            cells = [lab] + ["__"] * (n - 1)
        lines.append(" | ".join(cells))
    return T("\n".join(lines), w=w, tall=True, cls="ans " + cls)


# ---------------------------------------------------------------- text helpers

def P(t, cls=""):
    return f'<p class="{cls}">{t}</p>' if cls else f"<p>{t}</p>"


def REQ(items, title="Required"):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f'<div class="req"><div class="req-t">{title}</div><ol>{lis}</ol></div>'


def OL(items, start=1):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f'<ol class="plain" start="{start}">{lis}</ol>'


def UL(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def F(t):
    """Display formula."""
    return f'<div class="formula">{t}</div>'


def RULE(t, title="Rule"):
    return f'<div class="rule"><span class="rule-t">{title}</span> {t}</div>'


def CALC(rows, w=(30, 42, 28)):
    """Rows of (label, working, result) — the standard ratio layout."""
    out = ['<table class="calc"><colgroup>' + "".join(f'<col style="width:{x}%">' for x in w) + "</colgroup>"]
    for r in rows:
        if isinstance(r, str):
            out.append(f'<tr class="lab"><td colspan="3">{r}</td></tr>')
            continue
        a, b, c = r
        out.append(f'<tr><td>{a}</td><td class="wk">{b}</td><td class="res">{c}</td></tr>')
    out.append("</table>")
    return "".join(out)


def ANS(t):
    """Highlighted answer text inside a worked example."""
    return f'<span class="ans">{t}</span>'


def MCQ(n, q, opts, answer=None, why=None, box=True):
    letters = "ABCDEFG"
    o = "".join(f'<div class="opt"><b>{letters[i]}.</b> {x}</div>' for i, x in enumerate(opts))
    right = ""
    if answer is not None:
        right = f'<div class="mcq-sol">Answer: <b>{answer}</b>{" — " + why if why else ""}</div>'
    elif box:
        right = '<div class="abox"><span>Answer</span><i></i></div>'
    if answer is not None:
        return f'<div class="mcq"><div class="mq"><b>{n}.</b> {q}</div><div class="opts">{o}</div>{right}</div>'
    return f'<div class="mcq"><div class="mq"><b>{n}.</b> {q}</div>{right}<div class="opts">{o}</div></div>'


def TF(items, start=1, answers=None, why_line=False, title="True or false"):
    out = [f'<div class="tf-t">{title}</div>'] if title else []
    for i, s in enumerate(items):
        n = start + i
        if answers:
            a, why = answers[i]
            out.append(f'<div class="tf"><div class="tf-s"><b>{n}.</b> {s}</div>'
                       f'<div class="mcq-sol">Answer: <b>{a}</b> — {why}</div></div>')
        else:
            line = '<div class="why"></div>' if why_line else ""
            out.append(f'<div class="tf"><div class="tf-row"><div class="tf-s"><b>{n}.</b> {s}</div>'
                       f'<div class="tfbox"><span>T</span><span>F</span></div></div>{line}</div>')
    return "".join(out)


def COMPANY(name, sub):
    return f'<div class="co"><div class="co-n">{name}</div><div class="co-s">{sub}</div></div>'


# ---------------------------------------------------------------- workspace specs

def G(mm, label="Working"):
    """Graph-paper area for calculations."""
    return {"ws": "grid", "h": mm, "label": label}


def L(n, label="Comment"):
    """Ruled lines for written answers (8.5 mm spacing)."""
    return {"ws": "lines", "h": n * 8.5, "label": label}


def A(html, label=None):
    """A fixed answer element (e.g. a blank table) that is not stretched."""
    return {"html": html, "label": label}


# ---------------------------------------------------------------- structures

def WE(title, data, steps, comment=None):
    """Worked example: data (str or list) + list of (heading, html) steps."""
    if isinstance(data, str):
        data = [data]
    return {"title": title, "data": data, "steps": steps, "comment": comment}


def EX(eid, title, tag, body, work):
    if isinstance(body, str):
        body = [body]
    return {"id": eid, "title": title, "tag": tag, "body": body, "work": work}


def BLOCK(code, name, desc, we, exs):
    return {"code": code, "name": name, "desc": desc, "we": we, "exs": exs}


def SECTION(letter, title, intro, blocks):
    return {"letter": letter, "title": title, "intro": intro, "blocks": blocks}


# ---------------------------------------------------------------- rendering to atoms

def _atom(inner, cls="", kwn=False, pad=None, extra=""):
    c = "atom" + (" kwn" if kwn else "") + (" " + cls if cls else "")
    st = f' style="padding-top:{pad}mm"' if pad is not None else ""
    return f'<div class="{c}"{st}{extra}>{inner}</div>'


def _ws_atom(spec, pad=2.2):
    label = spec.get("label")
    lab = f'<div class="wl">✎ {label}</div>' if label else ""
    return (f'<div class="atom ws" data-kind="{spec["ws"]}" style="padding-top:{pad}mm">'
            f'{lab}<div class="wa {spec["ws"]}" style="height:{spec["h"]}mm"></div></div>')


def _work_atoms(work):
    out = []
    for spec in work:
        if "ws" in spec:
            out.append(_ws_atom(spec))
        else:
            lab = f'<div class="wl">✎ {spec["label"]}</div>' if spec.get("label") else ""
            out.append(_atom(lab + spec["html"], cls="ansatom", pad=2.4))
    return out


def render_we(we, num_label):
    atoms = []
    first = (f'<div class="we-box we-top"><div class="we-label">Worked example · solved</div>'
             f'<h4>{we["title"]}</h4>{we["data"][0]}</div>')
    atoms.append(_atom(first, pad=3.5, kwn=True))
    for d in we["data"][1:]:
        atoms.append(_atom(f'<div class="we-box">{d}</div>', pad=0))
    steps = list(we["steps"])
    if we.get("comment"):
        steps.append(("Comment", we["comment"]))
    for i, (head, html) in enumerate(steps):
        last = i == len(steps) - 1
        cls = "we-box" + (" we-bot" if last else "")
        h = f'<div class="step-h">{head}</div>' if head else ""
        atoms.append(_atom(f'<div class="{cls}">{h}{html}</div>', pad=0))
    if not steps:
        atoms[-1] = atoms[-1].replace("we-box", "we-box we-bot", 1)
    return atoms


def render_ex(ex):
    atoms = []
    head = (f'<h3 id="ex-{ex["id"]}"><span class="exid">{ex["id"]}</span>{ex["title"]}'
            f'<span class="tag">{ex["tag"]}</span><span class="todo">Your turn</span></h3>')
    body = ex["body"]
    work = ex["work"]
    # body items: HTML strings (statement) or workspace specs (dicts) interleaved
    seq = list(body) + list(work)

    def next_is_ws(k):
        return k + 1 < len(seq) and isinstance(seq[k + 1], dict)

    atoms.append(_atom(head + seq[0], cls="ex", pad=6, kwn=next_is_ws(0)))
    for k in range(1, len(seq)):
        b = seq[k]
        if isinstance(b, dict):
            atoms += _work_atoms([b])
        else:
            atoms.append(_atom(b, cls="ex", pad=3, kwn=next_is_ws(k)))
    return atoms


def render_section(sec):
    """Returns list of groups; each group is (attrs, [atom html])."""
    groups = []
    L_ = sec["letter"]
    sec_name = f'Section {L_} — {sec["title"]}'
    head = (f'<div class="sec-h"><div class="sec-k">Section {L_}</div>'
            f'<h1 id="sec-{L_}">{sec["title"]}</h1><div class="sec-i">{sec["intro"]}</div></div>')
    for bi, b in enumerate(sec["blocks"]):
        ids = " · ".join(e["id"] for e in b["exs"])
        th = (f'<div class="th"><div class="th-k">Type {b["code"]}</div>'
              f'<h2 id="type-{b["code"].replace(".", "-")}">{b["name"]}</h2>'
              f'<div class="th-d">{b["desc"]}</div>'
              f'<div class="th-p"><span class="pw">① Worked example</span> → '
              f'<span class="pe">② {b["exs"][0]["id"]}</span> → '
              f'<span class="pe">③ {b["exs"][1]["id"] if len(b["exs"]) > 1 else ""}</span></div></div>')
        atoms = []
        if bi == 0:
            atoms.append(_atom(head, cls="sech", kwn=True, pad=0))
        atoms.append(_atom(th, cls="thatom", kwn=True, pad=0 if bi == 0 else 9))
        atoms += render_we(b["we"], b["code"])
        groups.append(({"new": bi == 0, "sec": sec_name, "kind": "we"}, atoms))
        for ex in b["exs"]:
            groups.append(({"new": False, "sec": sec_name, "kind": "ex"}, render_ex(ex)))
    return groups
