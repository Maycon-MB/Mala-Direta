import PySimpleGUI as sg
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def create_pdf(data):
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    elements = []

    data_table = [[person['name'], person['address']] for person in data]

    # Defina o estilo da tabela
    style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    data_table = Table(data_table)
    data_table.setStyle(style)
    elements.append(data_table)

    doc.build(elements)
    pdf_buffer.seek(0)
    return pdf_buffer

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
