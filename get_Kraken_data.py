"""
Tasas de cambio EUR/USD del BCE
Obtenidas de https://exchangeratesapi.io
HTTP requests con instrucciones de:
https://www.datacamp.com/community/tutorials/making-http-requests-in-python
"""
import json
import settings
from datetime import datetime
import time
from krakenex import API as KrakenAPI
from pprint import pprint as pp


# Global configuration for HTTP headers
headers = {
    'Accepts': 'application/json',
    'Accept-Encoding': 'deflate, gzip',
}

# get kraken current time using Krakenex
kraken_api = KrakenAPI(settings.KRAKEN_API_KEY, settings.KRAKEN_API_SECRET)
kraken_api.query_public('Time')
data = json.loads(kraken_api.response.text)

kraken_time = data['result']['unixtime']
system_time = time.time()
time_difference = abs(kraken_time - system_time)
MAX_ALLOWED_TIME_DELTA = 3

if time_difference > MAX_ALLOWED_TIME_DELTA:
    raise Exception('Time delta between Kraken and local system is higher than {} seconds (current: {})\nTo fix this, run "sudo ntpdate -vu time.apple.com" command in terminal'.format(
        MAX_ALLOWED_TIME_DELTA, round(time_difference, 5)))
print('Delta between Kraken and system is {} seconds'.format(
    round(time_difference, 5)))

# Crypto exchange rates from Kraken, using Krakenex
pair = 'XXBTZEUR'
parameters = {
    'pair': pair,
    'since': ''
}
kraken_api.query_public('Trades', data=parameters)
data = json.loads(kraken_api.response.text)
# print(json.dumps(data, indent=4, sort_keys=True))
price = data['result'][pair][-1][0]
print('Current Bitcoin price is {} €'.format(round(float(price), 2)))

# # Closed orders from Kraken, using Krakenex
# year = 2019
# sorted_trades_list = []
# for month in range(1,12):
#     start_date = datetime(year,month,1)
#     end_date = datetime(year,month+1,1) if month < 12 else datetime(year,12,31)
#     parameters = {
#         'start': round(start_date.timestamp(), 0),
#         'end': round(end_date.timestamp(), 0)
#     }
#     kraken_api.query_private('Ledgers', data=parameters)
#     data = json.loads(kraken_api.response.text)
#     trades = data['result']['ledger']

#     trades_by_datetime = dict()
#     # Create new dict with dates as indices
#     for index,transaction_id in enumerate(trades):
#         timestamp_info = float(trades[transaction_id]['time'])
#         timestamp_data = {
#             "timestamp": timestamp_info,
#             "transaction_id": transaction_id,
#             "aclass": trades[transaction_id]['aclass'],
#             "amount": trades[transaction_id]['amount'],
#             "asset": trades[transaction_id]['asset'],
#             "balance": trades[transaction_id]['balance'],
#             "fee": trades[transaction_id]['fee'],
#             "refid": trades[transaction_id]['refid'],
#             "type": trades[transaction_id]['type']
#         }
#         trades_by_datetime[timestamp_info] = timestamp_data
#         # pp(datetime.fromtimestamp(timestamp_info).strftime('%Y-%m-%d %H:%M:%S'))

#     # get ordered list of keys from dictionary
#     sorted_trades = sorted(trades_by_datetime)

#     # create list to store ordered items from dictionary
#     for ordered_trade in sorted_trades:
#         sorted_trades_list.append(trades_by_datetime[ordered_trade])
#     time.sleep(1)

# with open("result_ledger_ordered.json", 'w') as f:
#   f.write(json.dumps(sorted_trades_list, indent=4, sort_keys=True))

# for trade in sorted_trades_list:
#     pp(datetime.fromtimestamp(trade['timestamp']).strftime('%Y-%m-%d %H:%M:%S'))


# Query for get a given transaction from Kraken, using refid field
parameters = {
    'txid': 'TN5RVP-OO4VQ-557SOH'
}
kraken_api.query_private('QueryTrades', data=parameters)
pp(json.loads(kraken_api.response.text))

print('Script finished successfully.')
