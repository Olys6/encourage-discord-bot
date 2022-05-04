from replit import db
import os
import discord
import requests 
import json
import random
from keep_alive import keep_alive
discord_token = os.environ['discord_token']

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person!"
]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = f"{json_data[0]['q']} -{json_data[0]['a']}"
  return quote

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]
    
def delete_encouragements(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements
  
@client.event
async def on_ready():
  print("WE HAVE LOGGED IN AS {0.user}"
  .format(client))

@client.event
async def on_message(message):
  # message.author is the user who send a message while client.user is the bot
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  
  options = starter_encouragements
  if "encouragements" in db.keys():
    # options.extend(db["encouragements"]) <- does the same as the code below
    options = options + list(db["encouragements"])

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ", 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del", 1)[1])
      delete_encouragements(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  print(encouragements)

keep_alive()
client.run(discord_token)