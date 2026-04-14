import logging
import time

logging.basicConfig(level=logging.INFO)

def log(message):
    logging.info(message)

def retry(func, retries=3):
    for i in range(retries):
        try:
            return func()
        except Exception as e:
            log(f"Retry {i+1}: {e}")
            time.sleep(1)
    raise Exception("Failed after retries")