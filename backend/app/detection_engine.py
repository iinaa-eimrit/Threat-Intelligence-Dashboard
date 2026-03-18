from datetime import datetime, timedelta
from models.models import Log, Alert
from app import db

def detect_failed_logins(threshold=10, window_minutes=5):
    """
    Rule: If failed_logins(ip) > threshold in window, create alert.
    """
    now = datetime.utcnow()
    window_start = now - timedelta(minutes=window_minutes)
    # Query logs for failed_login events in the window
    logs = Log.query.filter(
        Log.event == 'failed_login',
        Log.timestamp >= window_start
    ).all()
    # Count by IP
    ip_counts = {}
    for log in logs:
        ip_counts[log.ip] = ip_counts.get(log.ip, 0) + 1
    alerts = []
    for ip, count in ip_counts.items():
        if count > threshold:
            alert = Alert(
                log_id=None,  # Could link to most recent log
                severity='high',
                description=f"{count} failed logins from {ip} in {window_minutes} min"
            )
            db.session.add(alert)
            alerts.append(alert)
    db.session.commit()
    return alerts

def run_all_detection_rules():
    alerts = []
    alerts.extend(detect_failed_logins())
    # Add more rules here
    return alerts
