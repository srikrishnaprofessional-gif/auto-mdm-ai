import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from kafka import KafkaProducer
import json
import time
from app.ingestion import generate_data

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')
)

def stream():
    while True:
        stripe, hubspot, quickbooks = generate_data()

        for _, row in stripe.iterrows():
            producer.send("stripe_topic", row.to_dict())

        for _, row in hubspot.iterrows():
            producer.send("hubspot_topic", row.to_dict())

        for _, row in quickbooks.iterrows():
            producer.send("quickbooks_topic", row.to_dict())

        print("Streaming batch...")
        time.sleep(5)

if __name__ == "__main__":
    stream()