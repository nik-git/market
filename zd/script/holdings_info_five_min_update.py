from kitelib import kiteops
from pylib import pyops
from datetime import datetime
from pylib.logger import logger


def update_watch_instruments():
    logger.info("Running update_watch_instruments function.")
    date_time_now = datetime.now()
    watch_list = pyops.get_dict_from_json_file('data', "watch_instruments.json")
    live_ltp_info = kiteops.get_ltp(watch_list)
    price_info = pyops.get_dict_from_json_file('result', "price_info.json")
    price_info_date_time = price_info["date_time"]
    logger.info(f"date_time_now {date_time_now}")
    logger.info(f"datetime.fromisoformat(price_info_date_time) {datetime.fromisoformat(price_info_date_time)}")
    delta_days = (date_time_now.date() - datetime.fromisoformat(price_info_date_time).date()).days
    logger.info(delta_days)
    price_info["date_time"] = str(date_time_now)
    for live_instrument, live_ltp in live_ltp_info.items():
        if live_instrument in price_info.keys():
            price_info[live_instrument]["last_price"] = live_ltp["last_price"]

            if live_ltp["last_price"] > price_info[live_instrument]["max_price"]:
                price_info[live_instrument]["max_price"] = live_ltp["last_price"]
                price_info[live_instrument]["max_price_date"] = str(date_time_now)

            elif live_ltp["last_price"] < price_info[live_instrument]["min_price"]:
                price_info[live_instrument]["min_price"] = live_ltp["last_price"]
                price_info[live_instrument]["min_price_date"] = str(date_time_now)

            if delta_days >= 1:
                price_info[live_instrument]["max_price_list"].append(live_ltp["last_price"])
                price_info[live_instrument]["min_price_list"].append(live_ltp["last_price"])

            if live_ltp["last_price"] > price_info[live_instrument]["max_price_list"][-1]:
                price_info[live_instrument]["max_price_list"][-1] = live_ltp["last_price"]

            elif live_ltp["last_price"] < price_info[live_instrument]["min_price_list"][-1]:
                price_info[live_instrument]["min_price_list"][-1] = live_ltp["last_price"]

        else:
            price_info[live_instrument] = live_ltp
            price_info[live_instrument]["min_price"] = live_ltp["last_price"]
            price_info[live_instrument]["max_price"] = live_ltp["last_price"]
            price_info[live_instrument]["min_price_date"] = str(date_time_now)
            price_info[live_instrument]["max_price_date"] = str(date_time_now)
            price_info[live_instrument]["min_price_list"] = [live_ltp["last_price"]]
            price_info[live_instrument]["max_price_list"] = [live_ltp["last_price"]]

    pyops.write_dict_into_json_file("result", "price_info.json", price_info)


