class Conta:
    def __init__(self, numero_conta, saldo =0.0):
        self.numero_conta = numero_conta
        self.saldo = saldo
    
    def __str__(self):
        return f"Conta : {self.numero_conta} , \nSaldo: {self.saldo}"
    
class ContaBonus(Conta):
    def __init__(self, numero_conta, saldo=0):
        super().__init__(numero_conta, saldo)
        self.pontos = 10                    # Pontuação inicial

    def depositar(self, valor):
        resultado = super().depositar(valor)
        if "depositados" in resultado:
            self.pontos += valor // 100     # 1 ponto para cada R$ 100 depositados
        return resultado

    def receber_transferencia(self, valor):
        self.pontos += valor // 200         # 1 ponto para cada R$ 200 recebidos
        self.saldo += valor
        return f"R$ {valor:.2f} recebidos na conta {self.numero_conta}."
    
class ContaPoupanca(Conta):
    def __init__(self, numero_conta, saldo=0):
        super().__init__(numero_conta, saldo)
        
    def render_juros(self, taxa): #Metodo render Juros encapsulado dentro da classe
        self.saldo += self.saldo * (taxa / 100)
        return f"\n Novo saldo após rendimento: R$ {self.saldo:.2f}"
        