import PySimpleGUI as sg
from PySimpleGUI import (Window, Button, Text, Input, Column, VSeparator, Push, Multiline, popup_yes_no, popup)
from cep_util import consultar_cep
import funcoes_compartilhadas
from funcoes_compartilhadas import exibir_eleitores, registrar_eleitor
from funcoes_compartilhadas import deletar_porID, filtrar_por_obs, filtrar_por_bairro, filtrar_por_cep, filtrar_por_cidade, filtrar_por_complemento, filtrar_por_email, filtrar_por_instagram, filtrar_por_logradouro, filtrar_por_nascimento, filtrar_por_nome, filtrar_por_numero, filtrar_por_telefone, filtrar_por_uf
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import subprocess
from cep_util import formatar_cep
from fpdf import FPDF
import sys
import os

# ...

if getattr(sys, 'frozen', False):
    # Se estiver executando como um executável congelado, o ícone está incorporado.
    icon_path = sys._MEIPASS  # Caminho para o diretório temporário com ícones incorporados
    icon_file = os.path.join(icon_path, 'Mala.Direta.ico')
else:
    # Se estiver executando como script, o ícone deve estar no mesmo diretório.
    icon_file = 'Mala.Direta.ico'

# Use icon_file no restante do código para definir o ícone da interface gráfica.



formatted_data = ""  # Initialize formatted_data as an empty    string

def formatar_telefone(valor_atual):
    # Remove todos os caracteres não numéricos
    valor_formatado = ''.join(filter(str.isdigit, valor_atual))

    if len(valor_formatado) == 9:
        valor_formatado = f'{valor_formatado[0]} {valor_formatado[1:5]}-{valor_formatado[5:]}'
    # Se o número de telefone tiver exatamente 8 dígitos, adicione o formato XXXX-XXXX
    elif len(valor_formatado) == 8:
        valor_formatado = f'{valor_formatado[:4]}-{valor_formatado[4:]}'

    return valor_formatado

def formatar_nascimento(valor_atual):
    # Remove todos os caracteres não numéricos
    valor_formatado = ''.join(filter(str.isdigit, valor_atual))

    # Verifique se a data de nascimento tem pelo menos 4 dígitos
    if len(valor_formatado) >= 4:
        # Formate como "xx/xx"
        valor_formatado = f'{valor_formatado[:2]}/{valor_formatado[2:]}'
    
    return valor_formatado

def limpar_campos_janela(janela):
    # Identifique todos os elementos de entrada (sg.Input) em sua interface
    input_elements = [janela[key] for key in janela.AllKeysDict if isinstance(janela[key], (sg.Input, sg.Multiline))]
    
    # Limpe o valor de cada campo de entrada
    for input_element in input_elements:
        input_element.update(value="") 




# Função para formatar os dados de um eleitor em uma única string
def formatar_dados_eleitor(eleitor):
    formatted_data = f"{eleitor[2]}\t"
    formatted_data += f"{eleitor[1]}\t"
    formatted_data += f"{eleitor[3]}\t"
    formatted_data += f"{eleitor[4]}\t"
    formatted_data += f"{eleitor[5]}\t"
    formatted_data += f"{eleitor[6]}\t"
    formatted_data += f"{eleitor[7]}\t"
    formatted_data += f"{eleitor[8]}\t"
    formatted_data += f"{eleitor[9]}\t"
    formatted_data += f"{eleitor[10]}\t"
    formatted_data += f"{eleitor[11]}\t"
    formatted_data += f"{eleitor[12]}\t" 
    formatted_data += f"{eleitor[13]}\n"
    return formatted_data

# Mantenha uma variável global para rastrear o último ID usado
ultimo_id = 0

# Função para obter o próximo ID disponível
def obter_proximo_id():
    global ultimo_id
    ultimo_id += 1
    return ultimo_id

# Inicialize a variável para armazenar os dados filtrados
eleitores_filtrados = []

eleitores_selecionados = {}

# Na função que gera as etiquetas Nascimento, use a lista de eleitores filtrados

class PDF(FPDF):
    def set_line_height(self, height):
        self.ln(height)

