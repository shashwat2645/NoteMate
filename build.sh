#!/bin/bash
set -e
python3 -c "import os; print('DATABASE_URL set:', bool(os.getenv('DATABASE_URL')))"
python3 manage.py collectstatic --noinput
python3 manage.py migrate