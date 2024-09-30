from src.models.entities.user import User
from typing import Optional

async def get_user_by_id(id: str) -> Optional[User]:
  return await User.find_one(User.id == id)

async def get_user_by_email(email: str) -> Optional[User]:
  return await User.find_one(User.email == email)