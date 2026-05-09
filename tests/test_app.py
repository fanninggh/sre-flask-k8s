import pytest
from unittest.mock import patch, MagicMock
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


def test_home_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200


def test_home_returns_json(client):
    response = client.get('/')
    data = response.get_json()
    assert data is not None
    assert 'message' in data
    assert data['status'] == 'success'


def test_health_returns_ok(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'ok'


def test_health_has_uptime(client):
    response = client.get('/health')
    data = response.get_json()
    assert 'uptime' in data
    assert isinstance(data['uptime'], float)


def test_ready_returns_200_when_deps_up(client):
    with patch('psycopg2.connect') as mock_db, \
         patch('redis.from_url') as mock_redis:
        mock_db.return_value = MagicMock()
        mock_redis.return_value.ping.return_value = True
        response = client.get('/ready')
        assert response.status_code == 200
        assert response.get_json()['status'] == 'ready'


def test_ready_returns_503_when_db_down(client):
    with patch('psycopg2.connect') as mock_db, \
         patch('redis.from_url') as mock_redis:
        mock_db.side_effect = Exception('connection refused')
        mock_redis.return_value.ping.return_value = True
        response = client.get('/ready')
        assert response.status_code == 503
        assert response.get_json()['status'] == 'degraded'


def test_unknown_route_returns_404(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404
