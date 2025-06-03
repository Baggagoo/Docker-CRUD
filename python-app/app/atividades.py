from flask import Blueprint, jsonify, request
from database import get_db_connection, close_db_connection
from logger_config import log_operacao

atividades_bp = Blueprint('atividades', __name__)

# Listar todas as atividades
@atividades_bp.route('/atividades', methods=['GET'])
def get_atividades():
    """
    Listar todas as atividades
    ---
    responses:
      200:
        description: Lista de atividades
        schema:
          type: array
          items:
            type: object
            properties:
              atividade_id:
                type: integer
                description: ID da atividade
              titulo:
                type: string
                description: Título da atividade
              descricao:
                type: string
                description: Descrição da atividade
              data_entrega:
                type: string
                format: date
                description: Data de entrega da atividade
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT atividade_id, titulo, descricao, data_entrega FROM atividades')
        atividades = cursor.fetchall()
        cursor.close()
        close_db_connection(conn)

        log_operacao("READ_ATIVIDADES", True, detalhes={"total": len(atividades)})
        return jsonify([
            {
                "atividade_id": atividade[0],
                "titulo": atividade[1],
                "descricao": atividade[2],
                "data_entrega": atividade[3].strftime('%Y-%m-%d')
            }
            for atividade in atividades
        ])
    except Exception as e:
        log_operacao("READ_ATIVIDADES", False, erro=str(e))
        return jsonify({"error": "Erro ao listar atividades"}), 500

# Cadastrar uma nova atividade
@atividades_bp.route('/atividades', methods=['POST'])
def create_atividade():
    """
    Cadastrar uma nova atividade
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            titulo:
              type: string
              description: Título da atividade
            descricao:
              type: string
              description: Descrição da atividade
            data_entrega:
              type: string
              format: date
              description: Data de entrega da atividade
    responses:
      201:
        description: Atividade cadastrada com sucesso
    """
    data = request.get_json()
    titulo = data.get('titulo')
    descricao = data.get('descricao')
    data_entrega = data.get('data_entrega')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO atividades (titulo, descricao, data_entrega)
            VALUES (%s, %s, %s) RETURNING atividade_id
            ''',
            (titulo, descricao, data_entrega)
        )
        atividade_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        close_db_connection(conn)

        detalhes = {
            "atividade_id": atividade_id,
            "titulo": titulo,
            "descricao": descricao,
            "data_entrega": data_entrega
        }
        log_operacao("CREATE_ATIVIDADE", True, detalhes)
        return jsonify(detalhes), 201
    except Exception as e:
        log_operacao("CREATE_ATIVIDADE", False, detalhes=data, erro=str(e))
        return jsonify({"error": "Erro ao cadastrar atividade"}), 500

# Atualizar uma atividade existente
@atividades_bp.route('/atividades/<int:atividade_id>', methods=['PUT'])
def update_atividade(atividade_id):
    """
    Atualizar uma atividade existente
    ---
    parameters:
      - in: path
        name: atividade_id
        required: true
        type: integer
        description: ID da atividade
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            titulo:
              type: string
              description: Novo título da atividade
            descricao:
              type: string
              description: Nova descrição da atividade
            data_entrega:
              type: string
              format: date
              description: Nova data de entrega da atividade
    responses:
      200:
        description: Atividade atualizada com sucesso
    """
    data = request.get_json()
    titulo = data.get('titulo')
    descricao = data.get('descricao')
    data_entrega = data.get('data_entrega')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            UPDATE atividades
            SET titulo = %s, descricao = %s, data_entrega = %s
            WHERE atividade_id = %s
            ''',
            (titulo, descricao, data_entrega, atividade_id)
        )
        conn.commit()
        cursor.close()
        close_db_connection(conn)

        detalhes = {
            "atividade_id": atividade_id,
            "titulo": titulo,
            "descricao": descricao,
            "data_entrega": data_entrega
        }
        log_operacao("UPDATE_ATIVIDADE", True, detalhes)
        return jsonify(detalhes)
    except Exception as e:
        log_operacao("UPDATE_ATIVIDADE", False, detalhes={"atividade_id": atividade_id}, erro=str(e))
        return jsonify({"error": "Erro ao atualizar atividade"}), 500

# Excluir uma atividade
@atividades_bp.route('/atividades/<int:atividade_id>', methods=['DELETE'])
def delete_atividade(atividade_id):
    """
    Excluir uma atividade
    ---
    parameters:
      - in: path
        name: atividade_id
        required: true
        type: integer
        description: ID da atividade
    responses:
      200:
        description: Atividade excluída com sucesso
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM atividades WHERE atividade_id = %s', (atividade_id,))
        conn.commit()
        cursor.close()
        close_db_connection(conn)

        log_operacao("DELETE_ATIVIDADE", True, detalhes={"atividade_id": atividade_id})
        return jsonify({"message": f"Atividade com id {atividade_id} foi excluída com sucesso"})
    except Exception as e:
        log_operacao("DELETE_ATIVIDADE", False, detalhes={"atividade_id": atividade_id}, erro=str(e))
        return jsonify({"error": "Erro ao excluir atividade"}), 500