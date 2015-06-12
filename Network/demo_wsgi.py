#!/usr/bin/env python

def simple_wsgi_app(environ, start_response):
    'simpel wsgi application'
    status = '200 OK'
    headers = [('Content-Type', 'text/plain')]
    start_response(status, headers)
    return ['Hello, WSGI']

from wsgiref.simple_server import make_server

httpd = make_server('', 8080, simple_wsgi_app)
print 'Started app serving on port 8080...'
httpd.serve_forever()
