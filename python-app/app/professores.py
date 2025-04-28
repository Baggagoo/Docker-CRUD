from flask import Blueprint, jsonify, request
from database import get_db_connection, close_db_connection

professores_bp = Blueprint('professores', __name__)

# Listar todos os professores
@professores_bp.route('/professores', methods=['GET'])
def get_professores():
    """
    Listar todos os professores
    ---
    responses:
      200:
        description: Lista de professores
        schema:
          type: array
          items:
            type: object
            properties:
              professor_id:
                type: string
                description: ID do professor
              nome:
                type: string
                description: Nome do professor
              departamento:
                type: string
                description: Departamento do professor
              email:
                type: string
                description: Email do professor
              telefone:
                type: string
                description: Telefone do professor
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT professor_id, nome, departamento, email, telefone FROM professores')
    professores = cursor.fetchall()
    cursor.close()
    close_db_connection(conn)

    return jsonify([
        {
            "professor_id": professor[0],
            "nome": professor[1],
            "departamento": professor[2],
            "email": professor[3],
            "telefone": professor[4]
        }
        for professor in professores
    ])

# Cadastrar um novo professor
@professores_bp.route('/professores', methods=['POST'])
def create_professor():
    """
    Cadastrar um novo professor
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            professor_id:
              type: string
              description: ID do professor
            nome:
              type: string
              description: Nome do professor
            departamento:
              type: string
              description: Departamento do professor
            email:
              type: string
              description: Email do professor
            telefone:
              type: string
              description: Telefone do professor
    responses:
      201:
        description: Professor cadastrado com sucesso
    """
    data = request.get_json()
    professor_id = data.get('professor_id')
    nome = data.get('nome')
    departamento = data.get('departamento')
    email = data.get('email')
    telefone = data.get('telefone')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO professores (professor_id, nome, departamento, email, telefone)
        VALUES (%s, %s, %s, %s, %s)
        ''',
        (professor_id, nome, departamento, email, telefone)
    )
    conn.commit()
    cursor.close()
    close_db_connection(conn)

    return jsonify({
        "professor_id": professor_id,
        "nome": nome,
        "departamento": departamento,
        "email": email,
        "telefone": telefone
    }), 201

# Atualizar um professor existente
@professores_bp.route('/professores/<string:professor_id>', methods=['PUT'])
def update_professor(professor_id):
    """
    Atualizar um professor existente
    ---
    parameters:
      - in: path
        name: professor_id
        required: true
        type: string
        description: ID do professor
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              description: Nome do professor
            departamento:
              type: string
              description: Departamento do professor
            email:
              type: string
              description: Email do professor
            telefone:
              type: string
              description: Telefone do professor
    responses:
      200:
        description: Professor atualizado com sucesso
    """
    data = request.get_json()
    nome = data.get('nome')
    departamento = data.get('departamento')
    email = data.get('email')
    telefone = data.get('telefone')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        UPDATE professores
        SET nome = %s, departamento = %s, email = %s, telefone = %s
        WHERE professor_id = %s
        ''',
        (nome, departamento, email, telefone, professor_id)
    )
    conn.commit()
    cursor.close()
    close_db_connection(conn)

    return jsonify({
        "professor_id": professor_id,
        "nome": nome,
        "departamento": departamento,
        "email": email,
        "telefone": telefone
    })

# Excluir um professor
@professores_bp.route('/professores/<string:professor_id>', methods=['DELETE'])
def delete_professor(professor_id):
    """
    Excluir um professor
    ---
    parameters:
      - in: path
        name: professor_id
        required: true
        type: string
        description: ID do professor
    responses:
      200:
        description: Professor excluído com sucesso
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM professores WHERE professor_id = %s', (professor_id,))
    conn.commit()
    cursor.close()
    close_db_connection(conn)

    return jsonify({"message": f"Professor com id {professor_id} foi excluído com sucesso"})