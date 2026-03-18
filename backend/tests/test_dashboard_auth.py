import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_dashboard_requires_auth(client):
    resp = client.get('/api/dashboard')
    assert resp.status_code == 200
