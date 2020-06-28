# -*- coding: utf-8 -*-

import pandas as pd
import yfinance as yf
import os
yf.pdr_override()

# !!!!! set wd manually. Path up to (including) FF3_CW-master here !!!!!!!!!
FF3_in = r"C:\Users\kiril_000\Desktop\pr\FF3_better"
os.chdir(FF3_in + r"\data\Prices_yfin")

# Stocks.txt was created by simply combining all tickers in Bloobmerg_data
# the script is now lost
t = open(FF3_in + r"\scripts_f\Stocks.txt", "r")
stocks = t.read()
stocks = stocks.split("||")
t.close()
stocks = [st.replace("/", "-") for st in stocks]

inter = list(range(0, len(stocks), 1000))
inter.append(len(stocks))
for i in range(1, len(inter)):
    print(i, len(inter))
    data = yf.download(stocks[inter[i-1]:inter[i]], start="1993-01-01", 
                       end="2019-12-31", interval="1mo")["Adj Close"]
    name = "Stock_prices_" + str(i) + " .xlsx"
    data.to_excel(name)

# all files will be written int ~\data\Prices_yfin folder

