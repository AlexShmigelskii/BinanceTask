import pandas as pd
import requests
import time
import matplotlib.pyplot as plt

# Список криптовалют для анализа
symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "DOGEUSDT", "XRPUSDT", "SOLUSDT", "DOTUSDT", "LUNAUSDT"]

# Параметры запроса
url = "https://api.binance.com/api/v3/klines"
interval = "1d"
start_time = int(time.time() - 86400 * 365 * 3) * 1000  # 3 года назад в миллисекундах
end_time = int(time.time()) * 1000  # текущее время в миллисекундах
limit = 1000  # максимальное количество запросов

# Получение данных за день для каждой криптовалюты
for symbol in symbols:
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_time,
        "endTime": end_time,
        "limit": limit
    }
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data, columns=["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignored"])
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")
    df["open"] = df["open"].astype(float)
    df["close"] = df["close"].astype(float)
    print(f"Symbol: {symbol}, high price: {df['high']}")

    # Сохранение данных в csv
    file_name = f"data/{symbol}_data.csv"
    df.to_csv(file_name, index=True)

    # Строим график
    df.set_index('open_time', inplace=True)
    df.high = pd.to_numeric(df.high)
    df['high'].plot()

    plt.title(f'{symbol}')
    plt.xlabel('Дата')
    plt.ylabel('Цена')

    plt.show()
