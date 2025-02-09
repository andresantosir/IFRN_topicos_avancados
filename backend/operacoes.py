from backend.conta import Conta, ContaBonus, ContaPoupanca

class Sistema_Banco:
    
    def __init__(self):
        self.contas = {}    # Inicia um vetor chamado "contas"
        
    def criar_conta(self, numero_conta):
        if numero_conta in self.contas:
            return "\n Conta já existe."
        self.contas[numero_conta] = Conta(numero_conta)
        return "\n Conta criada com sucesso!"
    
    def criar_conta_bonus(self, numero_conta):
        if numero_conta in self.contas:
            return "\n Conta já existe."
        self.contas[numero_conta] = ContaBonus(numero_conta)
        return "\n Conta Bonus criada com sucesso!"
    
    def criar_conta_poupanca(self, numero_conta,valor):
        if numero_conta in self.contas:
            return "\n Conta já existe."
        self.contas[numero_conta] = ContaPoupanca(numero_conta,valor) 
        return "\n Conta Poupanca criada com sucesso!"
    
    def consultar_saldo(self, numero_conta):
        conta = self.contas.get(numero_conta)
        if not conta:
            return "\n Conta não encontrada."
        return f"\n Saldo: R$ {conta.saldo:.2f}"
    
    def creditar(self, numero_conta, valor):
        conta = self.contas.get(numero_conta)
        if not conta:
            return "\n Conta não encontrada."
        if valor <= 0:
            return "O valor não pode ser negativo, deve ser positivo."
        conta.saldo += valor
        return f"\n R$ {valor:.2f} creditados na conta {numero_conta}."
    
    def transferir(self, conta_origem, conta_destino, valor):
        if conta_origem not in self.contas or conta_destino not in self.contas:
            return "Uma ou ambas as contas não foram encontradas."
        if valor <= 0:
            return "O valor deve ser positivo."
        if self.contas[conta_origem].saldo < valor:
            return "Saldo insuficiente." 
        self.contas[conta_origem].saldo -= valor
        self.contas[conta_destino].saldo += valor
        return f"\n R$ {valor:.2f} transferidos de {conta_origem} para {conta_destino}."

    def debitar(self, numero_conta, valor):
        conta = self.contas.get(numero_conta)
        if not conta:
            return "Conta não encontrada."
        if valor <= 0:
            return "O valor dever ser positivo."
        if valor > conta.saldo:
            return "Saldo insuficiente." 
        conta.saldo -= valor
        return f"\n R$ {valor:.2f} debitados da conta {numero_conta}."    
    
    
    def render_juros(self, numero_conta, taxa):
        conta = self.contas.get(numero_conta) 
        if not conta:
            return "\n Conta não encontrada."
        if isinstance(conta, ContaPoupanca):
            return conta.render_juros(taxa)
        return "\n Operação disponível apenas para contas poupança."