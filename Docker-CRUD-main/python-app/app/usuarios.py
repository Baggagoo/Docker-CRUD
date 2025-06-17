from flask import Blueprint, jsonify, request
from database import get_db_connection, close_db_connection
import bcrypt  # Importa a biblioteca bcrypt
from logger_config import log_operacao  # Importa a função centralizada de log

usuarios_bp = Blueprint('usuarios', __name__)

# Listar todos os usuários
@usuarios_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    """
    Listar todos os usuários
    ---
    responses:
      200:
        description: Lista de usuários
        schema:
          type: array
          items:
            type: object
            properties:
              usuario_id:
                type: integer
                description: ID do usuário
              nome:
                type: string
                description: Nome do usuário
              email:
                type: string
                description: Email do usuário
              senha:
                type: string
                description: Senha do usuário (hash não exposto)
              tipo_usuario:
                type: string
                description: Tipo do usuário (ex: admin, aluno)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT usuario_id, nome, email, senha, tipo_usuario FROM usuarios')
        usuarios = cursor.fetchall()
        cursor.close()
        close_db_connection(conn)

        log_operacao("READ_USUARIOS", True, detalhes={"total": len(usuarios)})
        return jsonify([
            {
                "usuario_id": usuario[0],
                "nome": usuario[1],
                "email": usuario[2],
                "senha": "HASHED",  # Nunca exponha a senha real ou o hash
                "tipo_usuario": usuario[4]
            }
            for usuario in usuarios
        ])
    except Exception as e:
        log_operacao("READ_USUARIOS", False, erro=str(e))
        return jsonify({"error": "Erro ao listar usuários"}), 500

# Cadastrar um novo usuário
@usuarios_bp.route('/usuarios', methods=['POST'])
def create_usuario():
    """
    Cadastrar um novo usuário
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              description: Nome do usuário
            email:
              type: string
              description: Email do usuário
            senha:
              type: string
              description: Senha do usuário
            tipo_usuario:
              type: string
              description: Tipo do usuário (ex: admin, aluno)
    responses:
      201:
        description: Usuário cadastrado com sucesso
    """
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')  # Recebe a senha em texto puro
    tipo_usuario = data.get('tipo_usuario')

    try:
        # Criptografar a senha
        hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO usuarios (nome, email, senha, tipo_usuario)
            VALUES (%s, %s, %s, %s) RETURNING usuario_id
            ''',
            (nome, email, hashed_senha.decode('utf-8'), tipo_usuario)
        )
        usuario_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        close_db_connection(conn)

        detalhes = {
            "usuario_id": usuario_id,
            "nome": nome,
            "email": email,
            "tipo_usuario": tipo_usuario
        }
        log_operacao("CREATE_USUARIO", True, detalhes)
        return jsonify(detalhes), 201
    except Exception as e:
        log_operacao("CREATE_USUARIO", False, detalhes=data, erro=str(e))
        return jsonify({"error": "Erro ao cadastrar usuário"}), 500

# Atualizar um usuário existente
@usuarios_bp.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def update_usuario(usuario_id):
    """
    Atualizar um usuário existente
    ---
    parameters:
      - in: path
        name: usuario_id
        required: true
        type: integer
        description: ID do usuário
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              description: Nome do usuário
            email:
              type: string
              description: Email do usuário
            senha:
              type: string
              description: Nova senha do usuário
            tipo_usuario:
              type: string
              description: Tipo do usuário (ex: admin, aluno)
    responses:
      200:
        description: Usuário atualizado com sucesso
    """
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')  # Recebe a nova senha em texto puro
    tipo_usuario = data.get('tipo_usuario')

    try:
        # Criptografar a nova senha
        hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            UPDATE usuarios
            SET nome = %s, email = %s, senha = %s, tipo_usuario = %s
            WHERE usuario_id = %s
            ''',
            (nome, email, hashed_senha.decode('utf-8'), tipo_usuario, usuario_id)
        )
        conn.commit()
        cursor.close()
        close_db_connection(conn)

        detalhes = {
            "usuario_id": usuario_id,
            "nome": nome,
            "email": email,
            "tipo_usuario": tipo_usuario
        }
        log_operacao("UPDATE_USUARIO", True, detalhes)
        return jsonify(detalhes)
    except Exception as e:
        log_operacao("UPDATE_USUARIO", False, detalhes={"usuario_id": usuario_id}, erro=str(e))
        return jsonify({"error": "Erro ao atualizar usuário"}), 500

# Excluir um usuário
@usuarios_bp.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def delete_usuario(usuario_id):
    """
    Excluir um usuário
    ---
    parameters:
      - in: path
        name: usuario_id
        required: true
        type: integer
        description: ID do usuário
    responses:
      200:
        description: Usuário excluído com sucesso
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM usuarios WHERE usuario_id = %s', (usuario_id,))
        conn.commit()
        cursor.close()
        close_db_connection(conn)

        log_operacao("DELETE_USUARIO", True, detalhes={"usuario_id": usuario_id})
        return jsonify({"message": f"Usuário com id {usuario_id} foi excluído com sucesso"})
    except Exception as e:
        log_operacao("DELETE_USUARIO", False, detalhes={"usuario_id": usuario_id}, erro=str(e))
        return jsonify({"error": "Erro ao excluir usuário"}), 500