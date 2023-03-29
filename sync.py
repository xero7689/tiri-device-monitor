import sys
import os

from urllib.parse import urljoin
import datetime
import time

import requests

from record_reader import RecordReader
from settings import (TIRI_AUTH, DATA_PATH, TIMEZONE, TIRI_API_ENDPOINT, 
                      API_PATH_AIR_RECORD, API_PATH_HEALTH_CHECK, 
                      DEVICE_NAME, DEVICE_ID,
                      FILE_HEADER, FILE_DEVICE_NAME, FILE_SERIAL_NUM)

AIR_RECORD_ENDPOINT = urljoin(TIRI_API_ENDPOINT, API_PATH_AIR_RECORD)
HEALTH_CHECK_ENDPOINT = urljoin(TIRI_API_ENDPOINT, API_PATH_HEALTH_CHECK)


def is_tiri_server_available():
    try:
        response = requests.get(HEALTH_CHECK_ENDPOINT)
    except requests.exceptions.ConnectionError:
        print("TIRI server unavailable!")
        return False
    return True

def post_air_records(payload):
    try:
        response = requests.post(AIR_RECORD_ENDPOINT, auth=TIRI_AUTH, json=payload)
    except requests.exceptions.ConnectionError:
        print("TIRI server unavailable!")
        return False
    print(f'[POST][+] {payload["timestamp"]}')
    return True


def sync_data():
    payload = {
        "device_name": DEVICE_NAME,
    }

    query_string = f"?limit=1"
    air_record_url_limit_1 = urljoin(AIR_RECORD_ENDPOINT, query_string)
    print(air_record_url_limit_1)

    response = requests.get(air_record_url_limit_1, auth=TIRI_AUTH, data=payload)
    response_obj = response.json()

    if response.status_code == 401:
        print("Invalid credentials!")
        return

    if response.status_code == 200 and response_obj["results"] is not None:
        print(f'Device Name: {DEVICE_NAME}\nDevice ID: ({DEVICE_ID})')
        print(response_obj["results"])

        if response_obj["results"] != []:
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
                #file_timestamp_str = fn.split('.')[0]
                file_timestamp_str = fn.split('_')[-1].split('.')[0]
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


        # Do real-time sync to the latest data file
        # Read every last 3 records (last 3 mins)
        previous_records = []
        while True:
            try:
                # Get current datetime with timezone
                local_dt = datetime.datetime.now()
                local_dt = TIMEZONE.localize(local_dt)

                # Format filename using local_dt
                fn = FILE_HEADER + "_" + FILE_SERIAL_NUM + "_" + FILE_DEVICE_NAME
                fn = fn + "_" + local_dt.strftime('%Y%m%d') + '.txt'
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