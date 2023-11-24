import websockets
import asyncio
import orjson

# class WsConnector:
#     def __init__(self, symbols, queues):
#         self.symbols = symbols
#         self.queues = queues
#         self.running = True

#     async def run(self):
#         pass
#         # await self.connect()
    
#     async def connect(self, ws_url):
#         async with websockets.connect(ws_url) as ws:
#             await asyncio.gather(*(self.subscribe(ws, coin.lower() + 'usdt')
#                                     for coin in self.symbols))
                
#             while self.running:
#                 message = await ws.recv()
#                 asyncio.create_task(self.process_data(message))
#     async def subscribe(self, ws, coin):
#         pass

#     async def process_data(self, message):
#         pass

def main(ws_object):
    asyncio.run(ws_object.run())
            

