import argparse
from multiprocessing import Pool, Manager, Event
import threading
import sys
import logging
import time
import json
import os
import cProfile
import pstats
import traceback
import asyncio
from dotenv import load_dotenv

from mm_infra import config_parse, coin_parse
from mm_infra import AutoTrader
# from mm_infra.autotrader import AutoTrader
# import alpha.simple_mm.autotrader


CONFIG_FILE = 'config.json'
COIN_FILE = 'coin_config.json'
AUTH_FILE = 'auth.json'
LOG_FOLDER = 'logs'
LOG_FILE = 'mm.log'
last_conf_update = os.path.getmtime(CONFIG_FILE)
last_coin_update = os.path.getmtime(COIN_FILE)


def start_autotrader(coin, shared_config, shared_coin_config, update_event):
    print(f'{coin}: {shared_config}')
    print(f'{coin}: {shared_coin_config}')
    at = AutoTrader(coin, shared_config, shared_coin_config, update_event, False)
    print(f"intialized {coin}")
    at.start()
    # pass
    # asyncio.run(at.run())


def config_monitor(update_event, shared_config, shared_coin_config, all_coins):
    global last_coin_update, last_conf_update
    while True:
        if os.path.getmtime(COIN_FILE) != last_coin_update:
            print('DETECTED COIN CONF CHANGE')
            shared_coin_config.update(coin_parse(all_coins, COIN_FILE))
            last_coin_update = os.path.getmtime(COIN_FILE)
            update_event.set()
        elif os.path.getmtime(CONFIG_FILE) != last_conf_update:
            print('DETECTED CONF CHANGE')
            shared_config.update(config_parse(CONFIG_FILE))
            last_conf_update = os.path.getmtime(CONFIG_FILE)
            update_event.set()


def run(config):
    manager = Manager()

    # shared data
    shared_config = manager.dict()
    shared_coin_config = manager.dict()
    update_event = manager.Event()

    # Initial parsing
    shared_config.update(config)
    all_coins = config['Symbols']
    shared_coin_config.update(coin_parse(all_coins, COIN_FILE))

    print(config)

    # dynamic update / config watcher
    threading.Thread(target=config_monitor, args=(update_event, shared_config, shared_coin_config, all_coins)).start()
   
    # start_autotrader("BTC")
    with Pool(processes=len(all_coins)) as pool:
        # pool.map(start_autotrader, all_coins)

        pool.starmap(start_autotrader, [(coin, shared_config, shared_coin_config, update_event) for coin in all_coins])
       

def main():
    config = config_parse(CONFIG_FILE)
    for x in config['Symbols']:
        print(x)

    # load_dotenv()
    # print(os.getenv("ACCOUNT"))
    # log_file_path = os.path.join(LOG_FOLDER, LOG_FILE)
    # logging.basicConfig(filename=log_file_path, 
    #                     format="%(asctime)s [%(levelname)-7s] [%(name)s] %(message)s",
    #                     level=logging.INFO, 
    #                     filemode='w'
    #                     )
    run(config)





if __name__ == '__main__':
    # pr = cProfile.Profile()
    # pr.enable()
    # # "main" code
    
    
    
    main()

    
    
    
    
    # pr.disable()
    # pr.dump_stats("profile_results.stats")

    # # Load and print the stats
    # stats = pstats.Stats("profile_results.stats")

    # # Convert to milliseconds (ms)
    # stats.strip_dirs().sort_stats('cumulative').print_stats(0.001)