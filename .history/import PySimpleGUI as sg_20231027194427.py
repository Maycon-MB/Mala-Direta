import PySimpleGUI as sg
import pandas as pd

# Dados iniciais da tabela
data = {
    'Matrícula': [1, 2, 3],
    'Nome': ['Alice', 'Bob', 'Charlie'],
    'Nascimento': ['2000-01-01', '1995-02-15', '1990-07-30']
}

# Crie um DataFrame do pandas com os dados iniciais
df = pd.DataFrame(data)

# Defina o layout da janela
layout = [
    [sg.Table(values=df.values.tolist(), headings=df.columns.tolist(), auto_size_columns=False, justification='right',
              num_rows=20, enable_events=True, key='-TABLE-')],
    [sg.Button('Salvar', key='-SAVE-')],
]

window = sg.Window('Tabela Editável', layout, resizable=True)

# Loop principal
while True:
    event, values = window.read()

    if event in (sg.WINDOW_CLOSED, 'Exit'):
        break

    if event == '-SAVE-':
        # Atualize o DataFrame com os dados editados
        updated_data = pd.DataFrame(values['-TABLE-'], columns=df.columns.tolist())

        # Atualize o DataFrame original apenas se as formas forem compatíveis
        if updated_data.shape == df.shape:
            df = updated_data
        else:
            sg.popup_error("O número de colunas não corresponde aos dados originais.")

        # Atualize a tabela com os dados editados
        window['-TABLE-'].update(values=df.values.tolist())

window.close()
