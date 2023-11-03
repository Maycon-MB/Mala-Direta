import PySimpleGUI as sg

# Dados iniciais da tabela
dados_formatados = [
    ['Matrícula1', 'Nome1', 'Nascimento1'],
    ['Matrícula2', 'Nome2', 'Nascimento2'],
    # Adicione mais linhas conforme necessário
]

# Defina o layout da janela
layout = [
    [sg.Table(values=dados_formatados, headings=['Matrícula', 'Nome', 'Nascimento'], display_row_numbers=False,
              auto_size_columns=False, justification='right', num_rows=min(25, len(dados_formatados))),
    sg.Button('Salvar', key='-SAVE-')],
]

window = sg.Window('Tabela Editável', layout, resizable=True)

# Loop principal
while True:
    event, values = window.read()

    if event in (sg.WINDOW_CLOSED, 'Exit'):
        break

    if event == '-SAVE-':
        # Obtém os dados da tabela editável
        edited_data = values['-TABLE-']

        # Atualiza a lista de dados com as edições do usuário
        for i, row in enumerate(edited_data):
            dados_formatados[i] = row

        # Atualize a tabela com os dados editados
        window['-TABLE-'].update(values=dados_formatados)

window.close()
