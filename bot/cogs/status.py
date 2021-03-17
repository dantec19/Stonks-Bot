import discord
from discord.ext import commands

class Status(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Informs if the bot is ready
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online')

def setup(client):
    client.add_cog(Status(client))
