import PySimpleGUI as sg
from fpdf import FPDF

# Função para criar o PDF com 27 cadastros por página
def create_pdf(data):
    pdf = FPDF(format='letter')
    pdf.add_page()
    pdf.set_fill_color(255, 255, 255)

    for _ in range(27):
        pdf.cell(0, 20, txt='Cadastro', border=1, ln=True, align='C')

    pdf_file = 'cadastros.pdf'
    pdf.output(pdf_file)

layout = [[sg.Button('Gerar PDF')]]

window = sg.Window('Cadastro PDF', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    elif event == 'Gerar PDF':
        create_pdf([])

window.close()