from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

def generate_pdf(file_path, data):
    doc = SimpleDocTemplate(file_path, pagesize=landscape(letter))
    elements = []

    # Define o estilo dos parágrafos
    styles = getSampleStyleSheet()
    styleN = styles["Normal"]

    # Crie uma lista de elementos para adicionar ao documento
    for i in range(len(data)):
        elements.append([Paragraph(data[i], styleN)])

    # Divida a lista em 3 colunas
    num_columns = 3
    column_height = len(data) // num_columns
    columns = []

    for i in range(num_columns):
        start = i * column_height
        end = (i + 1) * column_height
        column = elements[start:end]
        columns.append(column)

    # Crie uma tabela com as colunas
    table_data = [[Table(column, colWidths=[doc.width / num_columns]) for column in columns]]
    table = Table(table_data, colWidths=[doc.width / num_columns] * num_columns)
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
    doc.build([table])

# Exemplo de uso
data = [f"Item {i+1}" for i in range(81)]  # 3 colunas x 3 linhas x 9 páginas
generate_pdf("MultiColumnRegularColumnsPDF.pdf", data)
