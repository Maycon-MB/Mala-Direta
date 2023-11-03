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

# Divida a lista em 3 colunas
num_columns = 3
column_height = len(elements) // num_columns
columns = []

for i in range(num_columns):
    start = i * column_height
    end = (i + 1) * column_height
    column = elements[start:end]
    columns.append(column)

# Crie uma tabela com as colunas
col_width = 200
col_sep = 20
table_data = [[Table(column, colWidths=[col_width]) for column in columns]]
table = Table(table_data, colWidths=[col_width] * num_columns)
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
