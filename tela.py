def main():
    while True:
        
        print("\n========== SISTEMA BANCÁRIO ==========")
        print("1. Cadastrar Conta")
        print("2. Consultar Saldo")
        print("3. Crédito")
        print("4. Débito")
        print("5. Transferência")
        print("6. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            numero_conta =input("Digite o número da conta: ")
        elif opcao == "2":
            numero_conta =input("Digite o número da conta que deseja consultar o saldo: ")
        elif opcao == "3":
            numero_conta =input("Digite o número da conta que deseja creditar valor: ")
            dinheiro = float(input("Digite a quantidade de dinheiro que deseja creditar: "))
        elif opcao == "4":
            numero_conta =input("Digite o número da conta que deseja retirar valor: ")
            dinheiro = float(input("Digite a quantidade de dinheiro que deseja debitar: "))
        #elif opcao == "5":
            #numero_conta =input("Digite o número da conta: ")
        elif opcao == "6":
            print("Encerrando...")
            break
        else:
            print("Digite um número válido.")
            
if __name__ == "__main__":
    main()