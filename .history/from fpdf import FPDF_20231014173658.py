from fpdf import FPDF

def generate_pdf(file_path, data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)

    page_width = pdf.w
    page_height = pdf.h
    item_width = page_width / 3
    item_height = page_height / 9

    # Ajuste manual do espaçamento entre as linhas
    line_spacing = 2  # Ajuste conforme necessário

    for i, item in enumerate(data):
        if i > 0 and i % 27 == 0:
            pdf.add_page()

        col = i % 3
        row = (i % 27) // 3
        x = col * item_width
        y = row * item_height + 1

        # Adicione espaços extras para ajustar o espaçamento entre as linhas
        adjusted_item = item + "\n" * line_spacing

        pdf.set_xy(x, y)
        pdf.multi_cell(item_width, item_height / 3, adjusted_item, border=0, align="C")

    pdf.output(file_path)

data = [
    "Nome 1\nLogradouro 1\nNúmero 1\nComplemento 1",
    "Nome 2\nLogradouro 2\nNúmero 2\nComplemento 2",
    "Nome 3\nLogradouro 3\nNúmero 3\nComplemento 3",
]

generate_pdf("MultiColumnAdjustedSpacing.pdf", data)
