import os
import tempfile
import pytest
from app import create_app, db
from models.models import Log

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

def test_upload_log(client):
    data = {
        'file': (tempfile.NamedTemporaryFile(suffix='.log', delete=False), 'test.log')
    }
    data['file'][0].write(b'Failed login from 1.2.3.4 at 10:32 PM\n')
    data['file'][0].seek(0)
    rv = client.post('/api/upload-log', data={'file': data['file']}, content_type='multipart/form-data')
    assert rv.status_code == 200
    assert b'Log upload accepted for processing' in rv.data

def test_upload_empty_file(client):
    data = {
        'file': (tempfile.NamedTemporaryFile(suffix='.log', delete=False), 'empty.log')
    }
    data['file'][0].write(b'')
    data['file'][0].seek(0)
    rv = client.post('/api/upload-log', data={'file': data['file']}, content_type='multipart/form-data')
    assert rv.status_code == 400
    assert b'File is empty' in rv.data

def test_get_events(client):
    # Upload a log first
    data = {
        'file': (tempfile.NamedTemporaryFile(suffix='.log', delete=False), 'test2.log')
    }
    data['file'][0].write(b'Failed login from 5.6.7.8 at 11:00 PM\n')
    data['file'][0].seek(0)
    client.post('/api/upload-log', data={'file': data['file']}, content_type='multipart/form-data')
    rv = client.get('/api/events')
    assert rv.status_code == 200
