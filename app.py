from flask import Flask, render_template, jsonify, request # type: ignore
from backend.conta import Conta, ContaBonus, ContaPoupanca

app = Flask(__name__)

# Simulando um banco de dados (dicionário)
banco = {}

# Pagina inicial.
@app.route('/')
def home(): # Página inicial.
    return render_template('index.html')

# API para cadastrar conta
@app.route('/banco/conta', methods=['POST'])
def cadastrar_conta(): # Cadastro de uma nova conta bancária.
    dados = request.json
    numero_conta = dados.get("numero_conta")

    if not numero_conta:
        return jsonify({"erro": "Número da conta é obrigatório!"}), 400

    if numero_conta in banco:
        return jsonify({"erro": "Conta já existe!"}), 400

    banco[numero_conta] = {"saldo": 0.0}  # Criando a conta com saldo inicial 0
    return jsonify({"mensagem": "Conta criada com sucesso!", "conta": numero_conta}), 201


@app.route('/banco/conta/<numero_conta>/saldo', methods=['GET'])
def consultar_saldo(numero_conta): # Consulta o saldo de uma conta bancária.
    if not numero_conta:
        return jsonify({"erro": "Número da conta é obrigatório"}), 400

    saldo = banco.get(numero_conta)  # Pegando o saldo da conta

    if saldo is None:
        return jsonify({"erro": "Conta não encontrada"}), 404

    # Garante que saldo é um número antes de formatar
    if isinstance(saldo, dict):  # Se saldo for um dicionário, pega o valor correto
        saldo = saldo.get("valor", 0)  

    try:
        saldo = float(saldo)  # Converte para float, caso não seja ainda
    except ValueError:
        return jsonify({"erro": "Erro ao obter saldo"}), 500

    return jsonify({"mensagem": f"Seu saldo atual é de: R$ {saldo:.2f}"}), 200

@app.route('/banco/conta/', methods=['GET'])
def consultar_conta(): # Consulta os detalhes de uma conta bancária.
    numero_conta = request.args.get("numero")
    conta = banco.get(numero_conta)

    if not conta:
        return jsonify({"erro": "Conta não encontrada"}), 404
    
    resposta = {
        "tipo": conta.__class__.__name__,
        "numero": conta.numero_conta,
        "saldo": conta.saldo
    }
    if isinstance(conta, ContaBonus):
        resposta["bonus"] = conta.pontos

    return jsonify(resposta)

@app.route('/banco/conta/<numero>/saldo', methods=['PUT'])
def creditar(numero): # Adiciona um valor do saldo de uma conta bancária.
    dados = request.json
    valor = dados.get("valor", 0)
    conta = banco.get(numero)
    if not conta:
        return jsonify({"erro": "Conta não encontrada"}), 404
    if valor <= 0:
        return jsonify({"erro": "Valor deve ser positivo"}), 400
    conta.saldo += valor
    return jsonify({"mensagem": f"R$ {valor:.2f} creditados na conta com sucesso"}), 200


@app.route('/banco/conta/<numero>/debito', methods=['PUT'])
def debitar(numero): # Retira um valor do saldo de uma conta bancária.
    dados = request.json
    valor = dados.get("valor", 0)
    conta = banco.get(numero)
    if not conta:
        return jsonify({"erro": "Conta não encontrada"}), 404
    if valor <= 0:
        return jsonify({"erro": "Valor deve ser positivo"}), 400
    if conta.saldo < valor:
        return jsonify({"erro": "Saldo insuficiente"}), 400
    conta.saldo -= valor
    return jsonify({"mensagem": f"R$ {valor:.2f} debitados na conta com sucesso"}), 200

@app.route('/banco/conta/transferencia', methods=['PUT'])
def transferir(): # Realiza uma transferência entre duas contas bancárias.
    dados = request.json
    conta_origem = dados['from']
    conta_destino = dados['to']
    valor = dados['amount']

    if conta_origem not in banco or conta_destino not in banco:
        return jsonify({"erro": "Conta de origem ou destino não encontrada"}), 404
    if valor <= 0:
        return jsonify({"erro": "Valor deve ser positivo"}), 400
    if banco[conta_origem].saldo < valor:
        return jsonify({"erro": "Saldo insuficiente"}), 400
    
    banco[conta_origem].saldo -= valor
    banco[conta_destino].saldo += valor
    return jsonify({"mensagem": f"Trasnferência de R$ {valor:.2f} realizada com sucesso"}), 200

@app.route('/banco/conta/rendimento', methods=['PUT'])
def render_juros(): # Aplica juros ao saldo de uma conta poupança.
    dados = request.json
    numero_conta = dados("numero")
    taxa = dados("taxa")
    conta = banco.get(numero_conta)

    if not conta or not isinstance(conta, ContaPoupanca):
        return jsonify({"erro": "Conta poupança não encontrada ou não é poupança"}), 400
    
    conta.render_juros(taxa)
    return jsonify({"mensagem": "Rendimento aplicado com sucesso"}), 200

#@app.route('/banco/conta/<id>/credito', methods=['PUT'])
#def creditar():
#   return

#@app.route('/banco/conta/<id>/debito', methods=['PUT'])
#def debitar():
#   return

#@app.route('/banco/conta/transferencia', methods=['PUT'])
#def transferencia():
#   return

#@app.route('/banco/conta/rendimento', methods=['PUT'])
#def render_juros():
#   return

if __name__ == '__main__':
    app.run(debug=True)