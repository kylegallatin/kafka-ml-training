from json import loads
from time import sleep

from kafka import KafkaConsumer

from river import linear_model
from river import compose
from river import preprocessing
from river import metrics

# use rocauc as the metric for evaluation
metric = metrics.ROCAUC()

# create a simple LR model with a scaler
model = compose.Pipeline(
    preprocessing.StandardScaler(), linear_model.LogisticRegression()
)

# create our Kafka consumer
consumer = KafkaConsumer(
    "ml_training_data",
    bootstrap_servers=["localhost:9092"],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="my-group-id",
    value_deserializer=lambda x: loads(x.decode("utf-8")),
)

# use each event to update our model and print the metrics
for event in consumer:
    event_data = event.value
    try:
        x = event_data["x"]
        y = event_data["y"]
        y_pred = model.predict_proba_one(x)
        model.learn_one(x, y)
        metric.update(y, y_pred)
        print(metric)
    except:
        print("Processing bad data...")
