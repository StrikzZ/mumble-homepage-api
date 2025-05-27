#!/bin/sh
#Using this script to start the API allows environmental variables to take effect

gunicorn -w 1 -b 0.0.0.0:${API_PORT:-6504} api:app