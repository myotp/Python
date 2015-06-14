# -*- coding: utf-8 -*-

#!/usr/bin/env python
import os
import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class MainHandler(webapp2.RequestHandler):
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render_front_page(self, title = "", art = "", error = ""):
        s = self.render_str('front.html', title=title, art=art, my_error_str=error)
        self.response.write(s)

    def get(self):
        self.render_front_page()

    def post(self):
        title = self.request.get('title')
        art = self.request.get('art')
        print 'title: ', title, ' art: ', art
        if title and art:
            self.response.write('Thanks')
        else:
            error_msg = "title and art"
            self.render_front_page(title=title, art=art, error=error_msg)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
