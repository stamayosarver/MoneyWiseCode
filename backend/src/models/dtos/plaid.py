from pydantic import BaseModel

class CreateLinkTokenRequest(BaseModel):
  user: str

class CreateAccessTokenRequest(BaseModel):
  user: str
  email: str
  public_token: str