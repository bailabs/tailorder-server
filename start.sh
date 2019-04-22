#!/bin/bash
export FLASK_APP=tailorder
echo "Broadcasted IP Addresses:"
ifconfig | grep "inet addr"
pipenv run flask run --host 0.0.0.0