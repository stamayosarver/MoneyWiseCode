import plaid
from plaid.api import plaid_api
from src.settings import app_settings

configuration = plaid.Configuration(
  host=plaid.Environment.Sandbox,
  api_key={
    'clientId': app_settings.plaid_client_id,
    'secret': app_settings.plaid_secret
  }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)