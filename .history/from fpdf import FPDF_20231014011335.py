from fpdf import FPDF

def generate_pdf(file_path, data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Define as dimensões da página
    page_width = pdf.w
    page_height = pdf.h

    # Define as dimensões dos itens na página
    num_columns = 3
    num_rows = 9

    item_width = page_width / num_columns
    item_height = page_height / num_rows

    for i, item in enumerate(data):
        if i > 0 and i % (num_columns * num_rows) == 0:
            # Adicione uma nova página após cada conjunto de 27 itens
            pdf.add_page()

        # Calcule a posição (x, y) para o item atual na página atual
        col = i % num_columns
        row = (i // num_columns) % num_rows

        x = col * item_width
        y = row * item_height

        # Defina a posição e adicione o item à página atual
        pdf.set_xy(x, y)
        pdf.multi_cell(item_width, item_height, item, border=1, align="L")

    # Salve o PDF no caminho especificado
    pdf.output(file_path)

# Exemplo de conteúdo
content = [
    'Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6',
    'Item 7', 'Item 8', 'Item 9', 'Item 10', 'Item 11', 'Item 12',
    'Item 13', 'Item 14', 'Item 15', 'Item 16', 'Item 17', 'Item 18',
    'Item 19', 'Item 20', 'Item 21', 'Item 22', 'Item 23', 'Item 24',
    'Item 25', 'Item 26', 'Item 27'
]

# Chame a função com o conteúdo e o nome do arquivo desejado
generate_pdf('output.pdf', content)