def update_holdings_info():
    logger.info("Fetching live holdings.")
    # get the live holdings status from kite account.
    holdings_info_live = kiteops.get_holdings()
    # Save current live holdings in a json file.
    pyops.write_dict_into_json_file('data', "holdings_info_live.json", holdings_info_live)
    # get the holdings status from previously saved holdings.
    offline_holdings = pyops.get_dict_from_json_file('result', "holdings_info_five_min_update.json")
    # All the required key of offline holdings json.
    holdings_info_schema_dict = pyops.get_dict_from_json_file("data", "holdings_info_schema.json")
    date_time_now = datetime.now()
    # Run a loop over all live holdings and update offline holdings.
    for i in range(len(holdings_info_live)):
        found = False
        for j in range(len(offline_holdings)):
            # if a stock name is matched in live and offline holdings.
            if holdings_info_live[i]["tradingsymbol"].rstrip('*') == offline_holdings[j]['tradingsymbol']:
                if "price_day_max_list" not in offline_holdings[j].keys():
                    offline_holdings[j]["price_day_max_list"] = [0]
                if "price_day_min_list" not in offline_holdings[j].keys():
                    offline_holdings[j]["price_day_min_list"] = [0]

                found = True

                # This is to record the min and max price of the day.
                # In the start of the day set the day min and max = last price.
                ltp_date_offline = datetime.fromisoformat(offline_holdings[j]["ltp_datetime"]).date()
                authorised_date_live = datetime.fromisoformat(holdings_info_live[i]["authorised_date"]).date()
                delta_days = (authorised_date_live - ltp_date_offline).days
                if delta_days >= 1:
                    offline_holdings[j]['price_day_max'] = holdings_info_live[i]["last_price"]
                    offline_holdings[j]['price_day_min'] = holdings_info_live[i]["last_price"]
                    offline_holdings[j]["price_day_min_list"].append(holdings_info_live[i]["last_price"])
                    offline_holdings[j]["price_day_max_list"].append(holdings_info_live[i]["last_price"])
                    # In the start of the day, add current day's max and min diff = 0 in the list.
                    offline_holdings[j]['price_diff_day_max_min'].append(holdings_info_live[i]["last_price"])
                    # Hold only 10 values in the list. List for holding last 10 days max and min price diff.
                    if len(offline_holdings[j]['price_diff_day_max_min']) >= 30:
                        # Remove the first day value from the list on 11th day.
                        logger.debug("Removing one entry from day max min price diff list.")
                        offline_holdings[j]['price_diff_day_max_min'] = offline_holdings[j]['price_diff_day_max_min'][
                                                                        1:]

                # Update basic values.
                offline_holdings[j]['quantity'] = holdings_info_live[i]["quantity"]
                offline_holdings[j]['average_price'] = round(holdings_info_live[i]["average_price"], 2)
                offline_holdings[j]['last_price'] = round(holdings_info_live[i]["last_price"], 2)
                offline_holdings[j]['ltp_datetime'] = str(date_time_now)

                # If last price of live holding is greater then max price of offline holding.
                # Update max price of offline holding. And increase the max count by one.
                # Update the max and min price diff.
                if holdings_info_live[i]["last_price"] > offline_holdings[j]['price_max']:
                    offline_holdings[j]['price_max'] = holdings_info_live[i]["last_price"]
                    offline_holdings[j]['count_max_price'] += 1
                    offline_holdings[j]['datetime_max_price'] = str(date_time_now)
                    offline_holdings[j]['price_diff_max_min'] = \
                        round(offline_holdings[j]['price_max'] - offline_holdings[j]['price_min'], 2)

                # If last price of live holding is less then min price of offline holding.
                # Update min price of offline holding. And increase the min count by one.
                # Update the max and min price diff.
                elif holdings_info_live[i]["last_price"] < offline_holdings[j]['price_min']:
                    offline_holdings[j]['price_min'] = holdings_info_live[i]["last_price"]
                    offline_holdings[j]['count_min_price'] += 1
                    offline_holdings[j]['datetime_min_price'] = str(date_time_now)
                    offline_holdings[j]['price_diff_max_min'] = \
                        round(offline_holdings[j]['price_max'] - offline_holdings[j]['price_min'], 2)

                # If the new value of day max price is hit, add it in day max.
                # And update the day max and min price diff in the list.
                if holdings_info_live[i]["last_price"] > offline_holdings[j]['price_day_max']:
                    offline_holdings[j]['price_day_max'] = holdings_info_live[i]["last_price"]
                    offline_holdings[j]['price_diff_day_max_min'][-1] = \
                        round(offline_holdings[j]['price_day_max'] - offline_holdings[j]['price_day_min'], 2)
                    offline_holdings[j]["price_day_max_list"][-1] = offline_holdings[j]['price_day_max']

                # If the new value of day min price is hit, add it in day min.
                # And update the day max and min price diff in the list.
                elif holdings_info_live[i]["last_price"] < offline_holdings[j]['price_day_min']:
                    offline_holdings[j]['price_day_min'] = holdings_info_live[i]["last_price"]
                    offline_holdings[j]['price_diff_day_max_min'][-1] = \
                        round(offline_holdings[j]['price_day_max'] - offline_holdings[j]['price_day_min'], 2)
                    offline_holdings[j]["price_day_min_list"][-1] = offline_holdings[j]['price_day_min']

        # if the stock is added for the first time. That is newly bought stock.
        # Add that stock in the offline json.
        if not found:
            temp_dict = holdings_info_schema_dict
            temp_dict["tradingsymbol"] = holdings_info_live[i]["tradingsymbol"]
            temp_dict["quantity"] = holdings_info_live[i]["quantity"]
            temp_dict["average_price"] = round(holdings_info_live[i]["average_price"], 2)
            temp_dict["last_price"] = holdings_info_live[i]["last_price"]
            temp_dict["price_max"] = holdings_info_live[i]["last_price"]
            temp_dict["price_min"] = holdings_info_live[i]["last_price"]
            temp_dict["count_max_price"] = 0
            temp_dict["count_min_price"] = 0
            temp_dict["datetime_max_price"] = ""
            temp_dict["datetime_min_price"] = ""
            temp_dict["ltp_datetime"] = str(date_time_now)
            temp_dict['price_diff_max_min'] = 0
            temp_dict['priority_buy'] = 0
            temp_dict['priority_sell'] = 0
            temp_dict['price_day_max'] = holdings_info_live[i]["last_price"]
            temp_dict['price_day_min'] = holdings_info_live[i]["last_price"]
            temp_dict['price_diff_day_max_min'] = [0]
            temp_dict['price_day_max_list'] = [0]
            temp_dict['price_day_min_list'] = [0]
            offline_holdings.append(temp_dict)

    logger.info("Updating offline holdings.")
    pyops.write_dict_into_json_file('result', "holdings_info_five_min_update.json", offline_holdings)


try:
    update_holdings_info()
    update_watch_instruments()
except Exception as ex:
    logger.exception(ex)
