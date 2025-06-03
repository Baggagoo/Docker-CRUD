from flask import Blueprint, jsonify, request
from database import get_db_connection, close_db_connection
from logger_config import log_operacao  # Importa a função centralizada de log

pagamentos_bp = Blueprint('pagamentos', __name__)

# Listar todos os pagamentos
@pagamentos_bp.route('/pagamentos', methods=['GET'])
def get_pagamentos():
    """
    Listar todos os pagamentos
    ---
    responses:
      200:
        description: Lista de pagamentos
        schema:
          type: array
          items:
            type: object
            properties:
              pagamento_id:
                type: integer
                description: ID do pagamento
              aluno_id:
                type: integer
                description: ID do aluno
              valor:
                type: number
                description: Valor do pagamento
              data_pagamento:
                type: string
                format: date
                description: Data do pagamento
              metodo_pagamento:
                type: string
                description: Método de pagamento
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT pagamento_id, aluno_id, valor, data_pagamento, metodo_pagamento FROM pagamentos')
        pagamentos = cursor.fetchall()
        cursor.close()
        close_db_connection(conn)

        log_operacao("READ_PAGAMENTOS", True, detalhes={"total": len(pagamentos)})
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
    except Exception as e:
        log_operacao("READ_PAGAMENTOS", False, erro=str(e))
        return jsonify({"error": "Erro ao listar pagamentos"}), 500

# Cadastrar um novo pagamento
@pagamentos_bp.route('/pagamentos', methods=['POST'])
def create_pagamento():
    """
    Cadastrar um novo pagamento
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            aluno_id:
              type: integer
              description: ID do aluno
            valor:
              type: number
              description: Valor do pagamento
            data_pagamento:
              type: string
              format: date
              description: Data do pagamento
            metodo_pagamento:
              type: string
              description: Método de pagamento
    responses:
      201:
        description: Pagamento cadastrado com sucesso
    """
    data = request.get_json()
    aluno_id = data.get('aluno_id')
    valor = data.get('valor')
    data_pagamento = data.get('data_pagamento')
    metodo_pagamento = data.get('metodo_pagamento')

    try:
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

        detalhes = {
            "pagamento_id": pagamento_id,
            "aluno_id": aluno_id,
            "valor": valor,
            "data_pagamento": data_pagamento,
            "metodo_pagamento": metodo_pagamento
        }
        log_operacao("CREATE_PAGAMENTO", True, detalhes)
        return jsonify(detalhes), 201
    except Exception as e:
        log_operacao("CREATE_PAGAMENTO", False, detalhes=data, erro=str(e))
        return jsonify({"error": "Erro ao cadastrar pagamento"}), 500

# Atualizar um pagamento existente
@pagamentos_bp.route('/pagamentos/<int:pagamento_id>', methods=['PUT'])
def update_pagamento(pagamento_id):
    """
    Atualizar um pagamento existente
    ---
    parameters:
      - in: path
        name: pagamento_id
        required: true
        type: integer
        description: ID do pagamento
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            valor:
              type: number
              description: Novo valor do pagamento
            data_pagamento:
              type: string
              format: date
              description: Nova data do pagamento
            metodo_pagamento:
              type: string
              description: Novo método de pagamento
    responses:
      200:
        description: Pagamento atualizado com sucesso
    """
    data = request.get_json()
    valor = data.get('valor')
    data_pagamento = data.get('data_pagamento')
    metodo_pagamento = data.get('metodo_pagamento')

    try:
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

        detalhes = {
            "pagamento_id": pagamento_id,
            "valor": valor,
            "data_pagamento": data_pagamento,
            "metodo_pagamento": metodo_pagamento
        }
        log_operacao("UPDATE_PAGAMENTO", True, detalhes)
        return jsonify(detalhes)
    except Exception as e:
        log_operacao("UPDATE_PAGAMENTO", False, detalhes={"pagamento_id": pagamento_id}, erro=str(e))
        return jsonify({"error": "Erro ao atualizar pagamento"}), 500

# Excluir um pagamento
@pagamentos_bp.route('/pagamentos/<int:pagamento_id>', methods=['DELETE'])
def delete_pagamento(pagamento_id):
    """
    Excluir um pagamento
    ---
    parameters:
      - in: path
        name: pagamento_id
        required: true
        type: integer
        description: ID do pagamento
    responses:
      200:
        description: Pagamento excluído com sucesso
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM pagamentos WHERE pagamento_id = %s', (pagamento_id,))
        conn.commit()
        cursor.close()
        close_db_connection(conn)

        log_operacao("DELETE_PAGAMENTO", True, detalhes={"pagamento_id": pagamento_id})
        return jsonify({"message": f"Pagamento com id {pagamento_id} foi excluído com sucesso"})
    except Exception as e:
        log_operacao("DELETE_PAGAMENTO", False, detalhes={"pagamento_id": pagamento_id}, erro=str(e))
        return jsonify({"error": "Erro ao excluir pagamento"}), 500