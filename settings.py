import os
from dotenv import load_dotenv
import pytz

load_dotenv()

TIMEZONE = pytz.timezone('Asia/Taipei')
TIRI_ENDPOINT=os.environ.get("TIRI_ENDPOINT")
TIRI_USER=os.environ.get("TIRI_USER")
TIRI_PASSWORD=os.environ.get("TIRI_PASSWORD")
TIRI_AUTH = (TIRI_USER, TIRI_PASSWORD)

DEVICE_NAME=os.environ.get("DEVICE_NAME")
DEVICE_ID=os.environ.get("DEVICE_ID")

DATA_PATH = "./data"