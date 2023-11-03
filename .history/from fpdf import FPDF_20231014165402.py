from fpdf import FPDF

def generate_pdf(file_path, data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=5)

    # Define as dimensões da página sem margens
    page_width = pdf.w - 2 * pdf.l_margin
    page_height = pdf.h - 2 * pdf.t_margin

    # Define as dimensões dos itens na página para 3 colunas e 9 linhas
    item_width = page_width / 3  # 3 colunas
    item_height = page_height / 9  # 9 linhas

    for i, item in enumerate(data):
        if i > 0 and i % 27 == 0:
            # Adicione uma nova página após cada 27 itens
            pdf.add_page()

        # Calcule a posição (x, y) para o item atual na página atual
        x = (i % 3) * item_width
        y = (i % 9) * item_height

        # Defina a posição e adicione o item à página atual
        pdf.set_xy(x, y)
        pdf.multi_cell(item_width, 2, item, border=0, align="C")

    # Salve o PDF no caminho especificado
    pdf.output(file_path)

# Exemplo de uso
data = [f"Item {i+1}" for i in range(100)]  # Substitua pelo seu conjunto de dados
generate_pdf("MultiColumnRegularColumnsPDF.pdf", data)
