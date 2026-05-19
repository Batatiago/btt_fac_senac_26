class Aluno:
	def __init__(self, nome, nota1, nota2):
		self.nome = nome
		self.nota1 = nota1
		self.nota2 = nota2

	def media(self):
		return (self.nota1 + self.nota2) / 2

	def aprovado(self):
		return self.media() >= 7


nome = input("Digite o nome do aluno: ")
nota1 = float(input("Digite a primeira nota: "))
nota2 = float(input("Digite a segunda nota: "))

aluno = Aluno(nome, nota1, nota2)

print(f"Média de {aluno.nome}: {aluno.media():.2f}")
print(f"Aprovado: {aluno.aprovado()}")
