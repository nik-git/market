from nsetools import Nse
from kitelib import kiteops
from datetime import datetime
from pylib.logger import logger
from pylib import pyops

nse = Nse()


def get_day_low_high_price():
    watch_list = pyops.get_dict_from_json_file('data', "watch_instruments.json")
    print(watch_list)
    day_low_high_price = {}
    for instrument in watch_list:
        stock = instrument.split(":")[1]
        #print(stock)
        print(nse.get_quote(stock)['dayHigh'])





try:
    get_day_low_high_price()
except Exception as ex:
    logger.info(ex)


