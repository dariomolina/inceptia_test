FROM python:3.10.12 AS base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  && apt-get install -y build-essential procps telnet curl unzip wget xvfb tar bzip2 libgtk-3-0 libdbus-glib-1-2 \
  && apt-get install -y python3-dev build-essential \
  && apt-get install -y libpq-dev \
  && apt-get install -y gettext git

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN python -m pip install --upgrade pip
RUN pip install -r /requirements/local.txt

COPY ./compose/local/python/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

WORKDIR /app

EXPOSE 8000

FROM base as local
RUN pip install debugpy -t /tmp ipython && pip install --upgrade 'jedi<0.18.0'
