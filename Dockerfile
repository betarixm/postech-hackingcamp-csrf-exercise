FROM python:3.9-alpine

ENV APP_USER "dreamhack"
ENV APP_PORT 5000

RUN adduser --disabled-password $APP_USER

RUN echo "http://dl-4.alpinelinux.org/alpine/v3.14/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.14/community" >> /etc/apk/repositories

RUN apk update
RUN apk add chromium chromium-chromedriver libffi-dev gcc musl-dev

RUN pip install --upgrade pip
RUN pip install selenium

COPY --chown=$APP_USER . /app
WORKDIR /app

RUN pip install -r requirements.txt

USER $APP_USER
EXPOSE $APP_PORT

CMD ["python", "app.py"]
