from fpdf import FPDF
import PySimpleGUI as sg

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        pass

def create_pdf(data):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    col_width = pdf.w / 3
    row_height = pdf.font_size * 2
    
    for person in data:
        pdf.cell(col_width, row_height, txt=person['name'], border=1)
        pdf.cell(col_width, row_height, txt=person['address'], border=1)
        pdf.cell(col_width, row_height, txt="", border=1)  # Espaço em branco
        pdf.ln()
    
    pdf.output('cadastro_pessoas.pdf')

data = [
    {'name': 'Nome 1', 'address': 'Endereço 1'},
    {'name': 'Nome 2', 'address': 'Endereço 2'},
    # Adicione as outras 25 pessoas aqui
]

# Adicione espaços em branco para preencher até 27 pessoas
while len(data) < 27:
    data.append({'name': '', 'address': ''})

layout = [
    [sg.Button('Gerar PDF')],
]

window = sg.Window('Gerar PDF com PySimpleGUI', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Gerar PDF':
        create_pdf(data)
        sg.popup('PDF gerado com sucesso!', 'Nome do arquivo: cadastro_pessoas.pdf')

window.close()
