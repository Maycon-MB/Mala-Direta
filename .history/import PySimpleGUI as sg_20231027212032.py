import PySimpleGUI as sg

# Exemplo de dados de eleitores (substitua isso com seus dados reais do banco)
dados_eleitores = [
    ['1', 'João', '25/05/1980', '12345', 'Rua A', '10', 'Apto 101', 'Bairro 1', 'Cidade 1', 'UF1', 'joao@email.com', '1234567890', 'joao_insta', 'Observações', 'Zona 1', 'Seção 1', 'Escola 1'],
    ['2', 'Maria', '10/12/1995', '54321', 'Rua B', '15', 'Apto 202', 'Bairro 2', 'Cidade 2', 'UF2', 'maria@email.com', '9876543210', 'maria_insta', 'Outras observações', 'Zona 2', 'Seção 2', 'Escola 2'],
]

# Layout da janela principal
layout = [
    [sg.Table(values=dados_eleitores, headings=['ID', 'Nome', 'Nascimento', 'CEP', 'Logradouro', 'Número', 'Complemento', 'Bairro', 'Cidade', 'UF', 'E-mail', 'Telefone', 'Instagram', 'Observações', 'Zona', 'Seção', 'Local'], auto_size_columns=False, justification='right', num_rows=10, display_row_numbers=False, col_widths=15, key='-TABLE-', enable_events=True, select_mode='browse')],
    [sg.Text('Editar valor:'), sg.InputText(key='-EDIT-VALUE-'), sg.Button('Salvar', key='-SAVE-')],
]

# Crie a janela
window = sg.Window('Cadastro de Eleitores', layout, finalize=True)

# Variáveis para controlar a edição em andamento e a célula sendo editada
cell_being_edited = None
edited_row = None
edited_col = None

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == '-TABLE-':
        row, col = values['-TABLE-'][0], values['-TABLE-'][1]

        if cell_being_edited:
            # Atualize os dados na lista de dados com o valor editado
            dados_eleitores[edited_row][edited_col] = values['-EDIT-VALUE-']
            cell_being_edited = None
            edited_row = None
            edited_col = None
            window['-EDIT-VALUE-'].update('')
        else:
            cell_being_edited = row, col
            edited_row = row
            edited_col = col
            window['-EDIT-VALUE-'].update(dados_eleitores[row][col])

    if event == '-SAVE-' and cell_being_edited is not None:
        # Salve o valor editado na tabela
        dados_eleitores[edited_row][edited_col] = values['-EDIT-VALUE-']
        window['-TABLE-'].update(values=dados_eleitores)

# Feche a janela quando terminar
window.close()