def generate_pdf(file_path, data):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=9)  # Define o tamanho padrão da fonte como 9

    page_width = pdf.w
    page_height = pdf.h

    # Ajuste o espaçamento vertical entre as linhas
    line_spacing = 5  # Espaçamento padrão

    # Defina a largura das colunas para preencher toda a largura da página
    item_width = page_width / 3

    item_height = page_height / 9

    reduce_line_spacing = False  # Variável para controlar a redução do espaçamento

    for i, item in enumerate(data):
        if i > 0 and i % 27 == 0:
            pdf.add_page()

        col = i % 3
        row = (i % 27) // 3
        x = col * item_width
        y = row * item_height + 1

        lines = item.split('\n')
        for line in lines:
            if "eleitor[1]" in line or "cep_formatado" in line:  # Verifica os campos que precisam de tamanho diferente
                pdf.set_font("Arial", size=11)  # Define a fonte como Arial com tamanho 11
            else:
                pdf.set_font("Arial", size=9)  # Define a fonte como Arial com tamanho 9

            pdf.set_xy(x, y)
            pdf.multi_cell(item_width, item_height / 3, line, border=0, align="L")  # Alinha o texto à esquerda

            if "eleitor[4]" in line:
                reduce_line_spacing = True  # Ativa a redução do espaçamento
            elif "eleitor[9]" in line:
                reduce_line_spacing = False  # Desativa a redução do espaçamento

            if reduce_line_spacing:
                line_spacing = 01  # Define um espaçamento menor entre as linhas
            else:
                line_spacing = 5  # Espaçamento padrão

            y += item_height / 3 - line_spacing  # Ajusta o espaço vertical entre as linhas

    pdf.output(file_path)


def etiqueta_Nascimento():
    global eleitores_filtrados

    eleitores_filtrados.sort(key=lambda eleitor: eleitor[1].lower())

    pdf_filename = "etiquetas-com-nascimento.pdf"

    # Criação do texto da etiqueta com nascimento
    etiqueta_data = []
    for eleitor in eleitores_filtrados:
        cep_formatado = formatar_cep(eleitor[3])

        etiqueta_text = (
            f"{eleitor[1].upper()}\n{eleitor[4]}, {eleitor[5]}, {eleitor[6]}\n{eleitor[7]}, {eleitor[8]} - {eleitor[9]}\n{cep_formatado}"
        )

        etiqueta_data.append(etiqueta_text)

    generate_pdf(pdf_filename, etiqueta_data)

    try:
        subprocess.Popen([pdf_filename], shell=True)
    except Exception as e:
        print(f"Erro ao abrir o PDF: {e}")

    sg.popup(f"Etiqueta com nascimento criada com sucesso: {pdf_filename}")

def etiqueta_semNascimento():
    global eleitores_filtrados

    eleitores_filtrados.sort(key=lambda eleitor: eleitor[1].lower())

    pdf_filename = "etiquetas-sem-nascimento.pdf"

    # Criação do texto da etiqueta sem nascimento
    etiqueta_data = []
    for eleitor in eleitores_filtrados:
        cep_formatado = formatar_cep(eleitor[3])

        etiqueta_text = (
            f"{eleitor[1].upper()}\n{eleitor[4]}, {eleitor[5]}, {eleitor[6]}\n{eleitor[7]}, {eleitor[8]} - {eleitor[9]}\n{cep_formatado}"
        )

        etiqueta_data.append(etiqueta_text)

    generate_pdf(pdf_filename, etiqueta_data)

    try:
        subprocess.Popen([pdf_filename], shell=True)
    except Exception as e:
        print(f"Erro ao abrir o PDF: {e}")

    sg.popup(f"Etiqueta sem nascimento criada com sucesso: {pdf_filename}")



pessoas_registradas = exibir_eleitores() #inicialize a lista global
eleitores_exibidos = []
dados_formatados = exibir_eleitores()


