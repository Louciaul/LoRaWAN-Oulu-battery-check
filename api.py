import requests

#API URL and HEADERS
URL = "https://smartcampus.oulu.fi/manage/api/devices/getByDeviceId"

HEADERS = {
    "accept": "*/*",
    "Content-Type": "application/json"
}

#Here we ask information the university LoWaRAN API

#we need first to have the uei in the good format

def transform_uei(uei):

    # uppercase
    uppercase_string = uei.upper()

    # cleaning the -
    cleaned_string = uppercase_string.replace('-', '')

    return cleaned_string



#request the id of an uei to the API

def ask_for_id(uei):

    clean_uei = transform_uei(uei)

    id = {
        "deviceId": clean_uei
    }

    try:
        answer = requests.post(URL, headers=HEADERS, json=id)

        #check the answer
        if answer.status_code == 200:
            data = answer.json()
            return data["device"]["_id"]
        else:
            print(f"Request failed {answer.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error during request : {e}")
        return None
