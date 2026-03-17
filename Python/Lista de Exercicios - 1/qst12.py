print("🥔🥔🥔🥔🥔Potato Price Choice🥔🥔🥔🥔🥔")
print("")

preco = float(200)
print(f"Valor padrão de R${preco}")
print("1 - Dinheiro | 2 - Crédito a vista | 3 - Crédito 3x | 4 - Credito 6x")
condicao = int(input("Digite o número da forma de pagamento: "))

if condicao == 1:
    print(f"Dinhero - total de R${preco-(preco*0.10)} com 10% de desconto")
elif condicao == 2:
    print(f"Credito a vista - total de R${preco-(preco*0.05)} com 5% de desconto")
elif condicao == 3:
    print(f"Credito 3x - total de R${preco} sem desconto")
elif condicao == 4:
    print(f"Credito 6x - total de R${(preco*1.10):.2f} com 10% de juros")
else:
    print("Esse número e invalido!!!")