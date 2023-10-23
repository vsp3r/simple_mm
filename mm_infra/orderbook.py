# from .types import ExchangeType
# from typing import Dict, Deque, List, NamedTuple    
# from collections import namedtuple


# PriceLevel = namedtuple('PriceLevel', ['px', 'sz', 'n'])
class Orderbook:
    pass

    # """An orderbook object"""
    # def __init__(self, coin: str, exchange: ExchangeType,
    #              px_dec: int, sz_dec: int):

    #         self.bid_prices: List = []
    #         self.bid_levels: Dict[int, PriceLevel(int, int, int)] = {}

    #         self.ask_prices = []
    #         self.ask_levels: Dict[int, PriceLevel(int, int, int)] = {}

    #         self.coin = coin
    #         self.exchange = exchange

            
    # def parse_hl(self, l2book):
    #       levels = data_dict['data']['levels']

    #         named_levels = []

    #         # Convert each inner list to a list of named tuples
    #         for inner_list in levels:
    #             named_inner_list = [PriceLevel(**item) for item in inner_list]
    #             named_levels.append(named_inner_list)

    #         data_dict['data']['levels'] = named_levels




    