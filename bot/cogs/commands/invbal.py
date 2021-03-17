import discord
from discord.ext import commands
import os
import sys
import json
import yfinance
import requests
import bs4
from .register import Register
from bot.helper_funcs import getYfPrice

class InvestBalance(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Change current working directory from .../stonks-bot/bot to .../stonks-bot/bot/economy to access mainbank.json if in main.py
    if sys.path[0].endswith('bot'):
        os.chdir(f'{sys.path[0]}/economy')

    @commands.command(aliases=['inv','buy'])
    async def invest(self, ctx, stockamount, symbol):
        # Automatically registers unregistered users
        await Register.open_account(Register, ctx.author)
        users = await Register.get_bank_data(Register)
        user = ctx.author

        amount = float('%.2f' % round(int(stockamount)*float(getYfPrice(symbol)), 2))
        if amount>users[str(user.id)]['Bank']:
            await ctx.send("Oops! You don't have enough money. Try with a lower amount.")
        else:
            users[str(user.id)]['Invested money'] += amount
            users[str(user.id)]['Bank'] -= amount
            upperSymbol = str(symbol).upper()
            symbolCount = 1
            if list(users[str(user.id)].keys()).count(upperSymbol) < 1:
                users[str(user.id)][upperSymbol] = {}
                users[str(user.id)][upperSymbol]['TotalShares'] = int(stockamount)
                users[str(user.id)][upperSymbol]['TotalPrice'] = float(getYfPrice(symbol)) * int(stockamount)
                users[str(user.id)][upperSymbol][symbolCount] = {}
                users[str(user.id)][upperSymbol][symbolCount]["Amount"] = int(stockamount)
                users[str(user.id)][upperSymbol][symbolCount]["Price"] = amount
            else:
                while list(users[str(user.id)][upperSymbol].keys()).count(str(symbolCount)) > 0:
                        symbolCount += 1
                users[str(user.id)][upperSymbol][symbolCount] = {}
                users[str(user.id)][upperSymbol]['TotalShares'] += int(stockamount)
                users[str(user.id)][upperSymbol]['TotalPrice'] += round(float(getYfPrice(symbol)) * int(stockamount), 2)
                users[str(user.id)][upperSymbol][symbolCount]["Amount"] = int(stockamount)
                users[str(user.id)][upperSymbol][symbolCount]["Price"] = amount
            round(users[str(user.id)]['Invested money'], 2)
            round(users[str(user.id)]['Bank'], 2)

            with open('mainbank.json', 'w') as f:
                json.dump(users, f)
            await ctx.send(f"You have succesfully invested ${amount} ({stockamount} shares of {symbol.upper()} at {getYfPrice(symbol)} each)")

    @commands.command(aliases=['retire','withdraw', 's', 'draw'])
    async def sell(self, ctx, stockamount, symbol):

        # Automatically registers unregistered users
        await Register.open_account(Register, ctx.author)
        users = await Register.get_bank_data(Register)
        user = ctx.author

        upperSymbol = str(symbol).upper()
        secamount = float(getYfPrice(symbol))*int(stockamount)
        singleShare = users[str(user.id)][upperSymbol][list(users[str(user.id)][upperSymbol].keys())[-1]]["Price"] // users[str(user.id)][upperSymbol][list(users[str(user.id)][upperSymbol].keys())[-1]]["Amount"]
        if users[str(user.id)][upperSymbol]['TotalShares'] < int(stockamount):
            await ctx.send("Oops! You don't have enough invested money. Sell a lower share amount.")

        elif int(stockamount)==1:
            users[str(user.id)][upperSymbol]['TotalPrice'] -= singleShare
            users[str(user.id)][upperSymbol]['TotalShares']-=1
            users[str(user.id)]['Invested money'] -= singleShare
            users[str(user.id)]['Bank'] += secamount
            users[str(user.id)][upperSymbol][list(users[str(user.id)][upperSymbol].keys())[-1]]["Price"] -= singleShare
            users[str(user.id)][upperSymbol][list(users[str(user.id)][upperSymbol].keys())[-1]]["Amount"] -= 1
            if users[str(user.id)][upperSymbol][list(users[str(user.id)][upperSymbol].keys())[-1]]["Amount"] == 0 :
                del users[str(user.id)][upperSymbol][list(users[str(user.id)][upperSymbol].keys())[-1]]
            if users[str(user.id)][upperSymbol]['TotalShares'] == 0:
                del users[str(user.id)][upperSymbol]

            with open('mainbank.json', 'w') as f:
                json.dump(users, f)
            await ctx.send(f"You have succesfully withdrawn ${secamount} ({stockamount} share of {symbol.upper()} at {getYfPrice(symbol)})")

        else:
            tempstockamount=int(stockamount)
            while tempstockamount > 0:
                    users[str(user.id)]['Invested money'] -= singleShare
                    users[str(user.id)][upperSymbol]['TotalShares'] -= 1
                    users[str(user.id)][upperSymbol]['TotalPrice'] -= singleShare
                    users[str(user.id)][upperSymbol][list(users[str(user.id)][upperSymbol].keys())[-1]]["Price"] -= singleShare
                    users[str(user.id)][upperSymbol][list(users[str(user.id)][upperSymbol].keys())[-1]]["Amount"] -= 1
                    tempstockamount -= 1
                    if users[str(user.id)][upperSymbol][list(users[str(user.id)][upperSymbol].keys())[-1]]["Amount"] == 0 :
                        del users[str(user.id)][upperSymbol][list(users[str(user.id)][upperSymbol].keys())[-1]]
                    if users[str(user.id)][upperSymbol]['TotalShares'] == 0:
                        del users[str(user.id)][upperSymbol]

            users[str(user.id)]['Bank'] += secamount
            with open('mainbank.json', 'w') as f:
                json.dump(users, f)
            await ctx.send(f"You have succesfully withdrawn ${secamount} ({stockamount} shares of {symbol.upper()} at {getYfPrice(symbol)} each)")

def setup(client):
    client.add_cog(InvestBalance(client))
