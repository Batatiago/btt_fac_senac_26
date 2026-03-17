numeros = []

for i in range(5):
    valor = int(input(f"Digite o {i+1}º número inteiro: "))
    numeros.append(valor)

print("\nÍndice e valor dos números:")
for indice, numero in enumerate(numeros):
    print(f"Posição {indice}: {numero}")