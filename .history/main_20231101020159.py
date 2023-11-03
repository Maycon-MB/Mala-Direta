import PySimpleGUI as sg
from PySimpleGUI import (Window, Button, Text, Input, Column, VSeparator, Push, Multiline, popup_yes_no, popup)
from cep_util import consultar_cep
import database
from database import exibir_eleitores, registrar_eleitor
from database import deletar_porID, filtrar_por_obs, filtrar_por_bairro, filtrar_por_cep, filtrar_por_cidade, filtrar_por_complemento, filtrar_por_email, filtrar_por_instagram, filtrar_por_logradouro, filtrar_por_nascimento, filtrar_por_nome, filtrar_por_numero, filtrar_por_telefone, filtrar_por_uf, filtrar_por_local, filtrar_por_secao, filtrar_por_zona
from reportlab.lib.pagesizes import landscape, letter, A4
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
import re



if getattr(sys, 'frozen', False):
    # Se estiver executando como um executável congelado, o ícone está incorporado.
    icon_path = sys._MEIPASS  # Caminho para o diretório temporário com ícones incorporados
    icon_file = os.path.join(icon_path, 'Mala.Direta.ico')
else:
    # Se estiver executando como script, o ícone deve estar no mesmo diretório.
    icon_file = 'Mala.Direta.ico'

# Use icon_file no restante do código para definir o ícone da interface gráfica.
#Comando para criar executável com ícone: pyinstaller --onefile --windowed --icon=seu_icone.ico seu_codigo.py



# Inicialize a variável para armazenar os dados filtrados
eleitores_filtrados = []

eleitores_selecionados = {}



