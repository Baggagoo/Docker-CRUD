import pytest
from main import app
from unittest.mock import patch, MagicMock


@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    yield client

def test_home(client):
    """Testa a rota principal."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {"message": "API CRUD para a tabela alunos da base escola"}

@patch('app.main.get_db_connection')
def test_get_alunos(mock_get_db_connection, client):
    """Testa a rota de listar alunos."""
    # Simulação (mock) da conexão ao banco de dados
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        ('A001', 'João Silva', 'Rua das Flores, 123', 'São Paulo', 'SP', '12345-678', 'Brasil', '11987654321')
    ]

    response = client.get('/alunos')
    assert response.status_code == 200
    assert response.get_json() == [
        {
            "aluno_id": 'A001',
            "nome": 'João Silva',
            "endereco": 'Rua das Flores, 123',
            "cidade": 'São Paulo',
            "estado": 'SP',
            "cep": '12345-678',
            "pais": 'Brasil',
            "telefone": '11987654321'
        }
    ]

@patch('app.main.get_db_connection')
def test_create_aluno(mock_get_db_connection, client):
    """Testa a rota de cadastro de aluno."""
    # Mock da conexão ao banco de dados
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = ['A002']

    aluno = {
        "aluno_id": 'A002',
        "nome": "Maria Oliveira",
        "endereco": "Av. Central, 456",
        "cidade": "Rio de Janeiro",
        "estado": "RJ",
        "cep": "23456-789",
        "pais": "Brasil",
        "telefone": "21987654322"
    }

    response = client.post('/alunos', json=aluno)
    assert response.status_code == 201
    assert response.get_json() == aluno

@patch('app.main.get_db_connection')
def test_delete_aluno(mock_get_db_connection, client):
    """Testa a exclusão de um aluno."""
    # Mock da conexão ao banco de dados
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.delete('/alunos/A001')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Aluno com id A001 foi excluído com sucesso"}