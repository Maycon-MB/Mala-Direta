import subprocess
import datetime

# Configurações do banco de dados
db_host = "seu_host_postgres"
db_port = "sua_porta_postgres"
db_name = "seu_nome_banco"
db_user = "seu_usuario_postgres"
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

# Adiciona a senha, se necessário
if db_password:
    command.extend(["--password", db_password])

# Executa o comando
subprocess.run(command)
