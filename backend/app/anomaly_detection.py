import numpy as np
from sklearn.ensemble import IsolationForest
from models.models import Log

def detect_anomalies(window_minutes=60):
    # Example: anomaly detection on failed login frequency per IP
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    window_start = now - timedelta(minutes=window_minutes)
    logs = Log.query.filter(Log.timestamp >= window_start).all()
    ip_counts = {}
    for log in logs:
        ip_counts[log.ip] = ip_counts.get(log.ip, 0) + 1
    if not ip_counts:
        return []
    X = np.array(list(ip_counts.values())).reshape(-1, 1)
    clf = IsolationForest(contamination=0.1)
    preds = clf.fit_predict(X)
    anomalies = [ip for ip, pred in zip(ip_counts.keys(), preds) if pred == -1]
    return anomalies
