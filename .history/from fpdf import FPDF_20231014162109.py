from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.paragraph import Paragraph

# Crie um arquivo PDF em branco
doc = SimpleDocTemplate("MultiColumnRegularColumnsPDF.pdf", pagesize=letter)

# Crie um estilo para o parágrafo
styles = getSampleStyleSheet()
styleN = styles["Normal"]

# Crie uma lista de elementos para adicionar ao documento
elements = []

for i in range(27):
    elements.append([Paragraph(str(i + 1), styleN)])
    elements.append([Paragraph("text text text text text text text text text text text", styleN)])

# Defina a largura da tabela para preencher a página inteira
table_width = letter[0]

# Crie a tabela com as colunas
col_width = table_width / len(elements)
table_data = [[Table(column, colWidths=[col_width]) for column in elements]]
table = Table(table_data, colWidths=[col_width] * len(elements))
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))

# Crie o documento e adicione a tabela
story = [table]
doc.build(story)
