from datetime import datetime, timedelta
from api import ask_for_id


def analyze(device, client, highly_suspected_uei, low_suspected_uei, time_guard, minimum_battery):

    #get the device
    uei = device["distinct"]

    #get the last data of this device
    query = "SELECT last(battery) FROM mqtt_consumer WHERE \"deveui\" = \'" + \
        uei + "\'"

    result = client.query(query, database="dev")

    # check if date of last result is more than X days
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    #get the time stamp of X days ago

    date_daysago = datetime.now() - timedelta(days=time_guard)

    timestamp_daysago = date_daysago.timestamp()

    for point in result.get_points():

        #Get the timestamp of the date of last data

        date_object = datetime.strptime(point["time"], date_format)

        timestamp = date_object.timestamp()

        #test result

        if (timestamp < timestamp_daysago and point["last"] < minimum_battery):
            # out of battery and out of network

            #get the map url of the device
            id = ask_for_id(uei)
            web_url = "https://smartcampus.oulu.fi/manage/map?activateById=" + id
            highly_suspected_uei.append([point["time"], uei, id, point["last"], web_url])

        elif timestamp < timestamp_daysago:
            # out of network since X days but battery is okay

            #get the map url of the device
            id = ask_for_id(uei)
            web_url = "https://smartcampus.oulu.fi/manage/map?activateById=" + id
            low_suspected_uei.append([point["time"], uei, id, point["last"], web_url])
