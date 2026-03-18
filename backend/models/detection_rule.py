from app import db

class DetectionRule(db.Model):
    __tablename__ = 'detection_rules'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    rule_type = db.Column(db.String(64))  # e.g. 'threshold', 'anomaly', 'pattern'
    params = db.Column(db.JSON)
    enabled = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<DetectionRule {self.name}>'
