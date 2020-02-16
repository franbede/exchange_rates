"""
Tasas de cambio EUR/USD del BCE
Obtenidas de https://exchangeratesapi.io
HTTP requests con instrucciones de:
https://www.datacamp.com/community/tutorials/making-http-requests-in-python
"""
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import settings


# Start and stop dates for date filtering
start_date = '2018-12-28'
stop_date = '2018-12-29'

# FIAT currency to get pair (EUR / fiat_currency)
fiat_currency = 'USD'

# EUR / fiat_currency exchange rate from BCE
r =requests.get(f'https://api.exchangeratesapi.io/history?start_at={start_date}&end_at={stop_date}&symbols={fiat_currency}')
print(f'Code: {r.status_code}')
print(json.dumps(json.loads(r.text), indent=4, sort_keys=True))
print()


# Crypto exchange rates from CoinMarketCap
fiat_market_currency = 'USD'

url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'1',
  'convert':f'{fiat_market_currency}'
}
headers = {
  'Accepts': 'application/json',
  'Accept-Encoding': 'deflate, gzip',
  'X-CMC_PRO_API_KEY': settings.SANDBOX_API_KEY,
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(json.dumps(data, indent=4, sort_keys=True))
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)
