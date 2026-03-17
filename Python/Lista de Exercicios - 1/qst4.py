print("🥔🥔🥔🥔🥔Potato Number Diferences🥔🥔🥔🥔🥔")
print("")
print("---------------Digite os Númeors-----------------")

n1 = float(input("Primeiro Número: "))
n2 = float(input("Segundo Número: "))

if n1 == n2:
    print("Os Números São Iguais!!")
elif n1 > n2:
    print(f"Os Números são diferentes, {n1} e Maior que {n2}!!")
else:
    print(f"Os Números são diferentes, {n2} e Maior que {n1}!!")
