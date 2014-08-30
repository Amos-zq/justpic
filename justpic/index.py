import os
import sys

path=os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(1,path)
path=os.path.dirname(os.path.abspath(__file__))+'/annotation'
if path not in sys.path:
    sys.path.insert(1,path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "annotation.settings")
from django.core.handlers.wsgi import WSGIHandler
try:
    from bae.core.wsgi import WSGIApplication
except ImportError,e:
    from annotation.wsgi import WSGIApplication

application=WSGIApplication(WSGIHandler())
