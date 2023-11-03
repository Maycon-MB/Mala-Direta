from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus import MultiColumn, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT

# Crie um arquivo PDF em branco
output_pdf = PdfFileWriter()

# Crie um documento ReportLab
doc = SimpleDocTemplate("MultiColumnRegularColumnsPDF.pdf", pagesize=letter)

# Configure as colunas
styles = getSampleStyleSheet()
styleN = styles["Normal"]
story = []

# Crie uma lista de elementos para adicionar ao documento
elements = []

for i in range(30):
    elements.append(Paragraph(str(i + 1), styleN))
    elements.append(Paragraph("text text text text text text text text text text text", styleN))

# Divida a lista em 3 colunas
num_columns = 3
column_height = len(elements) // num_columns
columns = []

for i in range(num_columns):
    start = i * column_height
    end = (i + 1) * column_height
    column = elements[start:end]
    columns.append(MultiColumn(column, colWidth=200, colSep=20, spaceBefore=10))

# Adicione as colunas ao documento
for column in columns:
    story.append(column)
    story.append(PageBreak())

doc.build(story)

# Adicione o conteúdo do documento ReportLab ao arquivo PDF de saída
input_pdf = PdfFileReader(open("MultiColumnRegularColumnsPDF.pdf", "rb"))
output_pdf.addPage(input_pdf.getPage(0))

# Salve o arquivo PDF final
with open("MultiColumnRegularColumnsPDF.pdf", "wb") as output_file:
    output_pdf.write(output_file)
