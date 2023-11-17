import os
import subprocess
from datetime import datetime

def fazer_backup(host, user, password, database, port):
    agora = datetime.now().strftime("%Y%m%d%H%M%S")
    arquivo_backup = f"backup_{agora}.sql"

    # Obter o diretório do script Python atual
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_backup = os.path.join(diretorio_atual, arquivo_backup)

    # Configurar a variável de ambiente PGPASSFILE para evitar a solicitação de senha
    os.environ["PGPASSFILE"] = os.path.join(diretorio_atual, "pgpass.conf")

    try:
        comando = [
            "pg_dump",
            "-h", host,
            "-U", user,
            "-d", database,
            "-p", port,
            "-f", caminho_backup
        ]

        # Adicione a senha ao comando
        p = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode != 0:
            print(f"Erro ao realizar backup: {err.decode()}")
            return None

        print("Backup realizado com sucesso!")
        return caminho_backup
    except Exception as e:
        print(f"Erro ao realizar backup: {e}")
        return None

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