# Função para gerar PDF com nome + email
def relatorio_email():
    global eleitores_filtrados  # Declare eleitores_filtrados como global

    # Ordene os eleitores em ordem alfabética pelo nome (índice 1)
    eleitores_filtrados.sort(key=lambda eleitor: eleitor[1].lower())

    pdf_filename = "Relatorio_email.pdf"
    
    doc = SimpleDocTemplate(pdf_filename)
    story = []

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    for i, eleitor in enumerate(eleitores_filtrados):
        nome = eleitor[1].upper()
        email = eleitor[10]

        # Crie parágrafos para o nome e telefone com negrito
        nome_paragraph = Paragraph(nome, normal_style)
        email_paragraph = Paragraph(email, normal_style)

        # Defina o estilo para negrito
        nome_paragraph = Paragraph(f"<b>{nome}</b>", normal_style)

        # Adicione os parágrafos à história do documento
        story.append(nome_paragraph)
        story.append(email_paragraph)

        # Adicione uma quebra de linha entre os registros
        story.append(Paragraph("<br/><br/>", normal_style))
    
        # Adicione uma linha divisória visível após cada registro
        if i < len(eleitores_filtrados) - 1: 
            story.append(HRFlowable(width="100%", thickness=1, color="black", spaceAfter=10))

    
    doc.build(story)

    # Abra o PDF com o visualizador padrão
    try:
        subprocess.Popen([pdf_filename], shell=True)
    except Exception as e:
        print(f"Erro ao abrir o PDF: {e}")

    sg.popup(f"Relatório por e-mail gerado com sucesso: {pdf_filename}")

# Função para gerar PDF com nome + telefone
# Função para gerar PDF com nome + telefone
def relatorio_telefone():
    global eleitores_filtrados  # Declare eleitores_filtrados como global

    # Ordene os eleitores em ordem alfabética pelo nome (índice 1)
    eleitores_filtrados.sort(key=lambda eleitor: eleitor[1].lower())

    pdf_filename = "Relatorio_telefone.pdf"
    
    doc = SimpleDocTemplate(pdf_filename)
    story = []

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    for i, eleitor in enumerate(eleitores_filtrados):
        nome = eleitor[1].upper()
        telefone = eleitor[11]

        # Formate o telefone usando a função que você já definiu
        telefone_formatado = formatar_telefone(telefone)

        # Crie parágrafos para o nome e telefone com negrito
        nome_paragraph = Paragraph(nome, normal_style)
        telefone_paragraph = Paragraph(telefone_formatado, normal_style)

        # Defina o estilo para negrito
        nome_paragraph = Paragraph(f"<b>{nome}</b>", normal_style)

        # Adicione os parágrafos à história do documento
        story.append(nome_paragraph)
        story.append(telefone_paragraph)

        # Adicione uma quebra de linha entre os registros
        story.append(Paragraph("<br/><br/>", normal_style))
    
        # Adicione uma linha divisória visível após cada registro
        if i < len(eleitores_filtrados) - 1: 
            story.append(HRFlowable(width="100%", thickness=1, color="black", spaceAfter=10))

    doc.build(story)

    # Abra o PDF com o visualizador padrão
    try:
        subprocess.Popen([pdf_filename], shell=True)
    except Exception as e:
        print(f"Erro ao abrir o PDF: {e}")

    sg.popup(f"Relatório por telefone gerado com sucesso: {pdf_filename}")


# Função para gerar PDF com nome + Instagram
def relatorio_instagram():
    global eleitores_filtrados  # Declare eleitores_filtrados como global

    # Ordene os eleitores em ordem alfabética pelo nome (índice 1)
    eleitores_filtrados.sort(key=lambda eleitor: eleitor[1].lower())

    pdf_filename = "Relatorio_instagram.pdf"
    
    doc = SimpleDocTemplate(pdf_filename)
    story = []

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    for i, eleitor in enumerate(eleitores_filtrados):
        nome = eleitor[1].upper()
        instagram = eleitor[12]

        # Crie parágrafos para o nome e Instagram com negrito
        nome_paragraph = Paragraph(nome, normal_style)
        instagram_paragraph = Paragraph(instagram, normal_style)

        # Defina o estilo para negrito
        nome_paragraph = Paragraph(f"<b>{nome}</b>", normal_style)

        # Adicione os parágrafos à história do documento
        story.append(nome_paragraph)
        story.append(instagram_paragraph)

        # Adicione uma quebra de linha entre os registros
        story.append(Paragraph("<br/><br/>", normal_style))

         # Adicione uma linha divisória visível após cada registro
        if i < len(eleitores_filtrados) - 1: 
            story.append(HRFlowable(width="100%", thickness=1, color="black", spaceAfter=10))
    
    doc.build(story)

    # Abra o PDF com o visualizador padrão
    try:
        subprocess.Popen([pdf_filename], shell=True)
    except Exception as e:
        print(f"Erro ao abrir o PDF: {e}")

    sg.popup(f"Relatório por Instagram gerado com sucesso: {pdf_filename}")

    # Função para gerar PDF com nome + obs
