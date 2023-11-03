from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Título do Documento', align='C', ln=True)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def generate_pdf(file_path, data):
    pdf = PDF()
    pdf.add_page()

    # Define as dimensões da página
    page_width = pdf.w
    page_height = pdf.h

    # Define as dimensões dos itens na página
    item_width = page_width / 3  # 3 colunas
    item_height = page_height / 3  # 3 linhas

    for i, item in enumerate(data):
        if i > 0 and i % 9 == 0:
            # Adicione uma nova página após cada 9 itens
            pdf.add_page()

        # Calcule a posição (x, y) para o item atual na página atual
        x = (i % 3) * item_width
        y = (i // 3) * item_height

        # Defina a posição e adicione o item à página atual
        pdf.set_xy(x, y)
        pdf.multi_cell(item_width, 10, item, border=0, align='C')

    # Salve o PDF no caminho especificado
    pdf.output(file_path)

# Exemplo de uso
data = [f"Item {i+1}" for i in range(27)]  # 3 colunas x 3 linhas
generate_pdf("MultiColumnRegularColumnsPDF.pdf", data)
