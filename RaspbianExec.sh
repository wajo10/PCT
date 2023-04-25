#!/bin/bash
cd "Server API"
node index.js &
cd ..
cd "Controller"
python3 main.py &
cd ..
cd "WebApp"
fuxa &
cd ..
