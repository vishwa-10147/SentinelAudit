# Placeholder for Report SQLAlchemy model
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from ..core.database import Base

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    file_path = Column(String)
    created_at = Column(DateTime)
