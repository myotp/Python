# -*- coding: utf-8 -*-

#!/usr/bin/env python
import webapp2

## 这里演示表格，Action的部分设置为Google处理
## 点击之后就会提交给Google了
demo_form = """
<form action="http://www.google.com/search">
  <input name="q">
  <input type="submit">
</form>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("先来演示Google处理表格")
        self.response.write(demo_form)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
