import sys
sys.path.append(r'C:\Users\andre\Desktop\IFRN_topicos_avancados') # altere o caminho da pasta para o seu diretório de trabalho
from backend.operacoes import Sistema_Banco

def main():
    banco = Sistema_Banco()
    while True:
        
        print("\n========== SISTEMA BANCÁRIO ==========")
        print("1. Cadastrar Conta")
        print("2. Consultar Saldo")
        print("3. Crédito")
        print("4. Débito")
        print("5. Transferência")
        print("6. Render Juros")
        print("7. Cadastrar Conta Bônus")
        print("8. Cadastrar Conta Poupança")
        print("9. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            numero_conta =input("Digite o número da conta: ")
            print(banco.criar_conta(numero_conta))
            
        elif opcao == "2":
            numero_conta =input("Digite o número da conta que deseja consultar o saldo: ")
            print(banco.consultar_saldo(numero_conta))
            
        elif opcao == "3":
            numero_conta =input("Digite o número da conta que deseja creditar valor: ")
            dinheiro = float(input("Digite a quantidade de dinheiro que deseja creditar: "))
            print(banco.creditar(numero_conta, dinheiro))
            
        elif opcao == "4":
            numero_conta =input("Digite o número da conta que deseja retirar valor: ")
            dinheiro = float(input("Digite a quantidade de dinheiro que deseja debitar: "))
            print(banco.debitar(numero_conta, dinheiro))
            
        elif opcao == "5":
            conta_origem = input("Digite o número da conta de origem: ")
            conta_destino = input("Digite o número da conta de destino: ")
            dinheiro = float(input("Digite o valor para transferência: "))
            print(banco.transferir(conta_origem, conta_destino, dinheiro))
            
        elif opcao == "6":
            numero_conta = input("Digite o número da conta: ")
            taxa = input("Digite sua taxa de juros: ")
            print(banco.render_juros(numero_conta, taxa))
        
        elif opcao == "7":
            numero_conta =input("Digite o número da conta bônus: ")
            print(banco.criar_conta_bonus(numero_conta))
            
        elif opcao == "8":
            numero_conta =input("Digite o número da conta poupança: ")
            print(banco.criar_conta_poupanca(numero_conta))
        
        elif opcao == "9":
            print("Encerrando...")
            break
        else:
            print("Digite um número válido.")
            
if __name__ == "__main__":
    main()