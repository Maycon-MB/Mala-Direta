import subprocess
import datetime

# Configurações do banco de dados
db_host = "monorail.proxy.rlwy.net"
db_port = "        port='53590'
"
db_name = "seu_nome_banco"
db_user = "postgres"
db_password = "sua_senha_postgres"

# Nome do arquivo de backup com a data atual
backup_file = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"

# Comando pg_dump
command = [
    "pg_dump",
    "--host", db_host,
    "--port", db_port,
    "--username", db_user,
    "--dbname", db_name,
    "--file", backup_file,
]


# Executa o comando
subprocess.run(command)
