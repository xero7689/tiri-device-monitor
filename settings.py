import os
from dotenv import load_dotenv
import pytz

load_dotenv()

TIRI_USER=os.environ.get('TIRI_USER')
TIRI_PASSWORD=os.environ.get('TIRI_PASSWORD')
TIRI_AUTH = (TIRI_USER, TIRI_PASSWORD)

DEVICE_NAME=os.environ.get("DEVICE_NAME")
DEVICE_ID=os.environ.get("DEVICE_ID")

# Settings For TIRI Sensor .NET Interface
DATA_PATH = os.environ.get("DATA_PATH")
FILE_HEADER = os.environ.get("FILE_HEADER")
FILE_SERIAL_NUM = os.environ.get("FILE_SERIAL_NUM")
FILE_DEVICE_NAME = os.environ.get("FILE_DEVICE_NAME")

TIMEZONE = pytz.timezone('Asia/Taipei')
TIRI_API_ENDPOINT='https://tiriiotsensor.com/'
API_PATH_AIR_RECORD='/smart-dust/air-records/'
API_PATH_HEALTH_CHECK='/ht/'