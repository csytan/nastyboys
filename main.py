import bs4
import urllib



def yahoo_finance_symbols(url):
	html = urllib.urlopen(url).read()
	soup = bs4.BeautifulSoup(html)
	movers = soup.find('div', attrs={'id':'yfitp'})
	stocks = movers.find_all('td', class_='first')
	return [stock.string for stock in stocks]

gainers = 'http://finance.yahoo.com/gainers?e=us'
losers = 'http://finance.yahoo.com/losers?e=us'


print yahoo_finance_symbols(gainers)
print yahoo_finance_symbols(losers)
