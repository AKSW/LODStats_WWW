# Add the virtual Python environment site-packages directory to the path
import site
site.addsitedir('/home/lodstats/lodstats-env/lib/python2.7/site-packages')

# Avoid ``[Errno 13] Permission denied: '/var/www/.python-eggs'`` messages
import os
os.environ['PYTHON_EGG_CACHE'] = '/home/lodstats/lodstatswww/egg-cache'

import sys
sys.path.append('/home/lodstats/lodstatswww')

# Load the Pylons application
from paste.deploy import loadapp
application = loadapp('config:production.ini', relative_to='/home/lodstats/lodstatswww/')
