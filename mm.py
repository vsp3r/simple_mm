import argparse
import multiprocessing
import sys
import logging
import time
import json
import os
import cProfile
import pstats
import traceback
import asyncio

from mm_infra import config_parse
from mm_infra import AutoTrader
# from mm_infra.autotrader import AutoTrader
# import alpha.simple_mm.autotrader


CONFIG_FILE = 'config.json'
AUTH_FILE = 'auth.json'
LOG_FOLDER = 'logs'
LOG_FILE = 'mm.log'


def start_autotrader(coin, config):
    at = AutoTrader(coin, config)
    at.start()
    # asyncio.run(at.run())



def run(config):
    print(config)
    all_coins = config['Symbols']
    # start_autotrader("BTC")
    with multiprocessing.Pool(len(all_coins)) as pool:
        # pool.map(start_autotrader, all_coins)

        pool.starmap(start_autotrader, [(coin, config) for coin in all_coins])
        # for coin in config['Symbols']:
        #     pool.apply_async(autotrader.main(coin, config), 
        #                     error_callback=lambda e: on_error(f"Autotrader {coin}: {e}"))


def on_error(name: str, error: Exception) -> None:
    print("%s threw an exception: %s" % (name, error), file=sys.stderr)
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def main():
    config = config_parse(CONFIG_FILE)
    for x in config['Symbols']:
        print(x)


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