def relatorio_obs():
    global eleitores_filtrados  # Declare eleitores_filtrados como global

    # Ordene os eleitores em ordem alfabética pelo nome (índice 1)
    eleitores_filtrados.sort(key=lambda eleitor: eleitor[1].lower())

    pdf_filename = "Relatorio_OBS.pdf"
    
    doc = SimpleDocTemplate(pdf_filename)
    story = []

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    for i, eleitor in enumerate(eleitores_filtrados):
        nome = eleitor[1].upper()
        telefone = eleitor[11]
        obs = eleitor[13]

        # Crie parágrafos para o nome e Instagram com negrito
        nome_paragraph = Paragraph(nome, normal_style)
        telefone_paragraph = Paragraph(telefone, normal_style)
        obs_paragraph = Paragraph(obs, normal_style)

        # Defina o estilo para negrito
        nome_paragraph = Paragraph(f"<b>{nome}</b>", normal_style)
       

        # Adicione os parágrafos à história do documento
        story.append(nome_paragraph)
        story.append(telefone_paragraph)
        story.append(obs_paragraph)

        # Adicione uma quebra de linha entre os registros
        story.append(Paragraph("<br/><br/>", normal_style))

         # Adicione uma linha divisória visível após cada registro
        if i < len(eleitores_filtrados) - 1: 
            story.append(HRFlowable(width="100%", thickness=1, color="black", spaceAfter=10))
    
    doc.build(story)

    # Abra o PDF com o visualizador padrão
    try:
        subprocess.Popen([pdf_filename], shell=True)
    except Exception as e:
        print(f"Erro ao abrir o PDF: {e}")

    sg.popup(f"Relatório por OBS gerado com sucesso: {pdf_filename}")

# Função para exibir o menu de opções
def exibir_menu_opcoes():
    options = ["Etiqueta 1 (Nascimento)", "Etiqueta 2 (S/ Nascimento)", "Relatório 1 (Instagram)", "Relatório 2 (E-mail)", "Relatório 3 (Telefone)", "Relatório 4 (OBS)"] 
    choice = sg.popup_get_choice("Selecione uma opção", options=options)
    return choice

# Função para limpar os filtros e restaurar a lista original de eleitores
def limpar_filtros():
    global eleitores_filtrados
    eleitores_filtrados = pessoas_registradas.copy()  # Restaura a lista original de eleitores
    janela_eleitores['-OUTPUT-'].update(values=eleitores_filtrados)
 

def contar_eleitores():
    # A função exibir_eleitores retorna uma lista de eleitores, então você pode usá-la para contar os eleitores registrados
    eleitores = exibir_eleitores()
    
    # O comprimento da lista de eleitores representa o total de eleitores registrados
    total_eleitores = len(eleitores)
    
    return total_eleitores


def converter_nome_maiusculas(event, value, window):
    window[event].update(value=value.upper())


#Layouts
# Layout Principal

sg.theme('DarkTeal12')

font= ("Arial", 12)

layout_coluna1 = [
    [sg.Text('Nome*', size=(10, 1), font=font)], [sg.InputText(key='nome', size=(20, 1), expand_x=True, expand_y=True, font=font, enable_events=True, k='-nome_key-')],

    [sg.Text('Data de nascimento', font=font),  sg.Text('(dd/mm)', size=(20,1), font=("Helvetica", 10))], [sg.InputText(key='nascimento', size=(20, 1), expand_x=True, expand_y=True, font=font, enable_events=True)],
    [Text('CEP', size=(10, 1), font=font)], [sg.InputText(key='cep', expand_x=True, expand_y=True, size=(20, 1), font=font, enable_events=True), Button('Consultar CEP', size=(20, 1), expand_x=True, expand_y=True)]
]

