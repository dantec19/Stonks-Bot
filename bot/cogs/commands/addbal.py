import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, CommandOnCooldown
import os
import sys
import json
import random
import time
from .register import Register

class AddBalance(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Change current working directory from .../stonks-bot/bot to .../stonks-bot/bot/economy to access mainbank.json if in main.py
    if sys.path[0].endswith('bot'):
        os.chdir(f'{sys.path[0]}/economy')

    # Gives user money if user's balance is less than 1000
    @commands.command(aliases =['beg', 'find'])
    async def broke(self, ctx):
        # Automatically registers unregistered users
        await Register.open_account(Register, ctx.author)
        users = await Register.get_bank_data(Register)
        user = ctx.author
        if users[str(user.id)]['Bank'] + users[str(user.id)]['Invested money'] <= 750:
            # Random money to give between 0 and 100
            earnings = random.randrange(750, 1200)
            await ctx.send(f'{earnings} coins have been added to your bank')
            users[str(user.id)]['Bank'] += earnings
            with open('mainbank.json', 'w') as f:
                json.dump(users, f)
        else:
            await ctx.send('You are too rich to beg!')

    @commands.command(aliases = ['d'])
    @commands.cooldown(1, 86400, BucketType.user)
    async def daily(self, ctx):
        # Automatically registers unregistered users
        await Register.open_account(Register, ctx.author)
        users = await Register.get_bank_data(Register)
        user = ctx.author
        earnings = 7500
        await ctx.send(f'{earnings} coins have been added to your bank')
        users[str(user.id)]['Bank'] += earnings
        with open('mainbank.json', 'w') as f:
            json.dump(users, f)
    @daily.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown, please try again in {time.strftime("%H hours, %M minutes and %S seconds", time.gmtime(error.retry_after))}')
        else:
            raise error


def setup(client):
    client.add_cog(AddBalance(client))
