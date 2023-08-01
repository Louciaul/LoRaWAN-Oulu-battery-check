import getpass
import csv
from influxdb import InfluxDBClient
from analyze import analyze
from html import generate_html_page

#in days
TIME_GUARD = 14

#in volt
MIMIMUM_BATTERY = 2.5


def progress_bar(total, progress):
    bar_length = 30
    filled_length = int(round(bar_length * progress / total))
    progressbar = '=' * filled_length + '-' * (bar_length - filled_length)
    percent = round(100.0 * progress / total, 1)
    print(f'Progress: [{progressbar}] {percent}%\r', end='', flush=True)



#credentials

print("Connection the University of Oulu influxDB...")

user_name = input("Please enter your Oulu's influxDB username: ")

user_password = getpass.getpass("Please enter your Oulu's influxDB password: ")



#connection

try:
    client = InfluxDBClient(host="smartcampus-influx.oulu.fi", port=443,
                            username=user_name, password=user_password, ssl=True, verify_ssl=True)



except Exception as error:
    print("Connection failed:", str(error))

print("Connection successful !")



#Number of devices

QUERY = "SELECT COUNT(DISTINCT(deveui)) FROM mqtt_consumer WHERE time < '2022-01-01T00:00:00Z'"

result = client.query(QUERY, database="dev")

for item in result.get_points():
    total_item = item["count"]

#List of devices

QUERY = "SELECT DISTINCT deveui FROM mqtt_consumer WHERE time < '2022-01-01T00:00:00Z'"

result = client.query(QUERY, database="dev")


# list of suspected uei that have ran out of battery
highly_suspected_uei = []
low_suspected_uei = []

# analyze each device
ITERATION = 0


#Check each device
for device in result.get_points():

    progress_bar(total_item, ITERATION)

    #check last data of this device
    analyze(device, client, highly_suspected_uei, low_suspected_uei, TIME_GUARD, MIMIMUM_BATTERY)

    ITERATION = ITERATION + 1

    if ITERATION == 30:
        break

#result file

with open("result_highly_suspicious.csv",'w',newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["time","eui","device_id", "Battery","URL"])
    writer.writerows(highly_suspected_uei)

with open("result_low_suspicious.csv",'w',newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["time","eui","device_id", "Battery","URL"])
    writer.writerows(low_suspected_uei)

generate_html_page("result_highly_suspicious.csv")