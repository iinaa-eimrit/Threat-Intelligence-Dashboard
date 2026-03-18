from flask import Blueprint, request, jsonify
from models.detection_rule import DetectionRule
from app import db

rules_bp = Blueprint('rules', __name__)

@rules_bp.route('/rules', methods=['GET'])
def get_rules():
    rules = DetectionRule.query.all()
    return jsonify([
        {
            'id': r.id,
            'name': r.name,
            'rule_type': r.rule_type,
            'params': r.params,
            'enabled': r.enabled
        } for r in rules
    ])

@rules_bp.route('/rules', methods=['POST'])
def add_rule():
    data = request.get_json()
    rule = DetectionRule(
        name=data['name'],
        rule_type=data['rule_type'],
        params=data.get('params', {}),
        enabled=data.get('enabled', True)
    )
    db.session.add(rule)
    db.session.commit()
    return jsonify({'message': 'Rule added', 'id': rule.id})

@rules_bp.route('/rules/<int:rule_id>', methods=['PUT'])
def update_rule(rule_id):
    rule = DetectionRule.query.get(rule_id)
    if not rule:
        return jsonify({'error': 'Rule not found'}), 404
    data = request.get_json()
    rule.name = data.get('name', rule.name)
    rule.rule_type = data.get('rule_type', rule.rule_type)
    rule.params = data.get('params', rule.params)
    rule.enabled = data.get('enabled', rule.enabled)
    db.session.commit()
    return jsonify({'message': 'Rule updated'})

@rules_bp.route('/rules/<int:rule_id>', methods=['DELETE'])
def delete_rule(rule_id):
    rule = DetectionRule.query.get(rule_id)
    if not rule:
        return jsonify({'error': 'Rule not found'}), 404
    db.session.delete(rule)
    db.session.commit()
    return jsonify({'message': 'Rule deleted'})
