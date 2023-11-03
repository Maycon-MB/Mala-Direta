from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, PageTemplate, Frame, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Função para criar um PDF de várias colunas
def create_multi_column_pdf(filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)

    # Estilo de parágrafo
    styles = getSampleStyleSheet()

    # Crie um PageTemplate com 3 colunas
    frame1 = Frame(doc.leftMargin, doc.bottomMargin, doc.width / 3 - 6, doc.height, id='col1')
    frame2 = Frame(doc.leftMargin + doc.width / 3, doc.bottomMargin, doc.width / 3 - 6, doc.height, id='col2')
    frame3 = Frame(doc.leftMargin + 2 * doc.width / 3, doc.bottomMargin, doc.width / 3, doc.height, id='col3')

    # Lista para armazenar os elementos do PDF
    elements = []

    # Crie parágrafos para cada coluna
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
    paragraph1 = Paragraph(text, styles["Normal"])
    paragraph2 = Paragraph(text, styles["Normal"])
    paragraph3 = Paragraph(text, styles["Normal"])

    # Adicione os parágrafos aos elementos do PDF em suas posições nas colunas
    elements.extend([Spacer(1, 12), paragraph1])
    elements.extend([Spacer(1, 12), paragraph2])
    elements.extend([Spacer(1, 12), paragraph3])

    # Associe o modelo da página aos elementos do PDF
    doc.addPageTemplates([PageTemplate(id='multi_column', frames=[frame1, frame2, frame3])])

    # Construa o documento PDF
    doc.build(elements)

# Chame a função para criar o PDF de várias colunas
create_multi_column_pdf("exemplo_multi_coluna.pdf")
