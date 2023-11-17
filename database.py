import psycopg2

def conectar_banco_dados():
    conexao = psycopg2.connect(
        host='roundhouse.proxy.rlwy.net', 
        user='postgres',
        password='FbBC5BdfeCaDdEF2aAcb6G2CdeFd366f',
        database='railway',
        port='32589'
    )
    return conexao

# Utilize o Context Manager (with) apenas para a conexão
def executar_query(query, params=None):
    conexao = conectar_banco_dados()
    cursor = conexao.cursor()
    cursor.execute(query, params)
    return conexao, cursor

def verificar_duplicata(nome):
    conexao, cursor = executar_query("SELECT COUNT(*) FROM tabela_eleitores WHERE nome = %s", (nome,))
    count = cursor.fetchone()[0]
    conexao.close()
    return count > 0

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
        comando_exibir = "SELECT * FROM tabela_eleitores ORDER BY nome"

        cursor.execute(comando_exibir)

        pessoas_registradas = cursor.fetchall()
        

    conexao.commit()

    # Substituir "None" por strings vazias para cada campo
    pessoas_registradas = [[str(field) if field is not None else "" for field in row] for row in pessoas_registradas]
    
    return pessoas_registradas



def atualizar_registro(id, newNome, newNascimento, newCep, newLogradouro, newNumero, newComplemento, newBairro, newCidade, newUF, newEmail, newTelefone, newInstagram, newObs, newZona, newSecao, newLocal):
    comando = """
        UPDATE tabela_eleitores
        SET nome = %s, nascimento = %s, cep = %s, logradouro = %s, numero = %s, complemento = %s, bairro = %s, cidade = %s, uf = %s, email = %s, telefone = %s, instagram = %s, obs = %s, zona = %s, secao = %s, local = %s 
        WHERE id = %s
    """

    parametros = (newNome, newNascimento, newCep, newLogradouro, newNumero, newComplemento, newBairro, newCidade, newUF, newEmail, newTelefone, newInstagram, newObs, newZona, newSecao, newLocal, id)

    conexao, cursor = executar_query(comando, parametros)
    conexao.commit()
        # Reordenar a tabela em ordem alfabética
    comando_ordenar = """
        SELECT * FROM tabela_eleitores
        ORDER BY nome
    """

    cursor.execute(comando_ordenar)
    resultados = cursor.fetchall()

    # Agora, a variável 'resultados' contém os registros ordenados por nome
    conexao.close()

    return resultados



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
    conexao, cursor = executar_query(comando, (f"%{zona}%",))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados

def filtrar_por_secao(secao):
    comando = "SELECT * FROM tabela_eleitores WHERE secao ILIKE %s"
    conexao, cursor = executar_query(comando, (f"%{secao}%",))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados

def filtrar_por_local(local):
    comando = "SELECT * FROM tabela_eleitores WHERE local ILIKE %s"
    conexao, cursor = executar_query(comando, (f"%{local}%",))
    resultados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultados
