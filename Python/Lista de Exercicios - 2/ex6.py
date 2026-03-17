nomes = []
print('Digite 5 nomes:')

for i in range(5):
    nome = (input(f'Digite o nome {i+1}: '))
    nomes.append(nome)

print(f'Nomes: {nomes}')

while True:
    try:
        posicao = int(input('Digite um número de 0 a 4 para remover o nome nessa posição: '))
        if 0 <= posicao <= 4:
            break
        else:
            print('Erro: O número deve estar entre 0 e 4.')
    except ValueError:
        print('Erro: Digite apenas números inteiros.')

nomeRemovido = nomes.pop(posicao)

print(f'O nome "{nomeRemovido}" foi removido da lista.')

print(f'Nomes restantes: {nomes}')