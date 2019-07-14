'''
Author:  Marcel Goodwin
Created: 6/24/19
Updated: 7/14/19
The anti-bot bot for all of your bot message killing needs. If another discord bot is annoying you,
simply install anti-bot bot and use the a!banish command to start deleting all messages sent to the server
by that bot!
'''

import discord
import asyncio
from discord.ext import commands
import json

#print(discord.__version__)
token = open("bot-token.txt", "r").read(59)

client  = discord.Client() #start the discord Client

backup = open("banned.txt", "r")
f = backup.readlines()
connectedServers = json.loads(f[0])
backup.close()
banished = []

bot = commands.Bot(command_prefix='a!')

#this function backs up the banished bots to a text file for persistance after shutdowns
def backup_banList():
    jsonBanList = json.dumps(connectedServers)
    backup = open("banned.txt", "w")
    backup.write(jsonBanList)
    backup.close()
    print("banishment list updated")

@bot.event
async def on_connect():
    print("antibot has connected to discord")

@bot.event
async def on_ready():
    print(f'we have logged in as client {bot.user}')
    for server in bot.guilds:
        if server.name not in connectedServers:
            connectedServers[server.name] = {}
    print(connectedServers)
    
@bot.command(pass_context=True)
async def banish(ctx, *args):
    print(args)
    name = args[0]
    for x in range(1, len(args)):
        name = name + " " + args[x]
    if name == "anti-bot bot":
        await ctx.send("Antibot refuses to banish itself. You have no power over it.")
    else:
        for user in ctx.guild.members:
            if user.name == name:
                if user.bot:
                    if user not in connectedServers[ctx.guild.name]:
                        guild = connectedServers[ctx.guild.name]
                        guild[user.name] = user.id
                        await ctx.send(user.name + " has been banished. Permanently.")
                        backup_banList()
                else:
                    await ctx.send(user.name + " is not a bot and cannot be banished.")

@bot.command(pass_context=True)
async def unbanish(ctx, *args):
    name = args[0]
    for x in range(1, len(args)):
        name = name + " " + args[x]
    guild = connectedServers[ctx.guild.name]
    print(guild)
    print(name)
    if name in guild:
        if name == "Dad Bot":
            await ctx.send("Dad Bot has performed many heinous acts against the creator of Antibot, and cannot be unbanished.")
        else:
            guild.pop(name)
            await ctx.send(name + " has been unbanished for now.")
        backup_banList()
    else:
        await ctx.send(name + " has not been banished and therefore cannot be unbanished.")

@bot.command(pass_context=True)
async def antibot_status(ctx):
    await ctx.send("Anti-bot is running.")


@bot.event
async def on_message(message):
    #print(f'{message.channel}: {message.author}: {message.author.name}: {message.content}')
    wordList  = message.content.split()
    print(wordList)
    if message.author.name in connectedServers[message.guild.name]:
        await message.delete()
    await bot.process_commands(message)

bot.run(token)
