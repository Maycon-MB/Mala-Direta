from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Título do Documento', 0, 1, 'C')
    
    def footer(self):
        # Não exibir número de página
        pass

def create_multi_column_pdf(filename):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font('Arial', '', 12)

    num_columns = 3
    num_rows = 3
    max_items_per_page = num_columns * num_rows

    item_count = 0

    for page in range(10):  # Criar 10 páginas (30 itens no total)
        pdf.add_page()

        for row in range(num_rows):
            for column in range(num_columns):
                item_count += 1
                pdf.cell(60, 10, f'Item {item_count}', ln=False)
                pdf.multi_cell(60, 10, 'Texto aqui', align='L')

        if item_count == max_items_per_page:
            item_count = 0

    pdf.output(filename)

create_multi_column_pdf("MultiColumnRegularColumnsPDF.pdf")
