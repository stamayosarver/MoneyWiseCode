import boto3
from src.settings import app_settings

ses_client = boto3.client(
  "ses",
  region_name="us-east-1",
  aws_access_key_id=app_settings.aws_access_key_id,
  aws_secret_access_key=app_settings.aws_secret_access_key
)