#!/bin/bash
# Author: Peter Lee
# This script is used to simulate the data of the TIRI sensor device.

data_dir="./data"
file_name="$(date +%Y%m%d).txt"
file_path="${data_dir}/${file_name}"
if [ ! -f "$file_path" ]; then
    touch "$file_path"
fi

while true; do
    timestamp=$(date +"%T")
    temperature=$(awk -v min=25 -v max=32 'BEGIN{srand(); print rand()*(max-min)+min}')
    humidity=$(awk 'BEGIN{srand(); print rand()*100}')
    resistance=$(jot -r 1 1000 1200)
    concentration=$(jot -r 1 1000 2000)

    echo "${timestamp}，溫度：${temperature}，單位攝氏。C，濕度：${humidity}，%，原始電阻：${resistance}，轉換濃度：${concentration}" >> "$file_path"
    sleep 1
done