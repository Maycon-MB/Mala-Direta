from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.paragraph import Paragraph

# Função para criar uma nova página após 27 itens
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
    elements.append([Paragraph(str(i + 1), styleN)])
    elements.append([Paragraph("text text text text text text text text text text text", styleN)])

    item_count += 1
    page_break = add_page_break(item_count, max_items_per_page)
    if page_break:
        elements.append([page_break])

# Divida a lista em 3 colunas
num_columns = 1  # Agora, teremos apenas uma coluna por página
column_height = 1  # Cada item ocupa uma página inteira
columns = []

for i in range(num_columns):
    start = i * column_height
    end = (i + 1) * column_height
    column = elements[start:end]
    columns.append(column)

# Crie uma tabela com as colunas
table_data = [[Table(column, colWidths=[500]) for column in columns]]
table = Table(table_data, colWidths=[500])

# Crie o documento e adicione a tabela
story = [table]
doc.build(story)
