from flask import Blueprint, jsonify, request
from database import get_db_connection, close_db_connection
from logger_config import log_operacao  # Importa a função centralizada de log

atividades_alunos_bp = Blueprint('atividades_alunos', __name__)

# Listar todas as atividades de alunos
@atividades_alunos_bp.route('/atividades_alunos', methods=['GET'])
def get_atividades_alunos():
    """
    Listar todas as atividades de alunos
    ---
    responses:
      200:
        description: Lista de atividades de alunos
        schema:
          type: array
          items:
            type: object
            properties:
              atividade_aluno_id:
                type: integer
                description: ID da atividade do aluno
              atividade_id:
                type: integer
                description: ID da atividade
              aluno_id:
                type: integer
                description: ID do aluno
              status:
                type: string
                description: Status da atividade
              nota:
                type: number
                description: Nota da atividade
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT atividade_aluno_id, atividade_id, aluno_id, status, nota FROM atividades_alunos')
        atividades_alunos = cursor.fetchall()
        cursor.close()
        close_db_connection(conn)

        log_operacao("READ_ATIVIDADES_ALUNOS", True, detalhes={"total": len(atividades_alunos)})
        return jsonify([
            {
                "atividade_aluno_id": atividade_aluno[0],
                "atividade_id": atividade_aluno[1],
                "aluno_id": atividade_aluno[2],
                "status": atividade_aluno[3],
                "nota": float(atividade_aluno[4]) if atividade_aluno[4] is not None else None
            }
            for atividade_aluno in atividades_alunos
        ])
    except Exception as e:
        log_operacao("READ_ATIVIDADES_ALUNOS", False, erro=str(e))
        return jsonify({"error": "Erro ao listar atividades de alunos"}), 500

# Cadastrar uma nova atividade para um aluno
@atividades_alunos_bp.route('/atividades_alunos', methods=['POST'])
def create_atividade_aluno():
    """
    Cadastrar uma nova atividade para um aluno
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            atividade_id:
              type: integer
              description: ID da atividade
            aluno_id:
              type: integer
              description: ID do aluno
            status:
              type: string
              description: Status da atividade
            nota:
              type: number
              description: Nota da atividade
    responses:
      201:
        description: Atividade cadastrada com sucesso
    """
    data = request.get_json()
    atividade_id = data.get('atividade_id')
    aluno_id = data.get('aluno_id')
    status = data.get('status')
    nota = data.get('nota')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO atividades_alunos (atividade_id, aluno_id, status, nota)
            VALUES (%s, %s, %s, %s) RETURNING atividade_aluno_id
            ''',
            (atividade_id, aluno_id, status, nota)
        )
        atividade_aluno_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        close_db_connection(conn)

        detalhes = {
            "atividade_aluno_id": atividade_aluno_id,
            "atividade_id": atividade_id,
            "aluno_id": aluno_id,
            "status": status,
            "nota": nota
        }
        log_operacao("CREATE_ATIVIDADE_ALUNO", True, detalhes)
        return jsonify(detalhes), 201
    except Exception as e:
        log_operacao("CREATE_ATIVIDADE_ALUNO", False, detalhes=data, erro=str(e))
        return jsonify({"error": "Erro ao cadastrar atividade para aluno"}), 500

# Atualizar uma atividade de um aluno
@atividades_alunos_bp.route('/atividades_alunos/<int:atividade_aluno_id>', methods=['PUT'])
def update_atividade_aluno(atividade_aluno_id):
    """
    Atualizar uma atividade de um aluno
    ---
    parameters:
      - in: path
        name: atividade_aluno_id
        required: true
        type: integer
        description: ID da atividade do aluno
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            status:
              type: string
              description: Novo status da atividade
            nota:
              type: number
              description: Nova nota da atividade
    responses:
      200:
        description: Atividade atualizada com sucesso
    """
    data = request.get_json()
    status = data.get('status')
    nota = data.get('nota')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            UPDATE atividades_alunos
            SET status = %s, nota = %s
            WHERE atividade_aluno_id = %s
            ''',
            (status, nota, atividade_aluno_id)
        )
        conn.commit()
        cursor.close()
        close_db_connection(conn)

        detalhes = {
            "atividade_aluno_id": atividade_aluno_id,
            "status": status,
            "nota": nota
        }
        log_operacao("UPDATE_ATIVIDADE_ALUNO", True, detalhes)
        return jsonify(detalhes)
    except Exception as e:
        log_operacao("UPDATE_ATIVIDADE_ALUNO", False, detalhes={"atividade_aluno_id": atividade_aluno_id}, erro=str(e))
        return jsonify({"error": "Erro ao atualizar atividade do aluno"}), 500

# Excluir uma atividade de um aluno
@atividades_alunos_bp.route('/atividades_alunos/<int:atividade_aluno_id>', methods=['DELETE'])
def delete_atividade_aluno(atividade_aluno_id):
    """
    Excluir uma atividade de um aluno
    ---
    parameters:
      - in: path
        name: atividade_aluno_id
        required: true
        type: integer
        description: ID da atividade do aluno
    responses:
      200:
        description: Atividade excluída com sucesso
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM atividades_alunos WHERE atividade_aluno_id = %s', (atividade_aluno_id,))
        conn.commit()
        cursor.close()
        close_db_connection(conn)

        log_operacao("DELETE_ATIVIDADE_ALUNO", True, detalhes={"atividade_aluno_id": atividade_aluno_id})
        return jsonify({"message": f"Atividade do aluno com id {atividade_aluno_id} foi excluída com sucesso"})
    except Exception as e:
        log_operacao("DELETE_ATIVIDADE_ALUNO", False, detalhes={"atividade_aluno_id": atividade_aluno_id}, erro=str(e))
        return jsonify({"error": "Erro ao excluir atividade do aluno"}), 500