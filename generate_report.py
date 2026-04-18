"""
Standalone script to generate a Sentinel PDF report from JSON files.
"""
import argparse
import json
from backend.app.services.report_generator import generate_pdf_report

def main():
    parser = argparse.ArgumentParser(description='Generate Sentinel PDF report')
    parser.add_argument('--company', required=True, help='Company name')
    parser.add_argument('--alerts', required=True, help='Path to alerts.json')
    parser.add_argument('--devices', required=True, help='Path to device_profiles.json')
    parser.add_argument('--output', required=True, help='Output PDF path')
    args = parser.parse_args()

    with open(args.alerts, 'r') as f:
        alerts = json.load(f)
    with open(args.devices, 'r') as f:
        device_profiles = json.load(f)
    # For now, risk_timeline is not used in the template
    risk_timeline = []

    pdf_bytes = generate_pdf_report(args.company, alerts, device_profiles, risk_timeline)
    with open(args.output, 'wb') as f:
        f.write(pdf_bytes)
    print(f"PDF report generated: {args.output}")

if __name__ == '__main__':
    main()
