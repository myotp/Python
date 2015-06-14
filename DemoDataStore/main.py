# -*- coding: utf-8 -*-

#!/usr/bin/env python
import os
import jinja2
import webapp2

from google.appengine.ext import db
from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

# NDB cheat sheet: https://docs.google.com/document/d/1AefylbadN456_Z7BZOpZEXDq8cR8LYu7QgI7bt5V0Iw/mobilebasic
# To save data in Google App Engine Data Store
class Art(ndb.Model):
    title = ndb.StringProperty(required=True)
    art = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)

class MainHandler(webapp2.RequestHandler):
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render_front_page(self, title = "", art = "", error = ""):
        #arts = db.GqlQuery('SELECT * FROM Art ORDER BY created DESC')
        arts = Art.query().fetch()
        s = self.render_str('front.html', title=title, art=art, my_error_str=error, arts=arts)
        self.response.write(s)

    def get(self):
        self.render_front_page()

    def post(self):
        title = self.request.get('title')
        art = self.request.get('art')
        print 'title: ', title, ' art: ', art
        print '请求是：', self.request
        if title and art:
            # Save Art object to Data Store
            a = Art(title=title, art=art)
            a.put()
            self.redirect('/')
        else:
            error_msg = "title and art"
            self.render_front_page(title=title, art=art, error=error_msg)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
