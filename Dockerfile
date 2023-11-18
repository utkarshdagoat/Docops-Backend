FROM python:3
ENV DOCKERHOME = /home/utkarsh/development/docops/backend 


RUN mkdir -p $DOCKERHOME


WORKDIR $DOCKERHOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

RUN pip install --upgrade pip

COPY . $DockerHOME  

RUN pip install -r requirements.txt

RUN python manage.py makemigrations files spaces myauth notifications

CMD python manage.py runserver 0.0.0.0:8000
