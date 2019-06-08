#!/bin/bash

source ./env/bin/activate
gunicorn --bind 127.0.0.1:8000 --workers=5 wsgi
