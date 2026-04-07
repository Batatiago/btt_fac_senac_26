import  mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="aulasegunda"
)
cursor = conexao.cursor()
cod = int(input("Digite o codigo do usuario: "))
nome = input("Digite o nome do usuario: ")
email = input("Digite o email do usuario: ")
senha = input("Digite a senha do usuario: ")

sql = f"update usuarios set nome='{nome}', email='{email}', senha='{senha}'  where cod={cod}";
cursor.execute(sql)
conexao.commit()


resultado = cursor.fetchall()
for item in resultado:
    print(item)

conexao.close()