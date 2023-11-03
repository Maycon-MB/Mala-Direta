from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, PageTemplate, Frame, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_multi_column_pdf(filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)

    styles = getSampleStyleSheet()

    # Crie três colunas em um único frame
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height)
    
    # Defina o número de colunas
    num_columns = 3
    
    # Calcule a largura de cada coluna
    column_width = frame.width / num_columns
    
    # Lista para armazenar os elementos do PDF
    elements = []

    # Crie um parágrafo para cada coluna
    for i in range(num_columns):
        col_text = "Conteúdo da coluna {}".format(i+1)
        paragraph = Paragraph(col_text, styles["Normal"])
        
        # Posicione o parágrafo na coluna correta
        paragraph.wrapOn(doc, frame.width, doc.height)
        paragraph.drawOn(doc, frame.left + i * column_width, frame.top - paragraph.height)

    # Adicione o frame aos elementos do PDF
    elements.append(frame)

    # Construa o documento PDF
    doc.build(elements)

# Chame a função para criar o PDF de várias colunas
create_multi_column_pdf("exemplo_multi_coluna.pdf")
