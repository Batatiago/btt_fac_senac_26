def operacao(n1, n2, oper):
    if oper == 1:
        return n1 + n2
    if oper == 2:
        return n1 - n2
    if oper == 3:
        if n2 == 0:
            return 'Erro: divisão por zero.'
        return n1 / n2
    if oper == 4:
        return n1 * n2
    return 'Operação inválida.'

oper = int(input('Digite um numero equivalente para cada operação:\n'
                    'soma = 1\n'
                    'subtração = 2\n'
                    'multiplicação = 3\n'
                    'divisão = 4\n'
                    'Qual a Operação: '))
a = float(input('Digite o Primeiro número: '))
b = float(input('Digite o Segundo número: '))
print(f'Resultado: {operacao(a, b, oper)}')