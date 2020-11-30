from Transaction import Transaction, Currency, OrderType, TransactionOperation, TransactionOperator
from decimal import *
from datetime import datetime


def get_patrimonial_increment(list_buys=[], list_sells=[]):

    list_buys = list_buys
    list_sells = list_sells

    global_increment = Decimal(0.0)
    summary = ""
    
    # Tomar una compra y una venta de las listas (siempre la primera, FIFO)
    if(len(list_buys) == 0 or len(list_sells) == 0):
        return global_increment, "No hay pares de compra/venta para esta divisa"
    else:
        current_buy = list_buys.pop(0)
        current_sell = list_sells.pop(0)

    while(True):
        if (current_buy.asset_amount > current_sell.asset_amount):
            # print("A compensar {} de los {} que quedan por comprar".format(round(current_buy.asset_amount, 8), round(current_sell.asset_amount, 8)))

            # Como la cantidad de compra es mayor, se toma en cuenta la cantidad de venta para comparar
            quantity_to_compare = current_sell.asset_amount
            
            # Se calcula el valor en € de las cantidades fraccionarias de coste de venta y fee de venta
            buy_fraction = quantity_to_compare / current_buy.asset_amount
            current_buy_cost = buy_fraction * current_buy.cost
            current_buy_fee = buy_fraction * current_buy.fee
            
            # Se calcula el incremento patrimonial
            increment = current_sell.cost - (current_buy_cost + current_buy_fee + current_sell.fee)

            summary = summary + "El día {sell_date} se vendieron {quantity_to_compare} {asset} comprados el día {buy_date}. Incremento parcial = {increment} €".format(
                quantity_to_compare=round(quantity_to_compare, 8), 
                asset=current_buy.asset.value, 
                sell_date=datetime.fromtimestamp(current_sell.transaction_date).strftime('%d-%m-%Y'), 
                buy_date=datetime.fromtimestamp(current_buy.transaction_date).strftime('%d-%m-%Y'), 
                increment=round(increment, 2)
                ) + "\n"

            global_increment = global_increment + increment

            # Hay que actualizar el coste y el fee para restar las cantidades ya usadas
            current_buy.cost = current_buy.cost - current_buy_cost
            current_buy.fee = current_buy.fee - current_buy_fee
            current_buy.asset_amount = round(current_buy.asset_amount - quantity_to_compare, 8)
            current_sell.asset_amount = current_sell.asset_amount - quantity_to_compare
            
            # Actualizar remainder de la venta para la próxima iteración
            current_buy.remainder = 1 - round(buy_fraction, 8)

        elif (current_buy.asset_amount < current_sell.asset_amount):
            # print("A compensar {} de los {} que quedan por vender".format(round(current_buy.asset_amount, 8), round(current_sell.asset_amount, 8)))

            # Como la cantidad de compra es mayor, se toma en cuenta la cantidad de venta para comparar
            quantity_to_compare = current_buy.asset_amount
            
            # Se calcula el valor en € de las cantidades fraccionarias de coste de compra y fee de compra
            sell_fraction = quantity_to_compare / current_sell.asset_amount
            current_sell_cost = sell_fraction * current_sell.cost
            current_sell_fee = sell_fraction * current_sell.fee
            
            increment = current_sell_cost - (current_buy.cost + current_buy.fee + current_sell_fee)
            summary = summary + "El día {sell_date} se vendieron {quantity_to_compare} {asset} comprados el día {buy_date}. Incremento parcial = {increment} €".format(
                quantity_to_compare=round(quantity_to_compare, 8), 
                asset=current_buy.asset.value, 
                sell_date=datetime.fromtimestamp(current_sell.transaction_date).strftime('%d-%m-%Y'), 
                buy_date=datetime.fromtimestamp(current_buy.transaction_date).strftime('%d-%m-%Y'), 
                increment=round(increment, 2)
                ) + "\n"

            global_increment = global_increment + increment

            # Hay que actualizar el coste y el fee para restar las cantidades ya usadas
            current_sell.cost = current_sell.cost - current_sell_cost
            current_sell.fee = current_sell.fee - current_sell_fee
            current_sell.asset_amount = round(current_sell.asset_amount - quantity_to_compare, 8)
            current_buy.asset_amount = current_buy.asset_amount - quantity_to_compare
            
            # Actualizar remainder de la venta para la próxima iteración
            current_sell.remainder = 1 - round(sell_fraction, 8)

        else:
            # Como las cantidades son iguales, se toma cualquiera de ellas como referencia
            quantity_to_compare = current_buy.asset_amount

            # Se calcula el valor en € de las cantidades fraccionarias de coste de compra y fee de compra
            sell_fraction = current_buy.asset_amount / current_sell.asset_amount
            
            increment = current_sell.cost - (current_buy.cost + current_buy.fee + current_sell.fee)
            summary = summary + "El día {sell_date} se vendieron {quantity_to_compare} {asset} comprados el día {buy_date}. Incremento parcial = {increment} €".format(
                quantity_to_compare=round(quantity_to_compare, 8), 
                asset=current_buy.asset.value, 
                sell_date=datetime.fromtimestamp(current_sell.transaction_date).strftime('%d-%m-%Y'), 
                buy_date=datetime.fromtimestamp(current_buy.transaction_date).strftime('%d-%m-%Y'), 
                increment=round(increment, 2)
                ) + "\n"

            current_buy.asset_amount = round(current_buy.asset_amount - quantity_to_compare, 8)
            current_sell.asset_amount = round(current_sell.asset_amount - quantity_to_compare, 8)

            # Actualizar remainder de la venta para la próxima iteración
            current_sell.remainder = 1 - round(sell_fraction, 8)
            current_buy.remainder = 1 - round(sell_fraction, 8)

            global_increment = global_increment + increment
        
        if round(current_buy.asset_amount, 8) == Decimal(0.0):
            if len(list_buys) > 0:
                current_buy = list_buys.pop(0)
            else:
                break
        if round(current_sell.asset_amount, 8) == Decimal(0.0):
            if len(list_sells) > 0:
                current_sell = list_sells.pop(0)
            else:
                break

    return global_increment, summary