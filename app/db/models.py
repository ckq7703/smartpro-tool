from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255), nullable=True)
    google_id = Column(String(255), unique=True, index=True, nullable=True)
    role = Column(String(50), default="user") # "admin" or "user"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    reports = relationship("ReportHistory", back_populates="owner")
    templates = relationship("TemplateDoc", back_populates="owner")

class ReportHistory(Base):
    __tablename__ = "reports_history"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    version = Column(String(50))
    filename = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="reports")

class TemplateDoc(Base):
    __tablename__ = "templates_doc"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    filename = Column(String(255))
    is_master = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="templates")
