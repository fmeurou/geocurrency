#!/usr/bin/env python3
import os
import subprocess
from datetime import date
from setuptools import setup, find_packages


def get_version(module):
    version = date.today().strftime('%Y-%m')
    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).rstrip().decode('utf8')
        git_describe = subprocess.check_output(["git", "describe", "--long"]).rstrip().decode('utf8')
        git_tag = git_describe.split('-')[0]
        git_commits = git_describe.split('-')[1]
        if branch == 'master':
            sep = '.'
        else:
            sep = 'dev'
        print(branch, git_tag, sep, git_commits)
        version = '{}{}{}'.format(git_tag, sep, git_commits)
    except (subprocess.CalledProcessError, OSError) as e:
        print('git not installed', e)
    try:
        fp = open('{}/__init__.py'.format(module), 'w')
        fp.write('__version__ = [{}, {}, "{}"]'.format(git_tag.replace('.', ','), git_commits, sep.replace('.', '')))
        fp.close()
    except Exception:
        print('ERROR opening {}/__init__.py'.format(module), os.curdir)
    return version

module = 'geocurrency'

setup(
    name='geocurrency',
    python_requires='>3.8.0',
    version=get_version(module),
    author='Frédéric MEUROU',
    author_email='fm@peabytes.me',
    description='Services for conversions',
    url='https://www.geocurrency.me',
    install_requires=[
        "Django~=3.1.0",
        "django-cors-headers~=3.2.0",
        "django-cors-middleware~=1.5.0",
        "django-createsuperuser",
        "django-extensions~=3.0.0",
        "django-filter~=2.3.0",
        "django-redis~=4.12.0",
        "django-sendfile~=0.3.0",
        "djangorestframework~=3.11.0",
        "drf-yasg~=1.17.0",
        "markdown~=3.0",
        "lxml~=4.0",
        "django_redis~=4.0",
        "pysendfile~=2.0",
        "gunicorn",
        "psycopg2",
        "mysql",
        "pytz",
        "pycountry",
        "countryinfo~=0.1.0",
        "timezonefinder~=4.4.0",
        "iso4217",
        "forex-python~=1.0",
        "Babel~=2.8",
        "Pint~=0.15"
    ],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
    py_modules=[
        'geocurrency.core',
        'geocurrency.countries',
        'geocurrency.currencies',
        'geocurrency.rates',
        'geocurrency.units',
        'geocurrency.converters'
    ],
)
