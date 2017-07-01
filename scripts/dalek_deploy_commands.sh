#!/usr/bin/env bash
set -e  # abort if one command fails

su blackhole

# Pull the latest commit
cd /home/blackhole/blackhole
git pull origin master

# Install the requirements
source /home/blackhole/venv/bin/activate
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

exit

# Restart gunicorn
supervisorctl restart blackhole
