numeros = []

for index in range(5):
    valor = int(input(f"Digite o {index+1}º número inteiro: "))
    numeros.append(valor)

print("\nÍndice e valor dos números:")

for index, numero in enumerate(numeros):
    print(f"Posição {index}: {numero}")