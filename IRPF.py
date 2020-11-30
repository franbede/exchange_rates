from Transaction import Transaction, Currency, OrderType, TransactionOperation, TransactionOperator
import ciso8601
import time
import pandas as pd
import csv
from datetime import datetime
from decimal import *
from patrimonial_increments import get_patrimonial_increment


t = "2020-05-13 18:23"
ts = ciso8601.parse_datetime(t)
#print("Time is {}".format(ts))
#print(time.mktime(ts.timetuple()))

transactions_list = []

with open("3. Calculo Incremento Patrimonial.csv", 'r') as f:
    r = csv.DictReader(f, delimiter=";")
    for line in r:
        # Format date
        t = line['Transaction_date']
        ts = ciso8601.parse_datetime(t)
        
        # Create Transaction object
        transaction = Transaction(refid=line['Ref_ID'],
                 transaction_date=time.mktime(ts.timetuple()),
                 transaction_operation=TransactionOperation[line['Transaction_operation']],
                 asset=Currency[line['Asset']],
                 asset_amount=Decimal(line['Asset_amount']),
                 order_type=OrderType[line['Order_Type']],
                 operator=TransactionOperator[line['Operator']],
                 cost=Decimal(line['Cost']),
                 fee=Decimal(line['Fee']),
                 price=Decimal(line['Price']),
                 remainder=Decimal(line['remainder']))
        
        # Add transaction object to transactions list
        transactions_list.append(transaction)

transactions_summary = ""
# Fees store
fees = Decimal(0.0)
# XBT buys & sells
list_buys_XBT = []
list_sells_XBT = []
# ETH buys& sells
list_buys_ETH = []
list_sells_ETH = []
# XRP buys& sells
list_buys_XRP = []
list_sells_XRP = []

for transaction in transactions_list:
    transaction_summary = transaction.get_transaction_summary()
    transactions_summary = transactions_summary + transaction_summary

    # Compute global fees as global metric
    fees = fees + transaction.fee

    # Classify transactions in buys and sells
    if(transaction.asset == Currency.Bitcoin and transaction.transaction_operation == TransactionOperation.Buy):
        list_buys_XBT.append(transaction)
    if(transaction.asset == Currency.Bitcoin and transaction.transaction_operation == TransactionOperation.Sell):
        list_sells_XBT.append(transaction)

    if(transaction.asset == Currency.Ethereum and transaction.transaction_operation == TransactionOperation.Buy):
        list_buys_ETH.append(transaction)
    if(transaction.asset == Currency.Ethereum and transaction.transaction_operation == TransactionOperation.Sell):
        list_sells_ETH.append(transaction)

    if(transaction.asset == Currency.Ripple and transaction.transaction_operation == TransactionOperation.Buy):
        list_buys_XRP.append(transaction)
    if(transaction.asset == Currency.Ripple and transaction.transaction_operation == TransactionOperation.Sell):
        list_sells_XRP.append(transaction)

# Count operations by asset
buys_XBT = sum(map(lambda x : (x.asset == Currency.Bitcoin and x.transaction_operation == TransactionOperation.Buy), transactions_list))
sells_XBT = sum(map(lambda x : (x.asset == Currency.Bitcoin and x.transaction_operation == TransactionOperation.Sell), transactions_list))
buys_ETH = sum(map(lambda x : (x.asset == Currency.Ethereum and x.transaction_operation == TransactionOperation.Buy), transactions_list))
sells_ETH = sum(map(lambda x : (x.asset == Currency.Ethereum and x.transaction_operation == TransactionOperation.Sell), transactions_list))
buys_XRP = sum(map(lambda x : (x.asset == Currency.Ripple and x.transaction_operation == TransactionOperation.Buy), transactions_list))
sells_XRP = sum(map(lambda x : (x.asset == Currency.Ripple and x.transaction_operation == TransactionOperation.Sell), transactions_list))

# Set summary of operations
operations_XBT = "Se han realizado {compras} compras y {ventas} ventas de Bitcoin".format(compras=buys_XBT, ventas=sells_XBT)
operations_ETH = "Se han realizado {compras} compras y {ventas} ventas de Ether".format(compras=buys_ETH, ventas=sells_ETH)
operations_XRP = "Se han realizado {compras} compras y {ventas} ventas de Ripple".format(compras=buys_XRP, ventas=sells_XRP)
fees_summary = "El gasto total en comisiones de compra y venta ha sido de {fees} €".format(fees=round(fees, 2))

# Compute patrimonial increments on every asset transaction list
global_increment_XBT, summary_XBT = get_patrimonial_increment(list_buys_XBT, list_sells_XBT)
global_increment_ETH, summary_ETH = get_patrimonial_increment(list_buys_ETH, list_sells_ETH)
global_increment_XRP, summary_XRP = get_patrimonial_increment(list_buys_XRP, list_sells_XRP)

# Set tax percentage
tax = Decimal(0.19) # 19% para los primeros 6.000€

summary_increment_XBT = "Incremento neto por Bitcoin: {} €".format(round(global_increment_XBT, 2))
summary_increment_ETH = "Incremento neto por Ethereum: {} €".format(round(global_increment_ETH, 2))
summary_increment_XRP = "Incremento neto por Ripple: {} €".format(round(global_increment_XRP, 2))

global_increment = global_increment_XBT + global_increment_ETH + global_increment_XRP

net_global_increment = "El incremento patrimonial neto global es de {} €".format(round(global_increment, 2))
tax_declaration_amount = "La cantidad que declarar a Hacienda ({}%) es de {} €".format(round(tax * 100, 2), round(global_increment * tax, 2))

print()

# Save summary to txt file
with open("Summary.txt", "w") as f:
    f.write("Resumen de transacciones\n-----------------------\n")
    f.write(operations_XBT + "\n" + operations_ETH + "\n" + operations_XRP + "\n" + fees_summary + "\n")
    f.write("\n")
    f.write(transactions_summary + "\n")
    f.write("Detalle de variación patrimonial\n-----------------------\n")
    f.write("Bitcoin:\n" + summary_XBT + "\n")
    f.write("Ethereum:\n" + summary_ETH + "\n")
    f.write("Ripple:\n" + summary_XRP + "\n")
    f.write("Resumen de variación patrimonial\n-----------------------\n")
    f.write(summary_increment_XBT + "\n")
    f.write(summary_increment_ETH + "\n")
    f.write(summary_increment_XRP + "\n")
    f.write(net_global_increment + "\n")
    f.write(tax_declaration_amount + "\n\n")
    f.write("Operaciones de compra restantes a compensar\n-----------------------\n")

    # Check remaining items in lists for next year tax calculations

    remaining_operations_XBT = list_buys_XBT + list_sells_XBT
    remaining_operations_XBT.sort(key=lambda x: x.transaction_date)

    for transaction in remaining_operations_XBT:
        f.write(transaction.get_transaction_summary())