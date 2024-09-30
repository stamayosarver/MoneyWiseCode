from beanie import Document
from datetime import datetime
from src.models.common import EmailAddress
from typing import List, Optional
from pydantic import BaseModel

class AccountBalance(BaseModel):
  available: float
  current: float

class FinancialAccount(Document):
  user_id: str
  account_id: str
  balances: AccountBalance
  name: str
  official_name: str
  subtype: str
  type: str

  class Settings:
    name = "financialAccount"