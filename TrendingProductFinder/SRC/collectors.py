
from pytrends.request import TrendReq
import pandas as pd
import time

pytrends = TrendReq(hl='en-US', tz=330) 

def fetch_interest_over_time(keywords, timeframe='now 7-d', geo=''):
    """
    keywords: list of strings (max 5 per request with pytrends)
    timeframe: e.g. 'now 7-d', 'today 3-m', '2019-01-01 2025-11-23'
    geo: country code like 'IN' or '' for worldwide
    """
    pytrends.build_payload(keywords, cat=0, timeframe=timeframe, geo=geo, gprop='')
    df = pytrends.interest_over_time()
    if 'isPartial' in df.columns:
        df = df.drop(columns=['isPartial'])
    return df 

if __name__ == "__main__":
    kws = ['wireless earbuds', 'smart watch', 'portable charger']
    df = fetch_interest_over_time(kws, timeframe='now 7-d', geo='IN')
    print(df.tail())
