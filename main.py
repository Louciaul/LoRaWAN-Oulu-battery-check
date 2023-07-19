from influxdb import InfluxDBClient
from analyze import *
import time
import getpass


def progress_bar(total, progress):
    bar_length = 30
    filled_length = int(round(bar_length * progress / total))
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    percent = round(100.0 * progress / total, 1)
    print(f'Progress: [{bar}] {percent}%\r', end='', flush=True)


print("Connection the University of Oulu influxDB...")

user_name = input("Please enter your Oulu's influxDB username: ")

user_password = getpass.getpass("Please enter your Oulu's influxDB password: ")

try:
    client = InfluxDBClient(host="smartcampus-influx.oulu.fi", port=443,
                            username=user_name, password=user_password, ssl=True, verify_ssl=True)

except Exception as error:
    print("Connexion failed:", str(error))

print("Connexion successful !")


query = "SELECT COUNT(DISTINCT(deveui)) FROM mqtt_consumer WHERE time < '2022-01-01T00:00:00Z'"

result = client.query(query, database="dev")

for item in result.get_points():
    total = item["count"]

query = "SELECT DISTINCT deveui FROM mqtt_consumer WHERE time < '2022-01-01T00:00:00Z'"

result = client.query(query, database="dev")

# list of suspected uei that have ran out of battery
suspected_uei = []

# analyze each device
device_number = 0

for device in result.get_points():
    progress_bar(total, device_number)
    analyze(device, client, suspected_uei)
    device_number = device_number + 1

for uei in suspected_uei:
    print(uei)
