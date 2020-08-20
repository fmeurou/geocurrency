#!/bin/bash

python /var/apps/api/manage.py migrate
python /var/apps/api/manage.py loaddata base_user