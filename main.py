import discord
from discord import app_commands
import resend
from functions import *

discordToken = readToken(0)
resend.api_key = readToken(1)
myGuild = discord.Object(1066163609190801500)

class myClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents = intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild = myGuild)
        await self.tree.sync(guild = myGuild)

intents = discord.Intents.default()
client = myClient(intents = intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user} ({client.user.id})")
    logChannel = client.get_channel(1332518941633024010)
    await logChannel.send(content = "Ready.")

@client.tree.command()
@app_commands.describe(email = "Your TTU or TTUHSC TechMail address.")
async def verify(interaction: discord.Interaction, email: str):
    quarantineChannel = client.get_channel(1332534981121150977)
    logChannel = client.get_channel(1332518941633024010)
    member = interaction.user
    if interaction.channel == quarantineChannel:
        if verifyTTUEmail(email):
            await interaction.response.send_message(f"{member}, an email containing a One-Time Passcode will be sent to: {email}\n**Please, check your \"Junk Email\"**", ephemeral = True)
            await logChannel.send(content = f"{member} entered a valid TTU/TTUHSC email: {email}")

        else:
            await interaction.response.send_message(f"{email} is not a valid TechMail address. Please try again.", ephemeral = True)
            await logChannel.send(content = f"{member} attempted to verify using {email}")

    else:
        await logChannel.send(content = f"{member} attempted to verify from outside quarantine.")
        print(f"{member} attempted to verify illegally.")

@client.tree.command()
@app_commands.describe(otp = "The One-Time Passcode that you recieved at your TechMail address.")
async def otp(interaction: discord.Interaction, otp: int):
    quarantineChannel = client.get_channel(1332534981121150977)
    logChannel = client.get_channel(1332518941633024010)


client.run(discordToken)
