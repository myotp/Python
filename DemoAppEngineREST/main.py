# -*- coding: utf-8 -*-
#!/usr/bin/env python

import webapp2
import json

from google.appengine.ext import ndb

class Person(ndb.Model):
    name = ndb.StringProperty(required=True)
    age = ndb.IntegerProperty(required=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

# Request in normal text
class AddPersonTextHandler(webapp2.RequestHandler):
    def post(self):
        name = self.request.get('name')
        age = int(self.request.get('age'))
        person = Person(name=name, age=age)
        person.put()

# JSON request
class AddPersonJsonHandler(webapp2.RequestHandler):
    def post(self):
        p = json.loads(self.request.body)
        print p
        name = p['name']
        age = int(p['age'])
        person = Person(name=name, age=age)
        person.put()

# Response in noraml text
class AllPersonsTextHandler(webapp2.RequestHandler):
    def get(self):
        persons = Person.query()
        result = ""
        for p in persons:
            result += " " + p.name + " " + str(p.age) + " "
        self.response.headers['Contetn-Type'] = 'text/plain'
        self.response.write(result)

# JSON response
class AllPersonsJsonHandler(webapp2.RequestHandler):
    def get(self):
        persons = Person.query()
        result = []
        for p in persons:
            result.append({'name':p.name, 'age':p.age})
        print 'persons: ', result
        self.response.headers['Contetn-Type'] = 'application/json'
        json_reply = json.dumps({'persons':result})
        self.response.write(json_reply)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/add_person_text', AddPersonTextHandler),
    ('/add_person_json', AddPersonJsonHandler),
    ('/all_persons_text', AllPersonsTextHandler),
    ('/all_persons_json', AllPersonsJsonHandler),

], debug=True)
