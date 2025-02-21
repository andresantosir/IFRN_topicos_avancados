from flask import Flask, render_template, jsonify, make_response, request


app = Flask(__name__)

# Simulando um banco de dados (dicionário)
banco = {}

# Página inicial
@app.route('/')
def home():
    return render_template('index.html')

# API para cadastrar conta
@app.route('/banco/conta', methods=['POST'])
def cadastrar_conta():
    dados = request.json
    numero_conta = dados.get("numero_conta")

    if not numero_conta:
        return jsonify({"erro": "Número da conta é obrigatório!"}), 400

    if numero_conta in banco:
        return jsonify({"erro": "Conta já existe!"}), 400

    banco[numero_conta] = {"saldo": 0.0}  # Criando a conta com saldo inicial 0
    return jsonify({"mensagem": "Conta criada com sucesso!", "conta": numero_conta}), 201


@app.route('/banco/conta/<numero_conta>/saldo', methods=['GET'])
def consultar_saldo(numero_conta):
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
