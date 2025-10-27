from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger
from db import db_service

# Cria o App e configura o CORS
app = Flask(__name__)
CORS(app)

# Configuracoes para a documentacao
app.config['SWAGGER'] = {
    'title': 'API de Gestão Ambiental (OGAS)',
    'uiversion': 3,
    'description': 'API RESTful para o projeto de APS, permitindo o gerenciamento de indicadores ambientais.',
    'version': '1.0.0'
}
swagger = Swagger(app)


# Lista todos os indicadores
@app.route('/indicadores', methods=['GET'])
def get_indicadores():
    """
    Lista todos os indicadores ambientais
    ---
    tags:
      - Indicadores
    responses:
      200:
        description: Uma lista de todos os indicadores.
        schema:
          type: array
          items:
            $ref: '#/definitions/Indicador'
    """
    result, error = db_service.get_all_indicadores()
    if error:
        return jsonify({"erro": error}), 500
    return jsonify(result)

# Lista Indicador pelo ID
@app.route('/indicadores/<int:id>', methods=['GET'])
def get_indicador(id):
    """
    Busca um indicador específico pelo ID
    ---
    tags:
      - Indicadores
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: O ID único do indicador a ser buscado.
    responses:
      200:
        description: O indicador correspondente ao ID.
        schema:
          $ref: '#/definitions/Indicador'
      404:
        description: Indicador não encontrado.
    """
    result, error = db_service.get_indicador_by_id(id)
    if error:
        return jsonify({"erro": error}), 500
    if not result:
        return jsonify({"erro": "Indicador não encontrado"}), 404
    return jsonify(result)

# Adiciona um novo indicador
@app.route('/indicadores', methods=['POST'])
def add_indicador():
    """
    Adiciona um novo indicador ambiental
    ---
    tags:
      - Indicadores
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        description: O objeto do indicador a ser criado.
        schema:
          $ref: '#/definitions/IndicadorInput'
    responses:
      201:
        description: Indicador criado com sucesso.
        schema:
          $ref: '#/definitions/Indicador'
      400:
        description: Dados incompletos ou inválidos.
    """
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
    """
    Atualiza um indicador existente
    ---
    tags:
      - Indicadores
    consumes:
      - application/json
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: O ID do indicador a ser atualizado.
      - in: body
        name: body
        required: true
        description: O objeto com os dados atualizados do indicador.
        schema:
          $ref: '#/definitions/IndicadorInput'
    responses:
      200:
        description: Indicador atualizado com sucesso.
        schema:
          $ref: '#/definitions/Indicador'
      400:
        description: Dados inválidos.
      404:
        description: Indicador não encontrado.
    """
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
    """
    Deleta um indicador
    ---
    tags:
      - Indicadores
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: O ID do indicador a ser deletado.
    responses:
      204:
        description: Indicador deletado com sucesso.
      404:
        description: Indicador não encontrado.
    """
    rowcount, error = db_service.delete_indicador_by_id(id)
    
    if error:
        return jsonify({"erro": error}), 500
    if rowcount == 0:
        return jsonify({"erro": "Indicador não encontrado"}), 404
        
    return '', 204


# Definicoes de Schema para o Swagger
@app.route('/definitions')
def definitions():
    """
    Definições de modelo para a documentação Swagger
    ---
    definitions:
      Indicador:
        type: object
        properties:
          id:
            type: integer
            description: O ID único do indicador (gerado pelo banco).
          empresa:
            type: string
          ano:
            type: integer
          consumo_agua_m3:
            type: number
            format: float
          residuos_ton:
            type: number
            format: float
          emissoes_co2_ton:
            type: number
            format: float
      IndicadorInput:
        type: object
        description: Modelo de dados para criar ou atualizar um indicador (sem o ID).
        properties:
          empresa:
            type: string
          ano:
            type: integer
          consumo_agua_m3:
            type: number
            format: float
          residuos_ton:
            type: number
            format: float
          emissoes_co2_ton:
            type: number
            format: float
    """
    pass


# Executa o servidor
if __name__ == '__main__':
    app.run(debug=True)