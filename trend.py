from pandas import Series, ols
from pandas.io.data import DataReader
import datetime

LARGE_DAILY_GAIN = 0.001

def determine_trend(symbol, trade_date=datetime.datetime.now(), 
                    trend_length=20, trend_end_days_ago=1): 
    """
    returns a "trend score" derived from performing a linear 
    regression on the daily closing price of the stock 
    identified by symbol.  
    
    This score is on the following scale: 
    "Negative Trend" ----- "Positive Trend"
       -1.0 -----------0-----------1.0

    The score considers both the slope of the linear model and
    the "fit" (based on the r^2 output of the ols function)

    trade_date -- date used to determine the trend from
    symbol -- the stock symbol to determine trend for
    trend_length -- the number of days to derive trend for
    trend_end_days_ago -- the number of days prior to trend_date to determine
                          when to end the trend analysis
    """
    end_date = datetime.date.today() - datetime.timedelta(days=trend_end_days_ago)
    start_date = end_date - datetime.timedelta(days=trend_length)
    stock_df = DataReader(symbol, "yahoo", start=start_date, end=end_date)
    stock_df = stock_df.reset_index()
    result = ols(y=stock_df['Adj Close'], x=Series(stock_df.index))
    
    # This is the formula for the score without adjusting to fit within the
    # -1.0 - 1.0 scale.  Basically this takes the slope/starting price to get
    # the % change per day.  This is divided by a somewhat arbitrary value of 
    score = (result.beta['x']/result.beta['intercept'])/LARGE_DAILY_GAIN * result.r2

    # Now adjust the score to keep it in our trend range:
    if score > 1.0:
        return 1.0
    elif score < -1.0:
        return -1.0
    else:
        return score
        

