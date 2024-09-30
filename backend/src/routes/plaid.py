from src.plaid.client import api_client, client
from src.models.dtos.plaid import CreateLinkTokenRequest, CreateAccessTokenRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.country_code import CountryCode
from plaid.model.products import Products
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from src.models.entities.user import User
from src.services.plaid import sync_user_financial_accounts, get_user_financial_accounts
from beanie.operators import Set
from src.services.email import send_email_message, RawEmailMessage
from src.models.common import EmailAddress, EmailParticipants
from fastapi import APIRouter

router = APIRouter(prefix="/plaid")

@router.post("/link-token")
async def create_link_token(body: CreateLinkTokenRequest):
  request = LinkTokenCreateRequest(
    client_name="MoneyWise Demo",
    country_codes=[CountryCode("US")],
    language="en",
    products=[Products("auth")],
    user=LinkTokenCreateRequestUser(
      client_user_id=body.user
    )
  )

  response = client.link_token_create(request)

  return { "token": response.link_token }

@router.post("/access-token")
async def create_access_token(body: CreateAccessTokenRequest):
  request = ItemPublicTokenExchangeRequest(public_token=body.public_token)
  response = client.item_public_token_exchange(request)

  insert_user = User(
    auth0_id=body.user,
    email=body.email,
    plaid_access_token=response["access_token"]
  )

  await User.find_one(
    User.auth0_id == body.user
  ).upsert(
    Set({
      User.auth0_id: body.user,
      User.email: body.email,
      User.plaid_access_token: response["access_token"]
    }),
    on_insert=User(
      auth0_id=body.user,
      email=body.email,
      plaid_access_token=response["access_token"]
    )
  )

  await sync_user_financial_accounts(insert_user)

  email_message = RawEmailMessage(
    participants=EmailParticipants(
      sender=EmailAddress(email="assistant@moneywise.wiki", name="MoneyWise"),
      receiver=EmailAddress(email=body.email)
    ),
    subject="Welcome to MoneyWise 🤑",
    text="Hi,\n\nYour financial acounts has been successfully linked to MoneyWise. You can reply to this email or send a new email to interact with the assistant.\n\nBest,\nMoneyWise Team",
  )
  mime = email_message.build_to_mime_message()

  send_email_message(mime)

  return { "status": "ok" }