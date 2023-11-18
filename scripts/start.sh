#!/bin/bash


source /home/utkarsh/development/docops/backend/venv/bin/activate



sudo docker run -d --name redis --rm -p 6379:6379 redis:7 > redis.logs &&
/home/utkarsh/elasticsearch-8.10.4/bin/elasticsearch -d > elasticsearch.logs && 
python manage.py runserver 8000 > server.logs &&
celery -A docops worker -l info > celery.log
