from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, PageTemplate, Frame, PageBreak, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

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

# Defina o número de colunas desejado
num_columns = 3

# Divida a largura da página igualmente entre as colunas
column_width = doc.width / num_columns

# Crie frames para cada coluna
frames = [Frame(
    x=col_idx * column_width,
    y=0,
    width=column_width,
    height=doc.height,
    leftPadding=10,
    rightPadding=10,
    showBoundary=1,  # Define para 1 para mostrar as bordas da frame (opcional)
) for col_idx in range(num_columns)]

for frame in frames:
    frame.add_from_list(elements, doc)

story.append(frames)

doc.build(story)
