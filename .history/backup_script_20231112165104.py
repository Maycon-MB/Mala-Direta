import os
import psycopg2
from datetime import datetime
import subprocess

def conectar_banco_dados():
    try:
        conexao = psycopg2.connect(
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            database=os.environ.get('DB_NAME', 'railway'),
            port=os.environ.get('DB_PORT', '53590')  # Porta padrão 5432 se não especificada
        )
        return conexao
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise

def realizar_backup():
    try:
        # Conectar ao banco de dados
        connection = conectar_banco_dados()
        cursor = connection.cursor()

        # Nome do arquivo de backup usando a data e hora atual
        backup_file = f"backup_{datetime.now().strftime('%Y%m%d%H%M%S%f')}.sql"

        # Comando para criar o backup
        backup_command = f"pg_dump -h {os.environ.get('DB_HOST')} -U {os.environ.get('DB_USER')} -p {os.environ.get('DB_PORT', '5432')} -Fc -d {os.environ.get('DB_NAME')} > {backup_file}"
        subprocess.run(backup_command, shell=True, check=True)

        # Confirmar as alterações e fechar a conexão
        connection.commit()
        connection.close()

        return backup_file

    except Exception as e:
        print(f"Ocorreu um erro ao realizar o backup: {e}")
        raise

# Exemplo de uso
if __name__ == "__main__":
    backup_result = realizar_backup()
    print("Backup realizado:", backup_result)
