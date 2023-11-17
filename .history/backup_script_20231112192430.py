import subprocess
import datetime
import psycopg2

def realizar_backup(host, user, password, database, port, nome_arquivo):
    try:
        # Gerar um nome de arquivo com a data e hora atual
        data_hora_atual = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        nome_arquivo_com_data = f"{nome_arquivo}_{data_hora_atual}.sql"

        # Comando para realizar o backup usando o utilitário pg_dump
        comando = f"pg_dump -h {host} -p {port} -U {user} -d {database} -f {nome_arquivo_com_data}"

        # Adicionar senha ao comando, se fornecida
        if password:
            comando += f" -W {password}"

        # Executar o comando
        subprocess.run(comando, shell=True)

        print(f"Backup realizado com sucesso. Arquivo: {nome_arquivo_com_data}")

    except Exception as e:
        print(f"Erro ao realizar backup: {e}")

# Configurações do banco de dados
host = 'monorail.proxy.rlwy.net'
user = 'postgres'
password = 'dfa5Bf1GDEEaeEGf6CFcga23EfF1G34E'
database = 'railway'
port = '53590'

# Nome desejado para o arquivo de backup
nome_arquivo_backup = "backup_mala_direta"

# Configurar psycopg2 para usar o arquivo .pgpass automaticamente
# Não precisa passar senha diretamente aqui
conn = psycopg2.connect(
    host=host,
    user=user,
    database=database,
    port=port
)

# Realizar o backup
realizar_backup(host, user, password, database, port, nome_arquivo_backup)
