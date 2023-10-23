import multiprocessing
import sys
import asyncio
import logging
import multiprocessing
import os
import websockets
import json

# from mm_infra import DataFeed, Orderbook, config_parse, auth_parse, ExchangeType
# from hyperliquid.exchange import Exchange
# from hyperliquid.info import Info
# from .mm_infra.feed import DataFeed
# from .mm_infra.types import ExchangeType
# import .feed
from .feed import DataFeed
# from .orderbook import Orderbook
# from .utils import config_parse, auth_parse



CONFIG_FILE = 'config.json'
AUTH_FILE = 'auth.json'

class AutoTrader:
    # def __init__(self, coin, wallet, hl_url, logger):
    def __init__(self, coin, config):

        # Hyperliquid connection
        # self.info = Info(hl_url, skip_ws=True)
        # self.exchange = Exchange(wallet, hl_url)
        # self.exchange.update_leverage(50, coin)
        self.position = None
        self.config = config
        self.coin = coin

        # self.hl_url = config['Exchange']['HL_URL']
        self.data_feed = DataFeed(coin, (self.hl_handler, self.bin_handler))


        # General config
        
        self.last_mtime = None

        # MM parameters
        self.fair_price = None
        self.spread = None
        self.fade = None # skew
        self.slack = None # spread flexibility as function of vol
        self.quote_refresh = None # time in seconds
        self.pennying = None # should we penny or no
        self.gridding = None # should we grid (multiple orders over levels) or no
        self.splitting = None # send total size in multiple orders or no

        # Trading parameters
        self.position_limit = None
        self.size = None
        self.step_size = None # step sizing into optimal size

        # Logging
        # self.logger = logger
        # self.log_filename = f'autotrader_{coin}.log'
        # self.log_file_path = os.path.join('logs', self.log_filename)

    # self.logger.info("%s started with arguments={%s}", self.name, ", ".join(sys.argv))
    # if self.config is not None:
    #     self.logger.info("configuration=%s", json.dumps(self.config, separators=(',', ':')))
    async def run(self):
        print(f'Running Autotrader {self.coin}')
        await self.data_feed.run()

    def hl_handler(self, message, n):
        # print(f'HyperLiquid[{self.coin}] ({n}): {message}')
        bids = message['data']['levels'][0][x]['px'] for x in message['data']['levels'][0]
        print(bids)

    def bin_handler(self, message, n):
        # print(f'Binance[{self.coin}] ({n}): {message}')
        pass

    def start(self):
        asyncio.run(self.run())
    

# def main():
#     config = config_parse(CONFIG_FILE)
#     auth = auth_parse(AUTH_FILE)

#     coin = config['Symbols'][0]
#     trader = AutoTrader(coin, config)
#     # asyncio.run(trader.run())
#     trader.start()

# if __name__ == '__main__':
#     # if sys.platform == 'darwin':
#     #     multiprocessing.set_start_method("spawn")
#     main()