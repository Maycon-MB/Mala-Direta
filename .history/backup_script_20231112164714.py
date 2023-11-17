# backup_script.py
from datetime import datetime
import subprocess
import os

def conectar_banco_dados():
    conexao = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'monorail.proxy.rlwy.net'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'sua_senha_segura'),
        database=os.environ.get('DB_NAME', 'railway'),
        port=os.environ.get('DB_PORT', '53590')
    )
    return conexao

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

        print(f"Backup realizado em {backup_file}")

    except Exception as e:
        print(f"Erro ao realizar o backup: {e}")

if __name__ == "__main__":
    realizar_backup()
