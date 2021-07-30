from alpaca_trade_api.rest import *
ticker = "SPY"
API_KEY="PKCVMVLPU8KRMKYP5AI0"
SECRET_KEY = "UCCF2nBznxa6lPP0iqewzfaZtRqL5RjiInrte2C6"
BASE_URL = "https://paper-api.alpaca.markets"
DATA_URL = "https://data.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
LATEST_QUOTE = "{}/v2/stocks/{}/quotes/latest".format(DATA_URL,ticker)
HEADERS = {'APCA-API-KEY-ID':API_KEY,'APCA-API-SECRET-KEY':SECRET_KEY}

api = REST(API_KEY,SECRET_KEY,BASE_URL,api_version='v2')#way to get historical data
positionSizing = 0.25

