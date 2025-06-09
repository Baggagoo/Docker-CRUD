import psycopg2
from flask import Blueprint, request, jsonify
from database import get_db_connection, close_db_connection
from logger_config import log_operacao  # Importa a função centralizada de log

alunos_bp = Blueprint('alunos', __name__)

# CREATE: Adicionar um novo aluno
@alunos_bp.route('/alunos', methods=['POST'])
def adicionar_aluno():
    """
    Adicionar um novo aluno
    ---
    tags:
      - Alunos
    summary: Adiciona um novo aluno ao banco de dados
    description: Adiciona um novo aluno com os campos nome, idade e turma.
    parameters:
      - in: body
        name: body
        required: true
        description: Dados do aluno a ser adicionado
        schema:
          type: object
          properties:
            nome:
              type: string
            idade:
              type: integer
            turma:
              type: string
          required:
            - nome
            - idade
            - turma
    responses:
      201:
        description: Aluno adicionado com sucesso
      400:
        description: Dados de entrada inválidos
      500:
        description: Erro ao adicionar aluno no banco de dados
    """
    try:
        dados = request.json
        if not dados or 'nome' not in dados or 'idade' not in dados or 'turma' not in dados:
            raise ValueError("Dados de entrada inválidos. Campos obrigatórios: nome, idade, turma.")

        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO alunos (nome, idade, turma) VALUES (%s, %s, %s) RETURNING id"
        cursor.execute(query, (dados['nome'], dados['idade'], dados['turma']))
        aluno_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        close_db_connection(conn)

        detalhes = {"id": aluno_id, "nome": dados['nome'], "idade": dados['idade'], "turma": dados['turma']}
        log_operacao("CREATE", True, detalhes)
        return jsonify({"id": aluno_id, "message": "Aluno adicionado com sucesso"}), 201
    except ValueError as ve:
        log_operacao("CREATE", False, detalhes=None, erro=str(ve))
        return jsonify({"error": str(ve)}), 400
    except psycopg2.Error as e:
        log_operacao("CREATE", False, detalhes=dados, erro=f"{e.pgcode} - {e.pgerror}")
        return jsonify({"error": "Erro ao adicionar aluno no banco de dados"}), 500
    except Exception as e:
        log_operacao("CREATE", False, detalhes=dados, erro=str(e))
        return jsonify({"error": "Erro inesperado ao adicionar aluno"}), 500

