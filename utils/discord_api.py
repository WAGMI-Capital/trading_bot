import os
from discord import Webhook, RequestsWebhookAdapter
from dotenv import load_dotenv

load_dotenv()
HOOK_URL = os.getenv('WEBHOOK_URL')

webhook = Webhook.from_url(HOOK_URL, adapter=RequestsWebhookAdapter()) # Initializing webhook

def notify_discord(msg):
    # Maximum of 2000 characters per Discord message
    msg = msg[:2000] if len(msg) > 2000 else msg
    webhook.send(msg)