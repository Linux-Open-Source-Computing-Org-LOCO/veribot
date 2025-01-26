import discord
import resend
from functions import *

resend.api_key = readToken(1)

class myClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    with channel.on_message() == "1332534981121150977":


    # async def verify():

    # async def otp():


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.messages = True

client = myClient(intents=intents)
client.run(readToken(0))
