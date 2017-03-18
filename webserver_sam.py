# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 22:33:47 2017

@author: sunlei
"""

from flask import Flask,request,json,session,redirect,url_for
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/')
def index():
    print(request.headers)
    print(request.cookies)
    if 'username' in session:
        return redirect(url_for('v_mail'))
    else:
	    return redirect(url_for('v_auth'))

@app.route('/mail')
def v_mail():
    return '''
        <!doctype html>
        <html>
        <head>
            <meta charset="utf-8">
            <script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
        </head>
        <body>
            <h1>My Home Page</h1>
            <ul>
                <li><a href="/music">Music</a></li>
                <li><a href="/movie">Movie</a></li>
                <li><a href="/logout">Logout</a></li>
                <li><a href="/add/4/3">add</a></li>
                <li><a href="sub/10/6">sub</a></li>
            </ul>
            <form action="/auth" method="POST">
                <input type="text" name="uid" placeholder="input your user id">
                <input type="password" name="pwd" placeholder="input your password">
                <input type="submit" value="submit">
            </form>
            <form action="/auth" method="get">
                <h2>name:</h2><input type="text" name="uid">
                <h2>password:</h2><input type="password" name="pwd">
                <input type="submit" value="submit">
            </form>
            <form id="test">
                <input type="text" name="name" placeholder="contact name">
                <input type="text" name="tel" placeholder="contact telephone">
                <input type="submit" value="Ajax POST">
            </form>
            <div id="status"></div>
            <script>
                $(function(){
                    $("form#test").submit(function(){
                        var data = $("form#test").serializeArray();
                        var jsondata = {}
                        data.forEach(function(d){jsondata[d.name] = d.value});
                        $.ajax({
                            url : "/user",
                            method : "POST",
                            data : JSON.stringify(jsondata),
                            contentType : "application/json;charset=UTF-8",
                            success : function(dt,er,xhr){
                                $("#status").text(dt);
                            },
                            error : function(){}
                        });
                        return false;
                    });
                })
            </script>
        </body>
        </html>
    '''
@app.route('/login',methods=["POST","GET"])
def v_auth():
    if request.method == 'GET':
        return  '''
        <h1>登录邮箱</h1>
                <form action="%s" method="POST">
                    <input type="text" name="username" placeholder="input your username">
                    <input type="password" name="password" placeholder="input your password">
                    <input type="submit" value="submit">
                </form>
                ''' % url_for('v_auth')
    if request.method == 'POST':
        if request.form['username']=='jason' and request.form['password']=='7878':
          session['username'] = request.form['username']
          return  'authorized! go <a href="%s">inbox</a>' % url_for('index')
        else:
          return 'not authorized.go <a href="%s">here</a> to authorize yourself' % url_for('v_auth')
    
@app.route('/music')           
def music():
    return '<h1>My Favorite Music</h1>'

@app.route('/movie')
def movie():
    return '<h1>My Favorite Movie</h1>'
    
@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('index'))

@app.route('/add/<int:var>/<int:var1>')
def add(var,var1):
    return '<h1>{0}+{1}={2}</h1>'.format(var,var1,var+var1)

@app.route('/sub/<int:var>/<int:var1>')
def sub(var,var1):
    return '<h1>{0}-{1}={2}</h1>'.format(var,var1,var-var1)

@app.route('/auth',methods=['POST','GET'])
def auth():
    uid = request.values.get('uid','空')
    pwd = request.values.get('pwd','空')
    if request.method == 'GET':
        return '<h1>这是get方法,use:{0},pass:{1}</h1>'.format(uid,pwd)
    if request.method == 'POST':
        if uid=='sunlei' and pwd=='slsgdhr':
            return '<h1>这是post方法,登录成功<h1>'
        else:
            return '<h1>这是post方法,用户名密码错误<h1>'

users = []    
@app.route('/user',methods=['POST'])
def v_user():
    users.append(request.json)
    print(users)
    return json.dumps(users)

app.run(host='0.0.0.0',port=8001)