from flask import Flask,session,request,redirect,render_template
import re

app = Flask(__name__)
app.secret_key = 'this is secret_key'

from views.page import page
from views.user import user
app.register_blueprint(page.pb)
app.register_blueprint(user.ub)

@app.route('/')
def hello_world():
    session.clear()
    return redirect('/user/login')  # 重定向到登录页面

@app.route('/<path:path>')
def catch_all(path):
    return render_template('404.html')

@app.before_request
def before_request():
    pat = re.compile(r'^/static')
    if re.search(pat,request.path): return
    elif request.path == '/user/login' or request.path == '/user/register': return
    elif session.get('username'): return
    return redirect('/user/login')

if __name__ == '__main__':
    app.run()
