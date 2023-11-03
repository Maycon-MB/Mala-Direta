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
    {'name': 'João Silva', 'address': 'Rua A, 123'},
    {'name': 'Maria Santos', 'address': 'Avenida B, 456'},
    {'name': 'Carlos Oliveira', 'address': 'Rua C, 789'},
    {'name': 'Ana Pereira', 'address': 'Avenida D, 1011'},
    {'name': 'José Rodrigues', 'address': 'Rua E, 1213'},
    {'name': 'Mariana Almeida', 'address': 'Avenida F, 1415'},
    {'name': 'Pedro Souza', 'address': 'Rua G, 1617'},
    {'name': 'Luiza Fernandes', 'address': 'Avenida H, 1819'},
    {'name': 'Ricardo Pereira', 'address': 'Rua I, 2021'},
    {'name': 'Sofia Ribeiro', 'address': 'Avenida J, 2223'},
    {'name': 'Fernando Santos', 'address': 'Rua K, 2425'},
    {'name': 'Amanda Lima', 'address': 'Avenida L, 2627'},
    {'name': 'Lucas Oliveira', 'address': 'Rua M, 2829'},
    {'name': 'Juliana Rodrigues', 'address': 'Avenida N, 3031'},
    {'name': 'Gustavo Mendes', 'address': 'Rua O, 3233'},
    {'name': 'Camila Alves', 'address': 'Avenida P, 3435'},
    {'name': 'Bruno Sousa', 'address': 'Rua Q, 3637'},
    {'name': 'Isabela Santos', 'address': 'Avenida R, 3839'},
    {'name': 'Miguel Pereira', 'address': 'Rua S, 4041'},
    {'name': 'Larissa Silva', 'address': 'Avenida T, 4243'},
    {'name': 'Paulo Ribeiro', 'address': 'Rua U, 4445'},
    {'name': 'Fernanda Almeida', 'address': 'Avenida V, 4647'},
    {'name': 'Felipe Souza', 'address': 'Rua W, 4849'},
    {'name': 'Vitória Lima', 'address': 'Avenida X, 5051'},
    {'name': 'Eduardo Santos', 'address': 'Rua Y, 5253'},
    {'name': 'Helena Fernandes', 'address': 'Avenida Z, 5455'},
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
