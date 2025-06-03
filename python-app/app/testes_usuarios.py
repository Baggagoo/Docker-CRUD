import pytest
from main import app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    yield client

@patch('app.main.get_db_connection')
def test_get_usuarios(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, 'Admin', 'admin@email.com', 'HASHED', 'admin')
    ]
    response = client.get('/usuarios')
    assert response.status_code == 200

@patch('app.main.get_db_connection')
def test_create_usuario(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]
    usuario = {
        "nome": "Novo Usuário",
        "email": "novo@email.com",
        "senha": "senha123",
        "tipo_usuario": "admin"
    }
    response = client.post('/usuarios', json=usuario)
    assert response.status_code == 201

@patch('app.main.get_db_connection')
def test_delete_usuario(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    response = client.delete('/usuarios/1')
    assert response.status_code == 200