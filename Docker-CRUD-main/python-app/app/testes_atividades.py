import pytest
from main import app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    yield client

@patch('app.main.get_db_connection')
def test_get_atividades(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, 'Atividade 1', 'Descrição', '2024-06-01')
    ]
    response = client.get('/atividades')
    assert response.status_code == 200

@patch('app.main.get_db_connection')
def test_create_atividade(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]
    atividade = {
        "titulo": "Atividade 1",
        "descricao": "Descrição",
        "data_entrega": "2024-06-01"
    }
    response = client.post('/atividades', json=atividade)
    assert response.status_code == 201

@patch('app.main.get_db_connection')
def test_delete_atividade(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    response = client.delete('/atividades/1')
    assert response.status_code == 200