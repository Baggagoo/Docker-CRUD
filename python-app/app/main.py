from flask import Flask
from alunos import alunos_bp
from professores import professores_bp
from pagamentos import pagamentos_bp
from presenca import presencas_bp
from atividades import atividades_bp
from atividades_alunos import atividades_alunos_bp
from usuarios import usuarios_bp
from database import get_db_connection, close_db_connection  # Importar as funções de conexão com o banco

app = Flask(__name__)

# Registrar os blueprints
app.register_blueprint(alunos_bp)
app.register_blueprint(professores_bp)
app.register_blueprint(pagamentos_bp)
app.register_blueprint(presencas_bp)
app.register_blueprint(atividades_bp)
app.register_blueprint(atividades_alunos_bp)
app.register_blueprint(usuarios_bp)

# Testar a conexão com o banco de dados
try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    print("Teste de conexão com o banco de dados:", cursor.fetchone())
    cursor.close()
    close_db_connection(conn)
except Exception as e:
    print("Erro ao conectar ao banco de dados:", e)

@app.route('/')
def home():
    return {"message": "API CRUD para a base escola"}

@app.route('/healthcheck')
def healthcheck():
    return {"status": "healthy"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)