import time 
import json
import asyncio
import websockets
import threading

class AutoTrader:
    def __init__(self, coin):
        self.coin = coin
        # self.load_auth()
        # self.check_config()

    async def run(self):
        await asyncio.gather(self.binance_feed(), self.hyperliquid_feed())

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
                print(f'BINANCE({m}): {json.loads(message)}')
                # self.handle_binance(json.loads(message), m)

    async def hyperliquid_feed(self):
        # uri = "wss://api.hyperliquid.xyz/ws"  
        uri = 'wss://api.hyperliquid-testnet.xyz/ws'   

        async with websockets.connect(uri) as websocket:
            subscription_message = {
                "method": "subscribe",
                "subscription": { "type": "l2Book", "coin": self.coin }
                # Add any additional fields specific to your subscription message
            }
            
            await websocket.send(json.dumps(subscription_message))
            n = 0
            msg = await websocket.recv()
            msg2 = await websocket.recv()
            while True:
                message = await websocket.recv()
                n += 1
                print(f'HYPERLIQUID({n}): {json.loads(message)}')
                # self.handle_hyperliquid(json.loads(message), n)



def main():
    trader = AutoTrader("BTC")
    asyncio.run(trader.run())

if __name__ == "__main__":
    main()
