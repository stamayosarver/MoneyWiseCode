from pydantic import BaseModel
from fastapi import APIRouter
from typing import List, Optional
from src.models.dtos.email import IncomingMessageRequest
from src.perplexity.client import pplx_client, DEFAULT_MODEL_NAME
from src.models.dtos.chat import ChatMessage
from src.models.common import EmailAddress, EmailParticipants
from src.services.email import RawEmailMessage, send_email_message, decode_incoming_message
from src.services.message import insert_incoming_message, insert_outgoing_message, find_conversation_messages, format_messages_for_completion
from src.services.user import get_user_by_email
from src.services.plaid import get_user_financial_accounts

router = APIRouter(prefix="/incoming")

async def get_chat_completion(user: Optional[str], formatted_messages: List[ChatMessage]):
  if user is not None:
    financial_accounts = await get_user_financial_accounts(user)
    mapped_accounts = list(map(lambda account: f"{account.name}: ${account.balances.current}", financial_accounts))
    mapped_accounts_str = "\n".join(mapped_accounts)

    prompt_addition = f"""
    The user has provided their financial accounts and balances. Only use this information if it is relevant to the conversation.
    <user_financial_accounts>
    { mapped_accounts_str }
    </user_financial_accounts>"""

    formatted_messages[0].content = f"{formatted_messages[0].content}{prompt_addition}"

  response = pplx_client.chat.completions.create(
    model=DEFAULT_MODEL_NAME,
    messages=formatted_messages,
  )

  return response.choices[0].message.content

@router.post("/")
async def incoming(body: IncomingMessageRequest):
  incoming_message = decode_incoming_message(body)

  await insert_incoming_message(incoming_message)

  messages = await find_conversation_messages(incoming_message.return_path.email)
  formatted_messages = format_messages_for_completion(messages)

  user = await get_user_by_email(incoming_message.return_path.email)
  completion = await get_chat_completion(user, formatted_messages)

  await insert_outgoing_message(completion, incoming_message)

  message = RawEmailMessage(
    message_id=incoming_message.message_id,
    participants=EmailParticipants(
      sender=EmailAddress(name=incoming_message.to[0].name, email=incoming_message.to[0].email),
      receiver=EmailAddress(name=incoming_message.from_.name, email=incoming_message.from_.email)
    ),
    subject=incoming_message.subject,
    text=completion
  )

  send_email_message(message.build_to_mime_message())

  return { "status": "ok" }