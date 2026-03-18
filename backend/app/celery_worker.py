
from celery import Celery
from models.models import Log
import os

celery_app = Celery(
    'threatintel',
    broker=os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0'),
    backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
)

@celery_app.task
def process_log(log_id, filename, content):
    from app import db, mongo_db
    from app.log_parser import parse_log_content
    # Store raw log in MongoDB
    log_doc = {'filename': filename, 'content': content}
    mongo_db.raw_logs.insert_one(log_doc)
    # Parse and store structured events in PostgreSQL
    events = parse_log_content(content)
    for event in events:
        log_entry = Log(
            ip=event.get('ip'), event=event.get('event'),
            timestamp=event.get('timestamp'), raw_log_id=log_id
        )
        db.session.add(log_entry)
    db.session.commit()
    return {'events_parsed': len(events)}
