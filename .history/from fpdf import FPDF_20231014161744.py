from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, PageBreak
from reportlab.platypus.frames import Frame
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Função para criar uma nova página após um número específico de itens
def add_page_break(item_count, max_items_per_page):
    if item_count % max_items_per_page == 0:
        return PageBreak()
    return None

# Crie um arquivo PDF em branco
doc = SimpleDocTemplate("MultiColumnRegularColumnsPDF.pdf", pagesize=letter)

# Crie um estilo para o parágrafo
styles = getSampleStyleSheet()
styleN = styles["Normal"]

# Crie uma lista de elementos para adicionar ao documento
elements = []

max_items_per_page = 27
item_count = 0

for i in range(30):
    elements.append(Paragraph(str(i + 1), styleN))
    elements.append(Paragraph("text text text text text text text text text text text", styleN))

    item_count += 1
    page_break = add_page_break(item_count, max_items_per_page)
    if page_break:
        elements.append(page_break)

# Divida os elementos em colunas
num_columns = 3
column_height = len(elements) // num_columns
columns = []

for i in range(num_columns):
    start = i * column_height
    end = (i + 1) * column_height
    column = elements[start:end]
    columns.append(column)

# Crie o documento e adicione as colunas
story = []
for i in range(column_height):
    for column in columns:
        if i < len(column):
            story.append(column[i])
    story.append(PageBreak())

doc.build(story)
