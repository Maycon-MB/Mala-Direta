from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Função para criar o PDF com várias colunas
def create_multi_column_pdf(filename):
    # Crie um objeto SimpleDocTemplate para o PDF
    doc = SimpleDocTemplate(filename, pagesize=letter)

    # Crie uma lista para armazenar os elementos do PDF
    elements = []

    # Estilos de parágrafo
    styles = getSampleStyleSheet()

    # Conteúdo de exemplo para as colunas
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
    
    # Crie três parágrafos com o conteúdo de exemplo
    paragraph1 = Paragraph(text, styles["Normal"])
    paragraph2 = Paragraph(text, styles["Normal"])
    paragraph3 = Paragraph(text, styles["Normal"])

    # Adicione os parágrafos à lista de elementos
    elements.append(paragraph1)
    elements.append(Spacer(1, 12))
    elements.append(paragraph2)
    elements.append(Spacer(1, 12))
    elements.append(paragraph3)

    # Crie o documento PDF
    doc.build(elements)

# Chame a função para criar o PDF com várias colunas
create_multi_column_pdf("exemplo_multi_coluna.pdf")
