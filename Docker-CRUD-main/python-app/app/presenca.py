from flask import Blueprint, jsonify, request
from database import get_db_connection, close_db_connection

presencas_bp = Blueprint('presencas', __name__)

# Listar todas as presenças
@presencas_bp.route('/presencas', methods=['GET'])
def get_presencas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT presenca_id, aluno_id, data, status FROM presencas')
    presencas = cursor.fetchall()
    cursor.close()
    close_db_connection(conn)

    return jsonify([
        {
            "presenca_id": presenca[0],
            "aluno_id": presenca[1],
            "data": presenca[2].strftime('%Y-%m-%d'),
            "status": presenca[3]
        }
        for presenca in presencas
    ])

# Cadastrar uma nova presença
@presencas_bp.route('/presencas', methods=['POST'])
def create_presenca():
    data = request.get_json()
    aluno_id = data.get('aluno_id')
    data_presenca = data.get('data')
    status = data.get('status')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO presencas (aluno_id, data, status)
        VALUES (%s, %s, %s) RETURNING presenca_id
        ''',
        (aluno_id, data_presenca, status)
    )
    presenca_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    close_db_connection(conn)

    return jsonify({
        "presenca_id": presenca_id,
        "aluno_id": aluno_id,
        "data": data_presenca,
        "status": status
    }), 201

# Atualizar uma presença existente
@presencas_bp.route('/presencas/<int:presenca_id>', methods=['PUT'])
def update_presenca(presenca_id):
    data = request.get_json()
    status = data.get('status')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        UPDATE presencas
        SET status = %s
        WHERE presenca_id = %s
        ''',
        (status, presenca_id)
    )
    conn.commit()
    cursor.close()
    close_db_connection(conn)

    return jsonify({
        "presenca_id": presenca_id,
        "status": status
    })

# Excluir uma presença
@presencas_bp.route('/presencas/<int:presenca_id>', methods=['DELETE'])
def delete_presenca(presenca_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM presencas WHERE presenca_id = %s', (presenca_id,))
    conn.commit()
    cursor.close()
    close_db_connection(conn)

    return jsonify({"message": f"Presença com id {presenca_id} foi excluída com sucesso"})