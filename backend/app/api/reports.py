# Placeholder for report CRUD and download endpoints
from fastapi import APIRouter

router = APIRouter()

@router.get("/reports/")
def list_reports():
    return ["List of reports"]
