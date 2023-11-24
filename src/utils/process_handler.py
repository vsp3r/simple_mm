import signal
import asyncio

class ProcessWrapper:
    def __init__(self, target):
        self.target = target
        

    def setup_signal_handling(self):
        for sig in ('SIGINT', 'SIGTERM'):
            self.loop.add_signal_handler(getattr(signal, sig), self.stop_loop)

    def stop_loop(self):
        self.target.running = False
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        for task in tasks:
            task.cancel()

        shutdown_task = asyncio.create_task(self.target.shutdown())

        def on_shutdown(future):
            self.loop.stop()
        
        shutdown_task.add_done_callback(on_shutdown)

    # async def run_target(self):
    #     await self.target.run()  # Assuming target.run is an async function

    def run(self):
        self.loop = asyncio.new_event_loop()
        self.setup_signal_handling()
        asyncio.set_event_loop(self.loop)
        try:
            self.loop.create_task(self.target.run())
            self.loop.run_forever()
        except Exception as e:
            pass
        finally:
            # self.loop.close()
            pass
            # try:
            #     self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            # finally:
            #     self.loop.close()