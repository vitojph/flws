# follow instructions from
# http://flask.pocoo.org/docs/deploying/mod_wsgi/#creating-a-wsgi-file
# https://beagle.whoi.edu/redmine/projects/ibt/wiki/Deploying_Flask_Apps_with_Apache_and_Mod_WSGI

# virtual env
activate_this = "/home/freelingr/flws/flws/venv/bin/activate_this.py"
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, "/home/freelingr/public_html/freeling-api/")
from flwses import app as application
