from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, PageBreak, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.units import inch

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

# Crie o documento e adicione as colunas
story = []
col_width = doc.width / 3  # Divida a largura da página em 3 colunas
col_height = doc.height - inch  # Reduza a altura da coluna em uma polegada

columns = [elements[i:i+2] for i in range(0, len(elements), 2)]
for column in columns:
    story.extend(column)
    story.append(Spacer(1, col_height))  # Adicione espaço para ocupar a altura da página
    story.append(PageBreak())

doc.build(story)
