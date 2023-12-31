import websockets
import asyncio
import orjson
import time


class BinanceConnector:
    def __init__(self, symbols, queues):
        self.symbols = symbols
        self.queues = queues
        
        self.ws_url = 'wss://fstream.binance.com/ws'
        print(f'BINANCE coins: {self.symbols}')
        print(f'BINANCE queues: {self.queues}')
    
    # def start(self):
    #     asyncio.run(self.run())

    async def run(self, shutdown_event):
        # print('starting BINANCE run')
        # await asyncio.gather(
        #     self.connect_feed()
        # )
        await self.connect(shutdown_event)

    async def connect(self, shutdown_event):
        # print('start binance connect')
        async with websockets.connect(self.ws_url) as ws:
            # self.ws = ws
            # print('start binance ws')
            try:
                await asyncio.gather(*(self.subscribe(ws, coin.lower() + 'usdt')
                                    for coin in self.symbols))
                
                while not shutdown_event.is_set():
                    message = await ws.recv()
                    times = []
                    times.append(time.time_ns())
                    asyncio.create_task(self.process_data(message, times))
            
            except KeyboardInterrupt:
                await self.shutdown(ws)
            except Exception as e:
                print(f'{e}')
                
            await self.shutdown(ws)



    async def subscribe(self, ws, coin):
        subscription_msg = {
            "method":"SUBSCRIBE",
            "params":[
                coin+"@depth5@0ms"
                # coin+"@aggTrade",
                # coin+"@markPrice@1s",
                # coin+"bookTicker"
            ],
            "id":1
        }
        # print(f'sending sub {subscription_msg}')
        await ws.send(orjson.dumps(subscription_msg).decode('utf-8'))
        # _ = await ws.recv() # drop first message

    async def process_data(self, message, times):
        data = orjson.loads(message)
        try:
            # Check if the keys exist in the data
            if 'e' in data and 's' in data:
                coin = data['s'][:-4]
                if coin in self.queues:  # Check if the coin is in the queues
                    times.append(time.time_ns())
                    self.queues[coin].put_nowait(('binance', coin, times, data))
            else:
                pass

        except Exception as e:
            print(f"(BINANCE) {self.symbols} Error processing message: {e}\nMessage: {message}")

    async def shutdown(self, ws):
        await asyncio.gather(*(self.unsubscribe(ws, coin)
                                  for coin in self.symbols))
        ws.close()
        
    async def unsubscribe(self, ws, coin):
        unsub = {
            "method":"UNSUBSCRIBE",
            "params":[
                coin+"@depth5@0ms"
                # coin+"@aggTrade",
                # coin+"@markPrice@1s",
                # coin+"bookTicker"
            ],
            "id":1
        }
        await ws.send(orjson.dumps(unsub).decode('utf-8'))



