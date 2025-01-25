import time, random

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

        otp = number # should be 10 digits

    except:
        print("Error in OTP creation.")

    return otp

def verifyTTUEmail(email):
    verified = False

    try:
        if "@ttu.edu" in email.lower() or "@ttuhsc.edu" in email.lower():
            verified = True

        else:
            print("Invalid email.")

    except:
        print("Invalid expression.")

    return verified
