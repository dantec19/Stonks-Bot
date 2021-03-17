import bs4
from bs4 import BeautifulSoup
import requests
import sys
import os

def getYfPrice(symbol):
	yfScrape = bs4.BeautifulSoup(requests.get(f'https://finance.yahoo.com/quote/{symbol.upper()}').text,'lxml')
	rawPrice = yfScrape.find_all('div',{'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
	yfPrice = ''
	for i in rawPrice:
		if i != ',':
			yfPrice += i
	return yfPrice

def getYfName(symbol):
	yfScrape = bs4.BeautifulSoup(requests.get(f'https://finance.yahoo.com/quote/{symbol.upper()}').text,'lxml')
	rawName = yfScrape.find_all('div',{'class': 'D(ib) Mt(-5px) Mend(20px) Maw(56%)--tab768 Maw(52%) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)'})[0].find('h1').text
	yfName = ''
	for i in rawName:
		if i != '(':
			yfName += i
		else:
			break
	return yfName

	