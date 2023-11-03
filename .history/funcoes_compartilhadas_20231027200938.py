import psycopg2

def conectar_banco_dados():
    conexao = psycopg2.connect(
        host='containers-us-west-150.railway.app', 
        user='postgres',
        password='dI3C8AraMRZkK9f6ZRfz',
        database='railway',
        port='5713'
    )
    return conexao

# Utilize o Context Manager (with) apenas para a conexão
def executar_query(query, params=None):
    conexao = conectar_banco_dados()
    cursor = conexao.cursor()
    cursor.execute(query, params)
    return conexao, cursor

def registrar_eleitor(valores):
    comando = """
        INSERT INTO tabela_eleitores (
            nome, nascimento, cep, logradouro, numero, complemento, bairro, cidade, uf, email, telefone, instagram, obs, zona, secao, local
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        ) RETURNING id;
    """
    
    cadastro_eleitor = (
        valores['nome'], valores['nascimento'], valores['cep'], valores['logradouro'],
        valores['numero'], valores['complemento'], valores['bairro'], valores['cidade'],
        valores['uf'], valores['email'], valores['telefone'], valores['instagram'], 
        valores['obs'], valores['zona'], valores['secao'], valores['local']
    )

    conexao, cursor = executar_query(comando, cadastro_eleitor)
    id_inserido = cursor.fetchone()[0]
    conexao.commit()
    conexao.close()
    return id_inserido


def exibir_eleitores():
    conexao = conectar_banco_dados()
    
    with conexao.cursor() as cursor:
        comando_exibir = "SELECT * FROM tabela_eleitores"

        cursor.execute(comando_exibir)

        pessoas_registradas = cursor.fetchall()

    conexao.commit()
    return pessoas_registradas


def deletar_porID(id_eleitor, janela_eleitores):
    try:
        conexao = conectar_banco_dados()
        cursor = conexao.cursor()
        delete_query = "DELETE FROM tabela_eleitores WHERE id = %s"
        cursor.execute(delete_query, (id_eleitor,))
        conexao.commit()
        conexao.close()
        
        janela_eleitores['-OUTPUT-'].update(values=exibir_eleitores())
        return True
    except Exception as e:
        print(f"Erro ao deletar eleitor: {e}")
        return False



def filtrar_por_nome(nome):
    comando = "SELECT * FROM tabela_eleitores WHERE nome ILIKE %s"
    conexao, cursor = executar_query(comando, (f"%{nome}%",))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados


def filtrar_por_nascimento(nascimento):
    comando = "SELECT * FROM tabela_eleitores WHERE nascimento ILIKE %s"
    conexao, cursor = executar_query(comando, (f"%{nascimento}%",))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados

def filtrar_por_cep(cep):
    comando = "SELECT * FROM tabela_eleitores WHERE cep ILIKE %s"
    conexao, cursor = executar_query(comando, (f"%{cep}%",))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados

def filtrar_por_logradouro(logradouro):
    comando = "SELECT * FROM tabela_eleitores WHERE logradouro ILIKE %s"
    conexao, cursor = executar_query(comando, (f"%{logradouro}%",))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados

def filtrar_por_numero(numero):
    comando = "SELECT * FROM tabela_eleitores WHERE numero ILIKE %s"
    conexao, cursor = executar_query(comando, (f"%{numero}%",))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados

def filtrar_por_complemento(complemento):
    comando = "SELECT * FROM tabela_eleitores WHERE complemento ILIKE %s"
    conexao, cursor = executar_query(comando, (f"%{complemento}%",))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados

def filtrar_por_bairro(bairro):
    comando = "SELECT * FROM tabela_eleitores WHERE bairro ILIKE %s"
    conexao, cursor = executar_query(comando, (f"%{bairro}%",))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados

def filtrar_por_cidade(cidade):
    comando = "SELECT * FROM tabela_eleitores WHERE cidade ILIKE %s"
    conexao, cursor = executar_query(comando, (f"%{cidade}%",))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados

def filtrar_por_uf(uf):
    comando = "SELECT * FROM tabela_eleitores WHERE uf ILIKE %s"
    conexao, cursor = executar_query(comando, (f"%{uf}%",))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados

def filtrar_por_email(email):
    comando = "SELECT * FROM tabela_eleitores WHERE email IS NOT NULL AND email != ''"
    conexao, cursor = executar_query(comando)
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados

def filtrar_por_telefone(telefone):
    comando = "SELECT * FROM tabela_eleitores WHERE telefone IS NOT NULL AND telefone != ''"
    conexao, cursor = executar_query(comando)
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados


def filtrar_por_instagram(instagram):
    comando = "SELECT * FROM tabela_eleitores WHERE instagram IS NOT NULL AND instagram != ''"
    conexao, cursor = executar_query(comando)
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados


def filtrar_por_obs(obs):
    comando = "SELECT * FROM tabela_eleitores WHERE obs IS NOT NULL AND obs != ''"
    conexao, cursor = executar_query(comando)
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados

def filtrar_por_zona(zona):
    comando = "SELECT * FROM tabela_eleitores WHERE zona ILIKE %s"
    conexao, cursor = executar_query(comando, (f"%{uf}%",))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados

def filtrar_por_uf(uf):
    comando = "SELECT * FROM tabela_eleitores WHERE uf ILIKE %s"
    conexao, cursor = executar_query(comando, (f"%{uf}%",))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados

def filtrar_por_uf(uf):
    comando = "SELECT * FROM tabela_eleitores WHERE uf ILIKE %s"
    conexao, cursor = executar_query(comando, (f"%{uf}%",))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados