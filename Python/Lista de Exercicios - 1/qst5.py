print("🥔🥔🥔🥔🥔Potato Number Range🥔🥔🥔🥔🥔")
print("")
print("--------------- Digite um Número entre 100 e 200 -----------------")

number = float(input("Número: "))

if number in range(100,200):
    print(f"O número {number:.2f} está entre 100/200!!")
else:
    print(f"O número {number:.2f} nao está entre 100/200!!")