layout_coluna2 = [
    [Text('Logradouro', size=(10, 1),   font=font)], [sg.InputText(key='logradouro', size=(20, 1), expand_x=True, expand_y=True, font=font)],
    [Text('Número', size=(10, 1), font=font)], [sg.InputText(key='numero', size=(20, 1), expand_x=True, expand_y=True, font=font)],
    [Text('Complemento', size=(11, 1), font=font)], [sg.InputText(key='complemento', size=(20, 1), expand_x=True, expand_y=True, font=font)],
]

layout_coluna3 = [
    [Text('Bairro', size=(10, 1), font=font)], [sg.InputText(key='bairro', expand_x=True, expand_y=True, size=(20, 1), font=font)],
    [Text('Cidade', size=(10, 1), font=font)], [sg.InputText(key='cidade',expand_x=True, expand_y=True, size=(20, 1),font=font)],
    [Text('UF', size=(10, 1), font=font)], [sg.InputText(key='uf', expand_x=True, expand_y=True, size=(20, 1), font=font)],
]

layout_coluna4 = [
    [Text('E-mail', size=(10, 1), font=font)], [sg.InputText(key='email', size=(20, 1), expand_x=True, expand_y=True,font=font)],
    [sg.Text('Telefone', size=(10, 1), font=font)], [sg.InputText(key='telefone', size=(20, 1), expand_x=True, expand_y=True, font=font, enable_events=True)],
    [Text('Instagram', size=(10, 1), font=font)], [sg.InputText(key='instagram', size=(20, 1), expand_x=True, expand_y=True, font=font)],
]

layout_coluna5 = [
    [Push(), Text('OBS:'), sg.Multiline(key='obs', expand_x=True, expand_y=True, size=(150, 10)), Push()],
]

layout_botoes = [
    [Push(), Button('Registrar eleitor', expand_x=True, expand_y=True), Push(), Button('Exibir Eleitores', expand_x=True, expand_y=True), Push(), Button('Fechar', expand_x=True, expand_y=True), Push()],
]

dados_exibidos = False  # Variável para controlar se os dados dos eleitores foram exibidos

layout = [
    [
        sg.Column(layout_coluna1, expand_x=True, expand_y=True),
        sg.VerticalSeparator(),
        sg.Column(layout_coluna2, expand_x=True, expand_y=True),
        sg.VerticalSeparator(),
        sg.Column(layout_coluna3, expand_x=True, expand_y=True),
        sg.VerticalSeparator(), 
        sg.Column(layout_coluna4, expand_x=True, expand_y=True),
    ],
    [sg.Column(layout_coluna5, expand_x=True, expand_y=True, justification='center')],
    [sg.Column(layout_botoes, expand_x=True, expand_y=True, justification='center')],
]
dados_exibidos = False

janela = sg.Window('Cadastro de Pessoas', layout=layout, resizable= True)
janela_eleitores = []



