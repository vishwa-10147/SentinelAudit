# Placeholder for Report Pydantic schema
from pydantic import BaseModel
from typing import Optional

class ReportBase(BaseModel):
    file_path: str

class ReportCreate(ReportBase):
    pass

class ReportOut(ReportBase):
    id: int
    customer_id: int
    created_at: Optional[str]

    class Config:
        orm_mode = True
