#!/bin/bash

cd /home/pi/pathephone

echo "Starting bot at $(date)" >> logs/$(date +%s).txt

python3 main.py 1>>logs/$(date +%s).txt 2>>logs/$(date +%s).txt