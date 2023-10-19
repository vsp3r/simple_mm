import multiprocessing
import sys
import asyncio

from mm_infra import DataFeed, Orderbook, config_parse, auth_parse, Exchange

CONFIG_FILE = 'config.json'
AUTH_FILE = 'auth.json'

class AutoTrader:
    def __init__(self):
        # General config
        self.coin = None
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



def main():
    config = config_parse(CONFIG_FILE)
    auth = auth_parse(AUTH_FILE)
    trader = AutoTrader()
    asyncio.run(trader.run())

if __name__ == '__main__':
    if sys.platform == 'darwin':
        multiprocessing.set_start_method("spawn")
    main()