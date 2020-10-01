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
Create a "packages" directory at the root of the project
Generate packages from "build.sh"

Folder "deployment/docker" provides an easy to setup docker environment running 
- Django app
- Redis cache
- Postgres backend
- nginx load balancer 

just run "docker-compose up"

### Using packages

ENV_NAME=<env_name>
PROJECT_NAME=<project_name>
PYTHON_VERSION=/usr/bin/python3 # use pypy :)
virtualenv -p $PYTHON_VERSION $ENV_NAME
cd $ENV_NAME
source bin/activate
pip install geocurrency
django-admin startproject $PROJECT_NAME
cp site_packages/geocurrency/core/settings.example.py $PROJECT_NAME/$PROJECT_NAME/settings.py
cp site_packages/geocurrency/core/urls.example.py $PROJECT_NAME/$PROJECT_NAME/urls.py
cd $PROJECT_NAME

Adapt settings and urls for your environment.

## Usage

### Routes
This package provides a OpenAPI documentation. See urls.example.py for a setup example. 

### Authentication
The app provides most services without authentication. 
Authentication is required to store custom conversion rates and custom conversion units.
By default, the app is configured to allow authentication through an API token that can be generated for a user on the 
Django admin site.

API authentication can be achieved with an Authorization header header with value Token <APIToken>
curl -H "Authorization: Token <user token>".

### Language support
The app supports translations for countries and units in 15 languages. More languages should be available soon.

### Fetch rates
The app uses python-forex as a mecanism to fetch currency rates. 
A django command is available to fetch rates from command line :
$ ./manage.py fetch_rates

## About 

### Project goals

Web based services to convert units and currencies. 
GeoCurrency is a portmanteau of the words "Geocoding" and "Currency" which where the main goals of the initial project

### Project website
A live version of this service is available at <https://api.geocurrency.me>.

### Leadership

This project is maintained by Frédéric Meurou <fm@peabytes.me>.
