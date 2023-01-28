FROM python:3.7-bullseye
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY ./docker.env /code/
ADD ./requirements.txt /code/
RUN pip install -r requirements.txt
EXPOSE 8000