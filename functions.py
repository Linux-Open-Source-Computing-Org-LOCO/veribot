import math, time, random

def readToken(line):
    token = ""
    with open(".tokens") as tokenfile:
       token = tokenfile.readlines()[line]

       # Just like an array, the lines start at 0, not 1.

    tokenfile.close()
    return token

def makeOTP():
    return 1
