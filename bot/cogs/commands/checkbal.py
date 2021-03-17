import discord
from discord.ext import commands
from .register import Register
import os
import sys

class CheckBalance(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Change current working directory from .../stonks-bot/bot to .../stonks-bot/bot/economy to access mainbank.json if in main.py
    if sys.path[0].endswith('bot'):
        os.chdir(f'{sys.path[0]}/economy')

    @commands.command(aliases = ['bal'])
    async def balance(self, ctx):
        await Register.open_account(Register,ctx.author)
        user = ctx.author
        users = await Register.get_bank_data(Register)
        # Returns embed message of current balance of the user
        bank = round(users[str(user.id)]['Bank'], 2)
        inv_money  = round(users[str(user.id)]['Invested money'], 2)
        emb = discord.Embed(title = f'{ctx.author.name}\'s balance', color = 0x07f7c7)
        emb.add_field(name = 'Bank', value = bank)
        emb.add_field(name = 'Invested money', value = inv_money)
        await ctx.send(embed=emb)

def setup(client):
    client.add_cog(CheckBalance(client))
