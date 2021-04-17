from kitelib import kiteops
from pylib import pyops
from pylib.logger import logger

QUANTITY = 5
NEW_COST = 2000


def place_daily_limit_order():
    holdings_info_live = kiteops.get_holdings()
    offline_holdings = pyops.get_dict_from_json_file('result', "holdings_info_five_min_update.json")
    order_id_list = []
    for offline_holding in offline_holdings:
        for live_holding in holdings_info_live:
            if offline_holding["tradingsymbol"] == live_holding["tradingsymbol"]:
                tradingsymbol = offline_holding["tradingsymbol"]
                min_price = offline_holding["price_min"]
                existing_cost = live_holding["authorised_quantity"] * live_holding["average_price"]
                new_cost = QUANTITY * live_holding['last_price']
                if offline_holding["priority_buy"] == 1 and existing_cost < 10000 and new_cost < NEW_COST:
                    order_id = kiteops.place_limit_order_buy(tradingsymbol,
                                                             min_price,
                                                             QUANTITY)
                    order_id_list.append(order_id)

    pyops.write_dict_into_json_file("data", "place_limit_buy_order_daily.json", order_id_list)


try:
    place_daily_limit_order()
except Exception as ex:
    logger.exception(ex)
