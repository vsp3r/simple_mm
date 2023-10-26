from tardis_dev import datasets
import pandas as pd

# datasets.download(
#     exchange="binance-futures",
#     data_types=[
#         # "incremental_book_L2",
#         # "trades",
#         "quotes",
#         # "derivative_ticker",
#         # "book_snapshot_25",
#         # "liquidations"
#     ],
#     from_date="2023-10-01",
#     to_date="2023-10-01",
#     # symbols=["BTC-PERPETUAL", "ETH-PERPETUAL"],
#     symbols=['solusdt']
#     # api_key="YOUR API KEY (optionally)",
# )

perp_quotes = pd.read_csv(f'datasets/bin_futures.csv.gz', compression='gzip')
print(perp_quotes.head())