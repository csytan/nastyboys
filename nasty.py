
"""
This runs the #NastyBoys trading algorithm from a command line interface

Use at your own risk!

"""

import bs4
import datetime
import urllib
import sys

from get_filings import get_latest_document
from trend import determine_trend

DEFAULT_TREND_LENGTH = 20

def get_extreme_performers (best=True):
    """Return a list of candidates stock symbols which
    performed the best (best=True) or worst (best=False)
    for the current trade date.

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
    """Return a tuple: (the filing date as a string in
    'YYYY-MM-DD' format, text of the latest public filing)
    corresponding to the given symbol and filing type, or
    (None, None) if the symbol is invalid or no such filing
    is available, etc.
    """

    return get_latest_document (symbol.upper(), filing_type)

def get_sentiment (filing_text):
    """Run a sentiment analysis on the text of the
    filing document, returning a float in the range
    -1.0 (bad) to 1.0 (good)

    Implementation: Myf Ma & Zaiming Yao
    """

    return 0.0

def get_performance_trend (symbol, trade_date=datetime.datetime.now()):
    """Determine the performance trend for the stock
    symbol from the given date, to trade_date, return
    a float in the range -1.0 (perfect negative trend)
    to 1.0 (perfect positive trend).

    Implementation: Chris Natali
    """
    return determine_trend(symbol, trade_date, DEFAULT_TREND_LENGTH, 
            trend_end_days_ago=1)

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


def test_candidate_symbols (best=True, use_sentiment=True):
    """Get a list of candidate symbols, based on their being
    either the best performers (best=True) or the worst (best=False),
    and decide whether or not to trade them, using their sentiment
    and trend scores."""

    trade_symbols = []
    for sym in get_extreme_performers(best):
        if sym not in trade_symbols:
            try:
                trend = get_performance_trend(sym)

                if use_sentiment:
                    filing_date, filing_text = get_latest_filing(sym)
                    sentiment = get_sentiment(filing_text)
                else:
                    # match the sentiment to the trend
                    # (so we don't have to rewrite the
                    # matches_bounce_expectation() fn)
                    sentiment = trend

                if matches_bounce_expectation(sym, sentiment, trend, best):
                    trade_symbols.append(sym)

            except Exception, e:
                sys.stderr.write("Exception processing symbol %s, Exception: %s\n" % (sym, e))

    return trade_symbols

                
def main():
    """Command-line entry point: provide the root folder of the csv log
    files and this module will parse + load all the csv files it finds
    under it"""

    if len(sys.argv[1:]) != 1:
        print ' '.join(["\nUsage:\n\tpython",
                        sys.argv[0],
                        "[with-sentiment-analysis (boolean)\n\n"])
    else:
        # Run the full algorithm and produce two lists:
        # symbols to buy, in the expectation they will rise
        # symbols to sell short, in the expectation they will fall.

        use_sentiment = (sys.argv[1].upper()[0] == 'T')

        to_buy  = test_candidate_symbols(best=False, use_sentiment=use_sentiment)
        to_sell = test_candidate_symbols(best=True,  use_sentiment=use_sentiment)

        if len(to_buy) > 0:
            print "*** BUY:"
            for sym in to_buy:
                print '\t', sym

        if len(to_sell) > 0:
            print "*** SELL SHORT:"
            for sym in to_sell:
                print '\t', sym

if __name__ == "__main__":
    main()
