from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.paragraph import Paragraph

# Crie um arquivo PDF em branco
doc = SimpleDocTemplate("MultiColumnRegularColumnsPDF.pdf", pagesize=letter)

# Crie um estilo para o parágrafo
styles = getSampleStyleSheet()
styleN = styles["Normal"]

# Crie uma lista de elementos para adicionar ao documento
elements = []

for i in range(30):
    elements.append(Paragraph(str(i + 1), styleN))
    elements.append(Paragraph("text text text text text text text text text text text", styleN))

# Crie o documento e adicione os elementos
story = []
for element in elements:
    story.append(element)
    if isinstance(element, PageBreak):
        story.append(PageBreak())

doc.build(story)
