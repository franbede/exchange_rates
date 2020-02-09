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

# EUR / USD exchange rate from BCE
r =requests.get('https://api.exchangeratesapi.io/history?start_at=2018-12-28&end_at=2018-12-29&symbols=USD')
print(f'Code: {r.status_code}')
print(json.dumps(json.loads(r.text), indent=4, sort_keys=True))
print()


# Crypto exchange rates from CoinMarketCap
url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'1',
  'convert':'USD'
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