def generate_pdf(filename, data):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Tamanho do retângulo para cada etiqueta
    rect_width = width / 3
    rect_height = height / 9

    for i, label in enumerate(data):
        if i > 0 and i % 27 == 0:
            c.showPage()  # Iniciar uma nova página a cada 27 itens

        x = (i % 3) * rect_width
        y = height - ((i // 3) % 9 + 1) * rect_height
              
        text_x = x + 15  # Margem à esquerda
        margin = 25  # Margem igual na parte superior e inferior
        text_y = y + rect_height - margin  # Margem superior e inferior

        # Divida o texto nas quebras de linha e coloque cada parte em uma nova linha
        lines = label.split('\n')

        for line in lines:
            # Defina diferentes tamanhos de fonte com base nas partes do texto
            if "cep_formatado" in line or "etiqueta[1]" in line:
                c.setFont("Helvetica", 11)  # Fonte maior
            else:
                c.setFont("Helvetica", 9)  # Fonte padrão
            
            c.drawString(text_x, text_y, line)
            text_y -= 11  # Ajuste para a próxima linha

        y -= margin  # Espaçamento igual entre as etiquetas

    c.save()



def etiqueta_Nascimento():
    global eleitores_filtrados

    eleitores_filtrados.sort(key=lambda eleitor: eleitor[1].lower())

    pdf_filename = "etiquetas-com-nascimento.pdf"

    # Criação do texto da etiqueta com nascimento
    etiqueta_data = []
    for eleitor in eleitores_filtrados:
        cep_formatado = formatar_cep(eleitor[3])

        etiqueta_text = (
            f"{eleitor[1].upper()}\n\n{eleitor[4]}, {eleitor[5]}, {eleitor[6]}\n{eleitor[7]}, {eleitor[8]} - {eleitor[9]}\n\n{cep_formatado}                                 {eleitor[2]}"
        )

        etiqueta_data.append(etiqueta_text)

    generate_pdf(pdf_filename, etiqueta_data)

    try:
        subprocess.Popen([pdf_filename], shell=True)
    except Exception as e:
        print(f"Erro ao abrir o PDF: {e}")

    sg.popup(f"Etiqueta com nascimento criada com sucesso: {pdf_filename}")

def etiqueta_Geral():
    # Use a lista de eleitores completa, sem filtrar
    eleitores_completos = exibir_eleitores()
    eleitores_completos.sort(key=lambda eleitor: eleitor[1].lower())

    pdf_filename = "etiqueta-geral.pdf"

    # Criação do texto da etiqueta sem nascimento
    etiqueta_data = []
    for eleitor in eleitores_completos:
        cep_formatado = formatar_cep(eleitor[3])

        etiqueta_text = (
            f"{eleitor[1].upper()}\n\n{eleitor[4]}, {eleitor[5]}, {eleitor[6]}\n{eleitor[7]}, {eleitor[8]} - {eleitor[9]}\n\n{cep_formatado}"
        )

        etiqueta_data.append(etiqueta_text)

    generate_pdf(pdf_filename, etiqueta_data)

    try:
        subprocess.Popen([pdf_filename], shell=True)
    except Exception as e:
        print(f"Erro ao abrir o PDF: {e}")

    sg.popup(f"Etiqueta Geral criada com sucesso: {pdf_filename}")


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

# Função para gerar PDF com nome + telefone
def relatorio_bairro():
    global eleitores_filtrados  # Declare eleitores_filtrados como global

 # Ordene os eleitores primeiro pelo bairro (índice 7) e, em seguida, pelo nome (índice 1)
    eleitores_filtrados.sort(key=lambda eleitor: (eleitor[7].lower(), eleitor[1].lower()))

    pdf_filename = "Relatorio_Bairro.pdf"
    
    doc = SimpleDocTemplate(pdf_filename)
    story = []

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    for i, eleitor in enumerate(eleitores_filtrados):
        bairro = eleitor[7].upper()
        logradouro = eleitor[4].upper()
        numero = eleitor[5].upper()
        complemento = eleitor[6].upper()
        nome = eleitor[1].upper()
        telefone = eleitor[11]

        # Formate o telefone usando a função que você já definiu
        telefone_formatado = formatar_telefone(telefone)

        # Crie uma string que combina logradouro, número e complemento
        endereco = f"{logradouro}, {numero} - {complemento}"

        # Crie parágrafos para bairro, nome e telefone
        bairro_paragraph = Paragraph(bairro, normal_style)
        endereco_paragraph = Paragraph(endereco, normal_style)
        nome_paragraph = Paragraph(nome, normal_style)
        telefone_paragraph = Paragraph(telefone_formatado, normal_style)


        # Adicione os parágrafos à história do documento
        story.append(bairro_paragraph)
        story.append(endereco_paragraph)
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

    sg.popup(f"Relatório por bairro gerado com sucesso: {pdf_filename}")

# Função para gerar PDF com nome + telefone
def relatorio_cidade():
    global eleitores_filtrados  # Declare eleitores_filtrados como global

 # Ordene os eleitores primeiro pelo bairro (índice 8) e, em seguida, pelo nome (índice 1)
    eleitores_filtrados.sort(key=lambda eleitor: (eleitor[8].lower(), eleitor[1].lower()))

    pdf_filename = "Relatorio_Cidade.pdf"
    
    doc = SimpleDocTemplate(pdf_filename)
    story = []

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    for i, eleitor in enumerate(eleitores_filtrados):
        cidade = eleitor[8].upper()
        logradouro = eleitor[4].upper()
        numero = eleitor[5].upper()
        complemento = eleitor[6].upper()
        nome = eleitor[1].upper()
        telefone = eleitor[11]

        # Formate o telefone usando a função que você já definiu
        telefone_formatado = formatar_telefone(telefone)

        # Crie uma string que combina logradouro, número e complemento
        endereco = f"{logradouro}, {numero} - {complemento}"

        # Crie parágrafos para bairro, nome e telefone
        cidade_paragraph = Paragraph(cidade, normal_style)
        endereco_paragraph = Paragraph(endereco, normal_style)
        nome_paragraph = Paragraph(nome, normal_style)
        telefone_paragraph = Paragraph(telefone_formatado, normal_style)


        # Adicione os parágrafos à história do documento
        story.append(cidade_paragraph)
        story.append(endereco_paragraph)
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

    sg.popup(f"Relatório por cidade gerado com sucesso: {pdf_filename}")
    

def relatorio_zona():
    global eleitores_filtrados  # Declare eleitores_filtrados como global

    # Ordene os eleitores em ordem alfabética pelo nome (índice 1)
    eleitores_filtrados.sort(key=lambda eleitor: eleitor[14].lower())

    pdf_filename = "Relatorio_Zona.pdf"
    
    doc = SimpleDocTemplate(pdf_filename)
    story = []

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    for i, eleitor in enumerate(eleitores_filtrados):
        zona = eleitor[14]
        secao = eleitor[15]
        local = eleitor[16]
        nome = eleitor[1].upper()
        telefone = eleitor[11]

        # Crie uma string que combina logradouro, número e complemento
        contato = f"{nome} - {telefone}"
        

        # Crie parágrafos para o nome e Instagram com negrito
        zona_paragraph = Paragraph(zona, normal_style)
        secao_paragraph = Paragraph(secao, normal_style)
        local_paragraph = Paragraph(local, normal_style)
        contato_paragraph = Paragraph(contato, normal_style)
        
        

        # Defina o estilo para negrito
        contato_paragraph = Paragraph(f"<b>{nome}</b>", normal_style)
       

        # Adicione os parágrafos à história do documento
        story.append(zona_paragraph)
        story.append(secao_paragraph)
        story.append(local_paragraph)
        story.append(contato_paragraph)
        

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

    sg.popup(f"Relatório por Zona gerado com sucesso: {pdf_filename}")

def relatorio_secao():
    global eleitores_filtrados  # Declare eleitores_filtrados como global

    # Ordene os eleitores em ordem alfabética pelo nome (índice 1)
    eleitores_filtrados.sort(key=lambda eleitor: eleitor[15].lower())

    pdf_filename = "Relatorio_Seção.pdf"
    
    doc = SimpleDocTemplate(pdf_filename)
    story = []

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    for i, eleitor in enumerate(eleitores_filtrados):
        secao = eleitor[15]
        zona = eleitor[14]
        local = eleitor[16]
        nome = eleitor[1].upper()
        telefone = eleitor[11]

        # Crie uma string que combina logradouro, número e complemento
        contato = f"{nome} - {telefone}"
        

        # Crie parágrafos para o nome e Instagram com negrito
        secao_paragraph = Paragraph(secao, normal_style)
        zona_paragraph = Paragraph(zona, normal_style)
        local_paragraph = Paragraph(local, normal_style)
        contato_paragraph = Paragraph(contato, normal_style)
        
        

        # Defina o estilo para negrito
        contato_paragraph = Paragraph(f"<b>{nome}</b>", normal_style)
       

        # Adicione os parágrafos à história do documento
        story.append(secao_paragraph)
        story.append(zona_paragraph)
        story.append(local_paragraph)
        story.append(contato_paragraph)
        

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

    sg.popup(f"Relatório por Local gerado com sucesso: {pdf_filename}")

def relatorio_local():
    global eleitores_filtrados  # Declare eleitores_filtrados como global

    # Ordene os eleitores em ordem alfabética pelo nome (índice 1)
    eleitores_filtrados.sort(key=lambda eleitor: eleitor[16].lower())

    pdf_filename = "Relatorio_Local.pdf"
    
    doc = SimpleDocTemplate(pdf_filename)
    story = []

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    for i, eleitor in enumerate(eleitores_filtrados):
        local = eleitor[16]
        secao = eleitor[15]
        zona = eleitor[14]
        nome = eleitor[1].upper()
        telefone = eleitor[11]

        # Crie uma string que combina logradouro, número e complemento
        contato = f"{nome} - {telefone}"
        

        # Crie parágrafos para o nome e Instagram com negrito
        local_paragraph = Paragraph(local, normal_style)
        secao_paragraph = Paragraph(secao, normal_style)
        zona_paragraph = Paragraph(zona, normal_style)
        contato_paragraph = Paragraph(contato, normal_style)
        
        

        # Defina o estilo para negrito
        contato_paragraph = Paragraph(f"<b>{nome}</b>", normal_style)
       

        # Adicione os parágrafos à história do documento
        story.append(local_paragraph)
        story.append(secao_paragraph)
        story.append(zona_paragraph)
        story.append(contato_paragraph)
        

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

    sg.popup(f"Relatório por Local gerado com sucesso: {pdf_filename}")


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
    formatted_data += f"{eleitor[13]}\t"
    formatted_data += f"{eleitor[14]}\t"
    formatted_data += f"{eleitor[15]}\n"
    formatted_data += f"{eleitor[16]}\n"
    return formatted_data

# Mantenha uma variável global para rastrear o último ID usado
ultimo_id = 0

# Função para obter o próximo ID disponível
def obter_proximo_id():
    global ultimo_id
    ultimo_id += 1
    return ultimo_id

# Função para exibir o menu de opções
def exibir_menu_opcoes():
    options = ["Etiqueta 1 (Nascimento)", "Etiqueta 2 (S/ Nascimento)", "Relatório 1 (Instagram)", "Relatório 2 (E-mail)", "Relatório 3 (Telefone)", "Relatório 4 (OBS)", "Relatório 5 (Bairro)", "Relatório 6 (Cidade)", "Relatório 7 (Zona)", "Reçatório 8 (Seção)", "Relatório 9 (Local)"] 
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

def atualizar_contagem_eleitores():
    global eleitores_filtrados  # Declarando eleitores_filtrados como global
    total_eleitores = len(eleitores_filtrados)
    janela_eleitores['-TOTAL-ELEITORES-'].update(f"Total de Eleitores Registrados: {total_eleitores}")


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
    [Text('Zona', size=(10, 1), font=font)], [sg.InputText(key='zona', expand_x=True, expand_y=True, size=(20, 1), font=font)],
    [Text('Seção', size=(10, 1), font=font)], [sg.InputText(key='secao',expand_x=True, expand_y=True, size=(20, 1),font=font)],
    [Text('Local', size=(10, 1), font=font)], [sg.InputText(key='local', expand_x=True, expand_y=True, size=(20, 1), font=font)],
]

layout_coluna6 = [
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
        sg.VerticalSeparator(),
        sg.Column(layout_coluna5, expand_x=True, expand_y=True),
    ],
    [sg.Column(layout_coluna6, expand_x=True, expand_y=True, justification='center')],
    [sg.Column(layout_botoes, expand_x=True, expand_y=True, justification='center')],
]
dados_exibidos = False

