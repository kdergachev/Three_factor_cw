# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os
import datetime as dt
import math
import statsmodels.api as sm

# !!!!! put path to FF3_CW-master (including itself) in FF3_in !!!!! 
# then data will be properly written/taken from folders
FF3_in = r"C:\Users\kiril_000\Desktop\pr\FF3_CW"
os.chdir(FF3_in + r"\data\results")

def to_num(value):
    
    """Input a value, returns a float interpreting letters M, T, k, B.
    Used in .apply"""
    
    # a neat if ladder
    
    if pd.isnull(value):
        return np.nan
    elif isinstance(value, int):
        return value
    elif isinstance(value, float):
        return value
    elif value.endswith("B"):
        return float(value[:-1]) * 10**9
    elif value.endswith("M"):
        return float(value[:-1]) * 10**6
    elif value.endswith("k"):
        return float(value[:-1]) * 10**3
    elif value.endswith("T"):
        return float(value[:-1]) * 10**12
    else:
        return float(value)
    


def get_rf(rfdf, year):
    
    """Input a data frame with risk free rates and year for which the rates 
    are required.
    The output is dataframe with risk free returns for july-dec of given year
    and jan-june of the next one. datetime index is saved so use .values to 
    subtract from monthly returns as dates may not coinside"""
    
    res = pd.DataFrame()
    tmp = rfdf[rfdf.index.year == year]
    tmp = tmp[tmp.index.month.isin([7,8,9,10,11,12])]
    res = pd.concat([res, tmp])
    tmp = rfdf[rfdf.index.year == (year + 1)]
    tmp = tmp[tmp.index.month.isin([1, 2, 3, 4, 5, 6])]
    res = pd.concat([res, tmp])
    return res


def get_weights(df, stlst=None):
    
    """Input dataframe with "Market Cap" column and stocks to use. Returns 
    weights for value-weighted portfolio. If stlist is None all stocks are 
    used in the portfolio"""
    
    if stlst is not None:
        df = df.loc[stlst]
    total = df["Market Cap"].sum()
    df["Weights"] = df["Market Cap"]/total
    df = df["Weights"]
    #df.index = df.index.str.split(" ").str[0]
    return df

def get_m_returns(df, weights, dateused):
    
    """Input price dataframe, weight dataframe and date for which the returns 
    are to be calculated. Outputs a returns for specified portfolio 
    dateframe"""
    
    dateused = int(dateused)
    start = dt.datetime(dateused, 7, 1)
    end = dt.datetime(dateused + 1, 7, 1)
    dates = pd.date_range(start, end, freq="MS")
    weights = weights[weights.index.isin(df.columns)]
    df = df.loc[dates, weights.index] # Should get July t - July (t+1) prices
    df = df.mul(weights, axis=1)
    Total = df.sum(axis=1)
    Total = Total.pct_change()
    return Total[1:]



def split_to_portf(df, by, bins):
    
    """Input dataframe with tickers and some columns, the function splits 
    tickers by the by column into bins specified with bins dictionary: key 
    is the name of the bin, value is len 2 tuple with proportion to be 
    allocated. Returns dictionary with named stock sets"""
    
    df = df.sort_values(by=by, ascending=False)
    total = len(df.index)
    bins = {k:(v[0]*total, v[1]*total) for k,v in bins.items()}
    bins = {k:df.index[math.ceil(v[0]):math.ceil(v[1])] 
            for k,v in bins.items()}
    return bins


def combine_portfolios(dict1, dict2):
    
    """Input 2 dictionaries as ones created split_to_portf(). Returns all
    intersections of said dictionaries. As a dictioinary with keys of type
    "<key1>|<key2>" """
    
    result = {}
    for k1, v1 in dict1.items():
        for k2, v2 in dict2.items():
            result[k1 + "|" + k2] = v1[v1.isin(v2)]
    return result



def returns_from_dict(dict1, df, price, year, RF=None):
    
    
    retd = {}
    for k in dict1.keys():
        wghts = get_weights(df, dict1[k])
        rets = get_m_returns(price, wghts, year)
        if RF is not None:
            rets = rets - RF
        retd[k] = rets
    return pd.DataFrame(retd)


def equal_splits(*args):
    
    """Supply arrays with names for splits, get list of dictionaries with
    names as keys and tuples of splits to be used in split_to_portf()"""
    
    out = []
    for i in args:
        temp = {}
        prop = 1/len(i)
        prop = [u*prop for u in range(len(i))]
        prop.append(1)
        for j in range(len(i)):
            temp[i[j]] = (prop[j], prop[j+1])
        out.append(temp)
    return out




#equal_splits(["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"], 
#             ["BE1", "BE2", "BE3", "BE4", "BE5", "BE6", "BE7", "BE8"])


# create splits beforehand    
Sz, BM  = equal_splits(["S1", "S2", "S3", "S4", "S5"], 
                       ["BE1", "BE2", "BE3", "BE4", "BE5"])