# READ: Listar todos os alunos
@alunos_bp.route('/alunos', methods=['GET'])
def listar_alunos():
    """
    Listar todos os alunos
    ---
    tags:
      - Alunos
    summary: Retorna uma lista de todos os alunos cadastrados
    description: Retorna uma lista com os campos id, nome, idade e turma de todos os alunos cadastrados no banco de dados.
    responses:
      200:
        description: Lista de alunos retornada com sucesso
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              nome:
                type: string
              idade:
                type: integer
              turma:
                type: string
      500:
        description: Erro ao listar alunos no banco de dados
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT id, nome, idade, turma FROM alunos"
        cursor.execute(query)
        alunos = cursor.fetchall()
        cursor.close()
        close_db_connection(conn)

        detalhes = {"total_alunos": len(alunos)}
        log_operacao("READ", True, detalhes)
        return jsonify([{"id": aluno[0], "nome": aluno[1], "idade": aluno[2], "turma": aluno[3]} for aluno in alunos]), 200
    except psycopg2.Error as e:
        log_operacao("READ", False, erro=f"{e.pgcode} - {e.pgerror}")
        return jsonify({"error": "Erro ao listar alunos no banco de dados"}), 500
    except Exception as e:
        log_operacao("READ", False, erro=str(e))
        return jsonify({"error": "Erro inesperado ao listar alunos"}), 500

# UPDATE: Atualizar informações de um aluno
@alunos_bp.route('/alunos/<int:aluno_id>', methods=['PUT'])
def atualizar_aluno(aluno_id):
    """
    Atualizar informações de um aluno
    ---
    tags:
      - Alunos
    summary: Atualiza as informações de um aluno existente
    description: Atualiza os campos nome, idade e turma de um aluno com base no ID fornecido.
    parameters:
      - in: path
        name: aluno_id
        required: true
        type: integer
        description: ID do aluno a ser atualizado
      - in: body
        name: body
        required: true
        description: Novos dados do aluno
        schema:
          type: object
          properties:
            nome:
              type: string
            idade:
              type: integer
            turma:
              type: string
          required:
            - nome
            - idade
            - turma
    responses:
      200:
        description: Aluno atualizado com sucesso
      400:
        description: Dados de entrada inválidos ou aluno não encontrado
      500:
        description: Erro ao atualizar aluno no banco de dados
    """
    try:
        dados = request.json
        if not dados or 'nome' not in dados or 'idade' not in dados or 'turma' not in dados:
            raise ValueError("Dados de entrada inválidos. Campos obrigatórios: nome, idade, turma.")

        conn = get_db_connection()
        cursor = conn.cursor()
        query = "UPDATE alunos SET nome = %s, idade = %s, turma = %s WHERE id = %s"
        cursor.execute(query, (dados['nome'], dados['idade'], dados['turma'], aluno_id))
        if cursor.rowcount == 0:
            raise ValueError(f"Aluno com ID {aluno_id} não encontrado.")
        conn.commit()
        cursor.close()
        close_db_connection(conn)

        detalhes = {"id": aluno_id, "nome": dados['nome'], "idade": dados['idade'], "turma": dados['turma']}
        log_operacao("UPDATE", True, detalhes)
        return jsonify({"message": "Aluno atualizado com sucesso"}), 200
    except ValueError as ve:
        log_operacao("UPDATE", False, detalhes={"id": aluno_id}, erro=str(ve))
        return jsonify({"error": str(ve)}), 400
    except psycopg2.Error as e:
        log_operacao("UPDATE", False, detalhes={"id": aluno_id}, erro=f"{e.pgcode} - {e.pgerror}")
        return jsonify({"error": "Erro ao atualizar aluno no banco de dados"}), 500
    except Exception as e:
        log_operacao("UPDATE", False, detalhes={"id": aluno_id}, erro=str(e))
        return jsonify({"error": "Erro inesperado ao atualizar aluno"}), 500

# DELETE: Remover um aluno
@alunos_bp.route('/alunos/<int:aluno_id>', methods=['DELETE'])
def remover_aluno(aluno_id):
    """
    Remover um aluno
    ---
    tags:
      - Alunos
    summary: Remove um aluno do banco de dados
    description: Remove um aluno com base no ID fornecido.
    parameters:
      - in: path
        name: aluno_id
        required: true
        type: integer
        description: ID do aluno a ser removido
    responses:
      200:
        description: Aluno removido com sucesso
      400:
        description: Aluno não encontrado
      500:
        description: Erro ao remover aluno no banco de dados
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "DELETE FROM alunos WHERE id = %s"
        cursor.execute(query, (aluno_id,))
        if cursor.rowcount == 0:
            raise ValueError(f"Aluno com ID {aluno_id} não encontrado.")
        conn.commit()
        cursor.close()
        close_db_connection(conn)

        detalhes = {"id": aluno_id}
        log_operacao("DELETE", True, detalhes)
        return jsonify({"message": "Aluno removido com sucesso"}), 200
    except ValueError as ve:
        log_operacao("DELETE", False, detalhes={"id": aluno_id}, erro=str(ve))
        return jsonify({"error": str(ve)}), 400
    except psycopg2.Error as e:
        log_operacao("DELETE", False, detalhes={"id": aluno_id}, erro=f"{e.pgcode} - {e.pgerror}")
        return jsonify({"error": "Erro ao remover aluno no banco de dados"}), 500
    except Exception as e:
        log_operacao("DELETE", False, detalhes={"id": aluno_id}, erro=str(e))
        return jsonify({"error": "Erro inesperado ao remover aluno"}), 500