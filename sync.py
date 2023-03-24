import sys
import os
import datetime
import time

import requests

from record_reader import RecordReader
from settings import DEVICE_NAME, DEVICE_ID, TIRI_AUTH, DATA_PATH, TIMEZONE

TIRI_URL = "https://tiriiotsensor.com/smart-dust/air-records/?limit=1"
PAYLOAD = {"device_name": DEVICE_NAME}

def is_tiri_server_available():
    try:
        response = requests.get(TIRI_URL, auth=TIRI_AUTH, data=PAYLOAD)
    except requests.exceptions.ConnectionError:
        print("TIRI server unavailable!")
        return False
    return True

def post_air_records(payload):
    AIR_RECORD_URL = "https://tiriiotsensor.com/smart-dust/air-records/"
    try:
        response = requests.post(AIR_RECORD_URL, auth=TIRI_AUTH, json=payload)
    except requests.exceptions.ConnectionError:
        print("TIRI server unavailable!")
        return False
    print(f'[POST][${response.status_code}] {payload["timestamp"]}')
    return True


def sync_data():
    response = requests.get(TIRI_URL, auth=TIRI_AUTH, data=PAYLOAD)
    response_obj = response.json()

    if response.status_code == 401:
        print("Invalid credentials! Please check your AUTH settings in .env")
        return

    if response.status_code == 200 and response_obj["results"] is not None:
        print(f'Device')
        timestamp = response_obj["results"][0]["timestamp"]
        server_dt = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z')

        # Compare server time with local time
        local_dt = datetime.datetime.now()
        local_dt = TIMEZONE.localize(local_dt)
        if server_dt > local_dt:
            print("[Invalid] Data from TIRI server is newer, please check!")
            sys.exit(1)

        # Sync data have not been updated to TIRI server
        # Check if remaining data is newer than the data from TIRI server
        need_update_files = []
        for fn in os.listdir(DATA_PATH):
            file_timestamp_str = fn.split('.')[0]
            file_timestamp = TIMEZONE.localize(datetime.datetime.strptime(file_timestamp_str, '%Y%m%d'))
            if file_timestamp >= server_dt:
                need_update_files.append(fn)

        #
        if need_update_files is not None:
            # Do full sync to need_update_files
            for fn in need_update_files:
                fp = os.path.join(DATA_PATH, fn)
                reader = RecordReader(fp, TIMEZONE)
                print(f'--- {fn} ---')
            print(f'[fake sync] {fn}')

        # Do real-time sync to the latest data file
        # Read every last 3 records (last 3 mins)
        previous_records = []
        while True:
            try:
                # Get current datetime with timezone
                local_dt = datetime.datetime.now()
                local_dt = TIMEZONE.localize(local_dt)

                # Format filename using local_dt
                fn = local_dt.strftime('%Y%m%d') + '.txt'
                fp = os.path.join(DATA_PATH, fn)

                # Check if file exists
                if not os.path.exists(fp):
                    print(f'Todays data file {fn} not found, did the device have been turned on?')
                    time.sleep(5)
                    continue

                # Read last 5 records
                reader = RecordReader(fp, TIMEZONE)
                records = reader.read_records_last_n_line(5)

                # Compare with previous records
                if previous_records == records:
                    print("No new records, skip sync!")
                    time.sleep(5)
                    continue

                # Construct payload and send to TIRI server
                print(f'--- [Sync] {datetime.datetime.now()} ---')
                for sync_ts, sync_data in records.items():
                    temperature = sync_data['temperature']
                    humidity = sync_data['humidity']
                    original_resistance = sync_data['resistance']
                    trans_concentrations = sync_data['concentration']
                    formatted_timestamp = sync_ts.strftime('%Y-%m-%dT%H:%M:%S')
                    payload = {
                        'device': DEVICE_ID,
                        'temperature': temperature,
                        'humidity': humidity,
                        'resistance': original_resistance,
                        'concentration': trans_concentrations,
                        'timestamp': formatted_timestamp
                    }
                    post_air_records(payload)

                previous_records = records
                time.sleep(5)
            except KeyboardInterrupt as ke:
                print("Cancel sync!")
                break


if __name__ == "__main__":
    if is_tiri_server_available():
        sync_data()