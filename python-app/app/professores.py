from flask import Blueprint, request, jsonify
from database import get_db_connection
from logger_config import log_operacao

professores_bp = Blueprint('professores', __name__)

@professores_bp.route('/professores', methods=['GET'])
def listar_professores():
    """
    Lista todos os professores
    ---
    tags:
      - Professores
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
              nome:
                type: string
              departamento:
                type: string
              email:
                type: string
              telefone:
                type: string
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT professor_id, nome, departamento, email, telefone FROM professores")
    professores = cur.fetchall()
    cur.close()
    conn.close()
    log_operacao("listar_professores", "Listou todos os professores")
    lista = [
        {
            "professor_id": p[0],
            "nome": p[1],
            "departamento": p[2],
            "email": p[3],
            "telefone": p[4]
        }
        for p in professores
    ]
    return jsonify(lista), 200

@professores_bp.route('/professores/<professor_id>', methods=['GET'])
def obter_professor(professor_id):
    """
    Busca um professor pelo ID
    ---
    tags:
      - Professores
    parameters:
      - name: professor_id
        in: path
        type: string
        required: true
        description: ID do professor (ex: P001)
    responses:
      200:
        description: Professor encontrado
        schema:
          type: object
          properties:
            professor_id:
              type: string
            nome:
              type: string
            departamento:
              type: string
            email:
              type: string
            telefone:
              type: string
      404:
        description: Professor não encontrado
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT professor_id, nome, departamento, email, telefone FROM professores WHERE professor_id = %s", (professor_id,))
    p = cur.fetchone()
    cur.close()
    conn.close()
    if p:
        log_operacao("obter_professor", f"Consultou professor {professor_id}")
        return jsonify({
            "professor_id": p[0],
            "nome": p[1],
            "departamento": p[2],
            "email": p[3],
            "telefone": p[4]
        }), 200
    else:
        log_operacao("obter_professor", f"Tentou consultar professor inexistente {professor_id}")
        return jsonify({"error": "Professor não encontrado"}), 404

@professores_bp.route('/professores', methods=['POST'])
def criar_professor():
    """
    Cadastra um novo professor
    ---
    tags:
      - Professores
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - professor_id
            - nome
            - departamento
            - email
            - telefone
          properties:
            professor_id:
              type: string
              example: P004
            nome:
              type: string
              example: Marina Lima
            departamento:
              type: string
              example: Química
            email:
              type: string
              example: marina.lima@escola.com
            telefone:
              type: string
              example: "41987654324"
    responses:
      201:
        description: Professor cadastrado com sucesso
      400:
        description: Erro de validação ou de banco de dados
    """
    data = request.get_json()
    required = ['professor_id', 'nome', 'departamento', 'email', 'telefone']
    if not data or not all(field in data for field in required):
        log_operacao("criar_professor", "Tentativa de cadastro com campos faltando")
        return jsonify({"error": "Campos obrigatórios: professor_id, nome, departamento, email, telefone"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO professores (professor_id, nome, departamento, email, telefone) VALUES (%s, %s, %s, %s, %s)",
            (data['professor_id'], data['nome'], data['departamento'], data['email'], data['telefone'])
        )
        conn.commit()
        log_operacao("criar_professor", f"Professor {data['professor_id']} cadastrado")
        return jsonify({"message": "Professor cadastrado com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        log_operacao("criar_professor", f"Erro ao cadastrar professor: {str(e)}")
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()