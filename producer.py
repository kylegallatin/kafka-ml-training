from time import sleep
from json import dumps
import random

from river import datasets
from kafka import KafkaProducer

# create a kafka product that connects to Kafka on port 9092
producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda x: dumps(x).encode("utf-8"),
)

# Initialize the River phishing dataset.
# This dataset contains features from web pages 
# that are classified as phishing or not.
dataset = datasets.Phishing()

# Send observations to the Kafka topic one-at-a-time with a random sleep
for x, y in dataset:
    print(f"Sending: {x, y}")
    data = {"x": x, "y": y}
    producer.send("ml_training_data", value=data)
    sleep(random.random())
