# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
此项目用来演示在Google App Engine当中应用Jinja2
若要使用Jinja2的话，需要在app.yaml里指明包含Jinja2类库
"""
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

    def get(self):
        s = self.render_str('demo.html')
        self.response.write(s)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
