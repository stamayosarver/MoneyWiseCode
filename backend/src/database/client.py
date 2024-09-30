from beanie import init_beanie
from src.settings import app_settings
from motor.motor_asyncio import AsyncIOMotorClient
from src.models.entities.email_message import EmailMessage
from src.models.entities.user import User
from src.models.entities.financial_account import FinancialAccount

async def initialize_database():
  client = AsyncIOMotorClient(app_settings.mongodb_connection_uri)
  
  await init_beanie(database=client.get_default_database(), document_models=[User, EmailMessage, FinancialAccount])