from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Título do Documento', 0, 1, 'C')
    
    def footer(self):
        # Não exibir número de página
        pass

def generate_pdf(file_path, data):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=0)
    pdf.set_font("Arial", size=12)

    page_width = pdf.w
    page_height = pdf.h

    item_width = page_width / 3  # 3 colunas
    item_height = page_height / 3  # 3 linhas

    for i, item in enumerate(data):
        if i > 0 and i % 9 == 0:
            pdf.add_page()

        x = (i % 3) * item_width
        y = (i % 9) * item_height

        pdf.set_xy(x, y)
        pdf.multi_cell(item_width, item_height, item, border=0, align='C')

    pdf.output(file_path)

# Exemplo de uso
data = [f"Item {i+1}" for i in range(81)]  # 3 colunas x 3 linhas x 9 páginas
generate_pdf("MultiColumnRegularColumnsPDF.pdf", data)
