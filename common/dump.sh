#!/bin/bash
cd ..
python3 manage.py dumpdata --format=xml --indent=1 --output=common/fixtures/towns.xml common.Town
python3 manage.py dumpdata --format=xml --indent=1 --output=common/fixtures/locations.xml common.Location
python3 manage.py dumpdata --format=xml --indent=1 --output=common/fixtures/bugs.xml common.BugRecord
cd common

