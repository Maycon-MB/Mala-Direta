import PySimpleGUI as sg

# Exemplo de dados de eleitores (substitua isso com seus dados reais do banco)
dados_eleitores = [
    ['1', 'João', '25/05/1980', '12345', 'Rua A', '10', 'Apto 101', 'Bairro 1', 'Cidade 1', 'UF1', 'joao@email.com', '1234567890', 'joao_insta', 'Observações', 'Zona 1', 'Seção 1', 'Escola 1'],
    ['2', 'Maria', '10/12/1995', '54321', 'Rua B', '15', 'Apto 202', 'Bairro 2', 'Cidade 2', 'UF2', 'maria@email.com', '9876543210', 'maria_insta', 'Outras observações', 'Zona 2', 'Seção 2', 'Escola 2'],
]

# Layout da janela principal
layout = [
    [sg.Table(values=dados_eleitores, headings=['ID', 'Nome', 'Nascimento', 'CEP', 'Logradouro', 'Número', 'Complemento', 'Bairro', 'Cidade', 'UF', 'E-mail', 'Telefone', 'Instagram', 'Observações', 'Zona', 'Seção', 'Local'], auto_size_columns=False, justification='right', num_rows=10, display_row_numbers=False, col_widths=15, key='-TABLE-', enable_events=True, select_mode='browse')],
]

# Crie a janela
window = sg.Window('Cadastro de Eleitores', layout, finalize=True)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == '-TABLE-':
        # Obtém a linha e a coluna da célula clicada
        row, col = values['-TABLE-']

        # Verifica se o evento foi um clique duplo (double click)
        if event.startswith('-TABLE-') and event.endswith('DOUBLECLICK'):
            # Abra uma caixa de diálogo de entrada para a edição
            novo_valor = sg.popup_get_text('Editar valor:', default_text=dados_eleitores[row][col])
            if novo_valor is not None:
                # Atualize o valor na lista de dados
                dados_eleitores[row][col] = novo_valor

                # Atualize a tabela na interface gráfica
                window['-TABLE-'].update(values=dados_eleitores)

# Feche a janela quando terminar
window.close()
