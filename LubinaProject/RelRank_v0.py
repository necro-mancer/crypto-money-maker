#imports

import os
data_repo = './Data/'
if not os.path.exists(data_repo):
	os.mkdir(data_repo);	

import sys, urllib
import json, csv
import objectpath
import itertools
from pycoingecko import CoinGeckoAPI
import datetime
import numpy as np
import re
from bs4 import BeautifulSoup
import time
import unicodedata

#func
def take(n, iterable):
	"Return first n items of the iterable as a list"
	return list(itertools.islice(iterable, n))

def print_words(words, n):
	"Return in n-column format"
	star = '{} '
	for i in range(n - 1):
		star = star + star
	columns, dangling = divmod(len(words), n)
	iterator = iter(words)
	columns = [take(columns + (dangling > i), iterator) for i in range(n)]
	for row in itertools.zip_longest(*columns, fillvalue=''):
		print(star.format(*row))

#__main__

Ntop = 500
NumDays = 100
BaseCurrency = 'BTC'

#get CMC list of N top coins

url_CMC = 'https://coinmarketcap.com/all/views/all/'
page = urllib.request.urlopen(url_CMC)
soup = BeautifulSoup(page, 'html.parser')
table = soup.find('table',{'id':'currencies-all'}).find('tbody')
CMC_id = []

for count, item in enumerate(table.select('tr'), start=1):
	ID = item.get('id').split('-')
	CMC_id.append('-'.join(ID[1:]))
	if count > Ntop:
		break

base = datetime.datetime.today()
ListOfDays = []
for day in range(1, NumDays):
	date = base - datetime.timedelta(days = day)
	day0 = str(date).split(' ')[0].split('-')
	ListOfDays.append('-'.join(reversed(day0)))


DataMain = CoinGeckoAPI()
Info = DataMain.get_coins_list()
#Info2 = DataMain.get_coins_markets(BaseCurrency.lower())
GeckoID = []

for item in Info:
	GeckoID.append(item['id'])

for date in ListOfDays:
	print('Date:' + date)
	Name = []; Symbol = []; MarketCap = []; Price = []; Rank = [];

	for item in CMC_id:
		if item in GeckoID:
			Coin = DataMain.get_coin_history_by_id(item,date)

			if 'market_data' in Coin:
				MarketCap.append(Coin['market_data']['market_cap'][BaseCurrency.lower()])
				Price.append(Coin['market_data']['current_price'][BaseCurrency.lower()])
				Symbol.append(Coin['symbol'].upper())
				Name.append(Coin['name'])
			else:
				MarketCap.append(0.0)
				Price.append(0.0)
				Symbol.append(Coin['symbol'].upper())
				Name.append(Coin['name'])
		else:
			continue
	
	MCapNeg = [-1.0 * item for item in MarketCap]
	Rank = list(np.argsort(np.argsort(MCapNeg)) + 1)
	data_array = zip(Name, Rank, Price, Symbol, MarketCap)

	with open((data_repo + date + '.csv'), 'w') as f:
		header = ['Name', 'Rank', 'Price', 'Symbol', 'MarketCap']
		writer = csv.DictWriter(f, fieldnames=header, delimiter=',')
		writer.writeheader()
		writer = csv.writer(f, delimiter=',')
		writer.writerows(data_array)

#print('\n\nAvailable calls:\n')
#print_words(dir(DataMain),1)
