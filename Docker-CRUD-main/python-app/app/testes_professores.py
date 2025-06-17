import pytest
from main import app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    yield client

@patch('app.main.get_db_connection')
def test_get_professores(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        ('P001', 'Prof. Ana', 'Matemática', 'ana@email.com', '11999999999')
    ]
    response = client.get('/professores')
    assert response.status_code == 200

@patch('app.main.get_db_connection')
def test_create_professor(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    professor = {
        "professor_id": "P002",
        "nome": "Prof. Beto",
        "departamento": "História",
        "email": "beto@email.com",
        "telefone": "11888888888"
    }
    response = client.post('/professores', json=professor)
    assert response.status_code == 201

@patch('app.main.get_db_connection')
def test_delete_professor(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    response = client.delete('/professores/P001')
    assert response.status_code == 200