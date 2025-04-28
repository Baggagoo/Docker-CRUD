from flask import Blueprint, jsonify, request
from database import get_db_connection, close_db_connection
import bcrypt  # Importa a biblioteca bcrypt

usuarios_bp = Blueprint('usuarios', __name__)

# Listar todos os usuários
@usuarios_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT usuario_id, nome, email, senha, tipo_usuario FROM usuarios')
    usuarios = cursor.fetchall()
    cursor.close()
    close_db_connection(conn)

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

# Cadastrar um novo usuário
@usuarios_bp.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')  # Recebe a senha em texto puro
    tipo_usuario = data.get('tipo_usuario')

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

    return jsonify({
        "usuario_id": usuario_id,
        "nome": nome,
        "email": email,
        "tipo_usuario": tipo_usuario
    }), 201

# Atualizar um usuário existente
@usuarios_bp.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def update_usuario(usuario_id):
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')  # Recebe a nova senha em texto puro
    tipo_usuario = data.get('tipo_usuario')

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

    return jsonify({
        "usuario_id": usuario_id,
        "nome": nome,
        "email": email,
        "tipo_usuario": tipo_usuario
    })

# Excluir um usuário
@usuarios_bp.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def delete_usuario(usuario_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE usuario_id = %s', (usuario_id,))
    conn.commit()
    cursor.close()
    close_db_connection(conn)

    return jsonify({"message": f"Usuário com id {usuario_id} foi excluído com sucesso"})