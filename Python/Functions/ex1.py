class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade
    
    def exibir_nomes(self):
        print(f"Ola, meu nome é {self.nome} e tenho {self.idade} anos, ")
pessoa1 = Pessoa("Ana Maria", 30)
pessoa2 = Pessoa("Tiago Batata", 24)
pessoaInput = Pessoa(input("Digite o nome: "), int(input("Digite a idade: ")))
pessoa1.exibir_nomes()
pessoa2.exibir_nomes()
pessoaInput.exibir_nomes()