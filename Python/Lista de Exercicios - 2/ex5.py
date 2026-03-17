lista = [40,80,219,33,412,566,44,3242,5666,423] 
read = (int(input(f"Digite um valor para saber se esta na lista: ")))

if read in lista:
    print(f"O numero {read} esta na lista!!!")
else:
    print(f"Numero {read} nao faz parte da lista!!!")
