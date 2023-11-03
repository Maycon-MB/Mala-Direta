from fpdf import FPDF

class PDF(FPDF):
    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, 0, 1, "C")

pdf = PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=0)
pdf.set_font("Arial", size=12)

# Tamanho do retângulo e espaçamento
rect_width = 60
rect_height = 40
spacing = 10

# Coordenadas iniciais
x = 10
y = 10

for i in range(27):
    if i % 3 == 0 and i != 0:
        x = 10
        y += rect_height + spacing
    pdf.rect(x, y, rect_width, rect_height)
    x += rect_width + spacing

pdf_filename = "retangulos.pdf"
pdf.output(pdf_filename)

print(f"PDF com retângulos criado com sucesso: {pdf_filename}")
