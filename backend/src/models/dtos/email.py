from pydantic import BaseModel, Field
from typing import List, Optional
from src.models.common import EmailAddress

class IncomingMessageRequest(BaseModel):
  content: str

class EmailAttachment(BaseModel):
  type: str
  name: str
  encoding: str
  content: str

class DecodedEmailMessage(BaseModel):
  text: str
  html: str
  subject: str
  from_: EmailAddress = Field(alias="from")
  date: str
  message_id: str = Field(alias="message-id")
  to: List[EmailAddress]
  return_path: EmailAddress = Field(alias="return-path")
  timestamp: int
  attachments: List[EmailAttachment] = []