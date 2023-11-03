from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Função para criar um PDF com várias colunas
def create_multi_column_pdf(filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)

    # Estilo de parágrafo
    styles = getSampleStyleSheet()

    # Crie uma lista para armazenar os elementos do PDF
    elements = []

    # Defina o número de colunas
    num_columns = 3
    column_width = doc.width / num_columns

    # Conteúdo de exemplo para as colunas
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."

    # Crie parágrafos com o conteúdo de exemplo e posicione-os nas colunas
    for i in range(num_columns):
        column_content = Paragraph(text, styles["Normal"])
        elements.append(column_content)
        if i < num_columns - 1:
            elements.append(Spacer(1, 12))  # Espaço entre as colunas

        # Posicione cada coluna manualmente
        column_content._x = i * column_width
        column_content._y = doc.height

    # Construa o documento PDF
    doc.build(elements)

# Chame a função para criar o PDF de várias colunas
create_multi_column_pdf("exemplo_multi_coluna.pdf")
