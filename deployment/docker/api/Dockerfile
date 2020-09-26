FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt update -y && apt upgrade -y
RUN apt install -y supervisor
RUN groupadd apps
RUN mkdir /var/apps /var/apps/bin /var/apps/packages /var/apps/media /var/apps/static /var/apps/logs
RUN useradd -g apps -s /bin/bash -d /var/apps apps
WORKDIR /var/apps
# COPY config/requirements.txt /var/apps/
COPY packages/ /var/apps/packages
# RUN pip install -r requirements.txt
RUN pip install --pre -f /var/apps/packages/ geocurrency
RUN django-admin startproject api
COPY config/settings.py /var/apps/api/settings.py
# TODO: fix path issue on gunicorn
COPY config/settings.py /var/apps/api/api/settings.py
COPY config/urls.py /var/apps/api/urls.py
COPY config/supervisor.conf /etc/supervisor/supervisor.conf
COPY config/api.conf /etc/supervisor/conf.d/api.conf
COPY scripts/gunicorn_start.sh /var/apps/bin/gunicorn_start.sh
RUN chmod +x /var/apps/bin/gunicorn_start.sh
RUN chown -R apps:apps /var/apps
USER apps
RUN python /var/apps/api/manage.py collectstatic
USER root
