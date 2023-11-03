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

    data = [f'Dado {i + 1}' for i in range(27)]  # Dados de exemplo

    x, y = 0, page_height  # Iniciar no canto superior esquerdo

    for i in range(27):
        c.rect(x, y - rect_height, rect_width, rect_height)
        c.setFont("Helvetica", 12)
        c.drawString(x + 5, y - rect_height + 5, data[i])

        # Avançar para a próxima posição da esquerda para a direita
        x += rect_width

        # Quando alcançamos a terceira coluna, movemos para a próxima linha
        if x >= page_width:
            x = 0
            y -= rect_height

    c.save()

create_pdf()
