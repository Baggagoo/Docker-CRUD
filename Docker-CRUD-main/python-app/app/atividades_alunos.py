from flask import Blueprint, jsonify, request
from database import get_db_connection, close_db_connection

atividades_alunos_bp = Blueprint('atividades_alunos', __name__)

# Listar todas as atividades de alunos
@atividades_alunos_bp.route('/atividades_alunos', methods=['GET'])
def get_atividades_alunos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT atividade_aluno_id, atividade_id, aluno_id, status, nota FROM atividades_alunos')
    atividades_alunos = cursor.fetchall()
    cursor.close()
    close_db_connection(conn)

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

# Cadastrar uma nova atividade para um aluno
@atividades_alunos_bp.route('/atividades_alunos', methods=['POST'])
def create_atividade_aluno():
    data = request.get_json()
    atividade_id = data.get('atividade_id')
    aluno_id = data.get('aluno_id')
    status = data.get('status')
    nota = data.get('nota')

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

    return jsonify({
        "atividade_aluno_id": atividade_aluno_id,
        "atividade_id": atividade_id,
        "aluno_id": aluno_id,
        "status": status,
        "nota": nota
    }), 201

# Atualizar uma atividade de um aluno
@atividades_alunos_bp.route('/atividades_alunos/<int:atividade_aluno_id>', methods=['PUT'])
def update_atividade_aluno(atividade_aluno_id):
    data = request.get_json()
    status = data.get('status')
    nota = data.get('nota')

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

    return jsonify({
        "atividade_aluno_id": atividade_aluno_id,
        "status": status,
        "nota": nota
    })

# Excluir uma atividade de um aluno
@atividades_alunos_bp.route('/atividades_alunos/<int:atividade_aluno_id>', methods=['DELETE'])
def delete_atividade_aluno(atividade_aluno_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM atividades_alunos WHERE atividade_aluno_id = %s', (atividade_aluno_id,))
    conn.commit()
    cursor.close()
    close_db_connection(conn)

    return jsonify({"message": f"Atividade do aluno com id {atividade_aluno_id} foi excluída com sucesso"})