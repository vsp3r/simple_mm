import argparse
import multiprocessing
import sys
import time
import json

CONFIG_FILE = 'config.json'
AUTH_FILE = 'auth.json'

def main():
    config = json.load(CONFIG_FILE)
    for x in config['Symbols']:
        print(x)

if __name__ == '__main__':
    main()