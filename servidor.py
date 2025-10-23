import json
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_FILE = 'db.json'

# Carrega os dados do banco
def carregar_dados():
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("nao foi possivel carregar o banco")
        return {"indicadores": {}}

# Sava os dados no banco
def salvar_dados(dados):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

# Lista os indicadores existentes
@app.route('/indicadores', methods=['GET'])
def get_indicadores():
    dados = carregar_dados()
    return jsonify(dados.get('indicadores', {}))

# Lista apenas um indicador
@app.route('/indicadores/<string:id>', methods=['GET'])
def get_indicador(id):
    dados = carregar_dados()
    indicador = dados.get('indicadores', {}).get(id)
    if not indicador:
        return jsonify({"erro": "Indicador não encontrado"}), 404
    return jsonify(indicador)

# Adiciona um novo indicador
@app.route('/indicadores', methods=['POST'])
def add_indicador():
    novo_indicador = request.json
    if not novo_indicador or not all(k in novo_indicador for k in ["empresa", "ano", "consumo_agua_m3", "residuos_ton", "emissoes_co2_ton"]):
        return jsonify({"erro": "Dados incompletos"}), 400
    
    dados = carregar_dados()
    novo_id = str(uuid.uuid4())
    
    dados['indicadores'][novo_id] = novo_indicador
    
    salvar_dados(dados)
    
    return jsonify(novo_indicador), 201

# Atualiza um indicador
@app.route('/indicadores/<string:id>', methods=['PUT'])
def update_indicador(id):
    dados = carregar_dados()

    if id not in dados.get('indicadores', {}):
        return jsonify({"erro": "Indicador não encontrado"}), 404
        
    dados_atualizados = request.json
    if not dados_atualizados:
        return jsonify({"erro": "Dados inválidos"}), 400
        
    dados['indicadores'][id].update(dados_atualizados)
    salvar_dados(dados)
    
    return jsonify(dados['indicadores'][id])

# Deleta um indicador
@app.route('/indicadores/<string:id>', methods=['DELETE'])
def delete_indicador(id):
    dados = carregar_dados()

    if id not in dados.get('indicadores', {}):
        return jsonify({"erro": "Indicador não encontrado"}), 404
        
    del dados['indicadores'][id]
    salvar_dados(dados)
    
    return '', 204

# Sobe o servidor 
if __name__ == '__main__':
    app.run(debug=True)