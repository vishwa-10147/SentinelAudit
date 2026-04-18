# Placeholder for customer management endpoints
from fastapi import APIRouter

router = APIRouter()

@router.get("/customers/")
def list_customers():
    return ["List of customers"]
