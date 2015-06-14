# -*- coding: utf-8 -*-

#!/usr/bin/env python
import webapp2

# 这里演示表格，Action的部分设置为Google处理
# 点击之后就会提交给Google了
demo_google_form = """
<form action="http://www.google.com/search">
  <input name="q">
  <input type="submit">
</form>
"""

# [Login STEP 0] define a form and handler
my_login_form = """
<form action="/login_handler">
  用户名<input type="text"name="username"><br>
  密码<input type="password" name="password">
  <input type="submit">
</form>
"""
# [Login STEP 3] callback handler to process request
class LoginHandler(webapp2.RequestHandler):
    """ 这里演示一下我自己的表格的回调处理
    """
    def get(self):
        username = self.request.get('username')
        password = self.request.get('password')
        print 'Username: [', username, ']'
        print 'Password: [', password, ']'
        if username == 'admin':
            self.redirect('/show_request') # 演示一下redirect效果
        else:
            self.response.write("username:" + username + " and password: " + password)

# 演示表格checkbox input类型，选中的时候就是参数=on
show_checkbox_form = """
<form action="show_request">
    <input type="checkbox" name="Monday">周一<br>
    <input type="checkbox" name="Tuesday">周二<br>
    <input type="checkbox" name="Wednesday">周三<br>
    <input type="submit">
</form>
"""

# 演示表格radio input类型
# 为了一次只能选中一个，必须所有都用相同的name才可以
# 然后具体的区别究竟哪个选中，用value属性
show_radio_form = """
<form action="show_request">
    <label><input type="radio" name="Monday" value="one">周一</label><br>
    <label><input type="radio" name="Monday" value="two">周二</label><br>
    <label><input type="radio" name="Monday" value="three">周三</label><br>
    <input type="submit">
</form>
"""

# 演示下拉框的类型
show_dropbox_form = """
<form action="show_request">
    <select name="number">
        <option value="1">one</option>
        <option value="2">two</option>
        <option value="3">three</option>
    </select>
    <br>
    <input type="submit">
</form>
"""

# 此表格演示请求直接打印出来
show_request_from = """
<form method="post" action="show_request">
  姓名<input name="username"><br>
  年龄<input name="age">
  <input type="submit">
</form>
"""
class ShowRequestHandler(webapp2.RequestHandler):
    def get(self):
        """
        表格默认的请求方式是GET，如果换成POST的话，就需要额外post函数处理了
        简单打印请求回去，在调试的时候很有用，可以看看客户端到底请求了什么
        """
        self.response.headers['Content-Type'] = "text/plain"
        self.response.write(self.request)

    def post(self):
        self.response.headers['Content-Type'] = "text/plain"
        self.response.write(self.request)

class DemoJsonHandler(webapp2.RequestHandler):
    """ 此类用来演示返回JSON格式
    """
    def get(self):
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        json_reply = '{"name":"汪佳", "city":"Stockholm", "age":33}'
        self.response.write(json_reply)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        print '默认的Content-Type是：', self.response.headers['Content-Type']
        print self.response.headers
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        self.response.write("<p>先来演示Google处理表格</p>")
        self.response.write(demo_google_form)

        self.response.write("<p>再来演示我自己的表格处理回调</>")
        self.response.write(my_login_form)  ## [Login STEP 1] send form to browser

        self.response.write("<p>再来演示一下仅仅直接显示具体请求</>")
        self.response.write(show_request_from)
        self.response.write("<p>直接显示具体请求-Checkbox</>")
        self.response.write(show_checkbox_form)
        self.response.write("<p>直接显示具体请求-Radio</>")
        self.response.write(show_radio_form)
        self.response.write("<p>直接显示具体请求-下拉框</>")
        self.response.write(show_dropbox_form)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/demo_json', DemoJsonHandler),        ## 演示返回JSON
    ('/login_handler', LoginHandler),       ## [Login STEP 2] map handler to class
    ('/show_request', ShowRequestHandler),  ## 简单打印请求
], debug=True)
