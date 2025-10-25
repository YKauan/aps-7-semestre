from flask import Flask, request, jsonify
from flask_cors import CORS
from db import db_service

# Cria o App e configura o CORS
app = Flask(__name__)
CORS(app)

# Retorna todos os indicadores
@app.route('/indicadores', methods=['GET'])
def get_indicadores():
    result, error = db_service.get_all_indicadores()
    if error:
        return jsonify({"erro": error}), 500
    return jsonify(result)

# Lista um indicador especifico
@app.route('/indicadores/<int:id>', methods=['GET'])
def get_indicador(id):
    result, error = db_service.get_indicador_by_id(id)
    if error:
        return jsonify({"erro": error}), 500
    if not result:
        return jsonify({"erro": "Indicador não encontrado"}), 404
    return jsonify(result)

# Adiciona um indicador
@app.route('/indicadores', methods=['POST'])
def add_indicador():
    novo_indicador = request.json
    if not novo_indicador or not all(k in novo_indicador for k in ["empresa", "ano", "consumo_agua_m3", "residuos_ton", "emissoes_co2_ton"]):
        return jsonify({"erro": "Dados incompletos"}), 400
    
    new_record, error = db_service.add_new_indicador(novo_indicador)
    if error:
        return jsonify({"erro": error}), 500
    
    return jsonify(new_record), 201

# Atualiza um indicador
@app.route('/indicadores/<int:id>', methods=['PUT'])
def update_indicador(id):
    dados_atualizados = request.json
    if not dados_atualizados:
        return jsonify({"erro": "Dados inválidos"}), 400

    rowcount, updated_record, error = db_service.update_indicador_by_id(id, dados_atualizados)
    
    if error:
        return jsonify({"erro": error}), 500
    if rowcount == 0:
        return jsonify({"erro": "Indicador não encontrado"}), 404
    
    return jsonify(updated_record)

# Deleta um indicador
@app.route('/indicadores/<int:id>', methods=['DELETE'])
def delete_indicador(id):
    rowcount, error = db_service.delete_indicador_by_id(id)
    
    if error:
        return jsonify({"erro": error}), 500
    if rowcount == 0:
        return jsonify({"erro": "Indicador não encontrado"}), 404
        
    return '', 204

# Executa o servidor
if __name__ == '__main__':
    app.run(debug=True)