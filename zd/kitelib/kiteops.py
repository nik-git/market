from kitelib import connect
from pylib.logger import logger


def get_holdings():
    return connect.KITE.holdings()


def place_limit_order_buy(tradingsymbol, limit_price, quantity):
    logger.info(f"Placing buy limit order: {tradingsymbol}, quantity:{quantity}, limit price: {limit_price}")
    order_id = connect.KITE.place_order(variety=connect.KITE.VARIETY_REGULAR,
                                        exchange=connect.KITE.EXCHANGE_NSE,
                                        order_type=connect.KITE.ORDER_TYPE_LIMIT,
                                        tradingsymbol=tradingsymbol,
                                        transaction_type=connect.KITE.TRANSACTION_TYPE_BUY,
                                        quantity=quantity,
                                        product=connect.KITE.PRODUCT_CNC,
                                        price=limit_price
                                        )
    logger.info(f"Order id: {order_id}")
    return order_id


def place_limit_order_sell(tradingsymbol, limit_price, quantity):
    logger.info(f"Placing sell limit order: {tradingsymbol}, quantity:{quantity}, limit price: {limit_price}")
    order_id = connect.KITE.place_order(variety=connect.KITE.VARIETY_REGULAR,
                                        exchange=connect.KITE.EXCHANGE_NSE,
                                        order_type=connect.KITE.ORDER_TYPE_LIMIT,
                                        tradingsymbol=tradingsymbol,
                                        transaction_type=connect.KITE.TRANSACTION_TYPE_SELL,
                                        quantity=quantity,
                                        product=connect.KITE.PRODUCT_CNC,
                                        price=limit_price
                                        )
    logger.info(f"Order id: {order_id}")


def get_orders():
    logger.info("Fetching all orders.")
    return connect.KITE.orders()


def get_ltp(instruments):
    return connect.KITE.ltp(instruments)
