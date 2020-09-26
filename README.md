# Geocurrency

API service that provides 
- List of countries according to ISO-3166
- List of currencies according to ISO-4217
- List of conversion rates fetched from BCE APIs
- Custom conversion rates support by key
- List of units and Unit Systems
- Conversions from from and to currencies
- Conversion from and to units

## Install

### Preparation
set the following environment variables
- VENV_DIR: virtualenv directory
- GEOCURRENCY_SRC: Source directory for geocurrency
- GEOCURRENCY_DB_NAME: database name
- GEOCURRENCY_DB_USERNAME: database username
- GEOCURRENCY_DB_PASSWORD: database password

### Docker

Generate packages from "deployment/scripts/packages.sh"

Folder "deployment/docker" provides an easy to setup docker environment running 
- Django app
- Redis cache
- Postgres backend
- nginx load balancer 

just run "docker-compose up"

### Local environment

1. install a python virtual environment
2. install required packages from deployment/docker/api/config/requirements.txt
3. link deployment/dev to your virtual environment
4. link each module (e.g. modules/converters/) to venv/dev/ 

### Using packages

ENV_NAME=<env_name>
PROJECT_NAME=<project_name>
PYTHON_VERSION=/usr/bin/python3 # use pypy :)
virtualenv -p $PYTHON_VERSION $ENV_NAME
cd $ENV_NAME
source bin/activate
pip install -f <path_to_packages> geocurrency
django-admin startproject $PROJECT_NAME
cp site_packages/geocurrency/core/settings.example.py $PROJECT_NAME/$PROJECT_NAME/settings.py
cp site_packages/geocurrency/core/urls.example.py $PROJECT_NAME/$PROJECT_NAME/urls.py
cd $PROJECT_NAME
cp 
