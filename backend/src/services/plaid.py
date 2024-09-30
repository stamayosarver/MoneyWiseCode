from src.plaid.client import client
from src.models.entities.user import User
from src.models.entities.financial_account import FinancialAccount, AccountBalance
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest

async def get_user_financial_accounts(user: User):
  accounts = await FinancialAccount.find(FinancialAccount.user_id == user.auth0_id).to_list()

  return accounts

async def sync_user_financial_accounts(user: User):
  request = AccountsBalanceGetRequest(access_token=user.plaid_access_token)
  response = client.accounts_balance_get(request)

  accounts = response["accounts"]
  financial_accounts = []

  for account in accounts:
    financial_accounts.append(
      FinancialAccount(
        user_id=user.auth0_id,
        account_id=account["account_id"],
        balances=AccountBalance(
          available=account["balances"]["available"],
          current=account["balances"]["current"],
        ),
        name=account["name"],
        official_name=account["official_name"],
        subtype=str(account["subtype"]),
        type=str(account["type"]),
      )
    )

  await FinancialAccount.insert_many(financial_accounts)