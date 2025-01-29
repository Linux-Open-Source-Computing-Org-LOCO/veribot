import discord
from discord import app_commands
import resend
from functions import *
import time
from pathlib import Path

discordToken = readToken(0)
resend.api_key = readToken(1)
myGuild = discord.Object(readConfig("guildID"))
OTPTries = {}
OTPWaitlist = {}
class myClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents = intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild = myGuild)
        await self.tree.sync(guild = myGuild)

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True
client = myClient(intents = intents)

logChannelID = int(readConfig("channel_logChannelID"))
quarantineChannelID = int(readConfig("channel_quarantineChannelID"))
deletedMessagesChannelID = int(readConfig("channel_deletedMessagesChannelID"))

@client.event
async def on_ready():
    print(f"Logged in as {client.user} ({client.user.id})")
    logChannel = client.get_channel(logChannelID)
    try:
        for root, dirs, files in Path(".cache").walk(on_error = print):
            numCleared = 0
            for name in files:
                print("Clearing " + str(root) + "/" + str(name))
                Path.unlink(str(root) + "/" + str(name))
                numCleared += 1

            await logChannel.send(content = f"Cleared {numCleared} cached OTPs.")

    except:
        await logChannel.send(content = "Error upon clearing cache.")

    await logChannel.send(content = "Ready.")

@client.tree.command()
@app_commands.describe(email = "Your TTU or TTUHSC TechMail address.")
async def verify(interaction: discord.Interaction, email: str):
    member = interaction.user
    logChannel = client.get_channel(logChannelID)
    quarantineChannel = client.get_channel(quarantineChannelID)
    if interaction.channel == quarantineChannel:
        if verifyTTUEmail(email) and readCachedOTP(member.id) == -1:
            await interaction.response.send_message(f"{member}, an email containing a One-Time Passcode will be sent to: {email}\n**Please, check your \"Junk Email\"**", ephemeral = True)
            await logChannel.send(content = f"<@{member.id}> entered a valid TTU/TTUHSC email: {email}")
            otp = makeOTP()
            cacheOTP(member.id, otp)
            params: resend.Emails.SendParams = {
                "from": readConfig("text_emailAddress"),
                "to": email,
                "subject": readConfig("text_emailSubject"),
                "html": getEmailHTML(member, otp, readConfig("text_fullClubTitle"))
            }
            print(resend.Emails.send(params))
            OTPTries[member.id] = 3
            OTPWaitlist[member.id] = time.clock_gettime(time.CLOCK_REALTIME)

        elif verifyTTUEmail(email) and not readCachedOTP(member.id) == -1:
            await interaction.response.send_message(f"{member}, your One-Time Passcode already exists.\nPlease try checking your \"Junk Mail.\"", ephemeral = True)
            await logChannel.send(content =  f"<@{member.id}> attempted to generate more than one OTP.")

        else:
            await interaction.response.send_message(f"{email} is not a valid TechMail address. Please try again.", ephemeral = True)
            await logChannel.send(content = f"<@{member.id}> attempted to verify using {email}")

    else:
        await logChannel.send(content = f"({member.id}){member} attempted to verify from outside quarantine.")
        print(f"<@{member} attempted to verify illegally.")

@client.tree.command()
@app_commands.describe(otp = "The One-Time Passcode that you recieved at your TechMail address.")
async def otp(interaction: discord.Interaction, otp: str):
    member = interaction.user
    Role = interaction.guild.get_role(readConfig("role_verifiedRoleID"))
    logChannel = client.get_channel(logChannelID)
    int(otp)
    if not readCachedOTP(member.id) == -1:
        if OTPTries[member.id] > 0:
            if compareOTP(otp, member.id):
                await logChannel.send(content = f"<@{member.id}> verified successfully.")
                await interaction.response.send_message(f"{member}, you have verified successfully. You will be redirected shortly.", ephemeral = True)
                await member.add_roles(Role)
                Path.unlink(f".cache/{member.id}")

            else:
                await logChannel.send(content = f"<@{member.id}> used an incorrect OTP.")
                await interaction.response.send_message(f"{member}, please try again.", ephemeral = True)
                OTPTries[member.id] = OTPTries[member.id] - 1

        else:
            await logChannel.send(content = f"<@{member.id}> ran out of attempts to enter OTP.")

            timeElapsed = time.clock_gettime(time.CLOCK_REALTIME) - OTPWaitlist[member.id]
            timeLeft = 1800 - timeElapsed

            if(timeLeft < 0):
                await interaction.response.send_message(f"{member}, please verify again.", ephemeral = True)
                Path.unlink(f".cache/{member.id}")
                OTPWaitlist.pop(member.id)
                OTPTries.pop(member.id)
            else:
                await interaction.response.send_message(f"{member}, please wait {timeLeft} seconds.", ephemeral = True)

@client.event
async def on_message(message):
    deletedMessagesChannel = client.get_channel(deletedMessagesChannelID)
    if message.channel.id == quarantineChannelID:
        embeds = [discord.Embed(title = f"{message.author.display_name} ({message.author.name})", description = message.content, url = f"https://discord.com/users/{message.author.id}")]
        embeds[0].set_thumbnail(url = message.author.avatar)
        if len(message.attachments) == 1:
            print(message.attachments[0].url)
            embeds[0].set_image(url = message.attachments[0].url)

        elif len(message.attachments) > 1:
            embeds[0].set_image(url = message.attachments[0].proxy_url)
            for Attachment in message.attachments:
                embeds.append(discord.Embed().set_image(url = Attachment.proxy_url))

        await deletedMessagesChannel.send(embeds = embeds)
        await message.delete()

client.run(discordToken)
