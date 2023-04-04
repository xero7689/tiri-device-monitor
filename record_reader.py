import os
import csv
import datetime
from collections import OrderedDict


class RecordReader:
    def __init__(self, file_path, timezone):
        self.file_path = file_path
        self.timezone = timezone

    def parse_row(self, row, record_date):
        # Parse the timestamp, temperature, and unit values from the row
        timestamp_str = row[0]
        temperature_str = row[1].split("：")[1]
        # unit_str = row[2].split("：")[1]
        humidity_str = row[3].split("：")[1]
        resistance_str = row[5].split("：")[1]
        concentration_str = row[6].split("：")[1]

        # Convert the timestamp string to a datetime object
        timestamp = datetime.datetime.strptime(timestamp_str, "%H:%M:%S")
        datetime_obj = datetime.datetime.combine(record_date, timestamp.time())

        # Add the timezone to the datetime object
        datetime_obj_with_tz = self.timezone.localize(datetime_obj)

        # Convert the temperature and humidity strings to floats
        temperature = float(temperature_str)
        humidity = float(humidity_str)

        # Convert the resistance and concentration strings to integers
        resistance = int(resistance_str)
        concentration = int(concentration_str)

        data_obj = {
            "temperature": temperature,
            # "unit": unit_str,
            "humidity": humidity,
            "resistance": resistance,
            "concentration": concentration
        }

        return (datetime_obj_with_tz, data_obj)

    def read_records_from_file(self):
        fn = os.path.basename(self.file_path)
        name, ext = fn.split(".")
        dt_obj = datetime.datetime.strptime(name, '%Y%m%d')
        record_date = dt_obj.date()

        delimiter = "，"
        data = OrderedDict()

        with open(self.file_path, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)
            for row in reader:
                datetime_obj_with_tz, data_obj = self.parse_row(row, record_date)
                data[datetime_obj_with_tz] = data_obj
        return data

    def read_records_last_n_line(self, n, delimiter=","):
        # Open the file in binary mode and move the file pointer to the end of the file
        with open(self.file_path, 'rb') as file:
            file.seek(0, 2)

            # Move the file pointer backwards until we find the start of the n-th last line
            pos = file.tell()
            lines_found = 0
            while pos > 0 and lines_found <= (n+1):
                pos -= 1
                file.seek(pos, 0)
                if file.read(1) == b'\n':
                    lines_found += 1
                    if lines_found == (n+1):
                        break

            # Read the last n lines of the file into a list
            file_contents = file.read().decode('utf-8')

            fn = os.path.basename(self.file_path)
            # name, ext = fn.split(".")
            name = fn.split('_')[-1].split('.')[0]
            dt_obj = datetime.datetime.strptime(name, '%Y%m%d')
            record_date = dt_obj.date()
            data = OrderedDict()

            for row in file_contents.splitlines():
                row = row.split(delimiter)
                datetime_obj_with_tz, data_obj = self.parse_row(row, record_date)
                data[datetime_obj_with_tz] = data_obj

            return data
