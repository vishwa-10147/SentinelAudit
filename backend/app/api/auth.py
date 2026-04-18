# Placeholder for authentication endpoints
from fastapi import APIRouter

router = APIRouter()

@router.post("/auth/login")
def login():
    return {"message": "Login"}

@router.post("/auth/register")
def register():
    return {"message": "Register"}
