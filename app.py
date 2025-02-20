from flask import Flask, render_template, jsonify, request

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

#@app.route('/banco/conta', methods=['GET'])
#def consultar_conta():
#    return 

@app.route('/banco/conta/<numero_conta>/saldo', methods=['GET'])
def consultar_saldo(numero_conta):
    dados = request.get_json()
    numero_conta = dados.get("numero_conta")

    if not numero_conta:
        return jsonify({"erro": "Número da conta é obrigatório"}), 400

    saldo = banco.consultar_saldo(numero_conta)
    return jsonify({"mensagem": saldo})


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
