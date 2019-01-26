#main
#run CLI with python2 (python3 lacks urllib2 package)

import sys
#if sys.version_info[0] > 2:
#	raise Exception("Python 3 not supported; run script with python2 instead")

import os
data_repo = './Data2/'
if not os.path.exists(data_repo):
	os.mkdir(data_repo);	

#lib
import urllib
import re
from bs4 import BeautifulSoup
import time
import unicodedata
import csv

#func

url = 'https://coinmarketcap.com/historical/'

page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')

history = soup.find_all("a", href=re.compile('historical'))
history = [str(s) for s in history]
dates = [];

for s in history:
	date = s[s.find('historical/') + len('historical/'):s.find('/">')]
	if date != '':
		dates.append(date)
	else:
		continue

#dates.reverse()

for date in dates:
	url_date = 'https://coinmarketcap.com/historical/' + date + '/'
	print('Importing data on :' + date[0:4] + '-' + date[4:6] + '-' + date[6:8])
	page_date = urllib.request.urlopen(url_date)
	soup_date = BeautifulSoup(page_date, 'html.parser')
	table = soup_date.find('table',{'id':'currencies-all'}).find('tbody')
	rank = []; names = []; symbol = []; price = []

	for count, item in enumerate(table.select('tr'), start=1):
		names.append((item.find('td',{'class':'no-wrap currency-name'}).get('data-sort')).encode('ascii','ignore'))
		rank.append(str(count))	
		symbol.append((item.find_all("td", {"class": "text-left col-symbol"})[0].string).encode('ascii','ignore'))
		price.append((item.find('td',{'class':'no-wrap text-right'}).get('data-sort')).encode('ascii','ignore'))

	data_array = zip(names, rank, price, symbol)

	with open((data_repo + date + '.csv'), 'w') as f:
		header = ['Name', 'Rank', 'Price', 'Symbol']
		writer = csv.DictWriter(f, fieldnames=header, delimiter=',')
		writer.writeheader()
		writer = csv.writer(f, delimiter=',')
		writer.writerows(data_array)




			
