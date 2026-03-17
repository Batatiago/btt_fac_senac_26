print("🥔🥔🥔🥔🥔Potato Dolar Converter🥔🥔🥔🥔🥔")
print("")

price = float(input("Digite a cotação do Dolar Hoje: "))
print("")
balance = float(input("Digite seu Saldo em Dolares: "))
print("")

result = price*balance

print(f"Seu saldo em Reais é: R${result:.2f}")