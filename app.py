from flask import Flask, render_template, jsonify, request # type: ignore
#from flask import Flask, render_template, jsonify, request # type: ignore
#from backend.conta import Conta, ContaBonus, ContaPoupanca

from bd import Conta

app = Flask(__name__)

# banco de dados fake (lista).
contas = []
contas_bonus = []
contas_poupanca = []

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

    # Verifica se a conta já existe em qualquer lista.
    todas_contas = contas + contas_bonus + contas_poupanca
    if any(c['numero_conta'] == numero_conta for c in todas_contas):
        return jsonify({"erro": "Conta já existe!"}), 400

    nova_conta = {
        "id": len(contas) + 1,
        "numero_conta": numero_conta,
        "saldo": 0.0
    }
    contas.append(nova_conta)
    return jsonify({"mensagem": "Conta criada com sucesso!", "conta": numero_conta}), 201

# Cria conta bonus (nova rota).
@app.route('/banco/conta/bonus', methods=['POST'])
def cadastrar_conta_bonus(): # Cadastro de uma nova conta bonus.
    dados = request.json
    numero_conta = dados.get("numero_conta")

    if not numero_conta:
        return jsonify({"erro": "Número da conta é obrigatório!"}), 400
    
    todas_contas = contas + contas_bonus + contas_poupanca
    if any(c['numero_conta'] == numero_conta for c in todas_contas):
        return jsonify({"erro": "Conta já existe!"}), 400
    
    nova_conta = {
        "id": len(contas_bonus) + 1,
        "numero_conta": numero_conta,
        "saldo": 0.0,
        "pontos": 10 # Pontuação inicial.
    }
    contas_bonus.append(nova_conta)
    return jsonify({"mensagem": "Conta bonus criada com sucesso!", "conta": numero_conta}), 201

# Cria conta poupança (nova rota).
@app.route('/banco/conta/poupanca', methods=['POST'])
def cadastrar_conta_poupanca(): # Cadastro de uma nova conta poupança.
    dados = request.json
    numero_conta = dados.get("numero_conta")

    if not numero_conta:
        return jsonify({"erro": "Número da conta é obrigatório!"}), 400
    
    todas_contas = contas + contas_bonus + contas_poupanca
    if any(c['numero_conta'] == numero_conta for c in todas_contas):
        return jsonify({"erro": "Conta já existe!"}), 400
    
    nova_conta = {
        "id": len(contas_poupanca) + 1,
        "numero_conta": numero_conta,
        "saldo": 0.0
    }
    contas_poupanca.append(nova_conta)
    return jsonify({"mensagem": "Conta poupança criada com sucesso!", "conta": numero_conta}), 201

# Consulta saldo (nova rota).
@app.route('/banco/conta/<numero_conta>/saldo', methods=['GET'])
def consultar_saldo(numero_conta): # Consulta o saldo de uma conta bancária.
    todas_contas = contas + contas_bonus + contas_poupanca
    for conta in todas_contas:
        if conta['numero_conta'] == numero_conta:
            return jsonify({"mensagem": f"Saldo: R$ {conta['saldo']:.2f}"}), 200
    return jsonify({"erro": "Conta não encontrada!"}), 404


# Creditar valor.
@app.route('/banco/conta/<numero>/saldo', methods=['PUT'])
def creditar(numero): # Adiciona um valor do saldo de uma conta bancária.
    dados = request.json
    valor = dados.get("valor", 0)
    
    todas_contas = contas + contas_bonus + contas_poupanca
    for conta in todas_contas:
        if conta['numero_conta'] == numero:
            if valor <= 0:
                return jsonify({"erro": "Valor deve ser positivo"}), 400
            conta['saldo'] += valor
            return jsonify({"mensagem": f"R$ {valor:.2f} creditados na conta com sucesso"}), 200
        
    return jsonify({"erro": "Conta não encontrada"}), 404


# Debitar valor.
@app.route('/banco/conta/<numero>/debito', methods=['PUT'])
def debitar(numero): # Retira um valor do saldo de uma conta bancária.
    dados = request.json
    valor = dados.get("valor", 0)
    
    todas_contas = contas + contas_bonus + contas_poupanca
    for conta in todas_contas:
        if conta['numero_conta'] == numero:
            if valor <= 0:
                return jsonify({"erro": "Valor deve ser positivo"}), 400
            if conta['saldo'] < valor:
                return jsonify({"erro": "Saldo insuficiente"}), 400
            conta['saldo'] -= valor
            return jsonify({"mensagem": f"R$ {valor:.2f} debitados da conta com sucesso"}), 200
    
    return jsonify({"erro": "Conta não encontrada"}), 404

# Trasnferencia de valor.
@app.route('/banco/conta/transferencia', methods=['PUT'])
def transferir(): # Realiza uma transferência entre duas contas bancárias.
    dados = request.json
    conta_origem = dados.get("conta_origem")
    conta_destino = dados.get("conta_destino")
    valor = dados.get("valor", 0)

    conta_origem = None
    conta_destino = None
    todas_contas = contas + contas_bonus + contas_poupanca
    for conta in todas_contas:
        if conta['numero_conta'] == conta_origem:
            conta_origem = conta
        if conta['numero_conta'] == conta_destino:
            conta_destino = conta

    if not conta_origem or not conta_destino:
        return jsonify({"erro": "Conta de origem/destino não encontrada"}), 404

    if valor <= 0:
        return jsonify({"erro": "Valor deve ser positivo"}), 400

    if conta_origem['saldo'] < valor:
        return jsonify({"erro": "Saldo insuficiente"}), 400

    conta_origem['saldo'] -= valor
    conta_destino['saldo'] += valor
    return jsonify({"mensagem": f" transferência de R${valor:.2f} realizada"}), 200      

# Render juros (apenas para poupança).
@app.route('/banco/conta/rendimento', methods=['PUT'])
def render_juros(): # Aplica juros ao saldo de uma conta poupança.
    dados = request.json
    numero_conta = dados.get("numero")
    taxa = dados.get("taxa")
    
    for conta in contas_poupanca:
        if conta['numero_conta'] == numero_conta:
            juros= conta['saldo'] * (taxa / 100)
            conta['saldo'] += juros
            return jsonify({"mensagem": f"Rendimento de R$ {juros:.2f} aplicado"}), 200
        
    return jsonify({"erro": "Conta poupança não encontrada"}), 404


# Consultar tipo de conta.
@app.route('/banco/conta', methods=['GET'])
def consultar_conta():
    numero_conta = request.args.get('numero_conta')
    todas_contas = contas + contas_bonus + contas_poupanca
    for conta in todas_contas:
        if conta["numero_conta"] == numero_conta:
            resposta = {
                "numero_conta": conta["numero_conta"],
                "saldo": conta["saldo"]
            }
            if conta in contas_bonus:
                resposta["tipo"] = "ContaBonus"
                resposta["pontos"] = conta.get["pontos", 0]
            elif conta in contas_poupanca:
                resposta["tipo"] = "ContaPoupanca"
            else:
                resposta["tipo"] = "Conta"
            return jsonify(resposta), 200

    return jsonify({"erro": "Conta não encontrada"}), 404                
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