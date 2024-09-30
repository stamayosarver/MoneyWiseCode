from beanie import Document
from datetime import datetime
from src.models.common import EmailAddress
from typing import List, Optional

class User(Document):
  auth0_id: str
  email: str
  plaid_access_token: Optional[str]

  class Settings:
    name = "user"