# Função para criar a janela de exibição de eleitores
def criar_janela_exibir_eleitores(total_eleitores):
    
    
    layout_total_eleitores = [
    [sg.Text(f'Total de Eleitores: {len(pessoas_registradas)}', key='-TOTAL-ELEITORES-')]
    ]

    layout_botoesSegundaTela = [
        [sg.Combo(['Etiqueta com Nascimento', 'Etiqueta sem Nascimento', 'Relatório por Instagram', 'Relatório por E-mail', 'Relatório por Telefone', 'Relatório por OBS'], key='-COMBO-'),
        sg.Button('Limpar Filtros', expand_x=True, expand_y=True, key='-LIMPAR-FILTROS-', size=(10, 1)), sg.Button('Deletar Eleitor', expand_x=True, expand_y=True, size=(10, 1)), sg.Button('Imprimir', expand_x=True, expand_y=True, key='-IMPRIMIR-', size=(10, 1)), sg.Button('Fechar', expand_x=True, expand_y=True, size=(10, 1)), ],
    ]

    layout_fecharExibicao = [
        [sg.Table(values=(dados_formatados), headings=['Matrícula', 'Nome', 'Nascimento', 'CEP','Logradouro', 'Número', 'Complemento', 'Bairro', 'Cidade', 'UF', 'E-mail', 'Telefone', 'Instagram', 'OBS'], auto_size_columns=True,
              justification='center', key='-OUTPUT-', alternating_row_color=sg.theme_button_color()[1], num_rows=min(25, len(dados_formatados)), expand_x=True, expand_y=True, size =(600,400)), ],
              [sg.Column(layout_botoesSegundaTela, justification='center')]
       
    ]

    layout_filtro1 = [
        [sg.Button('Filtrar por Nome', size=(20,1))],
        [sg.Button('Filtrar por Nascimento', size=(20,1))],
        [sg.Button('Filtrar por OBS', size = (20, 1))]
    ] 
    
    layout_filtro2 = [
         [sg.Button('Filtrar por Logradouro', size=(20,1))],
        [sg.Button('Filtrar por Bairro', size=(20,1))],
        [sg.Button('Filtrar por Cidade', size=(20,1))],
            ] 
    
    layout_filtro3 = [
        [sg.Button('Filtrar por E-mail', size=(20,1))],
        [sg.Button('Filtrar por Telefone', size=(20,1))],
        [sg.Button('Filtrar por Instagram', size=(20,1))],
    ]


    layout_filtros = [
    [Push(), Column(layout_filtro1),Push(), VSeparator(),Push(),
     Column(layout_filtro2), Push(), VSeparator(), Push(),
     Column(layout_filtro3), Push(), 
    ]
    ]


    return sg.Window('Eleitores Registrados', layout = [layout_filtros, layout_fecharExibicao, layout_total_eleitores], resizable=True, finalize=True)

    
if janela_eleitores:
    janela_eleitores.close()

id_eleitor_para_deletar = None

# Defina a função para filtrar os eleitores
def filtrar_eleitores(coluna, filtro):
    return [eleitor for eleitor in pessoas_registradas if filtro.lower() in str(eleitor[coluna]).lower()]

# Identifique todos os elementos de entrada (sg.Input) em sua interface
input_elements = [janela[key] for key in janela.AllKeysDict if isinstance(janela[key], sg.Input)]

# Dicionário para armazenar os eleitores já registrados
eleitores_registrados = {}

