import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os


base_path = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(base_path, "DejaVuSans.ttf")
sv_path = os.path.join(base_path, "veriler.csv")


pdfmetrics.registerFont(TTFont('DejaVu', font_path))


df = pd.read_csv(sv_path, encoding="utf-8", header=None)


col_count = len(df.columns)


default_cols = ['KOD', 'AD', 'MİKTAR', 'BİRİM', 'AÇIKLAMA']


df.columns = default_cols[:col_count]


for col in ['MİKTAR', 'AÇIKLAMA']:
    if col not in df.columns:
        df[col] = ""

df.fillna("", inplace=True)


veri = [list(df.columns)] + df.values.tolist()

pdf = SimpleDocTemplate("cikti.pdf", pagesize=A4)
col_widths = [70, 220, 50, 70, 100]  # Toplam 5 sütun varsayımı


col_widths = col_widths[:len(df.columns)]

table = Table(veri, repeatRows=1, colWidths=col_widths)

stil = TableStyle([
    ('FONTNAME', (0,0), (-1,-1), 'DejaVu'),
    ('FONTSIZE', (0,0), (-1,-1), 8),
    ('BACKGROUND', (0,0), (-1,0), colors.darkgray),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('GRID', (0,0), (-1,-1), 0.5, colors.black),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.whitesmoke, colors.lightgrey])
])

table.setStyle(stil)
pdf.build([table])

print("✅ PDF başarıyla oluşturuldu: cikti.pdf")
