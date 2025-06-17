import pytest
from main import app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    yield client

@patch('app.main.get_db_connection')
def test_get_atividades_alunos(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, 1, 1, 'concluída', 9.5)
    ]
    response = client.get('/atividades_alunos')
    assert response.status_code == 200

@patch('app.main.get_db_connection')
def test_create_atividade_aluno(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]
    atividade_aluno = {
        "atividade_id": 1,
        "aluno_id": 1,
        "status": "pendente",
        "nota": 8.0
    }
    response = client.post('/atividades_alunos', json=atividade_aluno)
    assert response.status_code == 201

@patch('app.main.get_db_connection')
def test_delete_atividade_aluno(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    response = client.delete('/atividades_alunos/1')
    assert response.status_code == 200