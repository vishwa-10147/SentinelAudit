# Placeholder for Razorpay payment endpoints
from fastapi import APIRouter

router = APIRouter()

@router.post("/payments/")
def create_payment():
    return {"message": "Payment created"}
