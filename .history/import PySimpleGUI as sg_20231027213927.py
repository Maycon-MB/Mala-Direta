import PySimpleGUI as sg

def fill_table(data):
    # Define o layout da janela
    layout = [
        [sg.Table(values=data, headings=['Column 1', 'Column 2', 'Column 3'], enable_events=True,
                  key='-TABLE-', num_rows=10, col_widths=[10, 10, 10])]
    ]

    window = sg.Window('Editable Table', layout)

    while True:
        event, values = window.read()

        # Verifica se o usuário fechou a janela
        if event == sg.WINDOW_CLOSED:
            break

        # Verifica se o usuário clicou duas vezes em uma célula da tabela
        if event == '-TABLE-' and values['-TABLE-'] != []:
            row, column = values['-TABLE-'][0]
            cell_value = values['-TABLE-'][0][3]

            # Abre uma nova janela de edição para o usuário
            layout_edit = [
                [sg.Text('New value:')],
                [sg.InputText(default_text=cell_value, key='new_value')],
                [sg.Button('OK'), sg.Button('Cancel')]
            ]

            window_edit = sg.Window('Edit Cell', layout_edit)

            while True:
                event_edit, values_edit = window_edit.read()

                # Verifica se o usuário fechou a janela de edição
                if event_edit == sg.WINDOW_CLOSED or event_edit == 'Cancel':
                    break

                # Atualiza o valor da célula na tabela
                if event_edit == 'OK':
                    new_value = values_edit['new_value']
                    data[row][column] = new_value
                    window['-TABLE-'].update(values=data)

                break

            window_edit.close()

    window.close()


data = [['Data 1', 'Data 2', 'Data 3'],
        ['Data 4', 'Data 
