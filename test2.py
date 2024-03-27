import requests
import pandas as pd


url = "https://www.moneycontrol.com/stocks/marketinfo/dividends_declared/"
data = {"sel_year": "2018", "x": "1", "y": "1"}

all_dfs = []
for data["sel_year"] in range(2018, 2022 + 1):
    df = pd.read_html(requests.post(url, data=data).text)[1]
    df["Year"] = data["sel_year"]
    all_dfs.append(df)

df_out = pd.concat(all_dfs)
print(df_out.head(10))