
vetor = []

for i in range(8):
    valor = int(input(f"Digite o valor {i}: "))
    vetor.append(valor)

x = int(input("Digite o valor da posicao x: "))
y = int(input("Digite o valor da posicao y: "))

if (0 <= x <=8 and 0 <=y <= 8):
    soma = vetor[x] + vetor[y]
    print(f"A soma dos valores {x} e {y}:{soma}!")
else:
    print("Os valores declarados nao correspondem a uma posicao valida")