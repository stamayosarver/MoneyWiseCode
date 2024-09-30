from beanie import Document
from datetime import datetime
from src.models.common import EmailAddress
from typing import List

class EmailMessage(Document):
  text: str
  html: str
  subject: str
  sender: EmailAddress
  recipients: List[EmailAddress]
  return_path: EmailAddress
  message_id: str
  send_at: datetime

  class Settings:
    name = "emailMessage"