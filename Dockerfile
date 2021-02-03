FROM alpine:3.12

RUN apk add --no-cache \
  libffi \
  python3 \
  py3-pip \
  py3-psycopg2 \
  py3-gunicorn \
  py3-wheel

RUN apk add --no-cache --virtual build-deps build-base libffi-dev openssl-dev python3-dev && \
  pip3 install \
    'django~=2.2.0' \
    'mailmanclient==3.3.2' \
    'postorius==1.3.4' \
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
