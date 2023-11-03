from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, PageBreak, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

def generate_pdf(file_path, data):
    doc = SimpleDocTemplate(file_path, pagesize=landscape(letter))
    story = []
    
    styles = getSampleStyleSheet()
    style = styles["Normal"]

    items_per_page = 27
    page_items = []

    for item in data:
        page_items.append(item)
        if len(page_items) == items_per_page:
            story.extend(create_page(page_items, style))
            page_items = []

    if page_items:
        story.extend(create_page(page_items, style))

    doc.build(story)

def create_page(items, style):
    page = []

    for i in range(3):
        col_items = items[i::3]
        for j in range(3):
            row_items = col_items[j::3]
            if row_items:
                for item in row_items:
                    p = Paragraph(item, style)
                    page.append(p)
                page.append(Spacer(1, 12))

    page.append(PageBreak())
    return page

data = [
    "Nome 1\nLogradouro 1\nNúmero 1\nComplemento 1",
    "Nome 2\nLogradouro 2\nNúmero 2\nComplemento 2",
    "Nome 3\nLogradouro 3\nNúmero 3\nComplemento 3",
    # Adicione mais itens conforme necessário
]

generate_pdf("MultiColumnAdjustedSpacing.pdf", data)
