class Conta:
    def __init__(self, numero_conta, saldo =0.0):
        self.numero_conta = numero_conta
        self.saldo = saldo
    
    def __str__(self):
        return f"Conta : {self.numero_conta} , \nSaldo: {self.saldo}"