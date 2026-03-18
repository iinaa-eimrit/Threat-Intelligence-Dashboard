from app import db
from datetime import datetime

class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(64))
    event = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    raw_log_id = db.Column(db.String(64))  # MongoDB reference

class Alert(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.Integer, db.ForeignKey('logs.id'))
    severity = db.Column(db.String(32))
    description = db.Column(db.String(256))
    status = db.Column(db.String(32), default='new')  # new, acknowledged, resolved
    acknowledged_by = db.Column(db.String(64), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class IPActivity(db.Model):
    __tablename__ = 'ip_activity'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(64))
    event = db.Column(db.String(128))
    count = db.Column(db.Integer, default=0)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
