import bs4
import datetime
import urllib



class NastyBoys ():
    """Implementation of the #NastyBoys trading strategy,
    as devised 11/12/2013"""

    def __init__(self, candidates=100, trade_date=None):
        if trade_date is None:
            self["candidates"] = candidates
            self["trade_date"] = datetime.datetime.now()

    def get_extreme_performers (best=True):
        """Return a list of self.candidates stock symbols
        which performed the best (best=True) or worst (best=False)
        for self.trade_date.

        Implementation: Chris Tan
        """
        gainers = 'http://finance.yahoo.com/gainers?e=us'
        losers = 'http://finance.yahoo.com/losers?e=us'
        url = gainers if best else losers
        html = urllib.urlopen(url).read()
        soup = bs4.BeautifulSoup(html)
        movers = soup.find('div', attrs={'id':'yfitp'})
        stocks = movers.find_all('td', class_='first')
        return [stock.string for stock in stocks]

    def get_latest_filing (symbol, filing_type='10-Q'):
        """Return the text of the latest public filing
        for the given symbol and filing type.

        Implementation: Denis Papathanasiou
        """

        return ""

    def get_sentiment (filing_text):
        """Run a sentiment analysis on the text of the
        filing document, returning a float in the range
        -1.0 (bad) to 1.0 (good)

        Implementation: Myf Ma & Zaiming Yao
        """

        return 0.0

    def get_performance_trend (symbol, from_date):
        """Determine the performance trend for the stock
        symbol from the given date, to self.trade_date,
        return a float in the range -1.0 (perfect negative
        trend) to 1.0 (perfect positive trend).

        Implementation: Chris Natali
        """

        return 0.0

    def matches_bounce_expectation (symbol, sentiment, trend, best=True):
        """Rule for determining whether or not this symbol
        should be bought (best=False) or sold short (best=True)
        based on its sentiment and performance trend scores."""

        result = False

        if best:
            if trend < 0.0 and sentiment < 0.0:
                result = True
        else:
            if trend > 0.0 and sentiment > 0.0:
                result = True

        return result

    def test_candidate_symbols (best=True):
        """Get a list of candidate symbols, based on their being
        either the best performers (best=True) or the worst (best=False),
        and decide whether or not to trade them, using their sentiment
        and trend scores."""

        trade_symbols = []
        for sym in self.get_extreme_performers(best):
            if sym not in trade_symbols:
                sentiment = self.get_sentiment(self.get_latest_filing(sym))
                trend = self.get_performance_trend(sym, from_date) #how far back???
                if self.matches_bounce_expectation(sym, sentiment, trend, best):
                    trade_symbols.append(sym)

        return trade_symbols

    def run ():
        """Run the full algorithm and produce two lists:
        symbols to buy, in the expectation they will rise
        symbols to sell short, in the expectation they will fall."""

        to_buy  = self.test_candidate_symbols(best=False)
        to_sell = self.test_candidate_symbols(best=True)

        if len(to_buy) > 0:
            print "*** BUY:"
            for sym in to_buy:
                print '\t', sym

        if len(to_sell) > 0:
            print "*** SELL SHORT:"
            for sym in to_sell:
                print '\t', sym


                