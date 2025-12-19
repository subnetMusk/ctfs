#!/usr/bin/env python3
import random
import os
import time

with open("top_secret", "rb") as f:
    content = f.read()

current_time = int(time.time())

for i in range(len(str(current_time)) - 5, len(str(current_time)) + 5):
    seed = content[i:] ^ [0x88]
