import discord
from discord.ext import commands
from discord.utils import get
import bs4
from bs4 import BeautifulSoup
import requests
from bot.helper_funcs import getYfPrice, getYfName

class PriceCheck(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Returns current price of stock
    @commands.command(aliases=['p'])
    async def price(self, ctx, symbol, time = '1d'):

        # Scrape graph from BigCharts according to time range specified
        if time == '1d':
            bcReq = requests.get(f'https://bigcharts.marketwatch.com/advchart/frames/frames.asp?show=&insttype=Stock&symb={symbol.upper()}&time=1&startdate=1%2F4%2F1999&enddate=2%2F3%2F2021&freq=9&compidx=aaaaa%3A0&comptemptext=&comp=none&ma=0&maval=9&uf=0&lf=1&lf2=0&lf3=0&type=8&style=320&size=2&x=36&y=13&timeFrameToggle=false&compareToToggle=false&indicatorsToggle=false&chartStyleToggle=false&state=9')
        elif time == '2d':
            bcReq = requests.get(f'https://bigcharts.marketwatch.com/advchart/frames/frames.asp?show=&insttype=Stock&symb={symbol.upper()}&time=2&startdate=1%2F4%2F1999&enddate=2%2F3%2F2021&freq=9&compidx=aaaaa%3A0&comptemptext=&comp=none&ma=0&maval=9&uf=0&lf=1&lf2=0&lf3=0&type=8&style=320&size=2&x=33&y=4&timeFrameToggle=false&compareToToggle=false&indicatorsToggle=false&chartStyleToggle=false&state=9')
        elif time == '5d':
            bcReq = requests.get(f'https://bigcharts.marketwatch.com/advchart/frames/frames.asp?show=&insttype=Stock&symb={symbol.upper()}&time=3&startdate=1%2F4%2F1999&enddate=2%2F3%2F2021&freq=6&compidx=aaaaa%3A0&comptemptext=&comp=none&ma=0&maval=9&uf=0&lf=1&lf2=0&lf3=0&type=8&style=320&size=2&x=46&y=13&timeFrameToggle=false&compareToToggle=false&indicatorsToggle=false&chartStyleToggle=false&state=9')
        elif time == '10d':
            bcReq = requests.get(f'https://bigcharts.marketwatch.com/advchart/frames/frames.asp?show=&insttype=Stock&symb={symbol.upper()}&time=18&startdate=1%2F4%2F1999&enddate=2%2F3%2F2021&freq=6&compidx=aaaaa%3A0&comptemptext=&comp=none&ma=0&maval=9&uf=0&lf=1&lf2=0&lf3=0&type=8&style=320&size=2&x=52&y=8&timeFrameToggle=false&compareToToggle=false&indicatorsToggle=false&chartStyleToggle=false&state=9')
        elif time == '1m' or time == '30d' or time == '31d':
            bcReq = requests.get(f'https://bigcharts.marketwatch.com/advchart/frames/frames.asp?show=&insttype=Stock&symb={symbol.upper()}&x=37&y=21&time=4&startdate=1%2F4%2F1999&enddate=2%2F3%2F2021&freq=1&compidx=aaaaa%3A0&comptemptext=&comp=none&ma=0&maval=9&uf=0&lf=1&lf2=0&lf3=0&type=8&style=320&size=2&timeFrameToggle=false&compareToToggle=false&indicatorsToggle=false&chartStyleToggle=false&state=9')
        elif time == '2m' or time == '60d' or time == '61d' or time == '62d':
            bcReq = requests.get(f'https://bigcharts.marketwatch.com/advchart/frames/frames.asp?show=&insttype=Stock&symb={symbol.upper()}&time=5&startdate=1%2F4%2F1999&enddate=2%2F3%2F2021&freq=1&compidx=aaaaa%3A0&comptemptext=&comp=none&ma=0&maval=9&uf=0&lf=1&lf2=0&lf3=0&type=8&style=320&size=2&x=41&y=1&timeFrameToggle=false&compareToToggle=false&indicatorsToggle=false&chartStyleToggle=false&state=9')
        elif time == '3m' or time == '90d':
            bcReq = requests.get(f'https://bigcharts.marketwatch.com/advchart/frames/frames.asp?show=&insttype=Stock&symb={symbol.upper()}&time=6&startdate=1%2F4%2F1999&enddate=2%2F3%2F2021&freq=1&compidx=aaaaa%3A0&comptemptext=&comp=none&ma=0&maval=9&uf=0&lf=1&lf2=0&lf3=0&type=8&style=320&size=2&x=38&y=19&timeFrameToggle=false&compareToToggle=false&indicatorsToggle=false&chartStyleToggle=false&state=9')
        elif time == '6m':
            bcReq = requests.get(f'https://bigcharts.marketwatch.com/advchart/frames/frames.asp?show=&insttype=Stock&symb={symbol.upper()}&x=51&y=7&time=7&startdate=1%2F4%2F1999&enddate=2%2F3%2F2021&freq=1&compidx=aaaaa%3A0&comptemptext=&comp=none&ma=0&maval=9&uf=0&lf=1&lf2=0&lf3=0&type=8&style=320&size=2&timeFrameToggle=false&compareToToggle=false&indicatorsToggle=false&chartStyleToggle=false&state=9')
        elif time == '1y' or time == '12m' or time == '365d':
            bcReq = requests.get(f'https://bigcharts.marketwatch.com/advchart/frames/frames.asp?show=&insttype=Stock&symb={symbol.upper()}&x=66&y=19&time=8&startdate=1%2F4%2F1999&enddate=2%2F3%2F2021&freq=1&compidx=aaaaa%3A0&comptemptext=&comp=none&ma=0&maval=9&uf=0&lf=1&lf2=0&lf3=0&type=8&style=320&size=2&timeFrameToggle=false&compareToToggle=false&indicatorsToggle=false&chartStyleToggle=false&state=9')
        elif time == 'max':
            bcReq = requests.get(f'https://bigcharts.marketwatch.com/advchart/frames/frames.asp?show=&insttype=Stock&symb={symbol.upper()}&time=20&startdate=1%2F4%2F1999&enddate=2%2F3%2F2021&freq=2&compidx=aaaaa%3A0&comptemptext=&comp=none&ma=0&maval=9&uf=0&lf=1&lf2=0&lf3=0&type=8&style=320&size=2&x=41&y=10&timeFrameToggle=false&compareToToggle=false&indicatorsToggle=false&chartStyleToggle=false&state=9')
        else:
            await ctx.send('$'+ str(getYfPrice(symbol)) + '\n' + 'Sorry, we were unable to make a graph on this stock for the time range specified')
        bcSoup = bs4.BeautifulSoup(bcReq.text,'lxml')
        bcScrapedImage = str(bcSoup.find('div', {'class': 'customchart acenter bedonkbottom'}).find('img')['src'])

        # Send as embed: Name of stock, Price, Graph as image and Credits
        embed=discord.Embed(title=f'{symbol.upper()} - ${getYfPrice(symbol)}', color=0x00ff33, description=f'{getYfName(symbol)}- Chart:  {time}')
        embed.set_image(url=bcScrapedImage)
        embed.set_footer(text= 'Bot created by @DantePicante#9639 and @tato#2767')
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(PriceCheck(client))
