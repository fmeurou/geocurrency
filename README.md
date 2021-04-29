# django-physics

Django APIs for Physics

## Countries
 List of countries according to ISO-3166 and details of a country based on PyCountry module.
 
## Currencies
 List of currencies based on ISO-4217

## Currencies conversion rates
List of conversion rates fetched from BCE APIs. 
The module provides a command line for fetching rates from different services. Custom services can be added.
Custom conversion rates can be created by registered users.

## Systems and Units
List of unit systems, dimensions, and units based on the excellent Pint library. 
Custom units can be created by registered users.

## Conversions
Conversions between currencies, with batch conversion support.
Conversions between units in a unit system with batch conversion support

## Evaluation
Check the syntax and dimension of a formula with units, and evaluate its value

## Install

pip install geocurrency

## Docker

doocker is available at fmeurou/geocurrency

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
