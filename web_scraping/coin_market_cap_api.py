import requests
import pandas as pd
import pprint as pp
import datetime as dt

coin = "SYS"
url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={coin}&market=USD&apikey=O3N4GIA6JBVS83QG'
api_key = 'O3N4GIA6JBVS83QG'

def request(url):
    r = requests.get(url)
    return r.json()

data = request(url)['Time Series (Digital Currency Daily)']

def parsing(response):
    result = []
    for item, value in response.items():
        day = {
            'coin': f'{coin}',
            'date': item,
            'open': response[item]['1b. open (USD)'],
            'high': response[item]['2b. high (USD)'],
            'low': response[item]['3b. low (USD)'],
            'close': response[item]['4b. close (USD)'],
            'volume': response[item]['5. volume']
        }
        result.append(day)
    return result

df_precos = pd.DataFrame(parsing(data)).set_index('date').sort_values('date')
df_precos.index = pd.to_datetime(df_precos.index)
df_precos[['open', 'high', 'low', 'close', 'volume']] = df_precos[['open', 'high', 'low', 'close', 'volume']].apply(pd.to_numeric)


# dataframe.set_index('date')
# dataframe.reset_index()
# dataframe.sort_index(level = ['', ''], ascending = [True, False])
# dataframe.isna().any()
# dataframe.fillna(0)


