# Placeholder for scan upload and processing endpoints
from fastapi import APIRouter

router = APIRouter()

@router.post("/scans/")
def upload_scan():
    return {"message": "Scan uploaded"}
