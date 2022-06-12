import os
from discord import Webhook, RequestsWebhookAdapter
from dotenv import load_dotenv

load_dotenv()
HOOK_URL = os.getenv('WEBHOOK_URL')

webhook = Webhook.from_url(HOOK_URL, adapter=RequestsWebhookAdapter()) # Initializing webhook

def notify_discord(msg):
    webhook.send(msg)