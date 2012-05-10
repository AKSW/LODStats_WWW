LODStatsWWW uses LODStats (https://github.com/AKSW/LODStats) to compute
various configurable statistics about datasets adhering to the Resource
Description Framework (RDF).
Datasets can either be entered manually, via a RESTful webservice or may
automatically be synced from a CKAN (http://ckan.org/) instance.

Installation and Setup
======================

Extract (fetch/move) to ~/lodstats_www:
    $ git clone https://github.com/jandemter/lodstats_www lodstats_www

Install dependencies:
    $ sudo apt-get install python-librdf postgresql python-psycopg2

Create DB:
    $ sudo -u postgres createuser -S -D -R -P lodstats
    $ sudo -u postgres createdb -O lodstats lodstats

Python virtualenv:
    $ virtualenv --system-site-packages pyenv-lodstats
    $ . pyenv-lodstats/bin/activate

Check for altered prompt with the virtual environment and change directory
    (lodstats-env)$ cd lodstats_www

Install dependencies:
    (lodstats-env)$ pip install -r pip-requirements.txt

Run setup.py egg_info:

    (lodstats-env)$ python setup.py egg_info

Make a config file as follows::

    (lodstats-env)$ paster make-config rdfstats production.ini

Tweak the config file as appropriate and then setup the application::

    (lodstats-env)$ paster setup-app production.ini

Then you are ready to go:
    (lodstats-env)$ paster serve production.ini

Direct your browser to http://localhost:5000/
