import os
import sys
import psycopg2
from datetime import datetime
from shutil import copyfile

if getattr(sys, 'frozen', False):
    # Se estiver executando como um executável congelado, o ícone está incorporado.
    icon_path = sys._MEIPASS  # Caminho para o diretório temporário com ícones incorporados
    icon_file = os.path.join(icon_path, 'Mala_Direta.ico')
else:
    # Se estiver executando como script, o ícone deve estar no mesmo diretório.
    icon_file = 'Mala_Direta.ico'

def conectar_banco_dados():
    conexao = psycopg2.connect(
        host='roundhouse.proxy.rlwy.net', 
        user='postgres',
        password='FbBC5BdfeCaDdEF2aAcb6G2CdeFd366f',
        database='railway',
        port='32589'
    )
    return conexao

def realizar_backup():
    # Obtém o diretório do script
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    
    conexao = conectar_banco_dados()
    data_backup = datetime.now().strftime("%d.%m.%Y_%H.%M")
    nome_arquivo_backup = f"backup_{data_backup}.sql"
    
    with conexao.cursor() as cursor:
        with open(nome_arquivo_backup, "w") as arquivo:
            cursor.copy_to(arquivo, 'tabela_eleitores', sep=';')
    
    # Mova o arquivo para o mesmo diretório do script
    caminho_backup_local = os.path.join(diretorio_script, nome_arquivo_backup)
    copyfile(nome_arquivo_backup, caminho_backup_local)
    
    # Feche a conexão
    conexao.close()

if __name__ == "__main__":
    realizar_backup()
