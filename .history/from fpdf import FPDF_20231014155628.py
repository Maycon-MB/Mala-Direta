from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, PageTemplate, Frame, Column, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak

# Função para criar um PDF de várias colunas
def create_multi_column_pdf(filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)

    # Estilo de parágrafo
    styles = getSampleStyleSheet()

    # Crie um PageTemplate com 3 colunas
    frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width / 3 - 6, doc.height)
    frame2 = Frame(doc.leftMargin + doc.width / 3, doc.bottomMargin, doc.width / 3 - 6, doc.height)
    frame3 = Frame(doc.leftMargin + 2 * doc.width / 3, doc.bottomMargin, doc.width / 3 - 6, doc.height)

    # Lista para armazenar os elementos do PDF
    elements = []

    # Crie um parágrafo para cada coluna
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
    paragraph1 = [Spacer(1, 12), Paragraph(text, styles["Normal"])]
    paragraph2 = [Spacer(1, 12), Paragraph(text, styles["Normal"])]
    paragraph3 = [Spacer(1, 12), Paragraph(text, styles["Normal"])]

    # Adicione as colunas aos elementos do PDF
    elements.append(Column(paragraph1, [frame1], id='col1'))
    elements.append(Column(paragraph2, [frame2], id='col2'))
    elements.append(Column(paragraph3, [frame3], id='col3'))

    # Construa o documento PDF
    doc.build(elements)

# Chame a função para criar o PDF de várias colunas
create_multi_column_pdf("exemplo_multi_coluna.pdf")
