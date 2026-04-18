from flask import Flask, render_template, request, redirect, url_for, session, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import and_
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SENTINEL_SECRET_KEY', 'sentinel-secret')
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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(16), default='viewer')  # 'admin' or 'viewer'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(64))
    action = db.Column(db.String(64))
    details = db.Column(db.String(256))

# Utility to log actions
def log_audit(username, action, details=''):
    entry = AuditLog(username=username, action=action, details=details)
    db.session.add(entry)
    db.session.commit()

@app.route('/')
def index():
    filters = []
    src_ip = request.args.get('src_ip', '').strip()
    dst_ip = request.args.get('dst_ip', '').strip()
    protocol = request.args.get('protocol', '').strip()
    mitre_id = request.args.get('mitre_id', '').strip()
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()

    if src_ip:
        filters.append(Detection.src_ip == src_ip)
    if dst_ip:
        filters.append(Detection.dst_ip == dst_ip)
    if protocol:
        filters.append(Detection.protocol.ilike(protocol))
    if mitre_id:
        filters.append(Detection.mitre_id.ilike(mitre_id))
    if date_from:
        try:
            dt_from = datetime.strptime(date_from, '%Y-%m-%d')
            filters.append(Detection.timestamp >= dt_from)
        except Exception:
            pass
    if date_to:
        try:
            dt_to = datetime.strptime(date_to, '%Y-%m-%d')
            filters.append(Detection.timestamp <= dt_to)
        except Exception:
            pass

    detections = Detection.query.filter(and_(*filters)).order_by(Detection.timestamp.desc()).limit(50).all()
    from flask import g
    if g.user:
        log_audit(g.user.username, 'view_dashboard', 'Viewed dashboard')
    return render_template('index.html', detections=detections, src_ip=src_ip, dst_ip=dst_ip, protocol=protocol, mitre_id=mitre_id, date_from=date_from, date_to=date_to)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            log_audit(username, 'login', 'User logged in')
            return redirect(url_for('index'))
        log_audit(username, 'login_failed', 'Failed login attempt')
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    from flask import g
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            log_audit(user.username, 'logout', 'User logged out')
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.before_request
def require_login():
    if request.endpoint not in ('login', 'static') and 'user_id' not in session:
        return redirect(url_for('login'))
    # Attach user to g for role checks
    if 'user_id' in session:
        from flask import g
        g.user = User.query.get(session['user_id'])

@app.route('/export')
def export_csv():
    filters = []
    src_ip = request.args.get('src_ip', '').strip()
    dst_ip = request.args.get('dst_ip', '').strip()
    protocol = request.args.get('protocol', '').strip()
    mitre_id = request.args.get('mitre_id', '').strip()
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()

    if src_ip:
        filters.append(Detection.src_ip == src_ip)
    if dst_ip:
        filters.append(Detection.dst_ip == dst_ip)
    if protocol:
        filters.append(Detection.protocol.ilike(protocol))
    if mitre_id:
        filters.append(Detection.mitre_id.ilike(mitre_id))
    if date_from:
        try:
            dt_from = datetime.strptime(date_from, '%Y-%m-%d')
            filters.append(Detection.timestamp >= dt_from)
        except Exception:
            pass
    if date_to:
        try:
            dt_to = datetime.strptime(date_to, '%Y-%m-%d')
            filters.append(Detection.timestamp <= dt_to)
        except Exception:
            pass

    detections = Detection.query.filter(and_(*filters)).order_by(Detection.timestamp.desc()).all()

    def generate():
        data = [
            ['Time', 'Source IP', 'Destination IP', 'Protocol', 'MITRE ID', 'Technique', 'Confidence', 'Risk', 'Reason']
        ]
        for d in detections:
            data.append([
                d.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                d.src_ip, d.dst_ip, d.protocol, d.mitre_id, d.mitre_name,
                f'{d.confidence:.2f}', d.risk_score, d.reason
            ])
        output = []
        writer = csv.writer(output)
        writer.writerows(data)
        return '\r\n'.join([','.join(map(str, row)) for row in data])

    from flask import g
    if not g.user or g.user.role != 'admin':
        return redirect(url_for('index'))
    log_audit(g.user.username, 'export_csv', 'Exported detections as CSV')
    return Response(generate(), mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=sentinel_detections.csv'})

@app.route('/users')
def users():
    from flask import g
    if not g.user or g.user.role != 'admin':
        return redirect(url_for('index'))
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
    from flask import g
    if not g.user or g.user.role != 'admin':
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        if User.query.filter_by(username=username).first():
            return render_template('add_user.html', error='Username exists')
        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        log_audit(g.user.username, 'add_user', f'Added user {username} ({role})')
        return redirect(url_for('users'))
    return render_template('add_user.html')

@app.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    from flask import g
    if not g.user or g.user.role != 'admin':
        return redirect(url_for('index'))
    user = User.query.get(user_id)
    if user and user.username != 'admin':  # Prevent deleting default admin
        db.session.delete(user)
        db.session.commit()
        log_audit(g.user.username, 'delete_user', f'Deleted user {user.username}')
    return redirect(url_for('users'))

@app.route('/users/reset/<int:user_id>', methods=['GET', 'POST'])
def reset_password(user_id):
    from flask import g
    if not g.user or g.user.role != 'admin':
        return redirect(url_for('index'))
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('users'))
    if request.method == 'POST':
        new_password = request.form['password']
        user.set_password(new_password)
        db.session.commit()
        log_audit(g.user.username, 'reset_password', f'Reset password for {user.username}')
        return redirect(url_for('users'))
    return render_template('reset_password.html', user=user)

@app.route('/audit')
def audit():
    from flask import g
    if not g.user or g.user.role != 'admin':
        return redirect(url_for('index'))
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(100).all()
    return render_template('audit.html', logs=logs)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create default admin user if not exists
        if not User.query.filter_by(username='admin').first():
            user = User(username='admin', role='admin')
            user.set_password('sentinel')
            db.session.add(user)
            db.session.commit()
    app.run(debug=True)
