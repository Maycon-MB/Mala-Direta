import PySimpleGUI as sg
import pandas as pd
import io
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Defina a função para criar o PDF
def create_pdf(dataframe, output_filename):
    doc = SimpleDocTemplate(output_filename, pagesize=A4)
    story = []

    # Converta o DataFrame em uma lista de listas (dados tabulares)
    data = [list(dataframe.columns)] + dataframe.values.tolist()

    # Divida os dados em três colunas
    num_cols = 3
    num_rows = len(data) - 1
    col_width = [1.7 * (A4[0] / num_cols) for _ in range(num_cols)]
    table_data = [data[i:i + num_rows] for i in range(1, len(data), num_rows)]

    # Crie uma tabela com 3 colunas
    table = Table(table_data, colWidths=col_width)

    # Defina o estilo da tabela
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)

    # Adicione a tabela à história do PDF
    story.append(table)

    # Construa o PDF
    doc.build(story)

# Defina a interface gráfica com PySimpleGUI
layout = [
    [sg.Text('Insira os dados na tabela:')],
    [sg.Multiline(size=(40, 10), key='data')],
    [sg.Button('Criar PDF')],
]

# Crie a janela
window = sg.Window('Criar PDF com DataFrame', layout)

# Loop para capturar eventos
while True:
    event, values = window.Read()
    if event is None:
        break
    if event == 'Criar PDF':
        data = values['data']
        # Crie um DataFrame a partir dos dados inseridos
        dataframe = pd.read_csv(io.StringIO(data), sep='\t')
        create_pdf(dataframe, 'dataframe_a4.pdf')
        sg.Popup('PDF criado com sucesso!', 'Arquivo: dataframe_a4.pdf')

window.Close()
