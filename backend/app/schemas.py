from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class EmailCreate(BaseModel):
    sender: EmailStr
    subject: str
    body: str
    received_at: Optional[datetime] = None


class EmailRead(BaseModel):
    id: int
    sender: EmailStr
    subject: str
    body: str
    received_at: datetime
    sentiment: str
    priority: str
    is_urgent: bool
    status: str
    extracted_contact: Optional[str] = None
    extracted_requirements: Optional[str] = None
    extracted_indicators: Optional[str] = None

    class Config:
        from_attributes = True


class ReplyCreate(BaseModel):
    to_address: EmailStr
    draft: str


class ReplyRead(BaseModel):
    id: int
    email_id: int
    draft: str
    sent_at: Optional[datetime] = None
    to_address: EmailStr

    class Config:
        from_attributes = True
