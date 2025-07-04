import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))


df = pd.read_csv("veriler.csv", encoding="utf-8")


df.fillna("", inplace=True)


if 'MİKTAR' not in df.columns:
    df.insert(2, 'MİKTAR', "")


veri = [list(df.columns)] + df.values.tolist()

# PDF belgesi oluştur
pdf = SimpleDocTemplate("cikti.pdf", pagesize=A4)
table = Table(veri, repeatRows=1, colWidths=[90, 250, 60, 60])


stil = TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'DejaVu'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BACKGROUND', (0, 0), (-1, 0), colors.darkgray),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])
])

table.setStyle(stil)


pdf.build([table])
print("✅ PDF başarıyla oluşturuldu: cikti.pdf")
