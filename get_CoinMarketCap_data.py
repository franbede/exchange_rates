from datetime import date, datetime, timedelta
import json
import time
from Transaction import Currency
from RequestManager import RequestManager


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

print(get_fiat_value("26-12-2018", "27-12-2018"))