import datetime
from src.models.dtos.email import DecodedEmailMessage
from src.models.dtos.chat import ChatMessage
from src.models.entities.email_message import EmailMessage
from src.models.common import EmailAddress
from src.perplexity.client import SYSTEM_PROMPT
from beanie.operators import Or
from typing import List

async def find_conversation_messages(sender: str):
  messages = await EmailMessage.find(
    Or(
      EmailMessage.sender.email == sender,
      EmailMessage.return_path.email == sender
    )
  ).sort(+EmailMessage.send_at).limit(10).to_list()

  return messages

async def insert_incoming_message(
  incoming_message: DecodedEmailMessage
):
  await EmailMessage.insert_one(EmailMessage(
    text=incoming_message.text,
    html=incoming_message.html,
    subject=incoming_message.subject,
    sender=incoming_message.from_,
    recipients=incoming_message.to,
    return_path=incoming_message.return_path,
    message_id=incoming_message.message_id,
    send_at=datetime.datetime.fromtimestamp(incoming_message.timestamp, datetime.timezone.utc)
  ))

async def insert_outgoing_message(
  assistant_response: str,
  incoming_message: DecodedEmailMessage
):
  await EmailMessage.insert_one(EmailMessage(
    text=assistant_response,
    html=assistant_response,
    subject=incoming_message.subject,
    sender=EmailAddress(email=incoming_message.to[0].email, name=None),
    recipients=[incoming_message.from_],
    return_path=incoming_message.return_path,
    message_id=incoming_message.message_id,
    send_at=datetime.datetime.now(datetime.timezone.utc)
  ))

def format_messages_for_completion(messages) -> List[ChatMessage]:
    messages = [{ "role": "assistant" if message.sender.email == "assistant@moneywise.wiki" else "user", "content": message.text.split("\n\n")[0] } for message in messages]
    messages = [{ "role": "system", "content": SYSTEM_PROMPT }, *messages]

    return [ChatMessage(**message) for message in messages]