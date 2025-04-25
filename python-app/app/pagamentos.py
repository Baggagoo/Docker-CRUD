from flask import Blueprint, jsonify, request
from database import get_db_connection, close_db_connection

pagamentos_bp = Blueprint('pagamentos', __name__)

# Listar todos os pagamentos
@pagamentos_bp.route('/pagamentos', methods=['GET'])
def get_pagamentos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT pagamento_id, aluno_id, valor, data_pagamento, metodo_pagamento FROM pagamentos')
    pagamentos = cursor.fetchall()
    cursor.close()
    close_db_connection(conn)

    return jsonify([
        {
            "pagamento_id": pagamento[0],
            "aluno_id": pagamento[1],
            "valor": float(pagamento[2]),
            "data_pagamento": pagamento[3].strftime('%Y-%m-%d'),
            "metodo_pagamento": pagamento[4]
        }
        for pagamento in pagamentos
    ])

# Cadastrar um novo pagamento
@pagamentos_bp.route('/pagamentos', methods=['POST'])
def create_pagamento():
    data = request.get_json()
    aluno_id = data.get('aluno_id')
    valor = data.get('valor')
    data_pagamento = data.get('data_pagamento')
    metodo_pagamento = data.get('metodo_pagamento')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO pagamentos (aluno_id, valor, data_pagamento, metodo_pagamento)
        VALUES (%s, %s, %s, %s) RETURNING pagamento_id
        ''',
        (aluno_id, valor, data_pagamento, metodo_pagamento)
    )
    pagamento_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    close_db_connection(conn)

    return jsonify({
        "pagamento_id": pagamento_id,
        "aluno_id": aluno_id,
        "valor": valor,
        "data_pagamento": data_pagamento,
        "metodo_pagamento": metodo_pagamento
    }), 201

# Atualizar um pagamento existente
@pagamentos_bp.route('/pagamentos/<int:pagamento_id>', methods=['PUT'])
def update_pagamento(pagamento_id):
    data = request.get_json()
    valor = data.get('valor')
    data_pagamento = data.get('data_pagamento')
    metodo_pagamento = data.get('metodo_pagamento')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        UPDATE pagamentos
        SET valor = %s, data_pagamento = %s, metodo_pagamento = %s
        WHERE pagamento_id = %s
        ''',
        (valor, data_pagamento, metodo_pagamento, pagamento_id)
    )
    conn.commit()
    cursor.close()
    close_db_connection(conn)

    return jsonify({
        "pagamento_id": pagamento_id,
        "valor": valor,
        "data_pagamento": data_pagamento,
        "metodo_pagamento": metodo_pagamento
    })

# Excluir um pagamento
@pagamentos_bp.route('/pagamentos/<int:pagamento_id>', methods=['DELETE'])
def delete_pagamento(pagamento_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pagamentos WHERE pagamento_id = %s', (pagamento_id,))
    conn.commit()
    cursor.close()
    close_db_connection(conn)

    return jsonify({"message": f"Pagamento com id {pagamento_id} foi excluído com sucesso"})