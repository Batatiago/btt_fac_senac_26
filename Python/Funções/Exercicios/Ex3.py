class Carro:
	def __init__(self, modelo, velocidade):
		self.modelo = modelo
		self.velocidade = velocidade

	def acelerar(self, valor):
		self.velocidade += valor

	def frear(self, valor):
		self.velocidade = max(0, self.velocidade - valor)

	def mostrar_velocidade(self):
		print(f"Velocidade atual do {self.modelo}: {self.velocidade}")


carro = Carro("Fusca", 0)
carro.acelerar(int(input("Digite a aceleração: ")))
carro.mostrar_velocidade()
carro.frear(int(input("Digite a frenagem: ")))
carro.mostrar_velocidade()
