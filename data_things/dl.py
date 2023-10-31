import boto3
import botocore
import os
# from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
import argparse
import numpy as np
import parse_data


# print(np.log(32))

def download_and_process_file(i, coin, day, offset):
    # Initialize a session using Amazon S3
    s3 = boto3.client('s3', config=boto3.session.Config(signature_version=botocore.UNSIGNED))
    
    # i += offset
    folder_path = f"data_trades/{coin}"
    try:
        os.makedirs(folder_path)
    except FileExistsError:
        pass
    
    local_file_path = f"{folder_path}/{i+offset}.lz4"

    # Your bucket and file path
    bucket_name = 'hyperliquid-archive'
    file_path = f'market_data/{day}/{i}/trades/{coin}.lz4'

    s3.download_file(bucket_name, file_path, local_file_path)
    os.system(f'lz4 {local_file_path}')
    os.system(f'rm {local_file_path}')



def main(coin, day):
    # print(f'main: {coin}, {day}')
    hours = 24
    offset = 24-hours
    arguments = [(i, coin, day, offset) for i in range(hours)]
    print(arguments)

    with Pool(hours, maxtasksperchild=1) as pool:
        pool.starmap(download_and_process_file, arguments)
    # download_and_process_file(hours, coin, day)
    # parse_data.main(coin, hours)

if __name__ == '__main__':
    # Create the parser
    parser = argparse.ArgumentParser(description='Download data for a specific coin and day.')

    # Add the arguments with default values
    parser.add_argument('coin', type=str, help='the coin to download data for', nargs='?', default='SOL')
    parser.add_argument('day', type=str, help='the day to download data for', nargs='?', default='20231001')
    # parser.add_argument('-y', '--yes', action='store_true', help='Automatically answer yes to all overwrite prompts')


    # Parse the arguments
    args = parser.parse_args()
    # print(f'args {args}. {args.coin}, {args.day}')

    # Call the main function
    main(args.coin, args.day)