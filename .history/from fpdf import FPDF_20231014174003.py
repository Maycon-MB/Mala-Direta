from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.units import inch

data = [
    ["Nome 1", "Logradouro 1", "Número 1", "Complemento 1"],
    ["Nome 2", "Logradouro 2", "Número 2", "Complemento 2"],
    ["Nome 3", "Logradouro 3", "Número 3", "Complemento 3"]
]

doc = SimpleDocTemplate("MultiColumnAdjustedSpacing.pdf", pagesize=letter)
styles = getSampleStyleSheet()
style = styles["Normal"]

# Ajuste o espaçamento entre as linhas
style.leading = 12  # Ajuste conforme necessário

elements = []

for item in data:
    text = "\n".join(item)
    para = Paragraph(text, style)
    elements.append(para)

doc.build(elements)
