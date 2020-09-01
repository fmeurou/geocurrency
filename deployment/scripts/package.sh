#!/bin/bash
source $VENV_DIR/dev/bin/activate
for MODULE in 'core' 'converters' 'countries' 'currencies' 'rates' 'units'
do
    cd $GEOCURRENCY_SRC/modules/$MODULE
    /usr/bin/find ./ -name "*.whl" -delete
    python setup.py bdist_wheel
done

cd $GEOCURRENCY_SRC
/bin/mkdir -p  $GEOCURRENCY_SRC/deployment/docker/api/packages
/usr/bin/find  $GEOCURRENCY_SRC/modules -name "*.whl" -exec /bin/cp "{}" $GEOCURRENCY_SRC/deployment/docker/api/packages/ \;
