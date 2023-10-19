import multiprocessing
import sys
import asyncio

from mm_infra import DataFeed, Orderbook, config_parse, auth_parse, Exchange


class AutoTrader:
    def __init__(self):



def main():
    trader = AutoTrader()
    asyncio.run(trader.run())

if __name__ == '__main__':
    if sys.platform == 'darwin':
        multiprocessing.set_start_method("spawn")
    main()