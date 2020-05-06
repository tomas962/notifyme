#!/bin/bash

python -m scraper_scheduler.listener &
gunicorn server.__main__:app -k gevent -w 6 -b 0.0.0.0:5000 --access-logfile -
