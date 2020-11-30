import unittest
from Transaction import Currency
from datetime import datetime, timedelta
from CurrencyRetriever import CurrencyRetriever
import settings


class TestCurrencyRetriever(unittest.TestCase):
    """Check network information retrieval from CoinMarketCap and ECB"""
    def setUp(self):
        self.currency_retriever = CurrencyRetriever(start_date=datetime(2020,4,8),
                 stop_date = datetime(2020,4,9),
                 base_currency=Currency.Euro,
                 target_currency=Currency.USDollar,
                 api_key_coinmarketcap = None)

    def tearDown(self):
        del self.currency_retriever

    def testCreateCurrencyRetriever(self):
        self.assertEqual(self.currency_retriever.base_currency, Currency.Euro)

    def testStartDateIsInTheFuture(self):
        date_fixed = datetime(2020,6,10)
        self.assertRaises(ValueError, lambda: CurrencyRetriever(start_date=date_fixed))

    def testStopDateIsInTheFuture(self):
        date_fixed = datetime(2020,6,10)
        self.assertRaises(ValueError, lambda: CurrencyRetriever(stop_date=date_fixed))

    def testExchangeRateIsCorrect(self):
        self.assertEqual(self.currency_retriever._current_rate, 1.0867)