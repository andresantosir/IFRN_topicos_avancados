from backend.conta import Conta

class Sistema_Banco:
    
    def __init__(self):
        self.contas = {}    # Inicia um vetor chamado "contas"
        
    def criar_conta(self, numero_conta):
        if numero_conta in self.contas:
            return "Conta já existe."
        self.contas[numero_conta] = Conta(numero_conta)
        return "Conta criada com sucesso!"