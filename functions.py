import time, random
from string import Template
import yaml

def readToken(line):
    token = ""
    with open(".tokens") as tokenfile:
       token = tokenfile.readlines()[line].rstrip()

    tokenfile.close()
    return token

def makeOTP():
    otp = "If you are recieving this, there has been a mistake.\nPlease contact one of the officers for assistance."

    try:
        number = str(int(time.clock_gettime(time.CLOCK_REALTIME) / random.random()))

        otp = number[0:5]
        int(otp)

    except:
        print("Error in OTP creation.")

    return otp

def returnBlocklist():
    blocklist = []
    try:
        with open(".blocklist") as blocklistFile:
            blocklist = blocklistFile.readlines()
            blocklistFile.close()

            for i in range(0, len(blocklist)):
                blocklist[i].rstrip().lower()

                if blocklist[i][-1:len(blocklist[i])] == "\n":
                    blocklist[i] = blocklist[i][:-1]

    except:
        print("Missing blocklist file.")

    return blocklist

def verifyTTUEmail(email):
    verified = False
    email.lower()

    try:
        if ("@ttu.edu" in email or "@ttuhsc.edu" in email) and (email[-3:len(email)] == "edu") and (email not in returnBlocklist()):
            verified = True

        else:
            print("Invalid email.")

    except:
        print("Invalid expression.")

    return verified

def cacheOTP(user_id, OTP):
    try:
        with open(f".cache/{user_id}", "r") as cachedOTPFile:
            cachedOTPFile.close()
            Path.unlink(cachedOTPFile)
            cacheOTP(user_id, OTP)

    except:
        with open(f".cache/{user_id}", "w") as cachedOTPFile:
            cachedOTPFile.write(str(OTP))
            cachedOTPFile.close()

def readCachedOTP(user_id):
    cachedOTP = -1
    try:
        with open(f".cache/{user_id}", "r") as cachedOTPFile:
            cachedOTP = cachedOTPFile.readlines()[0].rstrip()
            cachedOTPFile.close()

    except:
        print(f"Cached OTP file {user_id} does not exist.")

    return cachedOTP

def compareOTP(enteredOTP, user_id):
    valid = False
    readOTP = readCachedOTP(user_id)
    if enteredOTP == readOTP:
        valid = True

    return valid

def getEmailHTML(user_name, OTP, club_title):
    email = "Internal error."
    try:
        with open("message.html", "r") as messageFile:
            message = messageFile.read()
            email = Template(message).safe_substitute(username = user_name, OTPcode = OTP, fullClubTitle = club_title)
            messageFile.close()

    except:
        print("Missing email HTML message file.")

    return email

def readConfig(key):
    value = -1
    try:
        with open("config.yaml") as configFile:
            config = yaml.safe_load(configFile)
            if "channel_" in key:
                value = config["channels"][key.removeprefix("channel_")]

            elif "role_" in key:
                value = config["roles"][key.removeprefix("role_")]

            elif "text_" in key:
                value = config["text"][key.removeprefix("text_")]

            else:
                value = config[key]

            configFile.close()

                
    except:
        sys.exit("FATAL: Error reading config file.")

    return value
