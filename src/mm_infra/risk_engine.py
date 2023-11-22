from multiprocessing import Lock, Process
lock = Lock()


# singleton pattern example w/ risk engine
class RiskEngine:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            print("Creating new instance.")
            cls._instance = super(RiskEngine, cls).__new__(cls)

        return cls._instance
    
    def update_risk_engine(self):
        lock.acquire()
        try:
            # updated shared state
            print("updating")
        finally:
            lock.release()
    



# Usage
db1 = RiskEngine()
db2 = RiskEngine()

print(db1 is db2)  # Output: True
