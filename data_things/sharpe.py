import numpy as np
import pandas as pd

# Assuming trade_df contains a 'net_pnl' column that has the net profit/loss for each trade
# Calculate the return per trade
# trade_df['return'] = trade_df['net_pnl'] / trade_df['capital_deployed']
returns= pd.Series([0.00005, 0.00004, 0.00003, 0.00009, 0.00010, 0.00005, 0.00005, 0.0001, 0.00003, 0.00009, 0.00004])


# Calculate mean and standard deviation of returns
mean_return = returns.mean() - (0.005/252)
std_return = returns.std()

# Calculate the Sharpe Ratio, assuming risk-free rate is negligible
sharpe_ratio = mean_return / std_return * np.sqrt(252 * 1440)  # Annualize assuming 252 trading days and 390 minutes per day

print("Sharpe Ratio:", sharpe_ratio)
