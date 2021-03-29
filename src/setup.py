#!/usr/bin/env python3
import os
import subprocess
from datetime import date

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


def get_version(app):
    version = date.today().strftime('%Y-%m')
    git_tag = "0.0"
    git_commits = "0"
    suffix = "dev"
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"]).rstrip().decode('utf8')
        git_describe = subprocess.check_output(["git", "describe", "--long"]).rstrip().decode(
            'utf8')
        git_tag = git_describe.split('-')[0]
        git_commits = git_describe.split('-')[1]
        if branch == 'master':
            suffix = ''
        else:
            suffix = 'dev'
        print(branch, git_tag, git_commits, suffix)
        version = '{}.{}{}'.format(git_tag, git_commits, suffix)
    except (subprocess.CalledProcessError, OSError) as e:
        print('git not installed', e)
    try:
        fp = open('{}/__init__.py'.format(app), 'w')
        fp.write(
            '__version__ = [{}, {}, "{}"]'.format(git_tag.replace('.', ','), git_commits, suffix))
        fp.close()
    except Exception:
        print('ERROR opening {}/__init__.py'.format(app), os.curdir)
    return version


module = 'geocurrency'

setup(
    name='geocurrency',
    description='Web based services to convert units and currencies.',
    python_requires='>3.8.0',
    version=get_version(module),
    author='Frédéric MEUROU',
    author_email='fm@peabytes.me',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://api.geocurrency.me/swagger/',
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
        # "psycopg2",
        # "mysql",
        "pytz",
        "pycountry",
        "countryinfo~=0.1.0",
        "timezonefinder~=4.4.0",
        "iso4217",
        "forex-python~=1.0",
        "Babel~=2.8",
        "Pint~=0.15",
        "networkx~=2.5.0",
        "sympy~=1.7.0"
    ],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Environment :: Web Environment",
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Framework :: Django :: 3.1",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
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
