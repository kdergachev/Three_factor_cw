# -*- coding: utf-8 -*-

import requests as rq
from lxml import html
from bs4 import BeautifulSoup as bs
import datetime
import pandas as pd
import os

# !!!!! set wd manually. Path up to (including) FF3_CW-master here !!!!!!!!!
FF3_in = r"C:\Users\kiril_000\Desktop\pr\FF3_CW"
os.chdir(FF3_in + r"\data")

req = rq.get((r"https://www.treasury.gov/resource-center/data-chart-center"
              + r"/interest-rates/Pages/TextView.aspx?data=yieldAll"))

tree = bs(req.text, features="lxml")
tree = tree.find("table", {'class': 't-chart'})
startdate = 0
result = {}
for i in tree.findAll("tr"):
    temp = i.td
    if temp:
        date = temp.text
        dt = date[0:2]
        if int(dt) != startdate:
            print(date)
            date = datetime.datetime.strptime(date, "%m/%d/%y")
            """
            orders = [1, 1/2, 1/3, 1/6, 1/12]
            # result[date] = [0].text
            tags = i.findAll("td", {"scope": None})
            for j in range(len(tags)):
                print(tags[j].text)
                if "N/A" not in tags[j].text:
                    result[date] = (1 + float(tags[j].text)/100)**orders[j] - 1
                    print(result[date])
                    break
            #print("N/A" in result[date])
            startdate = int(dt)
            """
            tags = i.findAll("td", {"scope": None})
            for j in range(len(tags)):
                print(tags[j].text)
                if "N/A" not in tags[j].text:
                    result[date] = (float(tags[j].text))*30/360
                    print(result[date])
                    break
            #print("N/A" in result[date])
            startdate = int(dt)
    
result = pd.DataFrame.from_dict(result, orient="index", columns=["1mo_rf"])
# result = result/100
result.to_excel("Risk_free.xlsx")

# risk free written in ~\data folder
