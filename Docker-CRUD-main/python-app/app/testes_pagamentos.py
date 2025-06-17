import pytest
from main import app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    yield client

@patch('app.main.get_db_connection')
def test_get_pagamentos(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, 1, 100.0, '2024-06-01', 'PIX')
    ]
    response = client.get('/pagamentos')
    assert response.status_code == 200

@patch('app.main.get_db_connection')
def test_create_pagamento(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [1]
    pagamento = {
        "aluno_id": 1,
        "valor": 100.0,
        "data_pagamento": "2024-06-01",
        "metodo_pagamento": "PIX"
    }
    response = client.post('/pagamentos', json=pagamento)
    assert response.status_code == 201

@patch('app.main.get_db_connection')
def test_delete_pagamento(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    response = client.delete('/pagamentos/1')
    assert response.status_code == 200