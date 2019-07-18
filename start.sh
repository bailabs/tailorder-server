#!/bin/bash
export FLASK_APP=tailorder
echo "Broadcasted IP Addresses:"
ifconfig | grep "inet addr"

echo "--------------------------------------------"
echo "--------------------------------------------"
pipenv run python start_app.py
