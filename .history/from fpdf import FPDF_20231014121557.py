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
