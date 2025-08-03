from twilio.rest import Client
import os
from dotenv import load_dotenv
from globar_vars import Var

# # Twilio credentials
# ACCOUNT_SID = Var.ACCOUNT_SID
# AUTH_TOKEN = Var.AUTH_TOKEN
# WHATSAPP_NUMBER = Var.WHATSAPP_NUMBER
#
# # Initialize Twilio client
# client = Client(ACCOUNT_SID, AUTH_TOKEN)

load_dotenv()

async def snd_image(creds, to_number: str, image_url: str, body: str = "Here's an image for you!"):
    try:
        print(image_url)
        message = creds.get("whatsapp_client").messages.create(
            from_=creds.get("whatsapp_number", os.getenv("WHATSAPP_NUMBER")),
            to=f'whatsapp:{to_number}',
            body=body,
            media_url=[image_url]
        )
        return "Image sent successfully"
    except Exception as e:
        return "Error sending message: " + str(e)

async def snd_message(creds, to_number: str, body: str):
    try:
        message = creds.get("whatsapp_client").messages.create(
            from_=creds.get("whatsapp_number"),
            to=f'whatsapp:{to_number}',
            body=body
        )
        return "Message sent successfully"
    except Exception as e:
        return "Error sending message: " + str(e)
# cred = {"whatsapp_client": client,"account_sid":ACCOUNT_SID, "auth_token":AUTH_TOKEN, "whatsapp_number":WHATSAPP_NUMBER, }
# snd_message('+918891636432', "Myre")
# print(snd_image(cred,"+918891636432", "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSE_VHEsIHyx5bJ9AdDPUYMIsMd-1u14szqsA&s", "here is the image"))

