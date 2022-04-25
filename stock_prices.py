import requests
from requests.exceptions import HTTPError
import csv


def get_quote(symbol, endpoint='https://finnhub.io/api/v1/quote', key='c9iqrl2ad3iblk5af850'):
    try:
        headers = {'X-Finnhub-Token': key}
        res = requests.get(f'{endpoint}?symbol={symbol}', headers=headers)
        res.raise_for_status()
        return res.json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


def get_symbol(item):
    symbols = {
        'apple': 'APPL',
        'amazon': 'AMZN',
        'netflix': 'NFLX',
        'facebook': 'META',
        'google': 'GOOG'}
    return symbols.get(item)


def get_stocks(items):
    stocks = dict()
    for item in items:
        sym = get_symbol(item)
        stocks[item] = get_quote(sym)
    return stocks


def get_latest_prices(stocks):
    prices = dict()
    for key, val in stocks.items():
        prices[key] = val.get('c')
    return prices


def get_most_volatile(stocks):
    most_volatile = dict()

    def format_result(name, change, stock):
        sym = get_symbol(name)
        return {'stock_symbol': sym, 'percentage_change': change, 'current_price': stock.get('c'), 'last_close_price': stock.get('pc')}

    for key, stock in stocks.items():
        change = 0
        current_price = stock.get('c')
        last_close_price = stock['pc']

        try:
            value = ((current_price - last_close_price) /
                     abs(last_close_price)) * 100
            change = round(value, 2)
        except ZeroDivisionError:
            print(f'\nstarting value must be non-zero, ...skiping {key}')
            continue

        if len(most_volatile) == 0:
            most_volatile = (key, change, stock)
        else:
            if change > most_volatile[1]:
                most_volatile = (key, change, stock)

    return format_result(*most_volatile) if len(most_volatile) == 3 else None


def dic_to_csv(items, filename='most_volatile_stock.csv'):
    try:
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=items.keys())
            writer.writeheader()
            writer.writerow(items)
    except IOError:
        print('error writing to csv file')


stocks = get_stocks(['apple',  'amazon', 'netflix', 'facebook', 'google'])

# Get latest price for Apple, Amazon, Netflix, Facebook, Google
latest_prices = get_latest_prices(stocks)
print(f'latest stock prices: {latest_prices}')


# Between Apple, Amazon, Netflix, Facebook, Google: find the stock
# that moved the most percentage points from yesterday.
most_volatile_stock = get_most_volatile(stocks)
print(f"\n most volatile stock: {most_volatile_stock}")

# save to csv
dic_to_csv(most_volatile_stock)
