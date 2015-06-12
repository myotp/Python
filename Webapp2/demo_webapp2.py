'''
http://forums.udacity.com/questions/6012777/tutorial-how-to-run-appsexercises-withouth-gae-mostly#cs253
'''
import webapp2

class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello, webapp2!')

app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),], debug=True)

def main_webob():
    '''
    Use webob as a web server
    '''
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='8080')

def main_wsgi():
    '''
    Use wsgiref as WSGI web server
    '''
    from wsgiref.simple_server import make_server

    httpd = make_server('', 8080, app)
    print 'Started app serving on port 8080...'
    httpd.serve_forever()

if __name__ == '__main__':
    main_wsgi()
