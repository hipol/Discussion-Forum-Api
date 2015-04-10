import sys
flaskfirst = "/opt/python/current/app"
if not flaskfirst in sys.path:
    sys.path.insert(0, flaskfirst)

from app import app
application = app