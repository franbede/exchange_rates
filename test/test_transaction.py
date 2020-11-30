import unittest
from datetime import date, datetime
from Transaction import Transaction, TransactionOperation, Currency, TransactionOperator, OrderType


class TestTransaction(unittest.TestCase):

    def setUp(self):
        # create global objects
        self.transaction = Transaction(refid="TN5RVP-OO4VQ-557SOH",
                 transaction_date=1547145448.7345,
                 transaction_operation=TransactionOperation.Deposit,
                 asset=Currency.Euro,
                 order_type=OrderType.Market,
                 operator=TransactionOperator.Kraken,
                 cost=597.55,
                 fee=1.55363,
                 price=3145.0,
                 covered_amount=0.0)

    def tearDown(self):
        # Delete all used objects
        del self.transaction

    def testTransactionDate(self):
        date_fixed = 1547145448.7345
        new_transaction = Transaction(transaction_date=date_fixed)
        self.assertEqual(new_transaction.transaction_date, self.transaction.transaction_date)

    def testTransactionIsInTheFuture(self):
        date_fixed = 2547145448.7345
        self.assertRaises(ValueError, lambda: Transaction(transaction_date=date_fixed))

    def testTransactionOption(self):
        new_operation = TransactionOperation.Deposit
        new_transaction = Transaction(transaction_operation=new_operation)
        self.assertEqual(new_transaction.transaction_operation, self.transaction.transaction_operation)

    def testCurrency(self):
        new_currency = Currency.Euro
        new_transaction = Transaction(asset=new_currency)
        self.assertEqual(new_transaction.asset, self.transaction.asset)

    def testQuantityPositive(self):
        new_quantity = 597.55
        new_operation = TransactionOperation.Deposit
        new_transaction = Transaction(cost=new_quantity, transaction_operation=new_operation)
        self.assertGreater(new_transaction.cost, 0.0)

    def testQuantityNegative(self):
        new_quantity = -597.55
        self.assertRaises(ValueError, lambda: Transaction(cost=new_quantity))

    def testSummaryGeneration(self):
        expected_outcome = "El 10-01-2019 vendí 0.0 EUR a 3145.0€, comisión de venta de 1.55363 €. El coste es 597.55 €, y el valor total de venta es 599.1 €.\n"
        actual_outcome = self.transaction.get_transaction_summary()
        self.assertEqual(actual_outcome, expected_outcome)

