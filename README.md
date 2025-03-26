# veribot
Discord bot for verification via (TTU) .edu email accounts.

## Usage
Automatically, the bot will log:
* Username, display name and avatar changes.
* Messages entered in the quarantine channel.
* Email addresses entered by users.
* If any incorrect usage is detected, and by who.
Additionally, the bot will automatically delete messages sent by non-admins in the quarantine channel.

### App Commands
* `verify <email>`
    + User-facing.
    + Takes the `email` string as an argument, makes sure that it is a (TTU) email address, then sends an email containing a One-Time-Passcode to it.
* `otp <OTP Key>`
    + User-facing.
    + Takes the `OTP Key` string as an argument, casts it to an integer then checks if it matches the One-Time-Passcode on file.
    + If it matches, it grants the user access to the rest of the Discord server.
    + If it does not match, it removes one of the three tries.
    + At the end of the three tries, it institutes a 30 minute countdown on the `verify` command for the user and removes the One-Time-Passcode on file.
## Dependencies
python >3.12<br>
discord.py 2.4.0<br>
resend 2.6.0<br>
PyYAML 6.0.1<br>

## Installation
### Server-Side
* Clone the repository using `git clone https://github.com/Linux-Open-source-Computing-Org-LOCO/veribot.git` into the directory where you want to install it.
* There are two files and a directory that need to be created and populated before you launch the bot.
    + Create the directory `.cache` using the command `mkdir .cache` within the veribot directory.
    + Next, run `touch config.yaml .tokens` to create the other two required files.
    + Populate `.tokens` with the following:
        - Line 1: Discord Bot token
        - Line 2: Resend API token
        - Example:
```
discordtoken
resendtoken
```
<br>
    	- Ensure there is no extraneous text within this file. Extra newline characters will be taken care of.
    + Populate `config.yaml` with the following (replacing placeholder text with your own configuration):
```yaml
guildID: integer
channels:
  quarantineChannelID: integer
  logChannelID: integer
  deletedMessagesChannelID: integer
roles:
  verifiedRoleID: integer
  adminRoleID: integer
text:
  fullClubTitle: "string"
  emailAddress: "Example String <example@example.com>"
  emailSubject: "string"
  status: "string"
```
<br>
    + The IDs can be found by enabling "Developer Mode" on your Discord account, then opening the context menu of the relevant item.
    + Internally, Discord servers are known as guilds.
* Ideally, you would run the bot in a screen.
    + Ensure you have the `screen` program installed.
    + You can enter a screen by typing `screen` into the console.
    + You can reenter a screen by typing `screen -r <screen id>`.
    + You can list active screens by typing `screen -ls`.
    + You can exit a screen by pressing the key combination: `C-a d`. (aka `ctrl` + `a`, then `d`)
* Next, run the bot by typing `python3 main.py`.

### Client-Side
* You will need at least:
    + A quarantine channel, and a log channel.
    + An administrator or moderator role (can post messages in the quarantine channel).
    + A "verified" role that can see the rest of the public server, but not the quarantine channel.
* Configure the default @everyone permissions to be minimal.
* Configure the server so that @everyone can only see the quarantine channel.