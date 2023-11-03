from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak

def generate_pdf(file_path, data):
    doc = SimpleDocTemplate(file_path, pagesize=landscape(letter))
    elements = []
    col_width = doc.width / 3
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    for i, item in enumerate(data):
        if i > 0 and i % 27 == 0:
            elements.append(PageBreak())

        col = i % 3
        row = (i % 27) // 3
        table_data = [[item]]
        t = Table(table_data, colWidths=col_width, rowHeights=[1.2 * inch])
        t.setStyle(table_style)
        elements.append(t)

    doc.build(elements)

data = [
    "Nome 1\nLogradouro 1\nNúmero 1\nComplemento 1",
    "Nome 2\nLogradouro 2\nNúmero 2\nComplemento 2",
    "Nome 3\nLogradouro 3\nNúmero 3\nComplemento 3",
    # Adicione mais itens conforme necessário
]

generate_pdf("MultiColumnAdjustedSpacing.pdf", data)
