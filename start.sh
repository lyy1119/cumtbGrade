#!/bin/bash

# 启动 Nginx
nginx &
python3 main.py
wait
