import discord
from discord import app_commands
import resend
from functions import *

discordToken = readToken(0)
resend.api_key = readToken(1)
