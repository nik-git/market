from nsetools import Nse


def lambda_handler(event, context):
    nse = Nse()
    tcs = nse.get_quote("TCS")
    return tcs

