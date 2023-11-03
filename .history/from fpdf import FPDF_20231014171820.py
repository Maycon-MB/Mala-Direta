from fpdf import FPDF

def generate_pdf(file_path, data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=16)  # Ajuste o tamanho da fonte

    # Define as dimensões da página
    page_width = pdf.w
    page_height = pdf.h

    # Define as dimensões dos itens na página
    item_width = page_width / 3  # 3 colunas, cada uma ocupando 1/3 da largura
    item_height = page_height / 9  # 9 linhas

    for i, item in enumerate(data):
        if i > 0 and i % 27 == 0:
            # Adicione uma nova página após cada 27 itens
            pdf.add_page()

        # Calcule a posição (x, y) para o item atual na página atual
        col = i % 3
        row = (i % 27) // 3
        x = col * item_width
        y = row * item_height + 1  # Move todos os itens um pouco para baixo

        # Defina a posição e adicione o item à página atual
        pdf.set_xy(x, y)
        pdf.multi_cell(item_width, item_height / 3, item, border=0, align="C")

    # Salve o PDF no caminho especificado
    pdf.output(file_path)

# Exemplo de uso
data = [
    "Nome 1, Logradouro 1, Número 1, Complemento 1",
    "Nome 2, Logradouro 2, Número 2, Complemento 2",
    "Nome 3, Logradouro 3, Número 3, Complemento 3",
    # Adicione mais itens conforme necessário
]

generate_pdf("MultiColumnAdjustedWidth.pdf", data)