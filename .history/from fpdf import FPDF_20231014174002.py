from fpdf import FPDF
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.units import inch

# Dados para as colunas
data = [
    "Nome 1\nLogradouro 1\nNúmero 1\nComplemento 1",
    "Nome 2\nLogradouro 2\nNúmero 2\nComplemento 2",
    "Nome 3\nLogradouro 3\nNúmero 3\nComplemento 3",
]

# Configuração das colunas com o FPDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", size=12)
page_width = pdf.w
page_height = pdf.h
item_width = page_width / 3
item_height = page_height / 9

# Adicione os dados às colunas com FPDF
for i, item in enumerate(data):
    if i > 0 and i % 3 == 0:
        pdf.add_page()
    col = i % 3
    row = i // 3
    x = col * item_width
    y = row * item_height
    pdf.set_xy(x, y)
    pdf.multi_cell(item_width, item_height / 3, item, border=0, align="C")

pdf_filename = "MultiColumnAdjustedSpacing.pdf"
pdf.output(pdf_filename)

# Configuração do espaçamento entre as linhas com o ReportLab
doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
styles = getSampleStyleSheet()
style = styles["Normal"]

# Ajuste o espaçamento entre as linhas no ReportLab
style.leading = 12  # Ajuste conforme necessário

elements = [Paragraph(text, style) for text in data]

doc.build(elements)
