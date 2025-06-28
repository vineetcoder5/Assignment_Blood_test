from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    task_id = Column(String(100), primary_key=True)
    filename = Column(String(255))
    query = Column(Text)
    status = Column(String(50), default="PENDING")
    result = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
