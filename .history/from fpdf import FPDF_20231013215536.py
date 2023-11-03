from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        pass

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 6, title, 0, 1, "C")
        self.ln(10)

    def chapter_body(self, width, height):
        self.set_fill_color(200, 220, 255)
        self.rect(self.l_margin, self.get_y(), width, height, "F")
        self.set_fill_color(255, 255, 255)

# Crie o objeto PDF
pdf = PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_font("Arial", size=12)

# Tamanho do retângulo
rect_width = 50
rect_height = 50

for i in range(27):
    if i % 3 == 0 and i != 0:
        pdf.add_page()
    
    pdf.chapter_body(rect_width, rect_height)

# Salve o PDF em um arquivo
pdf_filename = "retangulos.pdf"
pdf.output(pdf_filename)

print(f"PDF com retângulos criado com sucesso: {pdf_filename}")