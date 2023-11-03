import PySimpleGUI as sg
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

def generate_pdf(contents, filename):
    # Configuração da janela PySimpleGUI
    sg.theme('LightGreen1')
    layout = [[sg.Button('Gerar PDF')]]
    window = sg.Window('Gerador de PDF', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Gerar PDF':
            # Configuração do PDF
            doc = SimpleDocTemplate(filename, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            style = styles['Normal']
            style.alignment = 0  # Alinhamento à esquerda
            style.fontSize = 12  # Tamanho da fonte

            # Dividindo o conteúdo em 3 colunas
            data = []
            for item in contents:
                data.append([Paragraph(item, style)] * 9)  # 9 linhas em cada coluna

            # Calculando o tamanho dos retângulos para preencher a página
            page_width, page_height = letter
            col_width = page_width / 3
            row_height = page_height / 9

            # Criando uma tabela com 3 colunas
            table = Table(data, colWidths=[col_width] * 3, rowHeights=[row_height] * 27)  # Corrigido para 27 alturas de linha
            table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)

            doc.build(elements)
            sg.popup('PDF gerado com sucesso!')

    window.close()

# Exemplo de conteúdo
content = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6', 'Item 7', 'Item 8', 'Item 9', 'Item 10', 'Item 11', 'Item 12', 'Item 13', 'Item 14', 'Item 15', 'Item 16', 'Item 17', 'Item 18', 'Item 19', 'Item 20', 'Item 21', 'Item 22', 'Item 23', 'Item 24', 'Item 25', 'Item 26', 'Item 27']

# Chame a função com o conteúdo e o nome do arquivo desejado
generate_pdf(content, 'output.pdf')