janela = sg.Window('Cadastro Mala Direta', layout=layout, return_keyboard_events=True, resizable= True)
janela_eleitores = []


# 1. Criar a lista focusable_elements com as chaves dos elementos que podem receber foco
focusable_elements = ['nome', 'nascimento', 'cep', 'Consultar CEP', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'uf', 'email', 'telefone', 'instagram', 'zona', 'secao', 'local', 'obs', 'Registrar eleitor', 'Exibir Eleitores', 'Fechar']

# 2. Defina a variável current_focus
current_focus = 0





# Função para criar a janela de exibição de eleitores
def criar_janela_exibir_eleitores(total_eleitores):
    
    
    layout_total_eleitores = [
    [sg.Text(f'Total de Eleitores: {len(pessoas_registradas)}', key='-TOTAL-ELEITORES-')]
    ]

    layout_botoesSegundaTela = [
        [sg.Combo(['Etiqueta Geral','Etiqueta com Nascimento', 'Relatório por Instagram', 'Relatório por E-mail', 'Relatório por Telefone', 'Relatório por OBS', 'Relatório por Bairro', 'Relatório por Cidade', 'Relatório por Zona', 'Relatório por Seção', 'Relatório por Local'], key='-COMBO-'),
        sg.Button('Imprimir', expand_x=True, expand_y=True, key='-IMPRIMIR-', size=(10, 1)), sg.Button('Limpar Filtros', expand_x=True, expand_y=True, key='-LIMPAR-FILTROS-', size=(10, 1)), sg.Button('Deletar Eleitor', expand_x=True, expand_y=True, size=(10, 1)), sg.Button('Fechar', expand_x=True, expand_y=True, size=(10, 1)), ],
    ]

    layout_fecharExibicao = [
        [sg.Table(values=(dados_formatados), headings=['Matrícula', 'Nome', 'Nascimento', 'CEP','Logradouro', 'Número', 'Complemento', 'Bairro', 'Cidade', 'UF', 'E-mail', 'Telefone', 'Instagram', 'OBS', 'Zona', 'Seção', 'Local'], auto_size_columns=True,
            justification='center', key='-OUTPUT-',text_color='black', background_color='#C7CEC9', alternating_row_color='#3DA5FF', num_rows=min(25, len(dados_formatados)), expand_x=True, expand_y=True, size=(550, 400), select_mode='browse'), 
        ],
        [sg.Button('Editar Tabela')],
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

    layout_filtro4 = [
        [sg.Button('Filtrar por Zona', size=(20,1))],
        [sg.Button('Filtrar por Seção', size=(20,1))],
        [sg.Button('Filtrar por Local', size=(20,1))],
    ]


    layout_filtros = [
    [Push(), Column(layout_filtro1),Push(), VSeparator(),Push(),
     Column(layout_filtro2), Push(), VSeparator(), Push(),
     Column(layout_filtro3), Push(), VSeparator(), Push(),
     Column(layout_filtro4), Push()
    ]
    ]


    return sg.Window('Eleitores Registrados', layout = [layout_filtros, layout_fecharExibicao, layout_total_eleitores], resizable=True, finalize=True)

# Variável para armazenar a última linha destacada
last_highlighted_row = None

# Cor de destaque personalizada
highlight_color = 'red'

# Função para criar a janela de edição
def criar_janela_edicao(data):
    layout = [
        [sg.Text('Matrícula:', size=12, justification='right'), sg.Text(data[0]) ],
        [sg.Text('Nome:', size=12, justification='right'), sg.Push(), sg.InputText(data[1], size=(40,1), key='nome', expand_x=True, expand_y=True)],
        [sg.Text('Nascimento:', size=12, justification='right'), sg.Push(), sg.InputText(data[2], size=(40,1), key='nascimento', expand_x=True, expand_y=True)],
        [sg.Text('CEP:', size=12, justification='right'), sg.Push(), sg.InputText(data[3], size=(40,1), key='cep', expand_x=True, expand_y=True)],
        [sg.Text('Logradouro:', size=12, justification='right'), sg.Push(), sg.InputText(data[4], size=(40,1), key='logradouro', expand_x=True, expand_y=True)],
        [sg.Text('Número:', size=12, justification='right'), sg.Push(), sg.InputText(data[5], size=(40,1), key='numero', expand_x=True, expand_y=True)],
        [sg.Text('Complemento:', size=12, justification='right'), sg.Push(), sg.InputText(data[6], size=(40,1), key='complemento', expand_x=True, expand_y=True)],
        [sg.Text('Bairro:', size=12, justification='right'), sg.Push(), sg.InputText(data[7], size=(40,1), key='bairro', expand_x=True, expand_y=True)],
        [sg.Text('Cidade:', size=12, justification='right'), sg.Push(), sg.InputText(data[8], size=(40,1), key='cidade', expand_x=True, expand_y=True)],
        [sg.Text('UF:', size=12, justification='right'), sg.Push(), sg.InputText(data[9], size=(40,1), key='uf', expand_x=True, expand_y=True)],
        [sg.Text('E-mail:', size=12, justification='right'), sg.Push(), sg.InputText(data[10], size=(40,1), key='email', expand_x=True, expand_y=True)],
        [sg.Text('Telefone:', size=12, justification='right'), sg.Push(), sg.InputText(data[11], size=(40,1), key='telefone', expand_x=True, expand_y=True)],
        [sg.Text('Instagram:', size=12, justification='right'), sg.Push(), sg.InputText(data[12], size=(40,1), key='instagram', expand_x=True, expand_y=True)],
        [sg.Text('Obs:', size=12, justification='right'), sg.Push(), sg.InputText(data[13],size=(40,1), key='obs', expand_x=True, expand_y=True)],
        [sg.Text('Zona:', size=12, justification='right'), sg.Push(), sg.InputText(data[14],size=(40,1), key='zona', expand_x=True, expand_y=True)],
        [sg.Text('Seção:', size=12, justification='right'), sg.Push(), sg.InputText(data[15],size=(40,1), key='secao', expand_x=True, expand_y=True)],
        [sg.Text('Local:', size=12, justification='right'), sg.Push(), sg.InputText(data[16],size=(40,1), key='local', expand_x=True, expand_y=True)],
        [sg.Button('Salvar')],
    ]

    return sg.Window('Editar Eleitor', layout, return_keyboard_events=True, finalize=True)

focusable_elements2 = ['nome', 'nascimento', 'cep', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'uf', 'email', 'telefone', 'instagram', 'obs', 'zona', 'secao', 'local', 'Salvar']

current_focus2 = 0

# Função para atualizar a tabela na janela principal
def atualizar_tabela(window, data):
    window['-OUTPUT-'].update(values=data)


if janela_eleitores:
    janela_eleitores.close()

selected_index = None

id_eleitor_para_deletar = None

# Defina a função para filtrar os eleitores
def filtrar_eleitores(coluna, filtro):
    return [eleitor for eleitor in pessoas_registradas if filtro.lower() in str(eleitor[coluna]).lower()]

# Identifique todos os elementos de entrada (sg.Input) em sua interface
input_elements = [janela[key] for key in janela.AllKeysDict if isinstance(janela[key], sg.Input)]

# Dicionário para armazenar os eleitores já registrados
eleitores_registrados = {}

# Senha de acesso
senha_correta = "dudu1717"

# Função para verificar a senha
def verificar_senha(senha_informada):
    return senha_informada == senha_correta

# Layout da primeira janela (tela de login)
layout_login = [
    [sg.Text("Digite a senha de acesso:")],
    [sg.Input(key="-SENHA-", password_char="*"), sg.Button("Mostrar / Ocultar"),],
    [sg.Button("Entrar")]
]

janela_login = sg.Window("Login", layout_login, return_keyboard_events=True, finalize=True)

# 1. Criar a lista focusable_elements com as chaves dos elementos que podem receber foco
focusable_elements3 = ['-SENHA-', 'Mostrar / Ocultar', 'Entrar']

# 2. Defina a variável current_focus
current_focus3 = 0

# Contador de tentativas
tentativas = 3

# Mostrar senha
mostrar_senha = False

# Loop principal da primeira janela
while tentativas > 0:
    event, values = janela_login.read()

    if event == sg.WIN_CLOSED:
        sys.exit()

    if event == '\r':
    # Quando Enter é pressionado, mova o foco para o próximo elemento
        current_focus3 = (current_focus3 + 1) % len(focusable_elements3)
        elemento_com_foco = focusable_elements3[current_focus3]
        janela_login[focusable_elements3        
        [current_focus3]].set_focus()

    if event == "Entrar":
        senha_informada = values["-SENHA-"]
        if verificar_senha(senha_informada):
            janela_login.close()
            break
        else:
            tentativas -= 1
            if tentativas > 0:
                sg.popup_error(f"Senha incorreta. Restam {tentativas} tentativas.")
            else:
                sg.popup_error("Tentativas esgotadas. O programa será encerrado.")
                sys.exit()

    elif event == "Mostrar / Ocultar":
        mostrar_senha = not mostrar_senha
        if mostrar_senha:
            janela_login["-SENHA-"].update(password_char='')
        else:
            janela_login["-SENHA-"].update(password_char='*')

# Aqui você pode adicionar o código da segunda janela
layout_segunda_janela = [
    [sg.Text("Bem-vindo à Mala Direta!")],
    [sg.Button("Fechar")]
]

janela_segunda = sg.Window("Janela", layout_segunda_janela, finalize=True)

# 1. Criar a lista focusable_elements com as chaves dos elementos que podem receber foco
focusable_elements = ['Fechar']

# 2. Defina a variável current_focus
current_focus3 = 0

while True:
    event2, values2 = janela_segunda.read()

    if event2 == sg.WIN_CLOSED or event2 == "Fechar":
        break

janela_segunda.close()

# Loop para lidar com eventos
while True:
    eventos, valores = janela.read()

    if eventos == sg.WINDOW_CLOSED or eventos == 'Fechar':
        break
          
    if eventos == '\r':
        # Quando Enter é pressionado, mova o foco para o próximo elemento
        current_focus = (current_focus + 1) % len(focusable_elements)
        elemento_com_foco = focusable_elements[current_focus]
        janela[focusable_elements[current_focus]].set_focus()

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
                formatted_data += f"{eleitor[13]}\t"
                formatted_data += f"{eleitor[14]}\t"
                formatted_data += f"{eleitor[15]}\t"
                formatted_data += f"{eleitor[16]}\n"
    
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

            elif event == '-OUTPUT-':
                # Evento de clique na tabela
                row, col = values['-OUTPUT-']
                if row != last_highlighted_row:
                    # Remove o destaque da linha anterior
                    if last_highlighted_row is not None:
                        janela_eleitores['-OUTPUT-'].update(select_rows=[last_highlighted_row], background_color='white')
                    # Aplica destaque na linha atual
                    janela_eleitores['-OUTPUT-'].update(select_rows=[row], background_color=highlight_color)
                    last_highlighted_row = row
            else:
                # Remove o destaque quando qualquer outra ação é realizada
                if last_highlighted_row is not None:
                    janela_eleitores['-OUTPUT-'].update(select_rows=[last_highlighted_row], background_color='white')
                last_highlighted_row = None

            if eventos_eleitores == 'Editar Tabela':
                selected_index = valores_eleitores['-OUTPUT-'][0] if valores_eleitores['-OUTPUT-'] else None
                if selected_index is not None:
                    selected_index = int(selected_index)  # Converta para inteiro
                    edit_window = criar_janela_edicao(dados_formatados[selected_index])
                
                    while True:
                        edit_event, edit_values = edit_window.read()
                        
                        if edit_event == '\r':
                            # Quando Enter é pressionado, mova o foco para o próximo elemento
                            current_focus2 = (current_focus2 + 1) % len(focusable_elements2)
                            elemento_com_foco = focusable_elements2[current_focus2]
                            edit_window[focusable_elements2[current_focus2]].set_focus()

                        if edit_event in (sg.WIN_CLOSED, 'Salvar'):
                            if edit_values is not None:
                                nome_input = edit_values['nome']
                                nascimento_input = edit_values['nascimento']
                                cep_input = edit_values['cep']
                                logradouro_input = edit_values['logradouro']
                                numero_input = edit_values['numero']
                                complemento_input = edit_values['complemento']
                                bairro_input = edit_values['bairro']
                                cidade_input = edit_values['cidade']
                                uf_input = edit_values['uf']
                                email_input = edit_values['email']
                                telefone_input = edit_values['telefone']
                                instagram_input = edit_values['instagram']
                                obs_input = edit_values['obs']
                                zona_input = edit_values['zona']
                                secao_input = edit_values['secao']
                                local_input = edit_values['local']

                                if nome_input is not None:
                                    dados_formatados[selected_index][1] = nome_input

                                if nascimento_input is not None:
                                    dados_formatados[selected_index][2] = nascimento_input
                                if cep_input is not None:
                                    dados_formatados[selected_index][3] = cep_input
                                if logradouro_input is not None:
                                    dados_formatados[selected_index][4] = logradouro_input   
                                if numero_input is not None:
                                    dados_formatados[selected_index][5] = numero_input
                                if complemento_input is not None:
                                    dados_formatados[selected_index][6] = complemento_input
                                if bairro_input is not None:
                                    dados_formatados[selected_index][7] = bairro_input
                                if cidade_input is not None:
                                    dados_formatados[selected_index][8] = cidade_input
                                if uf_input is not None:
                                    dados_formatados[selected_index][9] = uf_input
                                if email_input is not None:
                                    dados_formatados[selected_index][10] = email_input
                                if telefone_input is not None:
                                    dados_formatados[selected_index][11] = telefone_input
                                if instagram_input is not None:
                                    dados_formatados[selected_index][12] = instagram_input
                                if obs_input is not None:
                                    dados_formatados[selected_index][13] = obs_input
                                if zona_input is not None:
                                    dados_formatados[selected_index][14] = zona_input
                                if secao_input is not None:
                                    dados_formatados[selected_index][15] = secao_input
                                if local_input is not None:
                                    dados_formatados[selected_index][16] = local_input

                                atualizar_tabela(janela_eleitores, dados_formatados)
                            break

                    edit_window.close()
          
            if eventos_eleitores == '-IMPRIMIR-':
                selected_option = valores_eleitores['-COMBO-']  # Get the selected option from the combo box
                if selected_option == 'Etiqueta com Nascimento':
                    eleitores_filtrados.sort(key=lambda eleitor: eleitor[1])
                    # Generate the PDF for "Etiqueta com Nascimento"
                    etiqueta_Nascimento()
                    pessoas_registradas.append(eleitor) 
                elif selected_option == 'Etiqueta Geral':
                    # Generate the PDF for "Etiqueta Geral"
                    etiqueta_Geral()
                elif selected_option == 'Relatório por Telefone':
                    relatorio_telefone()
                elif selected_option == 'Relatório por Instagram':
                    relatorio_instagram()
                elif selected_option == 'Relatório por E-mail':
                    relatorio_email()
                elif selected_option == 'Relatório por OBS':
                    relatorio_obs()    
                elif selected_option == 'Relatório por Bairro':
                    relatorio_bairro()
                elif selected_option == 'Relatório por Cidade':
                    relatorio_cidade()
                elif selected_option == 'Relatório por Zona':
                    relatorio_zona()
                elif selected_option == 'Relatório por Seção':
                    relatorio_secao()
                elif selected_option == 'Relatório por Local':
                    relatorio_local()           

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
                    atualizar_contagem_eleitores()  # Atualizar a contagem de eleitores
            

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
                    atualizar_contagem_eleitores()  # Atualizar a contagem de eleitores


           
            if eventos_eleitores == 'Filtrar por Logradouro':
                logradouro_filtro = sg.popup_get_text("Digite o logradouro para filtrar:")
                if logradouro_filtro:
                    eleitores_filtrados = filtrar_por_logradouro(logradouro_filtro)
                    # Atualize a tabela com os resultados filtrados
                    janela_eleitores['-OUTPUT-'].update(values=eleitores_filtrados)
                    atualizar_contagem_eleitores()  # Atualizar a contagem de eleitores
            
            if eventos_eleitores == 'Filtrar por Bairro':
                bairro_filtro = sg.popup_get_text("Digite o Bairro para filtrar:")
                if bairro_filtro:
                    eleitores_filtrados = filtrar_por_bairro(bairro_filtro)
                    # Atualize a tabela com os resultados filtrados
                    janela_eleitores['-OUTPUT-'].update(values=eleitores_filtrados)
                    atualizar_contagem_eleitores()  # Atualizar a contagem de eleitores

            
            if eventos_eleitores == 'Filtrar por Cidade':
                cidade_filtro = sg.popup_get_text("Digite a Cidade para filtrar:")
                if cidade_filtro:
                    eleitores_filtrados = filtrar_por_cidade(cidade_filtro)
                    # Atualize a tabela com os resultados filtrados
                    janela_eleitores['-OUTPUT-'].update(values=eleitores_filtrados)
                    atualizar_contagem_eleitores()  # Atualizar a contagem de eleitores


            if eventos_eleitores == 'Filtrar por E-mail':
                eleitores_filtrados = filtrar_por_email("")
                janela_eleitores['-OUTPUT-'].update(values=eleitores_filtrados)
                atualizar_contagem_eleitores()  # Atualizar a contagem de eleitores

            if eventos_eleitores == 'Filtrar por Telefone':
                eleitores_filtrados = filtrar_por_telefone("")
                janela_eleitores['-OUTPUT-'].update(values=eleitores_filtrados)
                atualizar_contagem_eleitores()  # Atualizar a contagem de eleitores

            if eventos_eleitores == 'Filtrar por Instagram':
                eleitores_filtrados = filtrar_por_instagram("")
                janela_eleitores['-OUTPUT-'].update(values=eleitores_filtrados)
                atualizar_contagem_eleitores()  # Atualizar a contagem de eleitores

            if eventos_eleitores == 'Filtrar por OBS':
                eleitores_filtrados = filtrar_por_obs("")
                janela_eleitores['-OUTPUT-'].update(values=eleitores_filtrados)
                atualizar_contagem_eleitores()  # Atualizar a contagem de eleitores

            if eventos_eleitores == 'Filtrar por Zona':
                zona_filtro = sg.popup_get_text("Digite a Zona para filtrar:")
                if zona_filtro:
                    eleitores_filtrados = filtrar_por_zona(zona_filtro)
                    # Atualize a tabela com os resultados filtrados
                    janela_eleitores['-OUTPUT-'].update(values=eleitores_filtrados)
                    atualizar_contagem_eleitores()  # Atualizar a contagem de eleitores

            if eventos_eleitores == 'Filtrar por Seção':
                secao_filtro = sg.popup_get_text("Digite a Seção para filtrar:")
                if secao_filtro:
                    eleitores_filtrados = filtrar_por_secao(secao_filtro)
                    # Atualize a tabela com os resultados filtrados
                    janela_eleitores['-OUTPUT-'].update(values=eleitores_filtrados)
                    atualizar_contagem_eleitores()  # Atualizar a contagem de eleitores

            if eventos_eleitores == 'Filtrar por Local':
                local_filtro = sg.popup_get_text("Digite a Cidade para filtrar:")
                if local_filtro:
                    eleitores_filtrados = filtrar_por_local(local_filtro)
                    # Atualize a tabela com os resultados filtrados
                    janela_eleitores['-OUTPUT-'].update(values=eleitores_filtrados)
                    atualizar_contagem_eleitores()  # Atualizar a contagem de eleitores
                    
            def formatar_eleitor(eleitor):
                if len(eleitor) >= 16:
                    return '\t'.join(map(str, [eleitor[1], eleitor[2], eleitor[3], eleitor[4], eleitor[5], eleitor[6], eleitor[7], eleitor[8], eleitor[9], eleitor[10], eleitor[11], eleitor[12], eleitor[13], eleitor[14], eleitor[15], eleitor[16]]))
                else:
                    return ""  # Retorna uma string vazia se o eleitor não tiver todos os índices necessários

janela.close()