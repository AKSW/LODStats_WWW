LODStatsWWW uses LODStats (https://github.com/AKSW/LODStats) to compute
various configurable statistics about datasets adhering to the Resource
Description Framework (RDF).
Datasets can either be entered manually, via a RESTful webservice or may
automatically be synced from a CKAN (http://ckan.org/) instance.

Installation and Setup
======================

Install LODStats:
    https://github.com/AKSW/LODStats

Python virtualenv:
    $ workon lodstats
    $ cdvirtualenv

Check for altered prompt with the virtual environment and change directory
    (lodstats)$ cd src

Copy RDF.py to the local installation:
    $ dpkg-query -L python-librdf
    $ mkdir RDF
    $ cp /usr/lib/python2.7/dist-packages/Redland.so RDF/
    $ cp /usr/lib/python2.7/dist-packages/RDF.py RDF/
    $ add2virtualenv ./RDF

Clone git repository:
    (lodstats)$ git clone https://github.com/AKSW/LODStats_WWW.git && cd LODStats_WWW

Install dependencies:
    (lodstats-env)$ pip install --pre -r requirements.txt

Create DB:
    $ sudo -u postgres createuser -S -D -R -P lodstats
    $ sudo -u postgres createdb -O lodstats lodstats

Run setup.py egg_info:

    (lodstats-env)$ python setup.py egg_info

Make a config file as follows::

    (lodstats-env)$ paster make-config rdfstats production.ini

Tweak the config file as appropriate and then setup the application::

    (lodstats-env)$ paster setup-app production.ini

Then you are ready to go:
    (lodstats-env)$ paster serve production.ini

Direct your browser to http://localhost:5000/
