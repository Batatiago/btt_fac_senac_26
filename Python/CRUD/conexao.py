import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="aulasegunda"
)
cursor = conexao.cursor()
codigo = 'null'
nome = input("Digite o nome do usuario: ")
email = input("Digite o email do usuario: ")
senha = input("Digite a senha do usuario: ")

sql = f"insert into usuarios values (null, '{nome}', '{email}', '{senha}', now())"
cursor.execute(sql)
conexao.commit()

sql2 = "select * from usuarios"
cursor.execute(sql2)
resultado = cursor.fetchall()
for item in resultado:
    print(item)

conexao.close()
