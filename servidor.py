# servidor_api.py
# Web Service para Gestão Ambiental em Goiás (OGAS-API)

from flask import Flask, request, jsonify

# Inicialização do aplicativo Flask
app = Flask(__name__)

# Simulação de um banco de dados em memória
indicadores_db = {
    1: {"empresa": "ABC Indústria de Alimentos", "ano": 2023, "consumo_agua_m3": 1500, "residuos_ton": 75, "emissoes_co2_ton": 320},
    2: {"empresa": "Transportadora XYZ", "ano": 2023, "consumo_agua_m3": 400, "residuos_ton": 15, "emissoes_co2_ton": 950},
}
proximo_id = 3

# Rota para obter todos os indicadores
@app.route('/indicadores', methods=['GET'])
def get_indicadores():
    """Retorna a lista de todos os indicadores ambientais."""
    return jsonify(indicadores_db)

# Rota para obter um indicador específico pelo ID
@app.route('/indicadores/<int:id>', methods=['GET'])
def get_indicador(id):
    """Retorna um indicador ambiental específico."""
    indicador = indicadores_db.get(id)
    if not indicador:
        return jsonify({"erro": "Indicador não encontrado"}), 404
    return jsonify(indicador)

# Rota para adicionar um novo indicador
@app.route('/indicadores', methods=['POST'])
def add_indicador():
    """Adiciona um novo indicador ambiental."""
    global proximo_id
    novo_indicador = request.json
    if not novo_indicador or not all(k in novo_indicador for k in ["empresa", "ano", "consumo_agua_m3", "residuos_ton", "emissoes_co2_ton"]):
        return jsonify({"erro": "Dados incompletos"}), 400
    
    indicadores_db[proximo_id] = novo_indicador
    proximo_id += 1
    return jsonify(novo_indicador), 201

# Rota para atualizar um indicador existente
@app.route('/indicadores/<int:id>', methods=['PUT'])
def update_indicador(id):
    """Atualiza um indicador ambiental existente."""
    if id not in indicadores_db:
        return jsonify({"erro": "Indicador não encontrado"}), 404
        
    dados_atualizados = request.json
    if not dados_atualizados:
        return jsonify({"erro": "Dados inválidos"}), 400
        
    indicadores_db[id].update(dados_atualizados)
    return jsonify(indicadores_db[id])

# Rota para remover um indicador
@app.route('/indicadores/<int:id>', methods=['DELETE'])
def delete_indicador(id):
    """Remove um indicador ambiental."""
    if id not in indicadores_db:
        return jsonify({"erro": "Indicador não encontrado"}), 404
        
    del indicadores_db[id]
    return '', 204

# Execução do servidor
if __name__ == '__main__':
    app.run(debug=True)