import websockets
from websockets.exceptions import ConnectionClosedError
import asyncio
import orjson
import time
from queue import Full


class HyperliquidConnector:
    def __init__(self, symbols, queues):
        self.symbols = symbols
        self.queues = queues

        # self.ws = None
        self.running = True

        self.ws_url = 'wss://api.hyperliquid.xyz/ws'
        self.exchange = 'HYPERLIQUID'
        print(f'HYPERLIQUID coins: {self.symbols}')
        print(f'HYPERLIQUID queues: {self.queues}')

    # def start(self):
    #     asyncio.run(self.run())

    async def run(self):

        await self.connect()

    async def connect(self):
        # print('start hl connect')
        async with websockets.connect(self.ws_url) as ws:
            self.ws = ws
            # print('start hl websocket')
            # try:
            await asyncio.gather(*(self.subscribe(ws, coin)
                                for coin in self.symbols))
        
            while self.running:
                message = await ws.recv()
                times = []
                times.append(time.time_ns())
                asyncio.create_task(self.process_data(message, times))
            # except KeyboardInterrupt:
            #     await self.shutdown(ws)
            # except Exception as e:
            #     print(f'{e}')
                
            # await self.shutdown(ws)
        
    async def subscribe(self, ws, coin):
        subscription_message = {
            "method": "subscribe",
            "subscription": {"type": "l2Book", "coin":coin}
        }
        # print(f'sending hl sub {coin}')
        await ws.send(orjson.dumps(subscription_message).decode('utf-8'))
        # subscription_message = {
        #     "method": "subscribe",
        #     "subscription": {"type": "trades", "coin":coin}
        # }
        # # print(f'sending hl sub {coin}')
        # await ws.send(orjson.dumps(subscription_message))

    async def process_data(self, message, times):
        data = orjson.loads(message)
        # print(message)
        try:
            if 'channel' in data:
                coin = data['data']['coin']
                if coin in self.queues:
                    times.append(time.time_ns())
                    self.queues[coin].put_nowait(('hyperliquid', coin, times, data['data']))
            else:
                pass

            # if data['channel'] == 'trades':
            #     # print(data)
            #     for trade in data['data']:
            #         # print(trade)
            #         self.queue.put_nowait(('hyperliquid', trade['coin'], str(trade)))
            #         with self.size_counter.get_lock():
            #             self.size_counter.value += 1

        except Exception as e:
            print(f"(HYPERLIQUID) {self.symbols} ERROR PROCESSING MESSAGE: {e}\nMessage: {message}")

    async def shutdown(self):
        try:
            await asyncio.gather(*(self.unsubscribe(self.ws, coin)
                                    for coin in self.symbols))
            await self.ws.close()
        except ConnectionClosedError:
            pass
        
    async def unsubscribe(self, ws, coin):
        subscription_message = {
            "method": "subscribe",
            "subscription": {"type": "l2Book", "coin":coin}
        }
        unsub = {
            "method": "unsubscribe",
            "subscription": subscription_message
        }
        await ws.send(orjson.dumps(unsub).decode('utf-8'))

