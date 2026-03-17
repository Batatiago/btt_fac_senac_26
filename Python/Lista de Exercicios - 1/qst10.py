print("🥔🥔🥔🥔🥔Potato Númber Order🥔🥔🥔🥔🥔")
print("")
print("-----------Digite 3 Números Inteiros-----------")
print("")

n1 = int(input("Primeiro Número: "))
n2 = int(input("Segundo Número: "))
n3 = int(input("Terceiro Número: "))

if n1 == n2 or n1 == n3 or n2 == n3:
    print("Os números devem ser diferentes")
else:
    numbers = [n1, n2, n3]
    numbers.sort(reverse=True)
    print(f"Do maior para o maior os números sao {numbers[0]}, {numbers[1]} e {numbers[2]}")