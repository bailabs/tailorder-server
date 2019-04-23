#!/bin/bash
export FLASK_APP=tailorder
echo "Broadcasted IP Addresses:"
ifconfig | grep "inet addr"

echo "--------------------------------------------"
echo "--------------------------------------------"
pipenv run python create_instance.py

echo "--------------------------------------------"
echo "--------------------------------------------"
pipenv run flask run --host 0.0.0.0