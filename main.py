import discord
import resend
from functions import *

discordToken = readToken(0)
resendToken = readToken(1)

print(makeOTP())
