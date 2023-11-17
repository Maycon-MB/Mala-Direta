import psycopg2
from datetime import datetime
import subprocess
import os

def conectar_banco_dados():
    try:
        conexao = psycopg2.connect(
            host=os.environ.get('DB_HOST', 'monorail.proxy.rlwy.net'),
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASSWORD', 'sua_senha_segura'),
            database=os.environ.get('DB_NAME', 'railway'),
            port=os.environ.get('DB_PORT', '53590')
        )
        return conexao
    except psycopg2.Error as e:
        # Trate erros de conexão de forma mais específica
        return f"Erro ao conectar ao banco de dados: {e}"

def realizar_backup():
    try:
        # Conectar ao banco de dados
        connection = conectar_banco_dados()
        cursor = connection.cursor()

        # Nome do arquivo de backup usando a data e hora atual
        backup_file = f"backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.sql"

        # Comando para criar o backup
        backup_command = (
            f"pg_dump -h {os.environ.get('DB_HOST')} "
            f"-U {os.environ.get('DB_USER')} "
            f"-p {os.environ.get('DB_PORT')} "
            f"-Fc -d {os.environ.get('DB_NAME')} > {backup_file}"
        )
        subprocess.run(backup_command, shell=True, check=True)

        # Confirmar as alterações e fechar a conexão
        connection.commit()
        connection.close()

        return backup_file

    except psycopg2.Error as e:
        return f"Erro ao realizar o backup: {e}"