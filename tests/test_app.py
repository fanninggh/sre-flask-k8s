import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


def test_home_returns_200(client):
    """Home endpoint should return HTTP 200."""
    response = client.get('/')
    assert response.status_code == 200


def test_home_returns_json(client):
    """Home endpoint should return valid JSON."""
    response = client.get('/')
    data = response.get_json()
    assert data is not None
    assert 'message' in data
    assert 'status' in data
    assert data['status'] == 'success'


def test_health_returns_ok(client):
    """Health endpoint should return status ok."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'


def test_health_has_uptime(client):
    """Health endpoint should include uptime field."""
    response = client.get('/health')
    data = response.get_json()
    assert 'uptime' in data
    assert isinstance(data['uptime'], float)


from unittest.mock import patch, MagicMock

def test_ready_returns_200_when_deps_up(client):
    """Ready returns 200 when DB and Redis are reachable."""
    with patch('psycopg2.connect') as mock_db, \
         patch('redis.from_url') as mock_redis:
        mock_db.return_value = MagicMock()
        mock_redis.return_value.ping.return_value = True
        response = client.get('/ready')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ready'
        assert data['checks']['db'] == 'ok'
        assert data['checks']['redis'] == 'ok'

def test_ready_returns_503_when_db_down(client):
    """Ready returns 503 when DB is unreachable."""
    with patch('psycopg2.connect') as mock_db, \
         patch('redis.from_url') as mock_redis:
        mock_db.side_effect = Exception('connection refused')
        mock_redis.return_value.ping.return_value = True
        response = client.get('/ready')
        assert response.status_code == 503
        data = response.get_json()
        assert data['status'] == 'degraded'
        assert 'connection refused' in data['checks']['db']


def test_unknown_route_returns_404(client):
    """Unknown routes should return HTTP 404."""
    response = client.get('/does-not-exist')
    assert response.status_code == 404
