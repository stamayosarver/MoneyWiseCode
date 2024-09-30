from io import BytesIO
from PyPDF2 import PdfReader
from pydantic import BaseModel
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.models.common import EmailParticipants
from src.ses.client import ses_client
from src.models.dtos.email import IncomingMessageRequest, DecodedEmailMessage
import base64
from typing import Optional
from mailparse import EmailDecode

class RawEmailMessage(BaseModel):
  participants: EmailParticipants
  subject: str
  text: str
  message_id: Optional[str] = None

  def build_to_mime_message(self) -> MIMEMultipart:
    message = MIMEMultipart("mixed")
    body = MIMEMultipart("alternative")

    message['Subject'] = self.subject

    message['From'] = f"{self.participants.sender.name} <{self.participants.sender.email}>" if self.participants.sender.name else self.participants.sender.email
    message['To'] = f"{self.participants.receiver.name} <{self.participants.receiver.email}>" if self.participants.receiver.name else self.participants.receiver.email

    if self.message_id is not None:
      message.add_header("Message-Id", self.message_id)
      message.add_header("In-Reply-To", self.message_id)
      message.add_header("References", self.message_id)

    body.attach(MIMEText(self.text, "plain"))

    message.attach(body)

    return message

def send_email_message(mime: MIMEMultipart):
  strmsg = str(mime)
  body = bytes(strmsg, "utf-8")

  response = ses_client.send_raw_email(
    Source=mime['From'],
    Destinations=[
      mime['To']
    ],
    RawMessage={
      'Data': body
    }
  )

  return response

def decode_incoming_message(request: IncomingMessageRequest) -> DecodedEmailMessage:
  decoded_content = base64.b64decode(request.content).decode("utf-8")
  decoded_email = EmailDecode.load(decoded_content)

  result = DecodedEmailMessage(**decoded_email)

  if len(result.attachments) > 0:
    attachment = result.attachments[0]
    if attachment.type != "application/pdf":
      return result

    document_bytes = base64.b64decode(attachment.content)
    document_stream = BytesIO(document_bytes)

    reader = PdfReader(document_stream)

    attachment_content = ""

    for page in reader.pages:
      attachment_content += page.extract_text()

    result.text += f"""\nThe user has provided an attachment in this email. Here is the content:
    <attachment_content>
      { attachment_content }
    </attachment_content>
    """

  return result