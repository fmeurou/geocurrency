#!/bin/bash
rm packages/*
rm deployment/docker/api/packages/*
cd src || exit
python setup.py bdist_wheel
cp dist/*.whl ../packages
cp dist/*.whl ../deployment/docker/api/packages
rm -R build dist geocurrency.egg-info
cd ..