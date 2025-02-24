import pytest

#from typing import ByteString
from backend.conta import Conta, ContaBonus, ContaPoupanca
from backend.operacoes import Sistema_Banco

# Testes para a classe conta.
def test_conta_initialization():
    conta = Conta("12345", 100.0)
    assert conta.numero_conta == "12345"
    assert conta.saldo == 100.0

def test_conta_str():
    conta = Conta("12345", 100.0)
    assert str(conta) == "Conta : 12345 , \nSaldo: 100.0"    

# Testes para a classe ContaBônus.
def test_conta_bonus_initialization():
    conta_bonus = ContaBonus("54321")
    assert conta_bonus.numero_conta == "54321"
    assert conta_bonus.saldo == 0
    assert conta_bonus.pontos == 10

# Testes para operação depositar da ContaBonus.
def test_conta_bonus_depositar():
    conta_bonus = ContaBonus("54321")
    resultado = conta_bonus.depositar(300)
    assert conta_bonus.saldo == 300, "O saldo da conta bônus não foi atualizado corretamente."
    assert conta_bonus.pontos == 13, "Os pontos não foram calculados corretamente."
    assert resultado == "R$ 300.00 depositados com sucesso. Pontos acumulados: 13.", "A mensagem de retorno do depósito está incorreta."

# Testes para operação transferência da ContaBonus.
def test_conta_bonus_receber_transferencia():
    conta_bonus = ContaBonus("54321")
    resultado = conta_bonus.receber_transferencia(400)
    assert conta_bonus.saldo == 400
    assert conta_bonus.pontos == 12  # 10 pontos iniciais + 2 pontos (400 // 200)

# Testes para a Classe ContaPoupança.
def test_conta_poupanca_initialization():
    conta_poupanca = ContaPoupanca("67890")
    assert conta_poupanca.numero_conta == "67890"
    assert conta_poupanca.saldo == 0


# Testes para operação render juros da ContaPoupança.
def test_conta_poupanca_render_juros():
    conta_poupanca = ContaPoupanca("67890", 1000.0)
    resultado = conta_poupanca.render_juros(10)  # 10% de juros
    assert conta_poupanca.saldo == 1100.0
    assert resultado == "\n Novo saldo após rendimento: R$ 1100.00" 

# Testes para a classe Sistema Banco.
def test_sistema_banco_criar_conta():
    sistema = Sistema_Banco()
    resultado = sistema.criar_conta("12345", 100.0)
    assert resultado == "\n Conta criada com sucesso!"
    assert "12345" in sistema.contas  


# Testes para criação de Sistema ContaBonus.
def test_sistema_banco_criar_conta_bonus():
    sistema = Sistema_Banco()
    resultado = sistema.criar_conta_bonus("54321")
    assert resultado == "\n Conta criada com sucesso!"
    assert "54321" in sistema.contas
    assert isinstance(sistema.contas["54321"], ContaBonus)


# Testes para criação de Sistema ContaPoupança.
def test_sistema_banco_criar_conta_poupanca():
    sistema = Sistema_Banco()
    resultado = sistema.criar_conta_poupanca("67890")
    assert resultado == "\n Conta criada com sucesso!"
    assert "67890" in sistema.contas
    assert isinstance(sistema.contas["67890"], ContaPoupanca)

# Testes para operação de consultarSaldo.
def test_sistema_banco_consultar_saldo():
    sistema = Sistema_Banco()
    sistema.criar_conta("12345", 100.0)
    resultado = sistema.consultar_saldo("12345")
    assert resultado == "\n Saldo: R$ 100.00"

# Testes para operação de creditar.
def test_sistema_banco_creditar():
    sistema = Sistema_Banco()
    sistema.criar_conta("12345", 100.0)
    resultado = sistema.creditar("12345", 50.0)
    assert resultado == "\n R$ 50.00 creditados na conta 12345."
    assert sistema.contas["12345"].saldo == 150.0

# Testes para operação de debitar.
def test_sistema_banco_debitar():
    sistema = Sistema_Banco()
    sistema.criar_conta("12345", 100.0)
    resultado = sistema.debitar("12345", 50.0)
    assert resultado == "\n R$ 50.00 debitados da conta 12345."
    assert sistema.contas["12345"].saldo == 50.0      

# Testes para operação de transferir.
def test_sistemas_banco_transferir():
    sistema = Sistema_Banco()
    sistema.criar_conta("12345", 100.0)
    sistema.criar_conta("67890", 50.0)
    resultado = sistema.transferir("12345", "67890", 30.0)
    assert resultado == "\n R$ 30.00 transferidos de 12345 para 67890."
    assert sistema.contas["12345"].saldo == 70.0
    assert sistema.contas["67890"].saldo == 80.0


# Testes para operação de render juros.
def test_sistema_banco_render_juros():
    sistema = Sistema_Banco()
    resultado_criacao = sistema.criar_conta_poupanca("67890")
    assert resultado_criacao == "\n Conta criada com sucesso!", "Falha ao criar conta poupança."

    resultado_credito = sistema.creditar("67890", 1000.0)
    assert resultado_credito == "\n R$ 1000.00 creditados na conta 67890.", "Falha ao creditar valor na conta poupança."
    
    resultado_juros = sistema.render_juros("67890", 10)
    assert resultado_juros == "\n Novo saldo após rendimento: R$ 1100.00", "Falha ao render juros na conta poupança."
    
    conta = sistema.contas.get("67890")
    assert conta.saldo == 1100.0, "O saldo da conta poupança não foi atualizado corretamente após o rendimento de juros."


# Testes para a operação de creditar na conta inexistente.
def test_sistema_banco_creditar_conta_inexistente():
    sistema = Sistema_Banco()
    resultado = sistema.creditar("99999", 50.0)
    assert resultado == "\n Conta não encontrada."

# Testes para a operação de debitar na conta inexistente. 
def test_sistema_banco_debitar_conta_inexistente():
    sistema = Sistema_Banco()
    resultado = sistema.debitar("99999", 50.0)
    assert resultado == "Conta não encontrada."

# Testes para a operação de transferir na conta inexistente.
def test_sistema_banco_transferir_conta_inexistente():
    sistema = Sistema_Banco()
    resultado = sistema.transferir("12345", "67890", 30.0)
    assert resultado == "Uma ou ambas as contas não foram encontradas."   
  
# Testes para operação de render juros conta não-poupança.
def test_sistema_banco_render_juros_conta_nao_poupanca():
    sistema = Sistema_Banco()
    sistema.criar_conta("12345", 100.0)
    resultado = sistema.render_juros("12345", 10)
    assert resultado == "\n Operação disponível apenas para contas poupança."

if __name__ == '__main__':
    pytest.main()    
