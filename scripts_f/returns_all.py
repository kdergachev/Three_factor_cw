# -*- coding: utf-8 -*-

import pandas as pd
import datetime as dt
import os

# !!!!! set wd manually. Path up to (including) FF3_CW-master here !!!!!!!!!
FF3_in = r"C:\Users\kiril_000\Desktop\pr\FF3_better"
os.chdir(FF3_in + r"\data")
datad = FF3_in + r"\data\Prices_yfin"


dates = pd.date_range(start='1993-01-01', end='2019-12-01', freq="MS")
full = pd.DataFrame()

for i in range(1, 11):
    print(i)
    temp = pd.read_excel(datad + r"\Stock_prices_" 
                  + str(i) + ".xlsx")
    temp = temp.set_index("Date")
    temp = temp.loc[dates]
    temp = temp.dropna(1, "all")
    full = pd.concat([full, temp], axis=1)

full.to_excel("Full_prices.xlsx")

# Full_prices is written in ~\data
