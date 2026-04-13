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


def test_ready_returns_ready(client):
    """Ready endpoint should return status ready."""
    response = client.get('/ready')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ready'


def test_unknown_route_returns_404(client):
    """Unknown routes should return HTTP 404."""
    response = client.get('/does-not-exist')
    assert response.status_code == 404


def test_deliberate_failure():
    """This test deliberately fails to prove branch protection works."""
    assert False, "This failure proves CI blocks bad code from merging"
