import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, Preformatted
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

MD_FILE  = 'Nebula_Project_Report.md'
PDF_FILE = 'Nebula_Project_Report.pdf'

# ── Colour palette ────────────────────────────────────────────────────────────
C_BLACK   = colors.HexColor('#0c0c0c')
C_WHITE   = colors.white
C_GREEN   = colors.HexColor('#00aa33')
C_LGREEN  = colors.HexColor('#e8f5e9')
C_GRAY    = colors.HexColor('#444444')
C_LGRAY   = colors.HexColor('#f5f5f5')
C_DGRAY   = colors.HexColor('#cccccc')
C_ACCENT  = colors.HexColor('#1b5e20')
C_HEAD_BG = colors.HexColor('#1b5e20')
C_ROW_ALT = colors.HexColor('#f1f8f1')

PAGE_W, PAGE_H = A4
ML = MR = 2.2 * cm
MT = MB = 2.0 * cm

# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

cover_title = S('CoverTitle',
    fontName='Helvetica-Bold', fontSize=28, leading=34,
    textColor=C_WHITE, alignment=TA_CENTER, spaceAfter=8)

cover_sub = S('CoverSub',
    fontName='Helvetica', fontSize=13, leading=18,
    textColor=colors.HexColor('#ccffcc'), alignment=TA_CENTER, spaceAfter=6)

cover_meta = S('CoverMeta',
    fontName='Helvetica', fontSize=10, leading=14,
    textColor=C_DGRAY, alignment=TA_CENTER, spaceAfter=4)

h1 = S('H1',
    fontName='Helvetica-Bold', fontSize=16, leading=20,
    textColor=C_ACCENT, spaceBefore=18, spaceAfter=6,
    borderPad=4)

h2 = S('H2',
    fontName='Helvetica-Bold', fontSize=13, leading=17,
    textColor=C_ACCENT, spaceBefore=14, spaceAfter=4)

h3 = S('H3',
    fontName='Helvetica-BoldOblique', fontSize=11, leading=15,
    textColor=C_GRAY, spaceBefore=10, spaceAfter=3)

body = S('Body',
    fontName='Helvetica', fontSize=10, leading=15,
    textColor=C_BLACK, spaceBefore=2, spaceAfter=4,
    alignment=TA_JUSTIFY)

bullet_style = S('Bullet',
    fontName='Helvetica', fontSize=10, leading=14,
    textColor=C_BLACK, leftIndent=18, bulletIndent=6,
    spaceBefore=1, spaceAfter=1)

code_style = S('Code',
    fontName='Courier', fontSize=8.5, leading=12,
    textColor=colors.HexColor('#1a1a1a'),
    backColor=colors.HexColor('#f4f4f4'),
    borderColor=colors.HexColor('#dddddd'),
    borderWidth=0.5, borderPad=6,
    leftIndent=10, spaceBefore=6, spaceAfter=6)

toc_style = S('TOC',
    fontName='Helvetica', fontSize=10, leading=16,
    textColor=C_BLACK, leftIndent=14, spaceBefore=1, spaceAfter=1)

abstract_style = S('Abstract',
    fontName='Helvetica-Oblique', fontSize=10, leading=15,
    textColor=C_GRAY, spaceBefore=2, spaceAfter=4,
    alignment=TA_JUSTIFY, leftIndent=20, rightIndent=20)

# ── Header / Footer ───────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    # Header bar
    canvas.setFillColor(C_HEAD_BG)
    canvas.rect(ML, PAGE_H - MT + 2, PAGE_W - ML - MR, 18, fill=1, stroke=0)
    canvas.setFont('Helvetica-Bold', 8)
    canvas.setFillColor(C_WHITE)
    canvas.drawString(ML + 4, PAGE_H - MT + 7, 'NEBULA — AI-Powered Virtual Assistant')
    canvas.drawRightString(PAGE_W - MR - 4, PAGE_H - MT + 7, 'Project Report')
    # Footer line
    canvas.setStrokeColor(C_GREEN)
    canvas.setLineWidth(0.8)
    canvas.line(ML, MB - 6, PAGE_W - MR, MB - 6)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(C_GRAY)
    canvas.drawCentredString(PAGE_W / 2, MB - 16, f'Page {doc.page}')
    canvas.restoreState()

def on_first_page(canvas, doc):
    canvas.saveState()
    # Full dark cover background
    canvas.setFillColor(C_BLACK)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # Green accent band at top
    canvas.setFillColor(C_HEAD_BG)
    canvas.rect(0, PAGE_H - 60, PAGE_W, 60, fill=1, stroke=0)
    # Green accent band at bottom
    canvas.rect(0, 0, PAGE_W, 50, fill=1, stroke=0)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(C_WHITE)
    canvas.drawCentredString(PAGE_W / 2, 20, 'AI / Data Science Internship  —  Swecha Software Pvt Ltd')
    canvas.restoreState()

# ── Markdown parser → ReportLab flowables ─────────────────────────────────────
def escape(t):
    return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def inline(t):
    t = escape(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'\*(.+?)\*',     r'<i>\1</i>', t)
    t = re.sub(r'`(.+?)`',       r'<font face="Courier">\1</font>', t)
    return t

