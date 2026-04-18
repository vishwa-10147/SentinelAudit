# Placeholder for Celery background tasks
from celery import Celery

celery_app = Celery('sentinel', broker='redis://localhost:6379/0')

@celery_app.task
def generate_report_async():
    print("Generating report in background...")
