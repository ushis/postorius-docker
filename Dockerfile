FROM alpine:3.8

RUN apk add --no-cache \
  python3 \
  py3-pip \
  py3-psycopg2 \
  py3-gunicorn

RUN apk add --no-cache --virtual build-deps build-base python3-dev && \
  pip3 install \
    'mailmanclient==3.2.2' \
    'postorius==1.2.4' \
    'whitenoise' && \
  apk del build-deps

RUN addgroup -S postorius && \
  adduser -h /var/lib/postorius -s /bin/sh -S -D postorius postorius

WORKDIR /var/lib/postorius

COPY manage.py settings.py urls.py wsgi.py ./

RUN python3 manage.py collectstatic --noinput

USER postorius:postorius

EXPOSE 8000

CMD gunicorn --bind '0.0.0.0:8000' --workers 2 wsgi
