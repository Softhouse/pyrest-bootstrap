"""Web API and UI for Visual Units tracking"""
import cherrypy
import api
import os, os.path
import inspect
import datetime, decimal

from common  import *


def datahandler(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError("Cannae serialize %s of type %s" % (obj,type(obj)))

class Root(object):
    """Server application root"""

    
    def api(self, target, *args, **kwargs):
        """REST API handler"""
        handler = getattr(HANDLERS[target], 
                       cherrypy.request.method.lower())
        response = handler(*args, **kwargs)
        if hasattr(handler, 'binary'):
            cherrypy.response.headers['Content-Type'] = handler.content_type
            cherrypy.response.headers['Content-Disposition'] = handler.content_disposition
            return response

        cherrypy.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        
        cherrypy.response.status = response.status
        return response.content.encode('utf-8')

        
    def index(self, user=None, password=None):
        """Web UI for tracker"""
        raise cherrypy.HTTPRedirect("/login.html")
       
        
    index.exposed = True
    api.exposed = True

def get_handlers(package):
    handlers = {}

    for member_name, member in [module for module in inspect.getmembers(package) 
                                                    if inspect.ismodule(module[1])]:
        print("Adding handler %s" % member_name)
        handlers[member_name]  = member
    return handlers

HANDLERS = get_handlers(api)


CONF = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 1443,
        'tools.staticdir.on' : True,
        'tools.staticdir.dir' : os.path.join(os.path.abspath(os.curdir), 'static'),
        'tools.staticdir.content_types' : {'js':  'application/javascript; charset=utf-8'},

    },
    '/favicon.ico': {

        'tools.staticfile.on': True,
        'tools.staticfile.filename': os.path.abspath("favicon.ico")
        }
    }


if False: #if SSL is needed
    SSL_CRT = os.path.join(CFG_DIR, 'ssl/domain.se.crt')
    SSL_KEY = os.path.join(CFG_DIR, 'ssl/domain.se.key')
    SSL_BUNDLE = os.path.join(CFG_DIR, 'ssl/ssl_bundle.pem')
    cherrypy.server.ssl_certificate = SSL_CRT
    cherrypy.server.ssl_private_key = SSL_KEY
    cherrypy.server.ssl_certificate_chain = SSL_BUNDLE
    cherrypy.server.ssl_module = 'pyopenssl'


ROOT = Root()
cherrypy.quickstart(ROOT, '/', CONF)