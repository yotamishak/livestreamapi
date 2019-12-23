#!/bin/bash

##USERNAME=bsdoherty2007@hotmail.com
##PASSWORD=Anomaly1

gunicorn -b 127.0.0.1:5000 quickflash:app &

~/ngrok http 5000 --subdomain freebets &

python3 monitor.py 



































