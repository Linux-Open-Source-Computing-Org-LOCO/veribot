import time, random
from string import Template
import yaml
from threading import Thread
from pathlib import Path

def getVersion():
    version_path = Path(".git/HEAD").read_text()[5:].rstrip()
    version = f"veribot {version_path[11:]}/{Path(f".git/{version_path}").read_text()[:6].rstrip()}"
    return version

def onReady():
    version = getVersion()
    print(version)

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
        print("Error in reading config file. Dummy output returned.")

    return value


class bingus:
    _cache = readConfig("cache")
    _saveInterval = readConfig("saveInterval")
    _OTPTries = {}
    _OTPWaitlist = {}
    _OTPTokens = {}
    print(_saveInterval)

    def writeCacheToFile():
        print("Writing cache...")
        try:
            with open(".cache.yaml", "w") as cacheFile:
                cacheDict = {"OTPTries": _OTPTries, "OTPWaitlist": _OTPWaitlist, "OTPTokens": _OTPTokens}
                yaml.dump(cacheDict, cacheFile)
                cacheFile.close()
                print("Done")

        except:
            print("Error saving dictionaries to cache.")


    if _cache:
        try:
            with open(".cache.yaml", "r") as cacheFile:
                cacheDict = yaml.safe_load(cacheFile)
                _OTPTries = cacheDict["OTPTries"]
                _OTPWaitlist = cacheDict["OTPWaitlist"]
                _OTPTokens = cacheDict["OTPTokens"]
                cacheFile.close()
                print("Cache successfully loaded.")

        except:
            print("Error reading cache file, continuing with empty dictionaries.")

        writeCacheToFile()

    else:
        print("Beginning with empty dictionaries.")

    def readCachedOTP(id):
        try:
            return _OTPTokens[id]

        except:
            return -1

    def readCachedTry(id):
        try:
            return _OTPTries[id]

        except:
            return -1

    def readCachedWaitlist(id):
        try:
            return _OTPWaitlist[id]

        except:
            return -1


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

        otp = number[-5:]
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

def formatLogMessage(priority, user_id, message):
    output = ""
    when = time.strftime("%a, %d %b %Y %H:%M:%S -0600", time.localtime())
    if priority and user_id is not None:
        output = f"**[{when}] <@{user_id}>: {message}**"

    elif not priority and user_id is not None:
        output = f"[{when}] <@{user_id}>: {message}"

    elif priority and user_id is None:
        output = f"**[{when}]: {message}**"

    else:
        output = f"[{when}]: {message}"
