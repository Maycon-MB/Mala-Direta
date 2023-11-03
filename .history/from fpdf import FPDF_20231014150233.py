import PySimpleGUI as sg
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape

# Função para criar um novo PDF
def criar_pdf(cadastros):
    doc = SimpleDocTemplate("cadastros.pdf", pagesize=landscape(letter))
    elements = []

    for i in range(0, len(cadastros), 9):
        # Crie uma tabela para cada página
        data = cadastros[i:i+9]
        table_data = [["Nome", "Endereço", "", "Nome", "Endereço", "", "Nome", "Endereço"]] + data
        table = Table(table_data, colWidths=[150, 150, 150, 150, 150, 150, 150, 150, 150])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ]))
        elements.append(table)

    doc.build(elements)

# Crie uma interface gráfica com o PySimpleGUI para coletar os dados
layout = [
    [sg.Text("Cadastro de Nome e Endereço")],
    [sg.Text("Nome:"), sg.InputText(key="nome")],
    [sg.Text("Endereço:"), sg.InputText(key="endereco")],
    [sg.Button("Adicionar Cadastro"), sg.Button("Gerar PDF"), sg.Button("Sair")],
]

cadastros = []

window = sg.Window("Cadastro de Clientes", layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Sair":
        break

    if event == "Adicionar Cadastro":
        nome = values["nome"]
        endereco = values["endereco"]
        cadastros.append([nome, endereco])
        window["nome"].update("")
        window["endereco"].update("")

    if event == "Gerar PDF":
        criar_pdf(cadastros)
        sg.popup("PDF gerado com sucesso!", "Nome do arquivo: cadastros.pdf")

window.close()
