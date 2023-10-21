import asyncio
import multiprocessing


import working_feed
CONFIG_FILE = 'config.json'
AUTH_FILE = 'auth.json'
from mm_infra import config_parse


def start_autotrader(coin):
    autotrader = working_feed.AutoTrader(coin)
    # autotrader.start()
    asyncio.run(autotrader.run())



def run(config):
    print(config)
    all_coins = config['Symbols']
    start_autotrader("BTC")
    with multiprocessing.Pool(len(all_coins)) as pool:
        pool.map(start_autotrader, all_coins)

        # pool.starmap(start_autotrader, [(coin, config) for coin in all_coins])
        # for coin in config['Symbols']:
        #     pool.apply_async(autotrader.main(coin, config), 
        #                     error_callback=lambda e: on_error(f"Autotrader {coin}: {e}"))




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
    main()