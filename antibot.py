

import discord

#print(discord.__version__)
token = open("bot-token.txt", "r").read(59)

client  = discord.Client() #start the discord Client

connectedServers = {}
banished = []

@client.event
async def on_ready():
    print(f'we have logged in as client {client.user}')
    for server in client.guilds:
        if server not in connectedServers:
            connectedServers[server] = []


@client.event
async def on_message(message):
    #print(f'{message.channel}: {message.author}: {message.author.name}: {message.content}')
    wordList  = message.content.split()
    if message.author in connectedServers[message.guild]:
        await message.delete()
    else:
        if message.content == "!antibot status":
            await message.channel.send("Antibot-bot is running")
        if wordList[0] == "a!banish":
            username = wordList[1]
            for x in range(2, len(wordList)):
                username  = username + " " + wordList[x]
            if username == "anti-bot bot":
                await message.channel.send("Anti-bot refuses to banish itself. You hold no power over it.")
            else:
                for user in message.guild.members:
                    if user.name == username and user not in connectedServers[message.guild] and user.bot:
                        connectedServers[message.guild].append(user)
                        await message.channel.send(user.name + " has been banished. Permanently.")


client.run(token)
