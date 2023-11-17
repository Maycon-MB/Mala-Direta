import psycopg2
from datetime import datetime
import subprocess

def conectar_banco_dados():
    conexao = psycopg2.connect(
        host='monorail.proxy.rlwy.net',
        user='postgres',
        password='dfa5Bf1GDEEaeEGf6CFcga23EfF1G34E',
        database='railway',
        port='53590'
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
        backup_command = f"pg_dump -h monorail.proxy.rlwy.net -U postgres -p 53590 -Fc -d railway > {backup_file}"
        subprocess.run(backup_command, shell=True, check=True)

        # Confirmar as alterações e fechar a conexão
        connection.commit()
        connection.close()

        return backup_file

    except Exception as e:
        return str(e)

# Exemplo de uso
if __name__ == "__main__":
    backup_result = realizar_backup()
    print("Backup realizado:", backup_result)
