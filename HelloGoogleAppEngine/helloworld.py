import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, JiaWang!')

class DemoJson(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write('{"name":"Jia Wang", "age":33}')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/demo.json', DemoJson),
], debug=True)
