#!/bin/bash

python -m scraper_scheduler.listener &
python -m server.main
