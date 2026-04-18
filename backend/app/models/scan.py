# Placeholder for Scan SQLAlchemy model
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from ..core.database import Base

class Scan(Base):
    __tablename__ = "scans"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    status = Column(String)
    created_at = Column(DateTime)
