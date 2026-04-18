# Placeholder for Scan Pydantic schema
from pydantic import BaseModel
from typing import Optional

class ScanBase(BaseModel):
    status: str

class ScanCreate(ScanBase):
    pass

class ScanOut(ScanBase):
    id: int
    customer_id: int
    created_at: Optional[str]

    class Config:
        orm_mode = True
