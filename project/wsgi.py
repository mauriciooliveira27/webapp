import os, site, sys

#site.addsitedir('/usr/local/virtualenvs/MYAPP-VIRTUALENV/lib/python2.7/site-packages')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, '..'))

os.environ["DJANGO_SETTINGS_MODULE"] = "project.settings"  # see footnote [2]

from django.core.wsgi import get_wsgi_application
_application = get_wsgi_application()

env_variables_to_pass = ['TESTE',]
def application(environ, start_response):
    # pass the WSGI environment variables on through to os.environ
    for var in env_variables_to_pass:
        os.environ[var] = environ.get(var, '')
    return _application(environ, start_response)



