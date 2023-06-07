# kafka-ml-training

## Run Kafka
```bash
docker-compose up
```

## Install Libraries
```bash
python -m pip install kafka-python river
```

## Run the Producer
```bash
python producer.py
```

## Train a Model Using a Kafka Consumer
```bash
python consumer.py
```
