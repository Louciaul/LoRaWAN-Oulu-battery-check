from datetime import datetime, timedelta


def analyze(device, client, highly_suspected_uei, low_suspected_uei, TIME_GUARD, MIMIMUM_BATTERY):

    #get the device
    uei = device["distinct"]

    #get the last data of this device
    query = "SELECT last(battery) FROM mqtt_consumer WHERE \"deveui\" = \'" + \
        uei + "\'"

    result = client.query(query, database="dev")

    # check if date of last result is more than X days
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    #get the time stamp of X days ago
    current_timestamp = datetime.now().timestamp()

    date_daysago = datetime.now() - timedelta(days=TIME_GUARD)

    timestamp_daysago = date_daysago.timestamp()

    for point in result.get_points():

        #Get the timestamp of the date of last data

        date_object = datetime.strptime(point["time"], date_format)

        timestamp = date_object.timestamp()

        #test result

        if (timestamp < timestamp_daysago and point["last"] < MIMIMUM_BATTERY):
            # out of battery and out of network
            highly_suspected_uei.append((point["time"], uei, point["last"]))

        elif (timestamp < timestamp_daysago):
            # out of network since X days but battery is okay
            low_suspected_uei.append((point["time"], uei, point["last"]))
