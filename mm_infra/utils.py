import json
import os


def config_parse(config_file):
    current_dir = os.path.dirname(__file__)
    conf_data = {}
    config_path = os.path.join(os.path.dirname(current_dir), config_file)
    
    with open(config_path) as f:
        data = json.load(f)
        return data

def coin_parse(coins: list, coin_file):
    current_dir = os.path.dirname(__file__)
    coin_path = os.path.join(os.path.dirname(current_dir), coin_file)

    with open(coin_path, 'r+') as f:    
        coin_data = json.load(f)
        # coin_configs = {}
        # for coin in coins:
        #     if not (coin_data.get(coin, {}).get('CUSTOM', "False") == "True"):
        #         coin_configs[coin] = {"CUSTOM": "False",
        #                               "FADE": 0.1,
        #                               "SPREAD": 0.1,
        #                               "DEVIATION": 0.1}
                
        # # Writing the JSON with indentation
        # f.seek(0)  # Move the file pointer to the beginning
        # json.dump(coin_configs, f, indent=4) # 4 spaces for indentation
        # f.truncate() # Remove any remaining old data in the file

        return coin_data
