!!!! Non stationary series were run in empirical tests so conclusions should be reviewed !!!!
# Tests of 3 factor model coursework
The model is the one based on K. French & E. Fama (1993) work "Common risk factors in the returns on
stocks and bonds"
The repo is mostly for storing results of practical part of running regressions on portfolio returns and getting said returns from data initially collected
## Initial data
The project was started with yearly snapshots (June 31) of all tickers on NYSE obtained from Bloomberg terminal.
Then all other intermediate tables were produced and used to get result*.xlsx tables
## Process of getting the end result
### Started with
.  
+-- data  
|   +-- Bloomberg_data  
|   |   +-- 1993.xlsx  
|   |   +-- 1994.xlsx  
|   |   +-- ...  
|   |   +-- 2019.xlsx  
|   +-- Prices_yfin  
|   +-- results  
+-- scripts_f  
|   +-- <all the .py scripts>  
+-- texts        %% texts is not relevant for coding part  

All else is built up on the initial tables.
Order of scripts is st.py, returns_all.py, scrape_FED.py, Main.py
## Important concern!!
The data on prices is obtained from Yahoo finance based on Bloomberg tickers and thus overall tests are far from perfect as tickers may not coinside, some of them are omitted and so on, but getting all monthly prices from Bloomberg seemed too greedy. Though the data is far from perfect the results seem to imply that the size of dataset somewhat mitigated the incorrect tickers downloaded. (and some were excluded in Main.py as a couple of them were incredibly terrible)
