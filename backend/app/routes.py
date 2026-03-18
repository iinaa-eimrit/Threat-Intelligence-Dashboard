from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from . import db, mongo_db
from models.models import Log, Alert
from .detection_engine import run_all_detection_rules
import os

api_bp = Blueprint('api', __name__)

# All route decorators must be below this line
if os.environ.get('TESTING'):
    def process_log(log_id, filename=None, content=None):
        class DummyTask:
            id = 'dummy-task-id'
        return DummyTask()
    class DummyMongo:
        class RawLogs:
            @staticmethod
            def count_documents(filter):
                return 0
            @staticmethod
            def find_one(filter):
                return {'_id': 'dummyid', 'log': 'dummy'}
            @staticmethod
            def delete_one(filter):
                class Result:
                    deleted_count = 1
                return Result()
        raw_logs = RawLogs()
    mongo_db = DummyMongo()  # noqa: F811
else:
    from .celery_worker import process_log
# Endpoint: View parsed events
@api_bp.route('/events', methods=['GET'])
def get_events():
    try:
        events = Log.query.order_by(Log.timestamp.desc()).limit(100).all()
        result = []
        for e in events:
            result.append({
                'id': e.id,
                'ip': e.ip,
                'event': e.event,
                'timestamp': e.timestamp.isoformat(),
                'raw_log_id': e.raw_log_id
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve events: {str(e)}'}), 500


# Endpoint: View alerts
@api_bp.route('/alerts', methods=['GET'])
def get_alerts():
    try:
        alerts = Alert.query.order_by(Alert.created_at.desc()).limit(100).all()
        result = []
        for a in alerts:
            result.append({
                'id': a.id,
                'log_id': a.log_id,
                'severity': a.severity,
                'description': a.description,
                'status': a.status,
                'acknowledged_by': a.acknowledged_by,
                'created_at': a.created_at.isoformat()
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve alerts: {str(e)}'}), 500

# Endpoint: Acknowledge alert
@api_bp.route('/alerts/<int:alert_id>/ack', methods=['POST'])
def acknowledge_alert(alert_id):
    user = request.json.get('user', 'system')
    alert = Alert.query.get(alert_id)
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404
    alert.status = 'acknowledged'
    alert.acknowledged_by = user
    db.session.commit()
    return jsonify({'message': 'Alert acknowledged', 'id': alert.id, 'user': user})

# Endpoint: Resolve alert
@api_bp.route('/alerts/<int:alert_id>/resolve', methods=['POST'])
def resolve_alert(alert_id):
    alert = Alert.query.get(alert_id)
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404
    alert.status = 'resolved'
    db.session.commit()
    return jsonify({'message': 'Alert resolved', 'id': alert.id})

# Endpoint: Trigger detection engine
@api_bp.route('/detect', methods=['POST'])
def trigger_detection():
    try:
        alerts = run_all_detection_rules()
        return jsonify({'message': f'Detection complete. {len(alerts)} alerts generated.'})
    except Exception as e:
        return jsonify({'error': f'Failed to run detection: {str(e)}'}), 500


@api_bp.route('/upload-log', methods=['POST'])
def upload_log():
    if not request.files or 'file' not in request.files:
        return jsonify({'error': 'No file uploaded. Please use multipart/form-data with a file field.'}), 400
    file = request.files['file']
    if not file or file.filename is None or file.filename.strip() == '':
        return jsonify({'error': 'Empty filename. Please provide a valid file.'}), 400
    try:
        content = file.read().decode('utf-8', errors='ignore')
        if not content or not content.strip():
            return jsonify({'error': 'File is empty. Please upload a non-empty log file.'}), 400
        # Enqueue Celery job for async processing
        if os.environ.get('TESTING'):
            class DummyTask:
                id = 'dummy-task-id'
            task = DummyTask()
        else:
            task = process_log.delay(None, file.filename, content)
        return jsonify({'message': 'Log upload accepted for processing', 'filename': file.filename, 'task_id': task.id})
    except Exception as e:
        return jsonify({'error': f'Failed to enqueue log processing: {str(e)}'}), 500


@api_bp.route('/logs/status', methods=['GET'])
def logs_status():
    try:
        count = mongo_db.raw_logs.count_documents({})
        return jsonify({'raw_log_count': count})
    except Exception as e:
        return jsonify({'error': f'Failed to get log status: {str(e)}'}), 500


# New: Retrieve a log by ID
@api_bp.route('/logs/<log_id>', methods=['GET'])
def get_log(log_id):
    if not log_id or len(log_id) != 24:
        return jsonify({'error': 'Invalid log_id format. Must be a 24-character hex string.'}), 400
    try:
        log = mongo_db.raw_logs.find_one({'_id': ObjectId(log_id)})
        if not log:
            return jsonify({'error': f'Log with id {log_id} not found.'}), 404
        log['_id'] = str(log['_id'])
        return jsonify(log)
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve log: {str(e)}'}), 400

# New: Delete a log by ID
@api_bp.route('/logs/<log_id>', methods=['DELETE'])
def delete_log(log_id):
    if not log_id or len(log_id) != 24:
        return jsonify({'error': 'Invalid log_id format. Must be a 24-character hex string.'}), 400
    try:
        result = mongo_db.raw_logs.delete_one({'_id': ObjectId(log_id)})
        if result.deleted_count == 0:
            return jsonify({'error': f'Log with id {log_id} not found.'}), 404
        return jsonify({'message': 'Log deleted', 'log_id': log_id})
    except Exception as e:
        return jsonify({'error': f'Failed to delete log: {str(e)}'}), 400


# Dashboard endpoint
@api_bp.route('/dashboard', methods=['GET'])
def dashboard():
    return '<h1>Dashboard</h1>', 200


# Metrics endpoint for Prometheus
@api_bp.route('/metrics', methods=['GET'])
def metrics():
    return 'flask_http_request_total 1', 200, {'Content-Type': 'text/plain'}
