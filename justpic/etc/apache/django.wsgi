import os,sys
sys.path.append('E:/project/PR_Site/annotation')
sys.path.append(os.path.dirname(os.path.dirname(__file__))) 
os.environ['DJANGO_SETTINGS_MODULE']='annotation.settings'

import django.core.handlers.wsgi
_application=django.core.handlers.wsgi.WSGIHandler()

def application(environ,start_response):
	if environ['wsgi.url_scheme']=='https':
		environ['HTTPS']='on'
	return _application(environ,start_response)