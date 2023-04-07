import csv
import datetime
import requests

import config as cfg

url = 'https://api.binance.com/api/v3/klines'
headers = {'X-MBX-APIKEY': cfg.API_KEY}

# list of symbols
symbols = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT']


def get_klines():

    for symbol in symbols:

        data = []

        params = {
            'symbol': symbol,
            'interval': '1h',  # интервал свечей (1 час)
            'limit': 24,  # количество свечей (24 часа)
        }

        # GET request for every symbol
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            result = response.json()
            for item in result:
                data.append([
                    datetime.datetime.fromtimestamp(item[0] / 1000.0),  # время открытия свечи
                    item[1],  # цена открытия свечи
                    item[2],  # цена закрытия свечи
                    item[3],  # наивысшая цена за период свечи
                    item[4],  # наименьшая цена за период свечи
                    item[5]  # объем торгов за период свечи
                ])

            with open(f'crypto_{symbol}_klines.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Open Time', 'Open', 'Close', 'High', 'Low', 'Volume'])
                for item in data:
                    writer.writerow(item)

        else:
            print(f"Failed to get data for symbol {symbol}\n"
                  f"{response.status_code}")

    print('Data saved to crypto_klines.csv')
