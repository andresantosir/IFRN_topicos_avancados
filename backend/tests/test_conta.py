import unittest
from backend.conta import Conta, ContaBonus, ContaPoupanca

class TestSistemaBanco(unittest.TestCase):
    def setUp(self):
        self.conta = Conta("123", 500.0)
        self.conta_bonus = ContaBonus("456")
        self.conta_poupanca = ContaPoupanca("789", 1000.0)
    
    def test_cadastrar_conta(self):
        self.assertEqual(self.conta.numero_conta, "123")
        self.assertEqual(self.conta.saldo, 500.0)
    
    def test_cadastrar_conta_bonus(self):
        self.assertEqual(self.conta_bonus.numero_conta, "456")
        self.assertEqual(self.conta_bonus.saldo, 10)
#       self.assertEqual(self.conta_bonus.pontos, 10)
    
    def test_cadastrar_conta_poupanca(self):
        self.assertEqual(self.conta_poupanca.numero_conta, "789")
        self.assertEqual(self.conta_poupanca.saldo, 1000.0)
    
    def test_consultar_saldo(self):
        self.assertEqual(self.conta.saldo, 500.0)

    def test_creditar_valor(self):
        self.conta.saldo += 200
        self.assertEqual(self.conta.saldo, 700)

    def test_creditar_valor_negativo(self):
        with self.assertRaises(ValueError):
            self.conta.saldo += -200    
    
    def test_debitar_valor(self):
        self.conta.debitar(200)
        self.assertEqual(self.conta.saldo, 300.0)

    def test_debitar_valor_negativo(self):
        with self.assertRaises(ValueError):
            self.conta.debitar(-200)

    def test_debitar_saldo_insuficiente(self):
        with self.assertRaises(ValueError):
            self.conta.debitar(1000)            
    
    def test_transferencia_sucesso(self):
        self.conta.saldo -= 200
        self.conta_poupanca.saldo += 200
        self.assertEqual(self.conta.saldo, 300.0)
        self.assertEqual(self.conta_bonus.saldo, 1200.0)

    def test_transferencia_valor_negativo(self):
        with self.assertRaises(ValueError):
            self.conta.saldo -= -200

    def test_trasferencia_saldo_insuficiente(self):
        with self.assertRaises(ValueError):
            self.conta.saldo -= 1000            
    
    def test_render_juros(self):
        self.conta_poupanca.render_juros(10)
        self.assertEqual(self.conta_poupanca.saldo, 1100.0)

if __name__ == '__main__':
    unittest.main()    
