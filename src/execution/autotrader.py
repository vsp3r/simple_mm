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
        self.running = True


        # self.data_feed = DataFeed(coin, (self.hl_handler, self.bin_handler))
        print(f'AUTOTRADER {self.coin}: Dex_queue {dex_queue}')
        print(f'AUTOTRADER {self.coin}: Bin_queue {bin_queue}')

        self.dex_book = {}
        self.bin_book = {}
        self.total_times = []
     


    async def run(self):
        print(f'Running Autotrader {self.coin}')
        while self.running:

            await asyncio.gather(
                self.process_queue(self.bin_queue, 'binance'),
                self.process_queue(self.dex_queue, self.exchange)
            )
        
        print(self.get_performance_metrics())

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
        print(f'AUTOTRADER (HL, {self.coin}), times: {elapsed_times}, total: {total_time}')

    def get_performance_metrics(self):
        return (self.total_times, sum(self.total_times)/len(self.total_times))
    
    async def shutdown(self):
        print(self.get_performance_metrics())