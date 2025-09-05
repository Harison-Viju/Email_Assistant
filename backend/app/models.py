from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True)
    subject = Column(String, index=True)
    body = Column(Text)
    received_at = Column(DateTime, default=datetime.utcnow)
    sentiment = Column(String, default="neutral")
    priority = Column(String, default="not_urgent")
    is_urgent = Column(Boolean, default=False)
    status = Column(String, default="pending")  # pending, drafted, sent

    extracted_contact = Column(String, nullable=True)
    extracted_requirements = Column(Text, nullable=True)
    extracted_indicators = Column(String, nullable=True)

    reply = relationship("Reply", back_populates="email", uselist=False)


class Reply(Base):
    __tablename__ = "replies"

    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("emails.id"))
    draft = Column(Text)
    sent_at = Column(DateTime, nullable=True)
    to_address = Column(String)

    email = relationship("Email", back_populates="reply")
