import os
from dotenv import load_dotenv
import pytz

load_dotenv()

TIMEZONE = pytz.timezone('Asia/Taipei')
TIRI_USER=os.environ.get("TIRI_USER")
TIRI_PASSWORD=os.environ.get("TIRI_PASSWORD")
TIRI_AUTH = (TIRI_USER, TIRI_PASSWORD)

DEVICE_NAME=os.environ.get("DEVICE_NAME")
DEVICE_ID=os.environ.get("DEVICE_ID")

DATA_PATH = "./data"

TIRI_API_ENDPOINT=os.environ.get("TIRI_ENDPOINT")
API_PATH_AIR_RECORD=os.environ.get("API_PATH_AIR_RECORD")
API_PATH_HEALTH_CHECK=os.environ.get("API_PATH_HEALTH_CHECK")