dimen = "5x5"
outname1 = "results" + dimen + ".xlsx"
outname2 = "returns" + dimen + ".xlsx"
# #of size subsets x #of BE/ME subsets


datad = FF3_in + r"\data"
Bbg = datad + r"\Bloomberg_data"

prices = pd.read_excel(datad + r"\Full_prices.xlsx")
prices = prices.set_index("Date")
# drop stocks for which monthly returns were more than 70% in absolute values
drp = prices.pct_change()
drp = drp.iloc[1:, :]
drp = (abs(drp) < 70).all(axis=0)
drp = drp[drp].index
prices = prices.loc[:, drp]

rf = pd.read_excel(datad + r"\Risk_free.xlsx", index_col=0)
lst = os.listdir(Bbg)


prepdta = pd.DataFrame()
for i in lst[:-1]:
    print(i)
    storage = pd.DataFrame()
    year = int(i.split(".")[0])
    
    # prepare data: add nan, turn B, T, M, k into float
    curdta = pd.read_excel(Bbg + "\\" + i)
    curdta = curdta.set_index("Ticker")
    curdta = curdta.replace("--", np.nan)
    curdta["Market Cap"] = curdta["Market Cap"].apply(to_num)
    curdta["Tot CE LF"] = curdta["Tot CE LF"].apply(to_num)
    curdta.index = curdta.index.str.split(" ").str[0]
        # remove nan
    curdta = curdta.dropna(0, "any", subset=["Market Cap", "Tot CE LF"])
    curdta["BE/ME"] = curdta["Tot CE LF"]/curdta["Market Cap"]
    
    # get risk free for the year
    rfree = get_rf(rf, year)["1mo_rf"].values
    # Get market returns
    mrktw = get_weights(curdta)
    mrktret = get_m_returns(prices, mrktw, year)
    mrktret = mrktret - rfree
    # get BE, ME portfolios
    tempdf = curdta[curdta["Tot CE LF"] >= 0]
    # Size slices
    
    cutSB = split_to_portf(tempdf, "Market Cap", {"B":(0, 0.5), 
                                                  "S":(0.5, 1)})
    
    cutS = split_to_portf(tempdf, "Market Cap", Sz)
    
    cutH = split_to_portf(tempdf, "BE/ME", {"H":(0, 0.3), 
                                            "M":(0.3, 0.7),
                                            "L":(0.7, 1)})
    
    cutBE = split_to_portf(tempdf, "BE/ME", BM)
    
    
    indep = combine_portfolios(cutH, cutSB)
    indep = returns_from_dict(indep, tempdf, prices, year)
    SMB = ((indep["H|S"] + indep["M|S"] + indep["L|S"])/3) 
    - (indep["H|B"] + indep["M|B"] + indep["L|B"])/3
    
    HML = (((indep["H|S"] + indep["H|B"])/2) - (indep["L|S"] 
                                                + indep["L|B"])/2)
    
    storage = pd.concat({"mrkt":mrktret, "HML":HML, "SMB":SMB}, axis =1)
    
    dpnd = combine_portfolios(cutBE, cutS)
    dpnd = returns_from_dict(dpnd, tempdf, prices, year, rfree)
    
    
    storage = pd.concat([storage, dpnd], axis=1)
    prepdta = pd.concat([prepdta, storage])


#prepdta.to_excel(outname2)

regr = prepdta.columns[3:]
ex = prepdta[["mrkt", "HML", "SMB"]]
ex = sm.add_constant(ex)
indx = [["coef", "p-value"], 
        ["const", "mrkt", "HML", "SMB"], 
        list(BM.keys())]
indx = pd.MultiIndex.from_product(indx)
results = pd.DataFrame(columns=indx, index=list(Sz.keys()))
indx2 = [["fits"], 
         ["R2", "F-stat"], 
         list(BM.keys())]
indx2 = pd.MultiIndex.from_product(indx2)
fits = pd.DataFrame(columns=indx2, index=list(Sz.keys()))


for i in regr:
    #print(i)
    names = i.split("|")
    rgrs = sm.OLS(prepdta[i], ex, missing="drop")
    rgrs = rgrs.fit()
    print(sm.stats.diagnostic.acorr_breusch_godfrey(rgrs, 5)[1])
    for j in rgrs.params.index:
        cf = rgrs.params[j]
        results.loc[names[1], ("coef", j, names[0])] = float(cf)
        cf = rgrs.pvalues[j]
        results.loc[names[1], ("p-value", j, names[0])] = float(cf)
    fits.loc[names[1], ("fits", "R2", names[0])] = float(rgrs.rsquared)
    fits.loc[names[1], ("fits", "F-stat", names[0])] = float(rgrs.fvalue)
    #print(rgrs.fvalue)
    #results = results.dropna(1, "all")
    #print(rgrs.pvalues)
    #print(rgrs.params)

results = pd.concat((results, fits), axis=1)

results.to_latex("res.txt")
results.to_excel(outname1)



