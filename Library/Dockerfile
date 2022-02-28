FROM python:3.8.10
ENV PYTHONUNBUFFERED 1
WORKDIR /django_project
ADD . /django_project
RUN pip install -r requirements.txt
EXPOSE 8000