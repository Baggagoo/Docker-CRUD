import pytest
from main import app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    yield client

@patch('app.main.get_db_connection')
def test_get_presencas(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, 1, '2024-06-01', 'presente')
    ]
    response = client.get('/presencas')
    assert response.status_code == 200

@patch('app.main.get_db_connection')
def test_create_presenca(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]
    presenca = {
        "aluno_id": 1,
        "data": "2024-06-01",
        "status": "presente"
    }
    response = client.post('/presencas', json=presenca)
    assert response.status_code == 201

@patch('app.main.get_db_connection')
def test_delete_presenca(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    response = client.delete('/presencas/1')
    assert response.status_code == 200