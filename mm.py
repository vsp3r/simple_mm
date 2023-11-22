import os
import math
import asyncio
from dotenv import load_dotenv
import multiprocessing
import time
import signal
from functools import partial

from src.utils.utils import config_parse
from src.exchanges.binance import BinanceConnector
from src.exchanges.hyperliquid import HyperliquidConnector
from src.execution.autotrader import AutoTrader


MM_PARAMS_FILE = 'mm_params.yaml'
CONFIG_FILE = 'config.yaml'
COIN_CONFIG = 'coin_config.yaml'

shutdown_event = multiprocessing.Event()

def shutdown_sequence(shutdown_event, ws_processes, autotrader_processes):
    shutdown_event.set()
    for p in ws_processes + list(autotrader_processes.values()):
        p.join()

    # Collect and print performance metrics from AutoTraders
    for key, at_process in autotrader_processes.items():
        # This assumes you have a way to retrieve metrics from the process
        metrics = at_process.get_performance_metrics()
        print(f"Metrics for {key}: {metrics}")


def start_binance_websocket(coins, queues):
    ws = BinanceConnector(coins, queues)
    # print(queues)
    asyncio.run(ws.run(shutdown_event))

def start_dex_websocket(coins, exchange, queues):
    print("AHHHHHHHHH", exchange)
    if exchange == 'hyperliquid':
        ws = HyperliquidConnector(coins, queues)
        # ws.start()
        asyncio.run(ws.run(shutdown_event))

def start_autotrader(exchange, coin, dex_queue, bin_queue):
    at = AutoTrader(exchange, coin, dex_queue, bin_queue)
    asyncio.run(at.run(shutdown_event))


def main():
    config = config_parse(CONFIG_FILE)
    coins = config['Coins']
    exchanges = config['Exchanges']
    

    dex_queues = {
        exchange:{coin:multiprocessing.Queue() for coin in coins}
                  for exchange in exchanges
    }
    binance_queues = {coin: multiprocessing.Queue() for coin in coins}
  
    # Dex Websockets
    coins_per_feed = 5
    num_ws = math.ceil(len(coins) / coins_per_feed)

    ws_processes = []
    autotrader_processes = {}
    coin_pools = [coins[i:i+coins_per_feed] for i in range(0,len(coins),coins_per_feed)]
    # print(coin_pools)
    for group in coin_pools:
        bin_queues_group = {coin:binance_queues[coin] for coin in group}
        binance_ws_process = multiprocessing.Process(target=start_binance_websocket,
                                                     args=(group, bin_queues_group))
        binance_ws_process.start()
        ws_processes.append(binance_ws_process)
        for exchange in exchanges:
            dex_queues_group = {coin:dex_queues[exchange][coin] for coin in group}
            dex_ws_process = multiprocessing.Process(target=start_dex_websocket,
                                                     args=(group, exchange, dex_queues_group))
            dex_ws_process.start()
            ws_processes.append(dex_ws_process)

            # Init Autotrader Processes
            for coin in group:
                autotrader_process = multiprocessing.Process(target=start_autotrader,
                                                             args=(exchange, coin, 
                                                                   dex_queues[exchange][coin],
                                                                   binance_queues[coin]))
                process_key = (exchange, coin)
                # print(f'in loop {process_key}')
                autotrader_process.start()
                autotrader_processes[process_key] = autotrader_process

    for p in ws_processes:
        p.join()
    for p in autotrader_processes.values():
        p.join()

    
    # signal.signal(signal.SIGINT, partial(shutdown_sequence, shutdown_event, ws_processes, autotrader_processes))
    # signal.signal(signal.SIGTERM, partial(shutdown_sequence, shutdown_event, ws_processes, autotrader_processes))



if __name__ == '__main__':
    # multiprocessing.set_start_method('spawn')
    main()