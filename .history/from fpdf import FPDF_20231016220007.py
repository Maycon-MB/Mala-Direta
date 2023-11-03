from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Função para criar o PDF com 27 cadastros por página
def create_pdf():
    c = canvas.Canvas("cadastros.pdf", pagesize=A4)

    # Definir margens para zero
    c.setPageCompression(0)
    c.setPageSize(A4)

    # Tamanho da página
    page_width, page_height = A4

    # Tamanho do retângulo
    rect_width = page_width / 3  # Divide a página em 3 colunas
    rect_height = page_height / 9  # Divide a página em 9 linhas

    for i in range(3):
        for j in range(9):
            x = i * rect_width
            y = j * rect_height
            c.rect(x, y, rect_width, rect_height)

    c.save()

create_pdf()
