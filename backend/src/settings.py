from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
  mongodb_connection_uri: str
  perplexity_api_key: str
  aws_access_key_id: str
  aws_secret_access_key: str
  plaid_client_id: str
  plaid_secret: str

  model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

app_settings = AppSettings()