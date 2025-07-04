import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# Türkçe karakterler için uygun fontu yükle
pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))

# CSV dosyasını oku (utf-8 ile)
df = pd.read_csv("veriler.csv", encoding="utf-8")

# Boş MİKTAR hücrelerine "" (boş string) koy
df.fillna("", inplace=True)

# Miktar sütunu yoksa elle ekle (boş değerle)
if 'MİKTAR' not in df.columns:
    df.insert(2, 'MİKTAR', "")

# Tablo verisi (başlık + içerik)
veri = [list(df.columns)] + df.values.tolist()

# PDF belgesi oluştur
pdf = SimpleDocTemplate("cikti.pdf", pagesize=A4)
table = Table(veri, repeatRows=1, colWidths=[90, 250, 60, 60])

# Stil tanımla
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

# PDF dosyasına yaz
pdf.build([table])
print("✅ PDF başarıyla oluşturuldu: cikti.pdf")
