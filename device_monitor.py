import os
import random
import time

data_dir = "./data"
file_name = time.strftime("%Y%m%d") + ".txt"
file_path = os.path.join(data_dir, file_name)

if not os.path.exists(file_path):
    open(file_path, "w").close()

while True:
    timestamp = time.strftime("%T")
    temperature = random.uniform(25, 32)
    humidity = random.random() * 100
    resistance = random.randint(1000, 1200)
    concentration = random.randint(1000, 2000)

    with open(file_path, "a") as f:
        f.write(f"{timestamp}，溫度：{temperature}，單位攝氏。C，濕度：{humidity}，%，原始電阻：{resistance}，轉換濃度：{concentration}\n")
    
    time.sleep(1)
