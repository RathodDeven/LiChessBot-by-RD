import discord
import berserk
import os
from replit import db
from keep_alive import keep_alive

client = discord.Client()

session = berserk.TokenSession(os.getenv('TOKEN'))
liclient = berserk.Client(session)

if "helper" not in db.keys():
  db["helper"] = ["'li help' -> information on how use li bot.","li challenge [username] [rated=(True,False)] [clock_limit=(minutes)] [clock_increment=(seconds)]'  -> challenge other person with that username","'li create [clock_limit=(minutes)] [clock_increment=(seconds)] '  -> creates a open challenge where two players can join.","'li tourny [name] [clock_time=(minutes)] [clock_increment=(seconds)] [wait_minutes] [rated=(True,False)] [length_of_tournament_in_minutes] '  -> creates a tournament with given parameters ."]



@client.event
async def on_ready():
  print('We have logged in as {0.user} discord bot account'.format(client))
  usr_mail = liclient.account.get_email()
  print(f'We have logged in as {usr_mail} of lichess account')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  chn = message.channel

  if msg.startswith("li "):
    cmd = msg.split()
    if cmd[1].lower() == "help":
      temp = "USAGE : \n\n" + (" \n\n ".join(db["helper"]))
      await chn.send(temp)
    elif cmd[1].lower() == "create":
      if len(cmd) != 4 or (not cmd[2].isnumeric())  or (not cmd[3].isnumeric()):
        await chn.send("There is some mistake..!")
        await chn.send(db["helper"][2])
      else:
        t = liclient.challenges.create_open(clock_limit=(60*int(cmd[2])),clock_increment=int(cmd[3]))

        await chn.send(f"An Open Challenge has been created with clock_limit = {cmd[2]} minutes and clock_increment = {cmd[3]} seconds. \n\n Two players can join through below link")
        await chn.send(t['challenge']['url'])

    elif cmd[1].lower() == "tourny":
      if len(cmd) != 8 or (not cmd[3].isnumeric()) or (not cmd[4].isnumeric()) or (not cmd[5].isnumeric()) or (cmd[6].lower() != "true" and cmd[6].lower() != "false") or (not cmd[7].isnumeric()):
        await chn.send("There is some mistake..! \n\n")
        await chn.send(db["helper"][3])
      else:
        t = liclient.tournaments.create(clock_time=int(cmd[3]),clock_increment = int(cmd[4]),minutes=int(cmd[7]),name=cmd[2],wait_minutes=int(cmd[5]),rated=(cmd[6].lower() == "true"))
        temp = "https://lichess.org/tournament/" + t['id']
        await chn.send("Your tournament was created successfully. \n\n Click on the below link to join the tournament...! \n\n")
        await chn.send(temp)

    elif cmd[1].lower() == "challenge":
      if len(cmd) != 6 or (cmd[3].lower() != "true" and cmd[3].lower() != "false") or (not cmd[4].isnumeric()) or (not cmd[5].isnumeric()):
        await chn.send("There is some mistake..! \n\n" )
        await chn.send(db["helper"][1])
      else:
        t = liclient.challenges.create(username=cmd[2],rated=(cmd[3].lower() == "true"),clock_limit=(60*int(cmd[4])),clock_increment=int(cmd[5]))
        await chn.send("Your challenge was create successfully. \n\n Click below link to start playing..!")
        await chn.send(t['challenge']['url'])


keep_alive()
client.run(os.getenv('TOKEN_DI'))

