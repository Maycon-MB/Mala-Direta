from fpdf import FPDF

class PDF(FPDF):
    def set_line_height(self, height):
        self.ln(height)

def generate_pdf(file_path, data):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)

    page_width = pdf.w
    page_height = pdf.h
    item_width = page_width / 3
    item_height = page_height / 9

    # Ajuste o espaçamento vertical entre as linhas
    line_spacing = 5  # Ajuste conforme necessário

    for i, item in enumerate(data):
        if i > 0 and i % 27 == 0:
            pdf.add_page()

        col = i % 3
        row = (i % 27) // 3
        x = col * item_width
        y = row * item_height + 1

        lines = item.split('\n')
        for line in lines:
            pdf.set_xy(x, y)
            pdf.multi_cell(item_width, item_height / 3, line, border=0, align="C")
            y += item_height / 3 - line_spacing  # Reduz o espaço vertical entre as linhas

    pdf.output(file_path)

data = [
    "Nome 1\nLogradouro 1\nNúmero 1\nComplemento 1",
    "Nome 2\nLogradouro 2\nNúmero 2\nComplemento 2",
    "Nome 3\nLogradouro 3\nNúmero 3\nComplemento 3",
]

generate_pdf("MultiColumnAdjustedSpacing.pdf", data)
