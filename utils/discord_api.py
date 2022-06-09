import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
ready = False

@client.event
async def on_ready():
    ready = True
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_trade(msg):
    if ready:
        guild = client.guilds[0]
        for chan in guild.channels:
            # Looking for trade-alerts channel
            if 'trade' in str(chan):
                await chan.send(msg)
                return
    else:
        print('Client not ready')

client.dispatch('trade', 'Dispatched an event and mmsg')
client.run(TOKEN)