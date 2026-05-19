class Funcionario:
	def __init__(self, nome, salario):
		self.nome = nome
		self.salario = salario

	def exibir_dados(self):
		print(f"Nome: {self.nome}")
		print(f"Salário: R$ {self.salario:.2f}")


class Gerente(Funcionario):
	def __init__(self, nome, salario, departamento):
		super().__init__(nome, salario)
		self.departamento = departamento

	def exibir_dados(self):
		super().exibir_dados()
		print(f"Departamento: {self.departamento}")


nome = input("Digite o nome: ")
salario = float(input("Digite o salário: "))
departamento = input("Digite o departamento: ")

gerente = Gerente(nome, salario, departamento)
gerente.exibir_dados()
