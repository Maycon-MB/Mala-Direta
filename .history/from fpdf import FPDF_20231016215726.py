from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Função para criar o PDF com 27 cadastros por página
def create_pdf(data):
    c = canvas.Canvas("cadastros.pdf", pagesize=letter)

    # Definir margens para zero
    c.setLeftMargin(0)
    c.setRightMargin(0)
    c.setTopMargin(0)
    c.setBottomMargin(0)

    # Tamanho da página
    page_width, page_height = letter

    # Tamanho do retângulo
    rect_width = page_width / 3  # Divide a página em 3 colunas
    rect_height = page_height / 9  # Divide a página em 9 linhas

    for i in range(3):
        for j in range(9):
            x = i * rect_width
            y = page_height - (j + 1) * rect_height
            c.rect(x, y, rect_width, rect_height, fill=1)

    c.save()

create_pdf([])