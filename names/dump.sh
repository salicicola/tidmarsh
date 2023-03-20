#!/bin/bash
cd ..
python3 manage.py dumpdata --format=xml --indent=1 --output=names/fixtures/names.xml names.Name
python3 manage.py dumpdata --format=xml --indent=1 --output=names/fixtures/common_names.xml names.CommonName
python3 manage.py dumpdata --format=xml --indent=1 --output=names/fixtures/metarecords.xml names.SpeciesMeta
cd names

