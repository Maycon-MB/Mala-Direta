import psycopg2
from psycopg2 import sql

# Parâmetros de conexão com o banco de dados
conexao_parametros = {
    'dbname': 'seu_banco_de_dados',
    'user': 'seu_usuario',
    'password': 'sua_senha',
    'host': 'seu_host',
    'port': '53590'
}

# Nome da tabela que você deseja fazer backup
nome_tabela = 'sua_tabela'

# Nome do arquivo de backup
arquivo_backup = 'backup_tabela.sql'

# Conectar ao banco de dados
conexao = psycopg2.connect(**conexao_parametros)
cursor = conexao.cursor()

# Consulta SQL para selecionar todos os dados da tabela
consulta_sql = sql.SQL("SELECT * FROM {}").format(sql.Identifier(nome_tabela))

# Executar a consulta SQL
cursor.execute(consulta_sql)

# Obter todos os registros da tabela
registros = cursor.fetchall()

# Gerar o script SQL de backup
script_backup = f"COPY {nome_tabela} TO '{arquivo_backup}' WITH CSV HEADER;"

# Escrever o script de backup em um arquivo
with open(arquivo_backup, 'w') as arquivo:
    arquivo.write(script_backup)

# Fechar a conexão
cursor.close()
conexao.close()

print(f"Backup da tabela {nome_tabela} concluído. O script de backup foi salvo em {arquivo_backup}.")
