import subprocess
import os
from datetime import datetime

def realizar_backup(nome_arquivo):
    # Configurações de conexão
    host = 'monorail.proxy.rlwy.net'
    user = 'postgres'
    password = 'dfa5Bf1GDEEaeEGf6CFcga23EfF1G34E'
    database = 'railway'
    port = '53590'

    # Nome do arquivo de backup
    data_hora = datetime.now().strftime("%Y%m%d%H%M%S")
    nome_arquivo_backup = f"{nome_arquivo}_{data_hora}.sql"

    # Comando para realizar o backup usando pg_dump
    comando_backup = [
        'pg_dump',
        '-h', host,
        '-p', port,
        '-U', user,
        '-W', password,
        '-F', 'c',  # Formato do arquivo de backup
        '-b',  # Incluir instruções SQL para restaurar bancos de dados
        '-v',  # Modo verbose
        '-f', nome_arquivo_backup,  # Nome do arquivo de backup
        database
    ]

    try:
        # Executar o comando de backup
        subprocess.run(comando_backup, check=True)
        print(f"Backup realizado com sucesso. Arquivo: {nome_arquivo_backup}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao realizar backup: {e}")

# Chamando a função para realizar o backup
realizar_backup("backup_railway")