# Loop para lidar com eventos
while True:
    eventos, valores = janela.read()

    if eventos == sg.WINDOW_CLOSED or eventos == 'Fechar':
        break
      
    if eventos == 'nome':
        # Converte o texto do campo 'nome' para maiúsculas após o usuário terminar de digitar
        converter_nome_maiusculas(eventos, valores[eventos], janela)

    if eventos == 'telefone':
        valor_formatado = formatar_telefone(valores['telefone'])
        janela['telefone'].update(valor_formatado)

    if eventos == 'nascimento':
        valor_formatado = formatar_nascimento(valores['nascimento'])
        janela['nascimento'].update(valor_formatado)

    if eventos == 'cep':
        valor_formatado = formatar_cep(valores['cep'])
        janela['cep'].update(valor_formatado)
            

    if eventos == 'Registrar eleitor':
        nome = valores['nome']
        # Verifique se o nome já está registrado
        if nome in eleitores_registrados:
            sg.popup_error(f"O eleitor com o nome '{nome}' já está cadastrado.")
        elif not nome:  # Verifique se o campo "nome" está vazio
            sg.popup_error('Preencha o campo obrigatório (Nome).')
        else:
            # Se não estiver registrado e o campo "nome" não estiver vazio, adicione-o ao dicionário
            eleitores_registrados[nome] = valores
            sg.popup('Eleitor registrado(a) com sucesso!')
            registrar_eleitor(valores)
            limpar_campos_janela(janela)
                 # Após registrar um novo eleitor, atualize a segunda janela com os dados atualizados
               # Definir o foco no primeiro campo após limpar
            janela["nome"].set_focus()
            dados_formatados = exibir_eleitores()

    if eventos == 'Consultar CEP':
        consultar_cep(janela['cep'], janela['logradouro'], janela['bairro'], janela['cidade'], janela['uf'])
            
            # Crie uma string formatada com os dados dos eleitores
        formatted_data = ''
    if eventos == 'Exibir Eleitores':
        pessoas_registradas = exibir_eleitores()
        if pessoas_registradas:
           
            formatted_data = ''
            for idx, eleitor in enumerate(pessoas_registradas, start=1):
                formatted_data += f"{idx}\t"  # Inclui o ID do eleitor
                formatted_data += f"{eleitor[1]}\t"
                formatted_data += f"{eleitor[2]}\t"
                formatted_data += f"{eleitor[3]}\t"
                formatted_data += f"{eleitor[4]}\t"
                formatted_data += f"{eleitor[5]}\t"
                formatted_data += f"{eleitor[6]}\t"
                formatted_data += f"{eleitor[7]}\t"
                formatted_data += f"{eleitor[8]}\t"
                formatted_data += f"{eleitor[9]}\t"
                formatted_data += f"{eleitor[10]}\t"
                formatted_data += f"{eleitor[11]}\t"
                formatted_data += f"{eleitor[12]}\t"
                formatted_data += f"{eleitor[13]}\n"
    
        janela_eleitores = criar_janela_exibir_eleitores(formatted_data)
        pessoas_registradas.append(dados_formatados)
        janela.Hide()
        
        # Após exibir os eleitores em janela_eleitores
        total_eleitores = contar_eleitores()
        janela_eleitores['-TOTAL-ELEITORES-'].update(f"Total de Eleitores Registrados: {total_eleitores}")

    

        while True:
            eventos_eleitores, valores_eleitores = janela_eleitores.read()
            if eventos_eleitores == sg.WINDOW_CLOSED or eventos_eleitores == 'Fechar':
                janela_eleitores.close()  # Adicione este comando para fechar a janela "Eleitores Registrados"
                janela.UnHide()
                break   
          
            if eventos_eleitores == '-IMPRIMIR-':
                selected_option = valores_eleitores['-COMBO-']  # Get the selected option from the combo box
                if selected_option == 'Etiqueta com Nascimento':
                    eleitores_filtrados.sort(key=lambda eleitor: eleitor[1])
                    # Generate the PDF for "Etiqueta com Nascimento"
                    etiqueta_Nascimento()
                    pessoas_registradas.append(eleitor) 
                elif selected_option == 'Etiqueta sem Nascimento':
                    # Generate the PDF for "Etiqueta sem Nascimento"
                    etiqueta_semNascimento()
                elif selected_option == 'Relatório por Telefone':
                    relatorio_telefone()
                elif selected_option == 'Relatório por Instagram':
                    relatorio_instagram()
                elif selected_option == 'Relatório por E-mail':
                    relatorio_email()
                elif selected_option == 'Relatório por OBS':
                    relatorio_obs()             

            # Evento ao pressionar o botão "Deletar Eleitor"
            if eventos_eleitores == 'Deletar Eleitor':
                id_eleitor_para_deletar = sg.popup_get_text("Digite a Matrícula do eleitor que deseja deletar:")
                if id_eleitor_para_deletar:
                    # Tente converter o ID para um número inteiro
                    try:
                        id_eleitor_para_deletar = int(id_eleitor_para_deletar)
                    except ValueError:
                        sg.popup_error("Matrícula inválida. Certifique-se de digitar um número válido.")
                        continue  # Continue aguardando eventos se o ID for inválido

                    # Tente deletar o eleitor
                    if deletar_porID(id_eleitor_para_deletar, janela_eleitores):
                        sg.popup("Eleitor deletado com sucesso!")
                    
                     # Após a exclusão bem-sucedida, atualize o elemento de texto com o total de eleitores na janela de eleitores
                    total_eleitores = contar_eleitores()
                    janela_eleitores['-TOTAL-ELEITORES-'].update(f'Total de Eleitores Registrados: {total_eleitores}')
                else:
                        sg.popup_error("Erro ao deletar eleitor. Verifique a Matrícula e tente novamente.")
            
            if eventos_eleitores == '-LIMPAR-FILTROS-':
                # Verifique se há dados extras no final da lista
                if len(pessoas_registradas) > len(eleitores_filtrados):
                    # Remova o último registro, que é o extra
                    pessoas_registradas.pop()
                limpar_filtros()  # Chama a função para limpar os filtros
                # Atualize a interface ou faça qualquer outra coisa necessária após a limpeza dos filtros

            if eventos_eleitores == 'Filtrar por Nome':
                nome_filtro = sg.popup_get_text("Digite o nome para filtrar:")
                if nome_filtro:
                    eleitores_filtrados = filtrar_por_nome(nome_filtro)
                    # Atualize a tabela com os resultados filtrados
                    janela_eleitores['-OUTPUT-'].update(values=eleitores_filtrados)
            

            if eventos_eleitores == 'Filtrar por Nascimento':
                nascimento_filtro = sg.popup_get_text("Digite o nascimento para filtrar:")
                if nascimento_filtro:
                    # Remove barras do texto digitado
                    nascimento_filtro = nascimento_filtro.replace('/', '')
                    
                    # Adiciona uma barra após os dois primeiros dígitos, se houver pelo menos dois dígitos
                    if len(nascimento_filtro) >= 2:
                        nascimento_filtro = f"{nascimento_filtro[:2]}/{nascimento_filtro[2:]}"
                    
                    eleitores_filtrados = filtrar_por_nascimento(nascimento_filtro)
                    # Atualize a tabela com os resultados filtrados
                    janela_eleitores['-OUTPUT-'].update(values=eleitores_filtrados)


           
            if eventos_eleitores == 'Filtrar por Logradouro':
                logradouro_filtro = sg.popup_get_text("Digite o logradouro para filtrar:")
                if logradouro_filtro:
                    eleitores_filtrados = filtrar_por_logradouro(logradouro_filtro)
                    # Atualize a tabela com os resultados filtrados
                    janela_eleitores['-OUTPUT-'].update(values=eleitores_filtrados)
            
            if eventos_eleitores == 'Filtrar por Bairro':
                bairro_filtro = sg.popup_get_text("Digite o Bairro para filtrar:")
                if bairro_filtro:
                    eleitores_filtrados = filtrar_por_bairro(bairro_filtro)
                    # Atualize a tabela com os resultados filtrados
                    janela_eleitores['-OUTPUT-'].update(values=eleitores_filtrados)

            
            if eventos_eleitores == 'Filtrar por Cidade':
                cidade_filtro = sg.popup_get_text("Digite a Cidade para filtrar:")
                if cidade_filtro:
                    eleitores_filtrados = filtrar_por_cidade(cidade_filtro)
                    # Atualize a tabela com os resultados filtrados
                    janela_eleitores['-OUTPUT-'].update(values=eleitores_filtrados)


            if eventos_eleitores == 'Filtrar por E-mail':
                eleitores_filtrados = filtrar_por_email("")
                janela_eleitores['-OUTPUT-'].update(values=eleitores_filtrados)

            if eventos_eleitores == 'Filtrar por Telefone':
                eleitores_filtrados = filtrar_por_telefone("")
                janela_eleitores['-OUTPUT-'].update(values=eleitores_filtrados)

            if eventos_eleitores == 'Filtrar por Instagram':
                eleitores_filtrados = filtrar_por_instagram("")
                janela_eleitores['-OUTPUT-'].update(values=eleitores_filtrados)

            if eventos_eleitores == 'Filtrar por OBS':
                eleitores_filtrados = filtrar_por_obs("")
                janela_eleitores['-OUTPUT-'].update(values=eleitores_filtrados)
                    
            def formatar_eleitor(eleitor):
                if len(eleitor) >= 14:
                    return '\t'.join(map(str, [eleitor[1], eleitor[2], eleitor[3], eleitor[4], eleitor[5], eleitor[6], eleitor[7], eleitor[8], eleitor[9], eleitor[10], eleitor[11], eleitor[12], eleitor[13]]))
                else:
                    return ""  # Retorna uma string vazia se o eleitor não tiver todos os índices necessários

janela.close()