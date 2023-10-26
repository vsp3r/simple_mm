import json
import argparse
from multiprocessing import Pool
from datetime import datetime
import convert_time

def parse_file(i, coin):

    folder_path = f'data/{coin}'



    input_file = f'{folder_path}/{i}'
    output_file = f'{folder_path}/parsed.csv'

    with open(input_file, 'r') as infile, open(output_file, 'a') as outfile:
        if (i == 0):
            outfile.write("exchange,symbol,timestamp,ask_amount,ask_price,bid_price,bid_amount\n")

        for line in infile:
            # Parse the line as JSON
            data = json.loads(line)

            # Extract the relevant fields
            timestamp = convert_time.conv(data.get("time", "N/A"))
            # coin = data.get("raw", {}).get("data", {}).get("coin", "N/A")
            # first_bid = data.get("raw", {}).get("data", {}).get("levels", [[], []])[0][0] if data.get("raw", {}).get("data", {}).get("levels", [[], []])[0] else "N/A"
            # first_ask = data.get("raw", {}).get("data", {}).get("levels", [[], []])[1][0] if data.get("raw", {}).get("data", {}).get("levels", [[], []])[1] else "N/A"

            exchange = "hyperliquid"
            bid_price = data['raw']['data']['levels'][0][0]['px']
            bid_amount = data['raw']['data']['levels'][0][0]['sz']
            ask_price = data['raw']['data']['levels'][1][0]['px']
            ask_amount = data['raw']['data']['levels'][1][0]['sz']


            # Write to the oxtput file
            # outfile.write(f"{timestamp},{coin},{first_bid},{first_ask}\n")
            outfile.write(f"{exchange},{coin},{timestamp},{ask_amount},{ask_price},{bid_price},{bid_amount}\n")




def main(coin, hours):
    hours = int(hours)
    arguments = [(i, coin) for i in range(hours)]
    # print(arguments)

    # with Pool(hours, maxtasksperchild=1) as pool:
    #     pool.starmap(parse_file, arguments)

    for i in range(hours):
        parse_file(i, coin)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Input l2book, output top 5 levels')

    parser.add_argument('coin', type=str, help='which coin', nargs='?', default='SOL')
    parser.add_argument('hours', type=str, help='how many hours of the day', nargs='?', default='24')

    args = parser.parse_args()
    main(args.coin, args.hours)
