# import random
# from collections import deque

# class MarketData:
#     def __init__(self, name):
#         self.name = name
#         self.bid = 0
#         self.ask = 0

# class EWMA:
#     def __init__(self, alpha, n):
#         self.alpha = alpha
#         self.n = n
#         self.values = deque(maxlen=n)
#         self.ewma = None

#     def update(self, value):
#         self.values.append(value)
#         if len(self.values) < self.n:
#             return None

#         if self.ewma is None:
#             self.ewma = sum(self.values) / len(self.values)
#         else:
#             self.ewma = (1 - self.alpha) * self.ewma + self.alpha * value

#         return self.ewma

# # Initialize market data feeds
# binance = MarketData("Binance")
# exchange_a = MarketData("Exchange_A")

# # Initialize EWMA calculator with alpha=0.2 and n=10
# ewma_bid_diff = EWMA(0.2, 10)
# ewma_ask_diff = EWMA(0.2, 10)

# while True:
#     # Simulate market data updates (replace this with real data)
#     binance.bid = random.uniform(100, 101)
#     binance.ask = random.uniform(102, 103)
#     exchange_a.bid = random.uniform(99, 100)
#     exchange_a.ask = random.uniform(101, 102)

#     # Calculate bid and ask differences
#     bid_diff = binance.bid - exchange_a.bid
#     ask_diff = binance.ask - exchange_a.ask

#     # Update EWMA
#     ewma_bid = ewma_bid_diff.update(bid_diff)
#     ewma_ask = ewma_ask_diff.update(ask_diff)

#     if ewma_bid is not None and ewma_ask is not None:
#         # Calculate the fair price for quoting
#         fair_bid = binance.bid - ewma_bid
#         fair_ask = binance.ask - ewma_ask

#         # Calculate mid-price for Binance
#         binance_mid = (binance.bid + binance.ask) / 2

#         # Perform trading logic here based on the fair prices
#         print(f"Binance Bid: {binance.bid:.2f}, Binance Ask: {binance.ask:.2f}, Binance Mid: {binance_mid:.2f}")
#         print(f"Exchange_A Bid: {exchange_a.bid:.2f}, Exchange_A Ask: {exchange_a.ask:.2f}")
#         print(f"EWMA Bid Difference: {ewma_bid:.2f}, EWMA Ask Difference: {ewma_ask:.2f}")
#         print(f"Fair Bid: {fair_bid:.2f}, Fair Ask: {fair_ask:.2f}")
#         print("-----")

import collections
import numpy as np
import time  # Simulate real-time data

class OrderBook:
    def __init__(self, ewma_window_size):
        self.bids = collections.deque(maxlen=ewma_window_size)
        self.asks = collections.deque(maxlen=ewma_window_size)
        self.ewma_window_size = ewma_window_size
        self.fair_bid = None
        self.fair_ask = None

    def update_order_book(self, data):
        self.bids.append(data['bid'])
        self.asks.append(data['ask'])

    def calculate_ewma(self):
        if len(self.bids) >= self.ewma_window_size:
            ewma_bid = np.average(self.bids, weights=np.linspace(1, 0, len(self.bids)))
            ewma_ask = np.average(self.asks, weights=np.linspace(1, 0, len(self.asks)))
            return ewma_bid, ewma_ask
        else:
            return None, None

    def calculate_fair_prices(self, external_bid, external_ask):
        ewma_bid, ewma_ask = self.calculate_ewma()
        if ewma_bid is not None and ewma_ask is not None:
            self.fair_bid = external_bid - ewma_bid
            self.fair_ask = external_ask - ewma_ask

    def display_info(self):
        ewma_bid, ewma_ask = self.calculate_ewma()
        if ewma_bid is not None and ewma_ask is not None:
            print(f"Current Bid: {self.bids[-1]:.2f}, Current Ask: {self.asks[-1]:.2f}")
            print(f"EWMA Bid Difference: {ewma_bid:.2f}, EWMA Ask Difference: {ewma_ask:.2f}")
            
            if self.fair_bid is not None:
                print(f"Fair Bid: {self.fair_bid:.2f}", end=", ")
            else:
                print("Fair Bid: None", end=", ")

            if self.fair_ask is not None:
                print(f"Fair Ask: {self.fair_ask:.2f}")
            else:
                print("Fair Ask: None")
            print("-----")



def main():

    # Usage
    ewma_window_size = 5
    binance_order_book = OrderBook(ewma_window_size=ewma_window_size)
    exchange_a_order_book = OrderBook(ewma_window_size=ewma_window_size)

    # Simulated loop for real-time data (replace these with real data)
    for i in range(20):  # Simulating 20 updates
        binance_data = {'bid': 1678.7 + np.random.normal(0, 1), 'ask': 1679.3 + np.random.normal(0, 1)}
        exchange_a_data = {'bid': 1679.0 + np.random.normal(0, 1), 'ask': 1680.0 + np.random.normal(0, 1)}

        
        binance_order_book.update_order_book(binance_data)
        exchange_a_order_book.update_order_book(exchange_a_data)

        # Calculate fair prices based on each other's prices
        binance_order_book.calculate_fair_prices(exchange_a_data['bid'], exchange_a_data['ask'])
        exchange_a_order_book.calculate_fair_prices(binance_data['bid'], binance_data['ask'])

        # Display information
        print("Binance Order Book:")
        binance_order_book.display_info()
        
        print("Exchange_A Order Book:")
        exchange_a_order_book.display_info()

        time.sleep(1)  # Sleep for 1 second to simulate real-time data updates


if __name__ == '__main__':
    main()