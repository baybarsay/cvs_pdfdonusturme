import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Klasör yolları
base_path = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(base_path, "DejaVuSans.ttf")
sv_path = os.path.join(base_path, "veriler.csv")

# Fontu kaydet
pdfmetrics.registerFont(TTFont('DejaVu', font_path))

# CSV'yi oku (header=None ile)
df = pd.read_csv(sv_path, encoding="utf-8", header=None)

# Sütun sayısı
col_count = len(df.columns)

# İsimlendirme için olası sütun isimleri (İstersen arttırabilirsin)
default_cols = ['KOD', 'AD', 'MİKTAR', 'BİRİM', 'AÇIKLAMA']

# Okunan sütun sayısına göre isim ata (eğer fazla ise kes, az ise yettiği kadar)
df.columns = default_cols[:col_count]

# Gerekli sütunlar varsa yoksa ekle ve boş doldur
for col in ['MİKTAR', 'AÇIKLAMA']:
    if col not in df.columns:
        df[col] = ""

df.fillna("", inplace=True)

# Tablo verisini oluştur
veri = [list(df.columns)] + df.values.tolist()

pdf = SimpleDocTemplate("cikti.pdf", pagesize=A4)
col_widths = [70, 220, 50, 70, 100]  # Toplam 5 sütun varsayımı

# Eğer sütun sayısı 5'ten az ise genişlikleri kes
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
