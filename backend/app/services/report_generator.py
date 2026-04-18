"""
PDF report generator for Sentinel using Jinja2 and WeasyPrint.
"""
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os

def generate_pdf_report(company_name, alerts, device_profiles, risk_timeline):
    # 1. Calculate overall risk score (average of top device scores)
    # 2. Count critical/high/medium alerts
    # 3. Get top 5 threats sorted by risk score
    # 4. Get top 10 devices sorted by risk score
    # 5. Generate plain-English recommendations
    # 6. Render Jinja2 template with all data
    # 7. Convert HTML to PDF using WeasyPrint
    # 8. Return PDF as bytes

    # Example calculations (replace with real logic as needed)
    overall_risk_score = int(sum(d['risk_score'] for d in device_profiles.values()) / max(len(device_profiles), 1))
    risk_level = 'Critical' if overall_risk_score >= 75 else 'High' if overall_risk_score >= 50 else 'Medium' if overall_risk_score >= 25 else 'Low'
    critical_count = sum(1 for a in alerts if a['severity'] == 'Critical')
    high_count = sum(1 for a in alerts if a['severity'] == 'High')
    medium_count = sum(1 for a in alerts if a['severity'] == 'Medium')
    device_count = len(device_profiles)
    top_threats = sorted(alerts, key=lambda x: -x['risk_score'])[:5]
    top_devices = sorted([
        {'name': k, 'risk_score': v['risk_score'], 'risk_level': 'Critical' if v['risk_score'] >= 75 else 'High' if v['risk_score'] >= 50 else 'Medium' if v['risk_score'] >= 25 else 'Low'}
        for k, v in device_profiles.items()
    ], key=lambda x: -x['risk_score'])[:10]
    recommendations = [
        'Segment your network to isolate critical devices.',
        'Enforce strong password policies and multi-factor authentication.',
        'Update all systems and firmware regularly.',
        'Monitor for unusual outbound traffic and large file transfers.',
        'Educate staff on phishing and social engineering risks.'
    ]

    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '../templates')))
    template = env.get_template('report.html')
    html_out = template.render(
        company_name=company_name,
        overall_risk_score=overall_risk_score,
        risk_level=risk_level,
        critical_count=critical_count,
        high_count=high_count,
        medium_count=medium_count,
        device_count=device_count,
        top_threats=top_threats,
        top_devices=top_devices,
        recommendations=recommendations
    )
    pdf_bytes = HTML(string=html_out).write_pdf()
    return pdf_bytes
