"""
Currency retrieval class from CoinMarketCap and ECB
Tasas de cambio EUR/USD del BCE
Obtenidas de https://exchangeratesapi.io
HTTP requests con instrucciones de:
https://www.datacamp.com/community/tutorials/making-http-requests-in-python
"""
from datetime import date, datetime, timedelta
import json
import time
from Transaction import Currency
from RequestManager import RequestManager


class CurrencyRetriever:
    def __init__(self, start_date=datetime.now() - timedelta(days=1),
                 stop_date=datetime.now(),
                 base_currency=Currency.Euro,
                 target_currency=Currency.USDollar,
                 api_key_coinmarketcap = None):
        self.start_date = start_date
        self.stop_date = stop_date
        self.base_currency = base_currency
        self.target_currency = target_currency
        self._api_key_coinmarketcap_key = api_key_coinmarketcap
        self._current_rate, self._currency_rates = self.get_fiat_value(start_date, stop_date, base_currency, target_currency)

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        if value >= datetime.now():
            raise ValueError("Date must not be in the future or current date")
        else:
            self._start_date = value

    @property
    def stop_date(self):
        return self._stop_date

    @stop_date.setter
    def stop_date(self, value):
        if value >= datetime.now():
            raise ValueError("Date must not be in the future or current date")
        else:
            self._stop_date = value

    @property
    def base_currency(self):
        return self._base_currency

    @base_currency.setter
    def base_currency(self, value):
        if Currency.has_value(value):
            self._base_currency = value
        else:
            raise ValueError("Selected currency is not in currency list")

    @property
    def target_currency(self):
        return self._target_currency

    @target_currency.setter
    def target_currency(self, value):
        if Currency.has_value(value):
            self._target_currency = value
        else:
            raise ValueError("Selected currency is not in currency list")

    @property
    def api_key_coinmarketcap(self):
        return self._api_key_coinmarketcap

    def get_fiat_value(self, start_date=datetime.date(datetime.now() - timedelta(days=1)), stop_date=datetime.date(datetime.now()),
                       base_currency="EUR", target_currency="USD"):
        """
        FIAT currency converter from European Central Bank, through https://exchangeratesapi.io API
        Parameters
        ----------
        start_date : datetime
            starting date for currency retrieval (default value: yesterday)
        stop_date : datetime
            stop date for currency retrieval (default value = today)
        base_currency : string
            base currency to convert from (EUR, USD, ...)
        target_currency : string
            target currency to convert to (USD, JPY, GBP, ...)

        Returns
        -------
        current_rate : float
            Exchange rate for stop date
        currecy_rates : dictionary(date: string<YYYY-MM-DD>, float)
            Exchange rates for whole configured date span (bank holidays not included, no rate for those dates)

        Raises
        ------
        ValueError
            If base currency and target currency are the same
            If stop date is previous to start date
            If any of the dates is in the future (beyond today)
        ConnectionError
            If response from server is not 200
        """
        currency_rates = dict()
        if base_currency == target_currency:
            raise ValueError("Base currency and target currency can not be equal")
        elif start_date >= datetime.now():
            raise ValueError("Start date must not be in the future or current date")
        elif stop_date > datetime.now():
            raise ValueError("Start date must not be in the future or current date")
        elif start_date > stop_date:
            raise ValueError("Start date can not be greater than stop date")
        else:
            # EUR / fiat_currency exchange rate from BCE
            date_start = start_date.strftime('%Y-%m-%d')
            date_stop = stop_date.strftime('%Y-%m-%d')
            headers = {
                'Accepts': 'application/json',
                'Accept-Encoding': 'deflate, gzip',
            }
            request_address = f'https://api.exchangeratesapi.io/history?base={base_currency.value}&start_at={date_start}&end_at={date_stop}&symbols={target_currency.value}'
            manager_fiat = RequestManager(headers)
            data = manager_fiat.send_request(parameters={}, url=request_address)

            # Check that everything was OK
            if manager_fiat.status_code == 200:
                rates = data["rates"]
                for rate in rates:
                    currency_rates[rate] = round(rates[rate][target_currency.value],4)
                return currency_rates[stop_date.strftime('%Y-%m-%d')], currency_rates
            else:
                raise ConnectionError("Connection did not finish as expected. HTTP error code {}\nRequest was: {}".format(manager_fiat.status_code, request_address))

    def get_cypto_value(self, start_date=datetime.date(datetime.now() - timedelta(days=1)),
                       stop_date=datetime.date(datetime.now()),
                       currency="XBT"):
        """
        Crypto assets information gathered from CoinMarketCap
        Assets denomination can be found in ISO-4217 from IETF
        (https://tools.ietf.org/html/draft-stanish-x-iso4217-a3-01)
        Parameters
        ----------
        start_date : datetime
            starting date for currency retrieval (default value: yesterday)
        stop_date : datetime
            stop date for currency retrieval (default value = today)
        currency : string
            crypto currency to get information from (XBTC, XETH, ...)
        Returns
        -------
        data : JSON object
            data retreived from CoinMarketCap
        """
        url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
            'start':'1',
            'limit':'1',
            'convert':f'{base_currency}'
        }
        headers = {
            'Accepts': 'application/json',
            'Accept-Encoding': 'deflate, gzip'
        }

        if self.api_key_coinmarketcap:
            headers['X-CMC_PRO_API_KEY'] = self.api_key_coinmarketcap

        crypto_manager = RequestManager(headers)
        data = crypto_manager.send_request(parameters, url)
        return data
        #print(json.dumps(data, indent=4, sort_keys=True))
