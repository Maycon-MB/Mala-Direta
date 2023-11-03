from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch

# Dados fictícios
data = [f'Dado {i}' for i in range(1, 28)]

# Dividir os dados em listas de três colunas
data_columns = [data[i:i + 9] for i in range(0, len(data), 9)]

# Criar um PDF
pdf_file = "output.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=letter)

# Lista para armazenar o conteúdo da tabela
elements = []

for page_data in data_columns:
    # Criar uma tabela com três colunas
    table_data = [page_data]

    table = Table(table_data, colWidths=(2.7 * inch, 2.7 * inch, 2.7 * inch))
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)

# Construir o PDF
doc.build(elements)
