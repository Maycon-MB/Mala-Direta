from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Função para criar o PDF com 27 cadastros por página
def create_pdf(data):
    doc = SimpleDocTemplate("cadastros.pdf", pagesize=A4)
    elements = []

    # Tamanho da página
    page_width, page_height = A4

    # Número de itens por página
    num_items_per_page = 27

    # Tamanho das células na tabela
    cell_width = page_width / 3
    cell_height = page_height / 9

    # Crie uma lista de dados de exemplo (substitua pelo seu próprio conteúdo)
    data = [['Item {}'.format(i + 1) for i in range(num_items_per_page)]]

    # Repita os dados para preencher a página
    data *= 3  # Repetir 3 vezes para preencher 3 colunas

    # Crie uma tabela com os dados
    table = Table(data, colWidths=[cell_width] * 3, rowHeights=[cell_height] * 9)

    # Estilo da tabela
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)

    elements.append(table)

    doc.build(elements)

create_pdf([])
