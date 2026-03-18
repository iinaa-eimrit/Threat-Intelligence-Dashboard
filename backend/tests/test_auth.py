import os
import tempfile
import pytest
from app import create_app, db

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    os.environ['POSTGRES_URI'] = f'sqlite:///{db_path}'
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
    try:
        os.close(db_fd)
        os.unlink(db_path)
    except PermissionError:
        pass

def test_register(client):
    data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpass', 'role': 'analyst'}
    response = client.post('/register', json=data)
    assert response.status_code == 200

def test_login(client):
    # Register user first (each test gets a fresh DB)
    reg_data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpass', 'role': 'analyst'}
    client.post('/register', json=reg_data)
    data = {'username': 'testuser', 'password': 'testpass'}
    response = client.post('/login', json=data)
    assert response.status_code == 200
