from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, PageBreak, Paragraph
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

def generate_pdf(file_path, data):
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    elements = []

    # Estilo para o conteúdo
    styles = getSampleStyleSheet()
    style = styles["Normal"]

    # Divide os dados em páginas
    items_per_page = 27
    pages = [data[i:i+items_per_page] for i in range(0, len(data), items_per_page)]

    for page_data in pages:
        if pages.index(page_data) > 0:
            elements.append(PageBreak())

        data_table = []

        for item in page_data:
            data_table.append([Paragraph(item, style)])

        # Crie uma tabela com 3 colunas
        table = Table(data_table, colWidths=2.3*inch, spaceBefore=10, spaceAfter=10)
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)

    doc.build(elements)

data = [
    "Nome 1\nLogradouro 1\nNúmero 1\nComplemento 1",
    "Nome 2\nLogradouro 2\nNúmero 2\nComplemento 2",
    "Nome 3\nLogradouro 3\nNúmero 3\nComplemento 3",
    # Adicione mais itens conforme necessário
]

generate_pdf("MultiColumnAdjustedSpacing.pdf", data)
