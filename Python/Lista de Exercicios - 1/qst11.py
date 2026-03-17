print("🥔🥔🥔🥔🥔Potato IMC Calculator🥔🥔🥔🥔🥔")
print("")
print("-----------Digite Suas Medidas-----------")
print("")

weight = float(input("Digite seu peso: "))
heigth = float(input("Digite sua altura: "))

imc = weight / (heigth**2)

if imc < 18.5:
    print(f"O IMC de {imc:.2f} significa que voce está abaixo do peso")
elif imc < 25:
    print(f"O IMC de {imc:.2f} significa que voce está com peso normal")
elif imc < 30:
    print(f"O IMC de {imc:.2f} significa que voce está acima do peso")
elif imc < 40:
    print(f"O IMC de {imc:.2f} significa que voce está obeso")
else:
    print(f"O IMC de {imc:.2f} significa que voce está obesamente obeso")    