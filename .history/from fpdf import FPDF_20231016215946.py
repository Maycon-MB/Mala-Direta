from fpdf import FPDF

# Função para criar o PDF com 27 cadastros por página
def create_pdf():
    class PDF(FPDF):
        def header(self):
            pass

        def footer(self):
            pass

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=0)
    pdf.add_page()
    
    page_width = pdf.w
    page_height = pdf.h
    
    item_width = page_width / 3
    item_height = page_height / 9
    
    for _ in range(27):
        pdf.rect(pdf.get_x(), pdf.get_y(), item_width, item_height)
        pdf.multi_cell(item_width, item_height, txt='', border=0)
    
    pdf.output("cadastros.pdf")

create_pdf()
