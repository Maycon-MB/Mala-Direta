import subprocess
from datetime import datetime
import os

def realizar_backup(caminho_backup):
    # Configurações do banco de dados
    host = 'monorail.proxy.rlwy.net'
    port = '53590'
    user = 'postgres'
    password = 'dfa5Bf1GDEEaeEGf6CFcga23EfF1G34E'
    database = 'railway'

    # Garante que o caminho do backup existe
    os.makedirs(caminho_backup, exist_ok=True)

    # Nome do arquivo de backup com carimbo de data e hora
    nome_arquivo_backup = f"backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.dump"

    # Comando para realizar o backup
    comando_backup = [
        'pg_dump',
        '-h', host,
        '-p', port,
        '-U', user,
        '-d', database,
        '-W',  # Solicitar senha
        '-F', 'c',  # Formato custom
        '-f', os.path.join(caminho_backup, nome_arquivo_backup)
    ]

    try:
        # Executar o comando de backup
        subprocess.run(comando_backup, check=True)
        print("Backup realizado com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao realizar o backup: {e}")

if __name__ == "__main__":
    # Solicitar o caminho do backup ao usuário
    caminho_do_backup = input("Digite o caminho onde deseja salvar o backup: ")

    # Chamar a função para realizar o backup
    realizar_backup(caminho_do_backup)
