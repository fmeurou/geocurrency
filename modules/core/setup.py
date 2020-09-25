#!/usr/bin/env python3
import subprocess
from datetime import date

import os
from setuptools import setup, find_packages

module = 'geocurrency.core'


def get_version():
    version = date.today().strftime('%Y-%m')
    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).rstrip().decode('utf8')
        git_describe = subprocess.check_output(["git", "describe", "--long"]).rstrip().decode('utf8')
        git_tag = git_describe.split('-')[0]
        git_commits = git_describe.split('-')[1]
        if branch == 'release':
            sep = '.'
        else:
            sep = 'dev'
        print(branch, git_tag, sep, git_commits)
        version = '{}{}{}'.format(git_tag, sep, git_commits)
    except (subprocess.CalledProcessError, OSError) as e:
        print('git not installed', e)
    try:
        fp = open('{}/__init__.py'.format("/".join(module.split('.'))), 'w')
        fp.write('__version__ = [{}, {}, "{}"]'.format(git_tag.replace('.', ','), git_commits, sep.replace('.', '')))
        fp.close()
    except Exception:
        print('ERROR opening {}/__init__.py'.format(module), os.curdir)
    return version


setup(
    name='geocurrency.core',
    version=get_version(),
    author='Frédéric MEUROU',
    author_email='fm@peabytes.me',
    description='Core module',
    url='https://www.geocurrency.me',
    install_requires=[
        "django",
        "django-extensions",
        "djangorestframework",
        "markdown",
        "django-filter",
        "drf-yasg",
        "iso4217",
        "pycountry",
        "pytz",
        "lxml",
        "forex-python",
        "django_redis",
        "django-cors-middleware",
        "timezonefinder",
        "lxml",
        "pysendfile",
        "countryinfo",
        "pint",
        "gunicorn",
        "django-createsuperuser",
        "psycopg2",
        "mysql",
        "Babel"
    ],
    packages=find_packages(),
    package_data={
        'locales': ['locale/*.mo', ],
        'templates': ['templates', ],
        'fixtures': ['fixtures', ],
    },
    include_package_data=True,
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
    py_modules=['geocurrency.core'],
)
