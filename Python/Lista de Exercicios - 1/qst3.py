print("🥔🥔🥔🥔Potato Grade Average🥔🥔🥔🥔")
print("")

grd1 = float(input("Primeira Nota: "))
print("")
grd2 = float(input("Segunda Nota: "))
print("")
grd3 = float(input("Terceira Nota: "))
print("")

avrg = (grd1+grd2+grd3)/3

if avrg >= 7:
    print(f"Aprovado com {avrg:.2f} pontos!!")
elif avrg <= 5:
    print(f"Reprovado com {avrg:.2f} pontos!!")
else:
    print(f"Em recuperação com {avrg:.2f} pontos!!")    
        