#!/usr/bin/env zsh

source .venv/bin/activate
python ./manage.py runserver &\
docker compose up
