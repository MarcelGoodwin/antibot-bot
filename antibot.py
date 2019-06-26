

import discord

#print(discord.__version__)
token = open("bot-token.txt", "r").read(59)

client  = discord.Client() #start the discord Client



@client.event
async def on_ready():
    print(f'we have logged in as client {client.user}')

@client.event
async def on_message(message):
    #print(f'{message.channel}: {message.author}: {message.author.name}: {message.content}')
    if message.content == "!antibot status":
        await message.channel.send("Antibot-bot is running")

client.run(token)
