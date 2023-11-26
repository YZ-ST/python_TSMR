#!/bin/bash

# sudo pip install gunicorn

sudo gunicorn -w 1 -b 0.0.0.0:8000 main:app
