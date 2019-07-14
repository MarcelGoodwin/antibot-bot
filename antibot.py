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
bot.remove_command('help')

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
async def info(ctx):
    embed = discord.Embed(title="anti-bot bot", description="The anti-bot bot for all of your bot message killing needs. If another discord bot is annoying you, simply install anti-bot bot and use the a!banish command to start deleting all messages sent to the server by that bot!", color=0x008bf0)
    embed.add_field(name="Author", value="Marcel Goodwin")
    embed.add_field(name="Server Count", value=f"{len(bot.guilds)}")
    embed.add_field(name="Invite", value="[Invite link]https://discordapp.com/api/oauth2/authorize?client_id=445766934953459732&permissions=206912&scope=bot")
    await ctx.send(embed = embed)

@bot.command(pass_context=True)
async def help(ctx):
    print(ctx.message.author)
    embed = discord.Embed(title="anti-bot bot help", description="A list of commands for using Antibot properly", color=0x008bf0)
    embed.add_field(name="a!info", value="Sends bot information to channel.")
    embed.add_field(name="a!help", value="Sends message author a pm with a list of commands.")
    embed.add_field(name="a!banish <bot username>", value="Adds bot user with name \"bot username\" to a list of banished users. Messages sent by that bot are deleted.")
    embed.add_field(name="a!unbanish <bot username>", value="Removes bot with name \"bot username\" from the banished user list.")
    embed.add_field(name="a!banished", value="Returns list of banished bots for the server.")
    embed.add_field(name="a!antibot_status", value="Tells you if antibot is running or not.")
    await ctx.message.author.send(embed = embed)

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
async def banished(ctx):
    message = "Banished users are: \n"
    for bot in connectedServers[ctx.guild.name]:
        message += bot + '\n'
    await ctx.send(message)

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
    print(f'{message.channel}: {message.author}: {message.author.name}: {message.content}')
    wordList  = message.content.split()
    print(wordList)
    if message.guild == None:
        return
    if message.author.name in connectedServers[message.guild.name]:
        await message.delete()
    await bot.process_commands(message)

bot.run(token)
