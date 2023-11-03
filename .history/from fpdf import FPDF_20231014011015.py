from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def generate_pdf(contents, filename):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    page_width = pdf.w
    page_height = pdf.h

    num_rectangles = 27
    num_columns = 3
    num_rows = num_rectangles // num_columns

    rect_width = page_width / num_columns
    rect_height = page_height / num_rows

    for i in range(num_rectangles):
        x = (i % num_columns) * rect_width
        y = (i // num_columns) * rect_height
        pdf.rect(x, y, rect_width, rect_height)
        pdf.multi_cell(rect_width, rect_height, contents[i])

    pdf.output(filename)

# Exemplo de conteúdo
content = [
    'Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6',
    'Item 7', 'Item 8', 'Item 9', 'Item 10', 'Item 11', 'Item 12',
    'Item 13', 'Item 14', 'Item 15', 'Item 16', 'Item 17', 'Item 18',
    'Item 19', 'Item 20', 'Item 21', 'Item 22', 'Item 23', 'Item 24',
    'Item 25', 'Item 26', 'Item 27'
]

# Chame a função com o conteúdo e o nome do arquivo desejado
generate_pdf(content, 'output.pdf')
