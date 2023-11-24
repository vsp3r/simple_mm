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
import numpy as np
from src.utils import alerts
# from ..mm_infra.feed import DataFeed

class AutoTrader:
    def __init__(self, exchange, coin, dex_queue, bin_queue):
        self.exchange = exchange
        self.coin = coin
        self.dex_queue = dex_queue
        self.bin_queue = bin_queue
        self.running = True


        # self.data_feed = DataFeed(coin, (self.hl_handler, self.bin_handler))
        # print(f'AUTOTRADER {self.coin}: Dex_queue {dex_queue}')
        # print(f'AUTOTRADER {self.coin}: Bin_queue {bin_queue}')

        self.dex_book = {}
        self.bin_book = {}
        self.hl_times = []
        self.bin_times = []
     


    async def run(self):
        print(f'Running Autotrader {self.coin}')
        while self.running:

            await asyncio.gather(
                self.process_queue(self.bin_queue, 'binance'),
                self.process_queue(self.dex_queue, self.exchange)
            )
        
        # print(self.get_performance_metrics())

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
            msg = f'Incorrect coin in {expected_exchange} queue: {self.coin} expected, got {symbol}'
            alerts.post_message(msg)

        # print(data)  # Process the message as needed
        if exchange == 'binance' and exchange == expected_exchange:
            await self.process_binance(data, times)
        elif exchange == self.exchange and exchange == expected_exchange:
            await self.process_dex(data, times)
        else:
            msg = f'Unexpected exchange in {expected_exchange} queue: {exchange} for {self.coin}'
            alerts.post_message(msg)

    async def process_binance(self, data, times):
        bid_px, bid_sz = data["b"][0]
        ask_px, ask_sz = data["a"][0]
        times.append(time.time_ns())
        

        self.bin_times.append(times)
        print(f'AT (BIN, {self.coin}), times: {times}, total: {sum(times)}')
        elapsed_times = [(t - times[0]) / 1_000_000_000 for t in times] 
        # print(f'AT (BIN, {self.coin}), times: {elapsed_times}, total: {sum(elapsed_times)}')
        # print(f'AUTOTRADER (BIN, {self.coin}): {bid_sz, bid_px}, {ask_px, ask_sz}')
    
    async def process_dex(self, data, times):
        levels = data['levels']
        bid_px, bid_sz = levels[0][0]['px'], levels[0][0]['sz']
        ask_px, ask_sz = levels[1][0]['px'], levels[1][0]['sz']

        times.append(time.time_ns())

        # elapsed_times = [(t - times[0]) / 1_000_000_000 for t in times] 
        # total_time = sum(elapsed_times)
        # self.total_times.append(total_time)
        self.hl_times.append(times)
        print(f'AT (HL, {self.coin}), times: {times}, total: {sum(times)}')

    
    def get_performance_metrics(self):
        bin_col_avg, bin_total_avg = self.compute_times(self.bin_times)
        hl_col_avg, hl_total_avg = self.compute_times(self.hl_times)



        print(f'BIN {self.coin} col avg: {bin_col_avg}')
        print(f'HL {self.coin} col avg: {hl_col_avg}')
        print(f'BIN {self.coin} total time: {bin_total_avg}')
        print(f'HL {self.coin} total time: {hl_total_avg}')
    
    def compute_times(self, input):
        dec_places = 1e9
        input = np.array(input)
        input = np.diff(input, axis=1)

        # Calculate column averages
        col_avg = np.floor(np.mean(input, axis=0) / 1_000_000_000 * dec_places) / dec_places

        # Calculate total averages
        total_avg = np.floor(np.mean(np.sum(input, axis=1)) / 1_000_000_000 * dec_places) / dec_places

        return col_avg, total_avg



    async def shutdown(self):
        self.get_performance_metrics()