# import multiprocessing
# from src.execution.autotrader import AutoTrader
# from src.exchanges.binance import BinanceConnector
# from src.exchanges.hyperliquid import HyperliquidConnector



# def main(coins, exchanges, coins_per_feed): # return ws_processes, trader_processes
    

    # return ws_processes, autotrader_processes
    # # print(coin_pools)
    # for group in coin_pools:
    #     bin_queues_group = {coin:binance_queues[coin] for coin in group}
    #     binance_ws_process = multiprocessing.Process(target=start_binance_websocket,
    #                                                  args=(group, bin_queues_group))
    #     binance_ws_process.start()
    #     ws_processes.append(binance_ws_process)
    #     for exchange in exchanges:
    #         dex_queues_group = {coin:dex_queues[exchange][coin] for coin in group}
    #         dex_ws_process = multiprocessing.Process(target=start_dex_websocket,
    #                                                  args=(group, exchange, dex_queues_group))
    #         dex_ws_process.start()
    #         ws_processes.append(dex_ws_process)

    #         # Init Autotrader Processes
    #         for coin in group:
    #             autotrader_process = multiprocessing.Process(target=start_autotrader,
    #                                                          args=(exchange, coin, 
    #                                                                dex_queues[exchange][coin],
    #                                                                binance_queues[coin]))
    #             process_key = (exchange, coin)
    #             # print(f'in loop {process_key}')
    #             autotrader_process.start()
    #             autotrader_processes[process_key] = autotrader_process

    # for p in ws_processes:
    #     p.join()
    # for p in autotrader_processes.values():
    #     p.join()


# def autotrader_wrapper(autotrader_obj):
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     try:
#         loop.run_until_complete(autotrader_obj.run())
#     except Exception as e:
#         print(f"Autotrader process error: {e}")
#         raise
#     finally:
#         try:
#             loop.run_until_complete(loop.shutdown_asyncgens())
#         finally:
#             loop.close()

# def ws_wrapper(ws):
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     try:
#         loop.run_until_complete(ws.run())
#     except Exception as e:
#         print(f"Autotrader process error: {e}")
#         raise
#     finally:
#         try:
#             loop.run_until_complete(loop.shutdown_asyncgens())
#         finally:
#             loop.close()



# def shutdown_handler(processes):
#     print("Gracefully shutting down")
#     for process in processes:
#         process.terminate()
#     for process in processes:
#         process.join()

# signal.signal(signal.SIGINT, lambda sig, frame: shutdown_handler(ws_processes + autotrader_processes))