from flask import Flask
from app.alunos import alunos_bp
from app.professores import professores_bp
from app.pagamentos import pagamentos_bp
from app.presencas import presencas_bp
from app.atividades import atividades_bp
from app.atividades_alunos import atividades_alunos_bp
from app.usuarios import usuarios_bp

app = Flask(__name__)

# Registrar os blueprints
app.register_blueprint(alunos_bp)
app.register_blueprint(professores_bp)
app.register_blueprint(pagamentos_bp)
app.register_blueprint(presencas_bp)
app.register_blueprint(atividades_bp)
app.register_blueprint(atividades_alunos_bp)
app.register_blueprint(usuarios_bp)

@app.route('/')
def home():
    return {"message": "API CRUD para a base escola"}

@app.route('/healthcheck')
def healthcheck():
    return {"status": "healthy"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)