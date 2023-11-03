from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Título do Documento', 0, 1, 'C')
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def create_multi_column_pdf(filename):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font('Arial', '', 12)

    num_columns = 3
    column_width = pdf.w / num_columns

    for i in range(30):
        pdf.cell(column_width, 10, f'Item {i + 1}', ln=False)
        pdf.multi_cell(column_width, 10, 'Texto aqui', align='L')

    pdf.output(filename)

create_multi_column_pdf("MultiColumnRegularColumnsPDF.pdf")
