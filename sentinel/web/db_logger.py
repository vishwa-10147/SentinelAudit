import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# Setup a minimal Flask app context for DB usage
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sentinel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Detection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    src_ip = db.Column(db.String(64))
    dst_ip = db.Column(db.String(64))
    protocol = db.Column(db.String(16))
    mitre_id = db.Column(db.String(32))
    mitre_name = db.Column(db.String(128))
    confidence = db.Column(db.Float)
    risk_score = db.Column(db.Integer)
    reason = db.Column(db.String(256))

def log_detection(flow, mitre, risk_score):
    """Log a detection to the database."""
    with app.app_context():
        for m in mitre:
            d = Detection(
                src_ip=flow.get('src_ip'),
                dst_ip=flow.get('dst_ip'),
                protocol=flow.get('protocol'),
                mitre_id=m.get('id'),
                mitre_name=m.get('name'),
                confidence=m.get('confidence'),
                risk_score=risk_score,
                reason=m.get('reason'),
            )
            db.session.add(d)
        db.session.commit()
