import csv
import requests

import config as cfg

url = 'https://api.binance.com/api/v3/ticker/24hr'
headers = {'X-MBX-APIKEY': cfg.API_KEY}

# list of symbols
symbols = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT']


def get_day_stat():
    data = []

    # GET request for every symbol
    for symbol in symbols:
        params = {'symbol': symbol}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            result = response.json()
            data.append([
                result['symbol'],
                result['lastPrice'],
                result['priceChangePercent'],
                result['highPrice'],
                result['lowPrice'],
                result['volume']
            ])
        else:
            print(f"Failed to get data for symbol {symbol}")

    # save to CSV
    with open('crypto_prices_24hr.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Symbol', 'Last Price', 'Price Change (%)', 'High', 'Low', 'Volume'])
        writer.writerows(data)

    print('Data saved to crypto_prices.csv')
