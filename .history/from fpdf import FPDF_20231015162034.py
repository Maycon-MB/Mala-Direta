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
            pdf.multi_cell(item_width, item_height / 3, line, border=0, align="L")
            y += item_height / 3 - line_spacing  # Reduz o espaço vertical entre as linhas

    pdf.output(file_path)

fake_data = [
    "Nome 1\nLogradouro 1\nNúmero 1\nComplemento 1",
    "Nome 2\nLogradouro 2\nNúmero 2\nComplemento 2",
    "Nome 3\nLogradouro 3\nNúmero 3\nComplemento 3",
    "Nome 4\nLogradouro 4\nNúmero 4\nComplemento 4",
    "Nome 5\nLogradouro 5\nNúmero 5\nComplemento 5",
    "Nome 6\nLogradouro 6\nNúmero 6\nComplemento 6",
    "Nome 7\nLogradouro 7\nNúmero 7\nComplemento 7",
    "Nome 8\nLogradouro 8\nNúmero 8\nComplemento 8",
    "Nome 9\nLogradouro 9\nNúmero 9\nComplemento 9",
    "Nome 10\nLogradouro 10\nNúmero 10\nComplemento 10",
    "Nome 11\nLogradouro 11\nNúmero 11\nComplemento 11",
    "Nome 12\nLogradouro 12\nNúmero 12\nComplemento 12",
    "Nome 13\nLogradouro 13\nNúmero 13\nComplemento 13",
    "Nome 14\nLogradouro 14\nNúmero 14\nComplemento 14",
    "Nome 15\nLogradouro 15\nNúmero 15\nComplemento 15",
    "Nome 16\nLogradouro 16\nNúmero 16\nComplemento 16",
    "Nome 17\nLogradouro 17\nNúmero 17\nComplemento 17",
    "Nome 18\nLogradouro 18\nNúmero 18\nComplemento 18",
    "Nome 19\nLogradouro 19\nNúmero 19\nComplemento 19",
    "Nome 20\nLogradouro 20\nNúmero 20\nComplemento 20",
    "Nome 21\nLogradouro 21\nNúmero 21\nComplemento 21",
    "Nome 22\nLogradouro 22\nNúmero 22\nComplemento 22",
    "Nome 23\nLogradouro 23\nNúmero 23\nComplemento 23",
    "Nome 24\nLogradouro 24\nNúmero 24\nComplemento 24",
    "Nome 25\nLogradouro 25\nNúmero 25\nComplemento 25",
    "Nome 26\nLogradouro 26\nNúmero 26\nComplemento 26",
    "Nome 27\nLogradouro 27\nNúmero 27\nComplemento 27",
]

generate_pdf("MultiColumnAdjustedSpacing.pdf", fake_data)

