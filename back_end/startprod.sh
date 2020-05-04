#!/bin/bash

python -m scraper_scheduler.listener &
gunicorn server.main:app -k gevent -w 12 -b 0.0.0.0:5000 --access-logfile -
