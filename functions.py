import math, time, random

def readToken(line):
    token = ""
    with open(".tokens") as tokenfile:
       token = tokenfile.readlines()[line].rstrip()

       # Just like an array, the lines start at 0, not 1.

    tokenfile.close()
    return token

def makeOTP():
    otp = "If you are recieving this, there has been a mistake.\nPlease contact one of the officers for assistance."

    try:
        number = (int(time.clock_gettime(time.CLOCK_REALTIME) / random.random()))

        otp = number

    except:
        print("Error in OTP creation.")

    return otp
