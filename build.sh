#!/bin/bash
set -e
python3 manage.py collectstatic --noinput
python3 manage.py migrate