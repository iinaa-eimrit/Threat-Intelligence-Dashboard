import os
import tempfile
import pytest
from app import create_app, db


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    os.environ['POSTGRES_URI'] = f'sqlite:///{db_path}'
    os.environ['TESTING'] = '1'
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


def test_prometheus_metrics(client):
    resp = client.get('/api/metrics')
    assert resp.status_code == 200
    assert b'flask_http_request_total' in resp.data