import os
import subprocess
from datetime import datetime
import psycopg2

def fazer_backup(host, user, password, database, port):
    agora = datetime.now().strftime("%Y%m%d%H%M%S")
    arquivo_backup = f"backup_{agora}.sql"

    # Obter o diretório do script Python atual
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_backup = os.path.join(diretorio_atual, arquivo_backup)

    try:
        # Conectar ao banco de dados usando psycopg2
        conexao = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )

        # Criar um cursor
        cursor = conexao.cursor()

        # Executar o backup usando o pg_dump
        with open(caminho_backup, 'w') as arquivo_saida:
            subprocess.run(['pg_dump', '-h', host, '-U', user, '-d', database, '-p', port], stdout=arquivo_saida)

        print("Backup realizado com sucesso!")
        return caminho_backup
    except Exception as e:
        print(f"Erro ao realizar backup: {e}")
        return Nonet
    finally:
        # Fechar a conexão com o banco de dados
        if conexao:
            conexao.close()

# Exemplo de uso
host = 'monorail.proxy.rlwy.net'
user = 'postgres'
password = 'dfa5Bf1GDEEaeEGf6CFcga23EfF1G34E'
database = 'railway'
port = '53590'

arquivo_backup = fazer_backup(host, user, password, database, port)

if arquivo_backup:
    print(f"Backup salvo em: {arquivo_backup}")
else:
    print("Falha ao realizar o backup.")
