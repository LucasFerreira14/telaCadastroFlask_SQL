import pyodbc


def conn():
    connection = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                "Server=localhost;"
                                "Database=DB_AC3;"
                                "uid=python;"
                                "pwd=Saopaulo;")
    return connection


def createTable():
    connection = conn()
    cursor = connection.cursor()

    sql_line = '''CREATE TABLE TB_USERS(
        RA VARCHAR(20),
        NOME VARCHAR(200),
        SENHA VARCHAR(200),
        EMAIL VARCHAR(150),
        CEP VARCHAR(20),
        ENDERECO VARCHAR(350),
        BAIRRO VARCHAR(200),
        NUMERO VARCHAR(10))'''

    cursor.execute(sql_line)

    connection.commit()
    cursor.close()
    connection.close()


def insert(usuario):
    connection = conn()
    cursor = connection.cursor()

    sql_line = '''INSERT INTO TB_USERS (RA, NOME, SENHA, EMAIL, CEP, ENDERECO, BAIRRO, NUMERO)
                  VALUES (?,?,?,?,?,?,?,?)'''

    cursor.execute(sql_line,
                   usuario["ra"],
                   usuario["nome"],
                   usuario["senha"],
                   usuario["email"],
                   usuario["cep"],
                   usuario["endereco"],
                   usuario["bairro"],
                   usuario["numero"])

    connection.commit()

    cursor.close()
    connection.close()


def select(search):
    connection = conn()
    cursor = connection.cursor()

    sql_line = '''SELECT RA, SENHA FROM TB_USERS WHERE RA = ?'''

    cursor.execute(sql_line, search)
    row = cursor.fetchone()

    cursor.close()
    connection.close()

    return list(row)
