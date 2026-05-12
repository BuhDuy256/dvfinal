# Prompt: Convert report.md to report.docx

## Context

You have a Markdown file `report.md` containing a Vietnamese data visualization report about NYC Airbnb data (Tasks 5–8). The report includes:

- Section headings (H1–H3)
- Tables (Idiom tables with 2 columns: Đặc điểm / Chi tiết)
- Inline images referenced as `![caption](relative/path.png)`
- Bold text, italic text, bullet lists
- Vietnamese Unicode text throughout

You need to convert it to a properly formatted `.docx` file using Python (`python-docx`), matching the academic report style of the template.

## Target formatting requirements

- **Page margins:** 2 cm top/bottom, 2.5 cm left/right
- **Body font:** Times New Roman 12 pt
- **H1 headings:** Times New Roman 14 pt Bold (Task-level)
- **H2 headings:** Times New Roman 13 pt Bold (section-level e.g. 5.1, 5.2)
- **H3 headings:** Times New Roman 12 pt Bold (A/B/C subsections)
- **Table headers (bold key column):** left column bold, right column normal
- **Table style:** `Table Grid`
- **Images:** centered, width = 5.5 inches, italic caption below (11 pt)
- **Bullet lists:** use `List Bullet` style
- **Bold/italic inline:** preserve from markdown (`**text**` → bold, `*text*` → italic)

## Image path mapping

All images are in `C:\Users\Duy\Desktop\dvfinal\docs\tableau\`. The markdown uses relative paths like:

```
../docs/tableau/Task 5.1 - Price Distribution by Borough.png
../docs/tableau/Task 5.2 - Median Price by Borough.png
../docs/tableau/Task 6.1 - Price Outlier Map.png
../docs/tableau/Task 6.2 - Price vs Rating.png
../docs/tableau/Task 7.1 - Price per Person by Borough.png
../docs/tableau/Task 7.2 - Accommodates vs Price per Perso.png
../docs/tableau/Task 8.1 - Monthly Occupancy Rate.png
../docs/tableau/Task 8.2 - Heatmap Occupancy.png
```

Resolve them to absolute Windows paths at runtime using:
```python
import os
BASE_DIR = r'C:\Users\Duy\Desktop\dvfinal'
img_path = os.path.join(BASE_DIR, 'docs', 'tableau', filename)
```

## Parsing strategy

Parse `report.md` line by line:

1. **`# text`** → H1 heading (bold 14pt)
2. **`## text`** → H2 heading (bold 13pt)
3. **`### text`** → H3 heading (bold 12pt)
4. **`#### text`** → subheading (bold 12pt, smaller space)
5. **`| col | col |` + `|---|---|`** → detect table block, collect all rows until blank line, render as `doc.add_table()`
6. **`![caption](path)`** → extract path, call `doc.add_picture()` + italic caption paragraph
7. **`- text`** or **`* text`** → bullet (`List Bullet` style)
8. **`**text**`** inside paragraph → bold run; **`*text*`** → italic run (use regex split)
9. Blank line → skip (paragraph spacing handles gaps)
10. Any other non-empty line → normal paragraph

## Inline bold/italic parsing

Use this helper to split a line into runs:

```python
import re

def add_formatted_runs(paragraph, text, base_size=12):
    # Split on **bold** and *italic* markers
    parts = re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        elif part.startswith('*') and part.endswith('*'):
            run = paragraph.add_run(part[1:-1])
            run.italic = True
        else:
            paragraph.add_run(part)
        # set font for last run
        for run in paragraph.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(base_size)
```

## Table parsing

Markdown tables in this file always have exactly 2 columns: `| key | value |`.

```python
def parse_md_table(lines):
    """lines: list of '| col | col |' strings (excluding separator row)"""
    rows = []
    for line in lines:
        if line.startswith('|---'):
            continue
        cols = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cols) >= 2:
            rows.append((cols[0], cols[1]))
    return rows

def render_table(doc, rows):
    table = doc.add_table(rows=len(rows), cols=2)
    table.style = 'Table Grid'
    for i, (key, val) in enumerate(rows):
        # key cell — bold
        cell0 = table.rows[i].cells[0]
        cell0.text = ''
        r = cell0.paragraphs[0].add_run(key.replace('**',''))
        r.bold = True; r.font.name = 'Times New Roman'; r.font.size = Pt(12)
        # value cell — handle <br> as newline
        cell1 = table.rows[i].cells[1]
        cell1.text = ''
        val_clean = val.replace('<br>', '\n').replace('**','')
        r2 = cell1.paragraphs[0].add_run(val_clean)
        r2.font.name = 'Times New Roman'; r2.font.size = Pt(12)
    doc.add_paragraph()
```

## Output

Save to: `C:\Users\Duy\Desktop\dvfinal\generate_report\Bảo Duy.docx`

Run with: `C:\dev_env\miniconda\python.exe convert_md_to_docx.py`

## Complete script template

```python
import sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from docx import Document
from docx.shared import Pt, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

BASE_DIR = r'C:\Users\Duy\Desktop\dvfinal'
MD_FILE  = os.path.join(BASE_DIR, 'generate_report', 'report.md')
OUT_FILE = os.path.join(BASE_DIR, 'generate_report', 'Bảo Duy.docx')
IMG_DIR  = os.path.join(BASE_DIR, 'docs', 'tableau')

doc = Document()

# Margins
section = doc.sections[0]
section.top_margin    = Cm(2)
section.bottom_margin = Cm(2)
section.left_margin   = Cm(2.5)
section.right_margin  = Cm(2.5)

# Normal style
style_normal = doc.styles['Normal']
style_normal.font.name = 'Times New Roman'
style_normal.font.size = Pt(12)

def set_run(run, bold=False, italic=False, size=12):
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic

def add_runs(para, text, size=12):
    """Parse **bold** and *italic* and add runs."""
    parts = re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            r = para.add_run(part[2:-2])
            set_run(r, bold=True, size=size)
        elif part.startswith('*') and part.endswith('*'):
            r = para.add_run(part[1:-1])
            set_run(r, italic=True, size=size)
        else:
            r = para.add_run(part)
            set_run(r, size=size)

def add_heading(text, level):
    sizes = {1: 14, 2: 13, 3: 12, 4: 12}
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(4)
    r = p.add_run(text)
    set_run(r, bold=True, size=sizes.get(level, 12))

def add_image_block(rel_path, caption):
    # Extract filename from rel path
    fname = os.path.basename(rel_path)
    abs_path = os.path.join(IMG_DIR, fname)
    try:
        doc.add_picture(abs_path, width=Inches(5.5))
    except Exception as e:
        p = doc.add_paragraph()
        p.add_run(f'[Image not found: {fname}]').italic = True
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(caption)
    set_run(r, italic=True, size=11)

def render_md_table(table_lines):
    rows = []
    for line in table_lines:
        if re.match(r'\|[-: |]+\|', line):
            continue
        cols = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cols) >= 2:
            rows.append((cols[0], cols[1]))
    if not rows:
        return
    tbl = doc.add_table(rows=len(rows), cols=2)
    tbl.style = 'Table Grid'
    for i, (key, val) in enumerate(rows):
        c0 = tbl.rows[i].cells[0]
        c0.text = ''
        rk = c0.paragraphs[0].add_run(re.sub(r'\*+', '', key))
        set_run(rk, bold=True)
        c1 = tbl.rows[i].cells[1]
        c1.text = ''
        val_clean = val.replace('<br>', '\n')
        rv = c1.paragraphs[0].add_run(re.sub(r'\*+', '', val_clean))
        set_run(rv)
    doc.add_paragraph()

# ---- Parse markdown ----
with open(MD_FILE, encoding='utf-8') as f:
    lines = f.readlines()

i = 0
while i < len(lines):
    line = lines[i].rstrip('\n')

    # Headings
    m = re.match(r'^(#{1,4})\s+(.*)', line)
    if m:
        level = len(m.group(1))
        add_heading(m.group(2), level)
        i += 1
        continue

    # Table block
    if line.startswith('|'):
        block = []
        while i < len(lines) and lines[i].startswith('|'):
            block.append(lines[i].rstrip('\n'))
            i += 1
        render_md_table(block)
        continue

    # Image
    m = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', line)
    if m:
        caption = m.group(1)
        rel     = m.group(2)
        add_image_block(rel, caption)
        i += 1
        continue

    # Italic-only caption line (starts with *)
    if re.match(r'^\*[^*].*\*$', line):
        # skip — caption already added with image
        i += 1
        continue

    # Horizontal rule
    if re.match(r'^---+$', line.strip()):
        i += 1
        continue

    # Bullet
    m = re.match(r'^[-*]\s+(.*)', line)
    if m:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        add_runs(p, m.group(1))
        i += 1
        continue

    # Blank line
    if line.strip() == '':
        i += 1
        continue

    # Normal paragraph
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    add_runs(p, line)
    i += 1

doc.save(OUT_FILE)
print(f'Saved: {OUT_FILE}')
```
