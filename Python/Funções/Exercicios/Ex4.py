class ContaBancaria:
	def __init__(self, titular, saldo=0):
		self.titular = titular
		self.__saldo = saldo

	def depositar(self, valor):
		if valor > 0:
			self.__saldo += valor

	def sacar(self, valor):
		if valor > self.__saldo:
			print("Saldo insuficiente.")
			return

		if valor > 0:
			self.__saldo -= valor

	def exibir_saldo(self):
		print(f"Titular: {self.titular}")
		print(f"Saldo atual: R$ {self.__saldo:.2f}")


titular = input("Digite o nome do titular: ")
deposito = float(input("Digite o valor para depósito: "))
saque = float(input("Digite o valor para saque: "))

conta = ContaBancaria(titular)
conta.depositar(deposito)
conta.sacar(saque)
conta.exibir_saldo()