def parse_table(lines):
    rows = []
    for ln in lines:
        if re.match(r'^\s*\|[-| :]+\|\s*$', ln):
            continue
        cells = [c.strip() for c in ln.strip().strip('|').split('|')]
        rows.append(cells)
    if not rows:
        return []
    col_count = max(len(r) for r in rows)
    col_w = (PAGE_W - ML - MR - 20) / col_count

    tdata = []
    for i, row in enumerate(rows):
        while len(row) < col_count:
            row.append('')
        if i == 0:
            tdata.append([Paragraph(f'<b>{escape(c)}</b>', body) for c in row])
        else:
            tdata.append([Paragraph(escape(c), body) for c in row])

    ts = TableStyle([
        ('BACKGROUND',  (0,0), (-1,0),  C_HEAD_BG),
        ('TEXTCOLOR',   (0,0), (-1,0),  C_WHITE),
        ('FONTNAME',    (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',    (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_WHITE, C_ROW_ALT]),
        ('GRID',        (0,0), (-1,-1), 0.4, C_DGRAY),
        ('TOPPADDING',  (0,0), (-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING',(0,0), (-1,-1), 6),
        ('VALIGN',      (0,0), (-1,-1), 'TOP'),
    ])
    t = Table(tdata, colWidths=[col_w]*col_count, repeatRows=1)
    t.setStyle(ts)
    return [Spacer(1, 6), t, Spacer(1, 8)]

def md_to_flowables(text):
    story = []
    lines = text.splitlines()
    i = 0
    in_code  = False
    code_buf = []
    tbl_buf  = []
    in_tbl   = False

    while i < len(lines):
        ln = lines[i]

        # --- code block ---
        if ln.strip().startswith('```'):
            if in_code:
                in_code = False
                story.append(Preformatted('\n'.join(code_buf), code_style))
                code_buf = []
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_buf.append(ln)
            i += 1
            continue

        # --- table ---
        if ln.startswith('|'):
            tbl_buf.append(ln)
            i += 1
            continue
        if tbl_buf:
            story.extend(parse_table(tbl_buf))
            tbl_buf = []

        # --- headings ---
        m = re.match(r'^(#{1,3})\s+(.*)', ln)
        if m:
            lvl  = len(m.group(1))
            text_h = m.group(2).strip()
            if lvl == 1:
                # Chapter heading with green bar
                story.append(Spacer(1, 10))
                story.append(HRFlowable(width='100%', thickness=2,
                                        color=C_GREEN, spaceAfter=4))
                story.append(Paragraph(inline(text_h), h1))
                story.append(HRFlowable(width='100%', thickness=0.5,
                                        color=C_DGRAY, spaceBefore=2, spaceAfter=6))
            elif lvl == 2:
                story.append(Paragraph(inline(text_h), h2))
            else:
                story.append(Paragraph(inline(text_h), h3))
            i += 1
            continue

        # --- horizontal rule ---
        if re.match(r'^---+\s*$', ln):
            story.append(HRFlowable(width='100%', thickness=0.8,
                                    color=C_DGRAY, spaceBefore=6, spaceAfter=6))
            i += 1
            continue

        # --- bullet ---
        m = re.match(r'^[-*]\s+(.*)', ln)
        if m:
            story.append(Paragraph('• ' + inline(m.group(1)), bullet_style))
            i += 1
            continue

        # --- numbered list ---
        m = re.match(r'^\d+\.\s+(.*)', ln)
        if m:
            story.append(Paragraph('• ' + inline(m.group(1)), bullet_style))
            i += 1
            continue

        # --- blank line ---
        if ln.strip() == '':
            story.append(Spacer(1, 4))
            i += 1
            continue

        # --- plain paragraph ---
        story.append(Paragraph(inline(ln), body))
        i += 1

    if tbl_buf:
        story.extend(parse_table(tbl_buf))

    return story

# ── Cover page ────────────────────────────────────────────────────────────────
def make_cover():
    return [
        Spacer(1, 3.5 * cm),
        Paragraph('NEBULA', cover_title),
        Paragraph('AI-Powered Virtual Assistant', cover_sub),
        Spacer(1, 0.6 * cm),
        HRFlowable(width='60%', thickness=1.5, color=C_GREEN,
                   hAlign='CENTER', spaceBefore=4, spaceAfter=12),
        Spacer(1, 0.4 * cm),
        Paragraph('Project Report', cover_sub),
        Spacer(1, 1.5 * cm),
        Paragraph('Submitted By: <b>Akshara Budha</b>', cover_meta),
        Paragraph('Organization: <b>Swecha Software Pvt Ltd</b>', cover_meta),
        Paragraph('Role: AI / Data Science Intern', cover_meta),
        Paragraph('Technology: Python · PyQt5 · Anthropic Claude API', cover_meta),
        Paragraph('Platform: Windows 11', cover_meta),
        PageBreak(),
    ]

# ── Build PDF ─────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        PDF_FILE, pagesize=A4,
        leftMargin=ML, rightMargin=MR,
        topMargin=MT + 10, bottomMargin=MB + 10,
        title='Nebula — AI Virtual Assistant Project Report',
        author='Akshara Budha',
        subject='AI/Data Science Internship Project',
    )

    with open(MD_FILE, encoding='utf-8') as f:
        md_text = f.read()

    # Strip the very first H1 (cover title already on cover page)
    md_text = re.sub(r'^# .+\n', '', md_text, count=1)
    # Remove the ## ABSTRACT heading (keep content, style separately)
    md_text = re.sub(r'^## ABSTRACT\n', '## ABSTRACT\n', md_text, count=1)

    story = make_cover() + md_to_flowables(md_text)

    doc.build(story,
              onFirstPage=on_first_page,
              onLaterPages=on_page)
    print(f'PDF saved: {PDF_FILE}')

if __name__ == '__main__':
    build()
