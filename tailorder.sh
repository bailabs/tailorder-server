#!/bin/bash
export FLASK_APP=tailorder

if [ $1 == 'start' ]
then
    echo 'The app runs on'
    ifconfig | grep 'inet addr'
    pipenv run python start_app.py
fi

if [ $1 == 'install' ]
then
    echo 'Installing the app...'
    pipenv run python install_app.py
fi
