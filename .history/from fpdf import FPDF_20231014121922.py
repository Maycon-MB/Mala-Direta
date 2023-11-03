import PySimpleGUI as sg
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def create_pdf(data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    font_size_name = 12
    font_size_address = 10

    # Defina as dimensões das colunas
    col_width = width / 3
    col_height = height / 9

    x, y = 0, height - col_height

    for i, person in enumerate(data):
        if i > 0 and i % 3 == 0:
            x = 0
            y -= col_height

        c.setFont("Helvetica", font_size_name)
        c.drawString(x + 10, y - 20, person['name'])
        c.setFont("Helvetica", font_size_address)
        c.drawString(x + 10, y - 40, person['address'])

        x += col_width

    # Preencha com espaços em branco na última linha se necessário
    while x < width:
        c.drawString(x + 10, y - 20, ' ')
        c.drawString(x + 10, y - 40, ' ')
        x += col_width

    c.save()
    buffer.seek(0)
    return buffer

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
        pdf_buffer = create_pdf(data)
        with open('cadastro_pessoas.pdf', 'wb') as pdf_file:
            pdf_file.write(pdf_buffer.read())
        sg.popup('PDF gerado com sucesso!', 'Nome do arquivo: cadastro_pessoas.pdf')

window.close()
