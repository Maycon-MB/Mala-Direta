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
        row = i // 9
        x = col * col_width
        y = height - (row + 1) * col_height

        c.setFont("Helvetica", font_size_name)
        c.drawString(x + 10, y - 20, person['name'])
        c.setFont("Helvetica", font_size_address)
        c.drawString(x + 10, y - 40, person['address'])

        if i % 9 == 8 or i == len(data) - 1:
            c.showPage()

    c.save()
    buffer.seek(0)
    return buffer

# Defina seus dados de exemplo
data = [
    {'name': 'Nome 1', 'address': 'Endereço 1'},
    {'name': 'Nome 2', 'address': 'Endereço 2'},
    # Adicione as outras 25 pessoas aqui
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
