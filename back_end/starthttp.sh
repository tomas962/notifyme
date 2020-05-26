#!/bin/bash

gunicorn scraper_scheduler.__main__:app -b 127.0.0.1:40375 --access-logfile - &
gunicorn server.__main__:app -k eventlet -w 1 -b 0.0.0.0:5000 --access-logfile -
