# import websockets
import websocket
import asyncio
import logging
import json
import threading

from .types import Exchange

class DataFeed(threading.Thread):
    def __init__(self, url, coin, callback,
                 exchange):
        super().__init__()
        self.url = url
        self.coin = coin
        self.callback = callback
        self.exchange = exchange

        if exchange:
            self.hyperliquid_feed(url, coin, callback)
        else:
            self.binance_feed(url, coin, callback)

    async def hyperliquid_feed(self, url: str, coin: dict, callback: function):
        
        async with websockets.connect(url) as websocket:
            subscription_message = {
                "method": "subscribe",
                "subscription": {"type": "l2book", "coin":self.coin}
            }
            await websocket.send(json.dumps(subscription_message))
            
