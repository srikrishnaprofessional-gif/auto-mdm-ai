from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'stripe_topic',
    'hubspot_topic',
    'quickbooks_topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def consume():
    for message in consumer:
        print("Received:", message.value)

if __name__ == "__main__":
    consume()