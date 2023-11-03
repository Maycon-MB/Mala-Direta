from fpdf import FPDF

def generate_pdf(file_path, data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=16)  # Ajuste o tamanho da fonte

    # Define as dimensões da página
    page_width = pdf.w
    page_height = pdf.h

    # Define as dimensões dos itens na página
    item_width = page_width / 3  # 3 colunas
    item_height = page_height / 9  # 9 linhas

    # Ajuste o deslocamento vertical (Y) para deixar mais espaço acima de todos os itens
    vertical_offset = 10

    for i, item in enumerate(data):
        if i > 0 and i % 27 == 0:
            # Adicione uma nova página após cada 27 itens
            pdf.add_page()

        # Calcule a posição (x, y) para o item atual na página atual
        col = i % 3
        row = (i % 27) // 3
        x = col * item_width
        y = row * item_height + vertical_offset

        # Defina a posição e adicione o item à página atual
        pdf.set_xy(x, y)
        pdf.multi_cell(item_width, item_height / 3, item, border=0, align="C")

    # Salve o PDF no caminho especificado
    pdf.output(file_path)

# Exemplo de uso
data = [f"Item {i+1}" for i in range(100)]  # Substitua pelo seu conjunto de dados
generate_pdf("MultiColumnFullScreenPDF.pdf", data)
