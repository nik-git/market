from kitelib.connect import save_access_token


""" 
Run only once in a day.
    1. open URL : 'https://kite.trade/connect/login?api_key=x5uybcmbmzebgrxz&v=3' in web browser.
    2. Login manually.
    3. Copy request_token from URL and paste here.
"""
request_token = "YtIg1OegZiopJrc8jj1A2T9yWjF5xhPV"


save_access_token(request_token)