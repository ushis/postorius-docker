FROM alpine:3.6

RUN apk add --no-cache \
  python2 \
  py2-pip \
  py2-psycopg2 \
  py-gunicorn

RUN pip2 install \
  'mailmanclient==3.1.1' \
  'postorius==1.1.2' \
  'django==1.11.*' \
  'whitenoise'

RUN addgroup -S postorius && \
  adduser -h /var/lib/postorius -s /bin/sh -S -D postorius postorius

WORKDIR /var/lib/postorius

COPY manage.py settings.py urls.py wsgi.py ./

RUN python manage.py collectstatic --noinput

USER postorius:postorius

EXPOSE 8000

CMD gunicorn --bind '0.0.0.0:8000' --workers 2 wsgi
