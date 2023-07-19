import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def analyze(device, client, suspected_uei):

    uei = device["distinct"]
    query = "SELECT last(battery) FROM mqtt_consumer WHERE \"deveui\" = \'" + \
        uei + "\'"

    result = client.query(query, database="dev")

    # check if date of last result is more than 7 days
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    current_timestamp = datetime.now().timestamp()

    date_7daysago = datetime.now() - timedelta(days=7)

    timestamp_7daysago = date_7daysago.timestamp()

    for point in result.get_points():

        date_object = datetime.strptime(point["time"], date_format)

        timestamp = date_object.timestamp()

        if (timestamp < timestamp_7daysago or point["last"] < 2.5):
            # out of battery or out of network
            suspected_uei.append((point["time"], uei, point["last"]))
