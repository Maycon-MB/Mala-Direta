import PySimpleGUI as sg
import psycopg2

# Conecta ao banco de dados PostgreSQL
conn = psycopg2.connect("dbname=seu_banco_de_dados user=seu_usuario password=sua_senha")
cur = conn.cursor()

# Função para carregar os dados da tabela
def carregar_dados():
    cur.execute("SELECT * FROM sua_tabela")
    data = cur.fetchall()
    return data

# Função para atualizar um registro na tabela
def atualizar_registro(id, novo_nome, nova_idade):
    cur.execute("UPDATE sua_tabela SET nome = %s, idade = %s WHERE id = %s", (novo_nome, nova_idade, id))
    conn.commit()

# Layout da interface
layout = [
    [sg.Table(values=carregar_dados(), headings=['ID', 'Nome', 'Idade'], auto_size_columns=False, justification='right', key='-TABLE-')],
    [sg.Text('ID:'), sg.InputText(key='-ID-'), sg.Text('Nome:'), sg.InputText(key='-NOME-'), sg.Text('Idade:'), sg.InputText(key='-IDADE-')],
    [sg.Button('Atualizar'), sg.Button('Sair')]
]

window = sg.Window('Editar Tabela').Layout(layout)

while True:
    event, values = window.Read()

    if event == sg.WIN_CLOSED or event == 'Sair':
        break
    elif event == 'Atualizar':
        id = values['-ID-']
        novo_nome = values['-NOME-']
        nova_idade = values['-IDADE-']
        
        # Atualiza o registro com os novos valores
        atualizar_registro(id, novo_nome, nova_idade)

        # Recarrega os dados na tabela
        window['-TABLE-'].update(values=carregar_dados())

window.close()
conn.close()
