print("🥔🥔🥔🥔🥔Potato Calc A B C🥔🥔🥔🥔🥔")
print("")
print("-------------Digite 2 Números Inteiros-------------")
print("")

A = int(input("Digite o número de A: "))
B = int(input("Digite o número de B: "))

if A == B:
    C = A+B
    print(f"Os números sao iguais logo somam {C}")
elif A != B:
    C = A*B
    print(f"Os números sao diferentes logo multiplicarão {C}")
