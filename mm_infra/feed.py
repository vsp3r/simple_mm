# import websockets
import websockets
import asyncio
import logging
import json
import threading

# from .types import ExchangeType

class DataFeed:
    def __init__(self, coin, callbacks):
        # super().__init__()
        # self.url = url
        self.coin = coin
        self.callbacks: tuple = callbacks #(hl_handler, bin_handler)
        # self.exchange = exchange
        print(f'Intialized {coin} feed')
        # if exchange:
        #     self.binance_feed(url, coin, callback)
        # else:
        #     self.hyperliquid_feed(url, coin, callback)
        # pass

   
    async def hyperliquid_feed(self):
        url = "wss://api.hyperliquid.xyz/ws"
        print(f'starting hl for {self.coin} and url: {url}')
        async with websockets.connect(url) as websocket:
            subscription_message = {
                "method": "subscribe",
                "subscription": {"type": "l2book", "coin":self.coin}
            }

            await websocket.send(json.dumps(subscription_message))
            print(f'sent sub')
            msg = await websocket.recv()
            msg2 = await websocket.recv()
            print(f'received buffers {msg} + {msg2}')
            n = 0
            while True:
                message = await websocket.recv()
                n += 1
                # print(f'HYPERLIQUID({n}): {message}')
                self.callbacks[0](json.loads(message), n)
    
    async def binance_feed(self):
        uri = 'wss://fstream.binance.com/ws'  
        async with websockets.connect(uri) as websocket:
            c = self.coin.lower() + 'usdt'
            level = 5
            speed = 0
            stream = f'{c}@depth{level}@{speed}ms'
            stream = [stream]

            subscription_message = {
                "method":"SUBSCRIBE",
                "params":stream,
                'id':1
            }
            await websocket.send(json.dumps(subscription_message))

            m = 0
            msg = await websocket.recv()
            while True:
                m += 1
                message = await websocket.recv()
                # print(f'BINANCE({m}): {message}')
                self.callbacks[1](json.loads(message), m)
            
    async def run(self):
        print('Started datafeed async run')
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(asyncio.gather(self.hyperliquid_feed()))
        await asyncio.gather(
            self.hyperliquid_feed(),
            self.binance_feed()
        )

# def printing(message):
#     print(message)

# def main():
#     print('running raw feed')
#     feed = DataFeed("wss://api.hyperliquid.xyz/ws",
#                     "BTC",
#                     printing,
#                     "3")
#     feed.run()

# if __name__ == "__main__":
#     main()