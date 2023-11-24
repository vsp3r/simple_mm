import os
import math
import asyncio
from dotenv import load_dotenv
import multiprocessing
import time
import signal
from functools import partial
import traceback
import sys

from src.utils.utils import config_parse
# from src.utils import setup_processes
from src.exchanges import common
from src.execution import autotrader
from src.exchanges.binance import BinanceConnector
from src.exchanges.hyperliquid import HyperliquidConnector
from src.execution.autotrader import AutoTrader
from src.utils.process_handler import ProcessWrapper


MM_PARAMS_FILE = 'mm_params.yaml'
CONFIG_FILE = 'config.yaml'
COIN_CONFIG = 'coin_config.yaml'






def on_error(name: str, error: Exception) -> None:
    print("%s threw an exception: %s" % (name, error), file=sys.stderr)
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def main():
    config = config_parse(CONFIG_FILE)
    coins = config['Coins']
    exchanges = config['Exchanges']
    coins_per_feed = 5

    num_ws = (math.ceil(len(coins) / coins_per_feed)) * (len(exchanges) + 1)

    dex_connectors = {
        'hyperliquid': HyperliquidConnector
    }

    dex_queues = {
        exchange:{coin:multiprocessing.Queue() for coin in coins}
                  for exchange in exchanges
    }
    binance_queues = {coin: multiprocessing.Queue() for coin in coins}

    ws_objects = []
    ws_processes = []
    autotrader_objects = []
    autotrader_processes = []
    coin_pools = [coins[i:i+coins_per_feed] for i in range(0,len(coins),coins_per_feed)]

    for group in coin_pools:
        for exchange in exchanges:
            dex_queues_group = {coin:dex_queues[exchange][coin] for coin in group}
            dex_ws = dex_connectors[exchange](group, dex_queues_group)
            # ws_objects.append(dex_ws)
            wrapper = ProcessWrapper(dex_ws)
            p = multiprocessing.Process(target=wrapper.run)
            p.start()
            ws_processes.append(p)


            for coin in group:
                at = AutoTrader(exchange, coin,
                                        dex_queue=dex_queues[exchange][coin],
                                        bin_queue=binance_queues[coin]) 
                # autotrader_objects.append(autotrader)
                wrapper = ProcessWrapper(at)
                p = multiprocessing.Process(target=wrapper.run)
                p.start()
                autotrader_processes.append(p)
            
        bin_queues_group = {coin:binance_queues[coin] for coin in group}
        binance_ws = BinanceConnector(group, bin_queues_group)
        # ws_objects.append(binance_ws)
        wrapper = ProcessWrapper(binance_ws)
        p = multiprocessing.Process(target=wrapper.run)
        p.start()
        ws_processes.append(p)

    # for ws in ws_objects:
    #     wrapper = ProcessWrapper(ws)
    #     p = multiprocessing.Process(target=wrapper.run)
    #     p.start()
    #     ws_processes.append(p)

    # for at in autotrader_objects:
    #     wrapper = ProcessWrapper(at)
    #     p = multiprocessing.Process(target=wrapper.run)
    #     p.start()
    #     autotrader_processes.append(p)

    try:
        for p in ws_processes + autotrader_processes:
            p.join()
    except KeyboardInterrupt:
        print("Shutdown signal received")
        # Optionally send a signal to child processes to terminate
        for p in ws_processes + autotrader_processes:
            p.terminate()  # This is a forceful termination

    

if __name__ == '__main__':
    
    main()

   