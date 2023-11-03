 import requests
import PySimpleGUI as sg



def formatar_cep(valor_atual):
    # Remove todos os caracteres não numéricos
    valor_formatado = ''.join(filter(str.isdigit, valor_atual))

    # Verifique se o número de CEP tem pelo menos 8 dígitos
    if len(valor_formatado) >= 8:
        # Formate como "xxxxx-xxx"
        valor_formatado = f'{valor_formatado[:5]}-{valor_formatado[5:]}'
    
    return valor_formatado

def consultar_cep(cep_input, logradouro_input, bairro_input, cidade_input, uf_input):
    cep = cep_input.get()

    # Remove hífens e verifica se o CEP tem 8 dígitos numéricos
    cep_numerico = ''.join(filter(str.isdigit, cep))
    if len(cep_numerico) == 8:
        try:
            # Consulta CEP online
            url = f'https://viacep.com.br/ws/{cep_numerico}/json/'
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                logradouro_input.update(value=data.get('logradouro', ''))
                bairro_input.update(value=data.get('bairro', ''))
                cidade_input.update(value=data.get('localidade', ''))
                uf_input.update(value=data.get('uf', ''))
            else:
                sg.popup_error('CEP não encontrado')
        except Exception as e:
            sg.popup_error(f'Erro ao consultar o CEP: {str(e)}')
    else:
        sg.popup_error('CEP inválido (deve conter 8 dígitos numéricos)')
