#!/bin/bash
rm packages/*
rm deployment/docker/geocurrency/packages/*
cd src || exit
python setup.py sdist bdist_wheel
cp dist/* ../packages
cp dist/*.whl ../deployment/docker/geocurrency/packages
rm -R build dist geocurrency.egg-info
cd ..