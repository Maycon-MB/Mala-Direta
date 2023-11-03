from fpdf import FPDF
from PIL import Image

# Criar uma instância do FPDF
pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# Converter HTML para imagem (por exemplo, usando Pillow)
from weasyprint import HTML
HTML(string=html_code).write_png('html_to_image.png')

# Adicionar a imagem ao PDF
pdf.image('html_to_image.png', x=10, y=10, w=190)

# Salvar o PDF
pdf.output("output.pdf")
