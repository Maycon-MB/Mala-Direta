from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(file_path, data):
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    story = []
    
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    
    items_per_page = 27
    items = []

    for item in data:
        items.append(Paragraph(item, style))

    for i in range(0, len(items), items_per_page):
        page_items = items[i:i+items_per_page]
        col1 = page_items[0::3]
        col2 = page_items[1::3]
        col3 = page_items[2::3]

        data = [col1, col2, col3]
        table = create_table(data)
        story.append(table)
        story.append(PageBreak())

    doc.build(story)

def create_table(data):
    table_style = [
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black)
    ]

    table = []
    for col in data:
        rows = []
        for item in col:
            cell = Paragraph(item, style=getSampleStyleSheet()["Normal"])
            rows.append(cell)
        table.append(rows)

    return Table(table, style=table_style)

data = [
    "Nome 1\nLogradouro 1\nNúmero 1\nComplemento 1",
    "Nome 2\nLogradouro 2\nNúmero 2\nComplemento 2",
    "Nome 3\nLogradouro 3\nNúmero 3\nComplemento 3",
    # Adicione mais itens conforme necessário
]

generate_pdf("MultiColumnAdjustedSpacing.pdf", data)
