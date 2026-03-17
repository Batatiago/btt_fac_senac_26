lista = [] 

for n in range(10):
    lista.append(int(input(f"Digite o valor {n}: ")))
print(lista)
read = (int(input(f"Digite um valor para saber se esta na lista: ")))

if read in lista:
    print(f"O numero {read} esta na lista!!!")
else:
    print(f"Numero {read} nao faz parte da lista")
