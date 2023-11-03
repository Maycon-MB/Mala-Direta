import PySimpleGUI as sg
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def create_pdf(data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Defina as dimensões das colunas
    col_width = width / 3
    col_height = height / 9

    font_size_name = 12
    font_size_address = 10

    for i, person in enumerate(data):
        col = i % 3
        row = i // 3
        x = col * col_width
        y = height - (row + 1) * col_height

        c.setFont("Helvetica", font_size_name)
        c.drawString(x + 10, y - 20, person['name'])
        c.setFont("Helvetica", font_size_address)
        c.drawString(x + 10, y - 40, person['address'])

    c.save()
    buffer.seek(0)
    return buffer

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


layout = [
    [sg.Button('Gerar PDF')],
]

window = sg.Window('Gerar PDF com PySimpleGUI', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Gerar PDF':
        pdf_buffer = create_pdf(data)
        with open('cadastro_pessoas.pdf', 'wb') as pdf_file:
            pdf_file.write(pdf_buffer.read())
        sg.popup('PDF gerado com sucesso!', 'Nome do arquivo: cadastro_pessoas.pdf')

window.close()
