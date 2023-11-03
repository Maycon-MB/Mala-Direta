import PySimpleGUI as sg
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Defina a função para criar o PDF
def create_pdf(data, output_filename):
    doc = SimpleDocTemplate(output_filename, pagesize=A4)
    story = []

    # Crie uma tabela com 3 colunas e 9 linhas (27 células)
    table_data = [data[i:i + 3] for i in range(0, len(data), 3)]
    table = Table(table_data, colWidths=2.5 * [A4[0] / 3])
    
    # Defina o estilo da tabela
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)

    # Adicione a tabela à história do PDF
    story.append(table)

    # Construa o PDF
    doc.build(story)

# Defina a interface gráfica com PySimpleGUI
layout = [
    [sg.Text('Insira dados nas 27 células:')],
    [sg.InputText('Célula 1'), sg.InputText('Célula 2'), sg.InputText('Célula 3')],
    [sg.InputText('Célula 4'), sg.InputText('Célula 5'), sg.InputText('Célula 6')],
    [sg.InputText('Célula 7'), sg.InputText('Célula 8'), sg.InputText('Célula 9')],
    [sg.InputText('Célula 10'), sg.InputText('Célula 11'), sg.InputText('Célula 12')],
    [sg.InputText('Célula 13'), sg.InputText('Célula 14'), sg.InputText('Célula 15')],
    [sg.InputText('Célula 16'), sg.InputText('Célula 17'), sg.InputText('Célula 18')],
    [sg.InputText('Célula 19'), sg.InputText('Célula 20'), sg.InputText('Célula 21')],
    [sg.InputText('Célula 22'), sg.InputText('Célula 23'), sg.InputText('Célula 24')],
    [sg.InputText('Célula 25'), sg.InputText('Célula 26'), sg.InputText('Célula 27')],
    [sg.Button('Criar PDF')],
]

# Crie a janela
window = sg.Window('Criar PDF de Tabela A4').Layout(layout)

# Loop para capturar eventos
while True:
    event, values = window.Read()
    if event is None:
        break
    if event == 'Criar PDF':
        # Obtenha os dados inseridos
        data = [values[f'Célula {i + 1}'] for i in range(27)]
        create_pdf(data, 'tabela_a4.pdf')
        sg.Popup('PDF criado com sucesso!', 'Arquivo: tabela_a4.pdf')

window.Close()
