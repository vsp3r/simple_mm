# simple_mm

Bin -> HL

# Todos

### Setting up

- [ ] Config parser
- [ ] Auth parser

### Infra

- [ ] Async connect to data feeds
- [ ] Local orderbook (not just dict)

### Trading logic

- [x] Exec mode
- [ ] on_message calc
- [ ] sending updates to risk engine

### Risk Engine
This should be the only thing printing in console when we are trading all 50 coins
- [ ] What parameters to track?


# Process flow (with Locks)

Assuming we have a system with an autotrader per coin, handling 2 data feeds, and we want to trade multiple coins, and have all autotraders interact with a single risk engine

1. Initialize singleton risk engine and lock
2. Start multiprocessing pool, with a process for each coin (if 1-1 is performance intensive, then try 10 coins/traders per process or 5 or smth)
   1. Initialize async websocket feeds (2 total per autotrader)
   2. Set up local orderbooks to locally track each feed
3. On_message of binance feed, compute trade logic, and send order
   1. After logic is done, acquire lock for risk engine
   2. Update risk engine (total long-short, margin, etc.)
   3. Release lock
4. Have global monitoring thread to check for "on the fly" config updates
   1. Acquire lock
   2. Update autotrader's parameters
   3. Release lock
5. Check parameters to make sure they updated correctly
