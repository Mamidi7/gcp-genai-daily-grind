import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

# Create dummy data
data = {
    'Movie': ['Baahubali 2', 'RRR', 'Kalki 2898 AD', 'Pushpa 2', 'Salaar'],
    'Day 1 (Cr)': [217, 223, 191, 175, 178],
    'Day 2 (Cr)': [150, 140, 110, 120, 115],
    'Day 3 (Cr)': [160, 155, 125, 130, 120],
    'Total Weekend (Cr)': [527, 518, 426, 425, 413],
    'Verdict': ['All Time Blockbuster', 'Blockbuster', 'Blockbuster', 'Super Hit', 'Hit']
}

df = pd.DataFrame(data)

# Create Output Directory
output_dir = os.path.expanduser('~/projects/box_office_reports')
os.makedirs(output_dir, exist_ok=True)

# 1. Save as Excel
excel_path = os.path.join(output_dir, 'box_office_report.xlsx')
df.to_excel(excel_path, index=False)
print(f"Excel saved to: {excel_path}")

# 2. Save as PDF
pdf_path = os.path.join(output_dir, 'box_office_report.pdf')
doc = SimpleDocTemplate(pdf_path, pagesize=letter)
elements = []

styles = getSampleStyleSheet()
title = Paragraph("<b>Mass Box Office Report 2026</b>", styles['Title'])
elements.append(title)
elements.append(Spacer(1, 12))

# Convert DataFrame to list of lists for ReportLab
table_data = [df.columns.to_list()] + df.values.tolist()

# Create Table
t = Table(table_data)
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

elements.append(t)
doc.build(elements)
print(f"PDF saved to: {pdf_path}")
