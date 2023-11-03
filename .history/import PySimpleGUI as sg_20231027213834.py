import PySimpleGUI as sg

def fill_table(data):
    # Cria uma tabela vazia com 5 colunas
    layout = [
        [sg.Table(values=data, headings=['Column 1', 'Column 2', 'Column 3', 'Column 4', 'Column 5'], enable_events=True,
                  key='-TABLE-', num_rows=10, col_widths=[10, 10, 10, 10, 10])],
        [sg.Button('Add Row'), sg.Button('Delete Row')]
    ]

    window = sg.Window('Editable Table', layout)

    while True:
        event, values = window.read()

        # Verifica se o usuário fechou a janela
        if event == sg.WINDOW_CLOSED:
            break

        # Verifica se o usuário clicou no botão 'Add Row'
        if event == 'Add Row':
            # Adiciona uma nova linha vazia à tabela
            values['-TABLE-'].append([''] * 5)
            window['-TABLE-'].update(values['-TABLE-'])

        # Verifica se o usuário clicou no botão 'Delete Row'
        if event == 'Delete Row':
            # Remove a linha selecionada da tabela
            selected_row = values['-TABLE-'][0]
            values['-TABLE-'].remove(selected_row)
            window['-TABLE-'].update(values['-TABLE-'])

    window.close()


data = [['Data 1', 'Data 2', 'Data 3', 'Data 4', 'Data 5'],
        ['Data 6', 'Data 7', 'Data 8', 'Data 9', 'Data 10']]

fill_table(data)
