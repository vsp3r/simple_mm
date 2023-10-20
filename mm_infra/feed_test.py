import asyncio
import websockets
import json

class Feed:
    def __init__(self, coin):
        self.coin = coin
        print(f'init')
    
    async def run(self):
        print(f'start run')
        # loop = asyncio.get_event_loop()
        # print(f'got event loop')
        await asyncio.gather(self.connect_hl())
        # loop.run_until_complete(asyncio.gather(self.connect_hl()))
        print(f'ran loop')

    async def connect_hl(self):
        print(f'started hl connec')
        # uri = "wss://api.hyperliquid.xyz/ws"  
        # uri = 'wss://api.hyperliquid-testnet.xyz/ws'   
        uri = 'wss://api.hyperliquid-testnet.xyz/ws'  

        async with websockets.connect(uri) as websocket:
            print(f'ws conn')
            subscription_message = {
                "method": "subscribe",
                "subscription": { "type": "l2Book", "coin": self.coin }
                # Add any additional fields specific to your subscription message
            }
            print(f'boutta send')
            await websocket.send(json.dumps(subscription_message))
            print(f'sent')
            n = 0
            msg = await websocket.recv()
            msg2 = await websocket.recv()
            print(f'got buffer {msg}')
            while True:
                print(f'started true loop')
                message = await websocket.recv()
                n += 1
                # print(f'HYPERLIQUID({n}): {message}')
                self.handle_hyperliquid(json.loads(message), n)

    def handle_hyperliquid(self, message, n):
        print(f'{n}: {message}')



def main():
    f = Feed("GMT")
    asyncio.run(f.run())

if __name__ == '__main__':
    main()