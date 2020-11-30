"""Transaction class"""
from datetime import date, datetime
from enum import Enum
import logging
from decimal import *


class TransactionOperation(Enum):
    """Enum for operation options"""
    Buy = "BUY"
    Sell = "SEL"
    Withdrawal = "WIT"
    Deposit = "DEP"

    @classmethod
    def has_value(cls, value):
        return value in list(TransactionOperation)

class OrderType(Enum):
    """Order type enum"""
    Market = "MKT"
    Limit = "LIM"

    @classmethod
    def has_value(cls, value):
        return value in list(OrderType)

class TransactionOperator(Enum):
    """Exchange or wallet"""
    Kraken = "KRA"
    Coinbase = "COI"
    Ledger = "LED"
    Exodus = "EXO"
    External = "EXT"

    @classmethod
    def has_value(cls, value):
        return value in list(TransactionOperator)

class Currency(Enum):
    """Currency enum"""
    Euro = "EUR"
    USDollar = "USD"
    Bitcoin = "XBT"
    Ethereum = "ETH"
    Ripple = "XRP"

    @classmethod
    def has_value(cls, value):
        return value in list(Currency)

class Transaction:
    """Definition of a transaction model"""
    def __init__(self, refid=None,
                 transaction_date=datetime.now().timestamp(),
                 transaction_operation=TransactionOperation.Buy,
                 asset=Currency.Euro,
                 asset_amount=Decimal(0.0),
                 order_type=OrderType.Market,
                 operator=TransactionOperator.Kraken,
                 cost=Decimal(0.0),
                 fee=Decimal(0.0),
                 price=Decimal(0.0),
                 remainder=Decimal(1.0)):
        """Initialization method"""
        self.transaction_date = transaction_date
        self.transaction_operation = transaction_operation
        self.asset = asset
        self.asset_amount = asset_amount
        self.order_type = order_type
        self.operator = operator
        self.cost = cost
        self.fee = fee
        self.price = price
        self.remainder = remainder

    def __str__(self):
        return self.get_transaction_summary()
    @property
    def transaction_date(self):
        return self._transaction_date

    @transaction_date.setter
    def transaction_date(self, value):
        if value > datetime.now().timestamp():
            raise ValueError("Date must not be in the future")
        else:
            self._transaction_date = value

    @property
    def transaction_operation(self):
        return self._transaction_operation

    @transaction_operation.setter
    def transaction_operation(self, value):
        if TransactionOperation.has_value(value):
            self._transaction_operation = value
        else:
            raise NameError("The specified transaction operation does not exist")

    @property
    def asset(self):
        return self._asset

    @asset.setter
    def asset(self, value):
        if Currency.has_value(value):
            self._asset = value
        else:
            raise ValueError("Currency not found")  

    @property
    def asset_amount(self):
        return self._asset_amount

    @asset_amount.setter
    def asset_amount(self, value):
        if value >= Decimal(0.0):
            self._asset_amount = value
        else:
            raise ValueError("Quantity must be positive") 

    @property
    def order_type(self):
        return self._order_type

    @order_type.setter
    def order_type(self, value):
        if OrderType.has_value(value):
            self._order_type = value
        else:
            raise NameError('The specified order type does not exist')
    
    @property
    def operator(self):
        return self._operator

    @operator.setter
    def operator(self, value):
        if TransactionOperator.has_value(value):
            self._operator = value
        else:
            raise NameError("Specified operator was not found")

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        if value >= Decimal(0.0):
            self._cost = value
        else:
            raise ValueError("Quantity must be positive")

    @property
    def fee(self):
        return self._fee

    @fee.setter
    def fee(self, value):
        if value >= Decimal(0.0):
            self._fee = value
        else:
            raise ValueError("Quantity must be positive")

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < Decimal(0.0):
            raise ValueError("The price must not be negative")
        else:
            self._price = value

    @property
    def remainder(self):
        return self._remainder

    @remainder.setter
    def remainder(self, value):
        if value < Decimal(0.0) and value > Decimal(1.0):
            raise ValueError("The covered amount must be within 0.0 an 1.0")
        else:
            self._remainder = value

    def get_transaction_summary(self):
        date = datetime.fromtimestamp(self.transaction_date).strftime('%d-%m-%Y')
        operation = "compré" if self.transaction_operation == TransactionOperation.Buy else "vendí"
        comission_type = "compra" if operation == "compré" else "venta"
        asset_amount = self.asset_amount
        asset = self.asset
        price = self.price
        fee = self.fee
        total = round(self.cost + fee, 2)
        cost = round(self.cost, 2)

        transaction_summary = "El {date} {operation} {asset_amount} {asset} a {price}€, ".format(date=date, operation=operation, asset_amount=asset_amount, asset=asset.value, price=price) + \
                "comisión de {comission_type} de {fee} €. El coste es {cost} €, y el ".format(comission_type=comission_type, fee=round(fee, 2), cost=cost) + \
                "valor total de {comission_type} es {total} €.\n".format(comission_type=comission_type, total=total)

        return transaction_summary