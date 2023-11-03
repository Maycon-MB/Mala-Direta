from fpdf import FPDF

class PDF(FPDF):
    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, 0, 1, "C")

pdf = PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=0)
pdf.set_font("Arial", size=12)

# Tamanho da página
page_width = 210
page_height = 297

# Quantidade de retângulos em cada direção
num_columns = 3
num_rows = 9

# Tamanho dos retângulos
rect_width = page_width / num_columns
rect_height = page_height / num_rows

for i in range(num_rows):
    for j in range(num_columns):
        x = j * rect_width
        y = i * rect_height
        pdf.rect(x, y, rect_width, rect_height)

pdf_filename = "retangulos.pdf"
pdf.output(pdf_filename)

print(f"PDF com retângulos preenchendo a página criado com sucesso: {pdf_filename}")
