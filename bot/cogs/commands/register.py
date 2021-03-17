import discord
from discord.ext import commands
import json
import os
import sys
import random
import datetime

class Register(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Change current working directory from .../stonks-bot/bot to .../stonks-bot/bot/economy to access mainbank.json if in main.py
    if sys.path[0].endswith('bot'):
        os.chdir(f'{sys.path[0]}/economy')

    # Opens account with empty balance for unregistered users
    async def open_account(self, user):
        users = await self.get_bank_data(self)
        # Check if user already has an account in the bank
        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]['Bank'] = 0
            users[str(user.id)]['Invested money'] = 0
        # Open account in json for the user
        with open('mainbank.json', 'w') as f:
            json.dump(users, f)
        return True

    # Helper function: Check user's data from json bank
    async def get_bank_data(self):
        with open('mainbank.json', 'r') as f:
            users = json.load(f)
        return users

def setup(client):
    client.add_cog(Register(client))
