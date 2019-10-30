#!/bin/bash

gunicorn -b 127.0.0.1:5000 quickflash:app &

autossh -M -0 -R freebets:80:localhost:5000 serveo.net &

python3 monitor.py 



































