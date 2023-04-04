import os
import random
import time

import settings

data_dir = settings.DATA_PATH

# File_1_SensorA_20230318
file_header = settings.FILE_HEADER
file_serial_num = settings.FILE_SERIAL_NUM
file_device_name = settings.FILE_DEVICE_NAME

file_name = file_header + "_" + file_serial_num + "_" + file_device_name
file_name = file_name + "_" + time.strftime("%Y%m%d") + ".txt"

file_path = os.path.join(data_dir, file_name)

if not os.path.exists(file_path):
    open(file_path, "w").close()

while True:
    timestamp = time.strftime("%T")
    temperature = round(random.uniform(25, 32), 2)
    humidity = round(random.random() * 100, 2)
    resistance = random.randint(1000, 1200)
    concentration = random.randint(1000, 2000)

    with open(file_path, "a", encoding="utf-8") as f:
        s = f"{timestamp},{temperature},{humidity},{resistance},{concentration}"
        print(f'[+] {s}')

        f.write(f"{timestamp},溫度：{temperature},單位攝氏。C,濕度：{humidity},%,原始電阻：{resistance},轉換濃度：{concentration}\n")
    
    time.sleep(1)
