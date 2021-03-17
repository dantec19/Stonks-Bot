import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents = discord.Intents(messages=True, guilds=True)
intents.members = True
fetch_offline_members = True

# Command Prefix
client = commands.Bot(command_prefix = '$', intents=intents)
# Load selected commands
@client.command()
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')

# Unload selected commands
@client.command()
async def unload(ctx, extension):
    client.punload_extension(f'cogs.{extension}')

# Links main to cogs
for filename in os.listdir('./cogs') :
    if filename.endswith('.py') and not filename.startswith('__'):
        client.load_extension(f'cogs.{filename[:-3]}')
for filename in os.listdir('./cogs/commands') :
    if filename.endswith('.py') and not filename.startswith('__'):
        client.load_extension(f'cogs.commands.{filename[:-3]}')

#Run Bot
client.run('ODA0ODk4ODI4NDI3ODUzODY0.YBTCcg.ub_W_1WnyC-56RQHngCCuz-QYys')
