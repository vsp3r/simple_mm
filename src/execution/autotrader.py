import multiprocessing
import sys
import asyncio
import logging
import multiprocessing
import os
import websockets
import json
import time
import threading
import math
import queue
# from ..mm_infra.feed import DataFeed

class AutoTrader:
    def __init__(self, exchange, coin, dex_queue, bin_queue):
        self.exchange = exchange
        self.coin = coin
        self.dex_queue = dex_queue
        self.bin_queue = bin_queue
        # self.running = True


        # self.data_feed = DataFeed(coin, (self.hl_handler, self.bin_handler))
        print(f'AUTOTRADER {self.coin}: Dex_queue {dex_queue}')
        print(f'AUTOTRADER {self.coin}: Bin_queue {bin_queue}')

        self.dex_book = {}
        self.bin_book = {}
        self.total_times = []
     


    async def run(self, shutdown_event):
        print(f'Running Autotrader {self.coin}')
        while not shutdown_event.is_set():
            try: 
                await asyncio.gather(
                    self.process_queue(self.bin_queue, 'binance'),
                    self.process_queue(self.dex_queue, self.exchange)
                )
            except Exception as e:
                print(f"Error in Autotrader {self.coin}: {e}")
                break
        print(self.get_performance_metrics)

    async def process_queue(self, message_queue, exchange_type):
        try:
            message = message_queue.get_nowait()
            await self.process_message(message, exchange_type)
        except queue.Empty:
            # No message in the queue, schedule to run again
            await asyncio.sleep(0)  # Adjust the sleep time if needed

    async def process_message(self, message, expected_exchange):
        exchange, symbol, times, data = message
        times.append(time.time_ns())

        if self.coin != symbol:
            # this would be something to alert in discord
            print(f'Incorrect coin in {expected_exchange} queue: {self.coin} expected, got {symbol}')

        # print(data)  # Process the message as needed
        if exchange == 'binance' and exchange == expected_exchange:
            await self.process_binance(data, times)
        elif exchange == self.exchange and exchange == expected_exchange:
            await self.process_dex(data, times)
        else:
            print(f'Unexpected exchange in {expected_exchange} queue: {exchange} for {self.coin}')

    async def process_binance(self, data, times):
        bid_px, bid_sz = data["b"][0]
        ask_px, ask_sz = data["a"][0]
        x = time.time_ns()
        times.append(x)
        elapsed_times = [(t - times[0]) / 1_000_000_000 for t in times] 
        print(f'AUTOTRADER (BIN, {self.coin}), times: {elapsed_times}, total: {sum(elapsed_times)}')
        # print(f'AUTOTRADER (BIN, {self.coin}): {bid_sz, bid_px}, {ask_px, ask_sz}')
    
    async def process_dex(self, data, times):
        levels = data['levels']
        bid_px, bid_sz = levels[0][0]['px'], levels[0][0]['sz']
        ask_px, ask_sz = levels[1][0]['px'], levels[1][0]['sz']
        x = time.time_ns()
        times.append(x)

        elapsed_times = [(t - times[0]) / 1_000_000_000 for t in times] 
        total_time = sum(elapsed_times)
        self.total_times.append(total_time)
        print(f'times: {elapsed_times}, total: {total_time}')

    def get_performance_metrics(self):
        return (self.total_times, sum(self.total_times)/len(self.total_times))

    
        # print(f'AUTOTRADER ({self.exchange.upper()}, {self.coin}): {bid_sz, bid_px}, {ask_px, ask_sz}')
#     def hl_handler(self, message, n):
#         bid_price = float(message['data']['levels'][0][0]['px'])
#         bid_sz = float(message['data']['levels'][0][0]['sz'])
#         ask_price = float(message['data']['levels'][1][0]['px'])
#         ask_sz = float(message['data']['levels'][1][0]['sz'])

#         self.hl_book['bid'] = (bid_price, bid_sz)
#         self.hl_book['ask'] = (ask_price, ask_sz)

#         # print(f'{message}({n}): Max pos {self.glob_position}, coin pos {self.coin_pos}')
#         print(f'HyperLiquid[{self.coin}] ({n}): {message}')
#         # bids = message['data']['levels'][0][x]['px'] for x in message['data']['levels'][0]
#         # print(message)

#     def bin_handler(self, message, n):
#         bid_price = float(message['b'][0][0])
#         bid_sz = float(message['b'][0][1])
#         ask_price = float(message['a'][0][0])
#         ask_sz = float(message['a'][0][1])

#         self.bin_book['bid'] = (bid_price, bid_sz)
#         self.bin_book['ask'] = (ask_price, ask_sz)
#         self.bin_book['book_pressure'] = ((bid_price * ask_sz) + (ask_price * bid_price)) / (ask_sz + bid_sz)

#         # print(f'Binance[{self.coin}] ({n}): {message}')

    # def start(self):
    #     # print(f'started {self.coin}')

    #     asyncio.run(self.run())

    # def shutdown(self):
    #     self.running = False
    