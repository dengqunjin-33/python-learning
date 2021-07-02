import logging

from binance_f import SubscriptionClient, RequestClient
from binance_f.base.printobject import *
from binance_f.exception.binanceapiexception import BinanceApiException
from binance_f.model import *

logger = logging.getLogger("binance-futures")
logger.setLevel(level=logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# conn = pymysql.connect(host='58.67.156.39',
#                        port=6033,
#                        user='jiyu',
#                        password='jiyu',
#                        database='mw_aitrade',
#                        charset='utf8')


def callback(data_type: 'SubscribeMessageType', event: 'any'):
    if data_type == SubscribeMessageType.RESPONSE:
        print("Event ID: ", event)
    elif data_type == SubscribeMessageType.PAYLOAD:
        print(event.data, flush=True)
        PrintBasic.print_obj(event)

    else:
        print("Unknown Data:")
    print()


def error(e: 'BinanceApiException'):
    print(e.error_code + e.error_message)


request_client = RequestClient(api_key="", secret_key="", url="https://fapi.binance.com")

exchange_information = request_client.get_exchange_information()

symbols = exchange_information.get_symbols()

sub_client = SubscriptionClient(api_key='', secret_key='')
for symbol in symbols:
    sub_client.subscribe_candlestick_event('btcusdt', CandlestickInterval.MIN1, callback, error)
