numeros = [1,2,3,4,5,6,7,8,9,10]

par = [numero for numero in numeros if numero % 2 == 0]
impar = [numero for numero in numeros if numero % 2 != 0]

print(f"Os números {par} sao pares, e os numeros {impar} sao impares!!")