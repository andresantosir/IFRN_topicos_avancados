from backend.conta import Conta

class Sistema_Banco:
    
    def __init__(self):
        self.contas = {}    # Inicia um vetor chamado "contas"
        
    def criar_conta(self, numero_conta):
        if numero_conta in self.contas:
            return "Conta já existe."
        self.contas[numero_conta] = Conta(numero_conta)
        return "Conta criada com sucesso!"
    
    def consultar_saldo(self, numero_conta):
        conta = self.contas.get(numero_conta)
        if not conta:
            return "Conta não encontrada."
        return f"Saldo: R$ {conta.saldo:.2f}"
    
    def creditar(self, numero_conta, valor):
        conta = self.contas.get(numero_conta)
        if not conta:
            return "Conta não encontrada."
        if valor <= 0:
            return "O valor não pode ser negativo, deve ser positivo."
        conta.saldo += valor
        return f"R$ {valor:.2f} creditados na conta {numero_conta}."
    
    def transferir(self, conta_origem, conta_destino, valor):
        if conta_origem not in self.contas or conta_destino not in self.contas:
            return "Uma ou ambas as contas não foram encontradas."
        if valor <= 0:
            return "O valor deve ser positivo."
        if self.contas[conta_origem].saldo < valor:
            return "Saldo insuficiente." 
        self.contas[conta_origem].saldo -= valor
        self.contas[conta_destino].saldo += valor
        return f"R$ {valor:.2f} transferidos de {conta_origem} para {conta_destino}."

    def debitar(self, numero_conta, valor):
        conta = self.contas.get(numero_conta)
        if not conta:
            return "Conta não encontrada."
        if valor <= 0:
            return "O valor dever ser positivo."
        if valor > conta.saldo:
            return "Saldo insuficiente." 
        conta.saldo -= valor
        return f"R$ {valor:.2f} debitados da conta {numero_conta}."    