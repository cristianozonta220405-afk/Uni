# FSA Exercise Book — workbook edition

`FSA_5_-_Exercise_Book_with_space.pdf` is the exercise book rebuilt on a dark background, with:

- **space to write** after every exercise, sized to the question (graph-paper grid for calculations,
  ruled lines for comments, pre-drawn blank tables for plans, ratios, horizontal/common-size columns
  and cash flow statements, answer boxes for multiple choice and true/false);
- **one worked example (solved) before every type of exercise**, followed by **two exercises to do** —
  67 types, 134 exercises (the 128 by topic plus the six full papers). Exercise numbers are unchanged,
  so the solutions file *FSA 6 — Exercise Solutions* still applies.

## Rebuild

```
python3 src/build.py            # writes FSA_5_-_Exercise_Book_with_space.pdf
```

Needs Python 3 with `fonttools`, Node with Playwright/Chromium, and the Inter font
(`/usr/share/fonts/opentype/inter`). Content lives in `src/sec_a.py` … `src/sec_x.py`;
`src/lib.py` holds the building blocks and `src/build.py` the styling and the paginator.
