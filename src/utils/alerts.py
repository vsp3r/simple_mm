import datetime
import os
import requests
from dotenv import load_dotenv

ENV_PATH = '~/algotrading/alpha/simple_mm/.env'


def post_message(message):
    load_dotenv(dotenv_path=ENV_PATH)
    url = os.getenv("DISCORD_URL")
    current_time = datetime.now()
    message = f'{current_time}: GOT ALERT: {message}'
    payload = {
        "username":"alerts",
        "content":message
    }
    requests.post(url, json=payload)
