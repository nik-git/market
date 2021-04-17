import logging
from kiteconnect import KiteConnect
import requests
import pprint

logging.basicConfig(level=logging.DEBUG)

kite = KiteConnect(api_key="x5uybcmbmzebgrxz")
access_token = open('aceess_token.txt', 'r').read()
kite.set_access_token(access_token=access_token)

# refresh once in a day
# def get_access_token():
#     print(kite.login_url())
#     data = kite.generate_session("Mk0dcFCORo9Jsu1zLyjOT0K7s37lIxzR", api_secret='mp8wj09ss3cjny9jefx0a5z8kzf1ud1r')
#     access_token = data['access_token']
#     with open('aceess_token.txt', 'w') as fp:
#         fp.write(access_token)


#run only once in a day.
#get_access_token()
# hol = kite.holdings()
# pprint.pprint(hol)

#print(kite.ltp('NSE:IDEA'))
#print(kite.orders())
#print(kite.historical_data(408065, '2021-03-01 10:00:00', '2021-03-05 10:00:00', '30minute', continuous=False, oi=False))
#print(kite.profile())
# order_id = kite.place_order(variety=kite.VARIETY_REGULAR,
#                             exchange=kite.EXCHANGE_NSE,
#                             order_type=kite.ORDER_TYPE_MARKET,
#                             tradingsymbol='IDEA',
#                             transaction_type=kite.TRANSACTION_TYPE_BUY,
#                             quantity=1,
#                             product=kite.PRODUCT_CNC,
#                             )
#EDELWEISS
# order_id = kite.place_order(variety=kite.VARIETY_REGULAR,
#                             exchange=kite.EXCHANGE_NSE,
#                             order_type=kite.ORDER_TYPE_MARKET,
#                             tradingsymbol='EDELWEISS',
#                             transaction_type=kite.TRANSACTION_TYPE_SELL,
#                             quantity=1,
#                             product=kite.PRODUCT_CNC,
#                             )