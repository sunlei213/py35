# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 16:06:01 2017

@author: sunlei
"""

from flask import Flask
 
# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
 
app = Flask(__name__)
# We'll just use SQLite here so we don't need an external database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
 
db = SQLAlchemy(app)

class Lunch(db.Model):
    """A single lunch"""
    id = db.Column(db.Integer, primary_key=True)
    submitter = db.Column(db.String(63))
    food = db.Column(db.String(255))

class computer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    mac =db.Column(db.String(12))
    hd_no = db.Column(db.String(60))
    children = db.relationship("use_list", backref="computer", lazy='dynamic')
    
class user(db.Model):
    id = db.Column(db.String(6), primary_key=True)
    name = db.Column(db.String(20))
    child = db.relationship("use_list", backref="user", lazy='dynamic')
    
class use_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime, default=datetime.now)
    end = db.Column(db.DateTime)
    c_no = db.Column(db.Integer, db.ForeignKey('computer.id'))
    u_no = db.Column(db.String(6), db.ForeignKey('user.id'))
    
from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
 
app.config['SECRET_KEY'] = 'please, tell nobody'
 
class LunchForm(Form):
    submitter = StringField(u'Hi, my name is')
    food = StringField(u'and I ate')
    # submit button will read "share my lunch!"
    submit = SubmitField(u'share my lunch!')

from flask import render_template, url_for, redirect
 
@app.route("/")
def root():
    lunches = Lunch.query.all()
    form = LunchForm()
    return render_template('index.html', form=form, lunches=lunches)

@app.route(u'/new', methods=[u'POST'])
def newlunch():
    form = LunchForm()
    if form.validate_on_submit():
        lunch = Lunch()
        form.populate_obj(lunch)
        db.session.add(lunch)
        db.session.commit()
    return redirect(url_for('root'))

if __name__ == "__main__":
    db.create_all()  # make our sqlalchemy tables
    app.run(host='0.0.0.0',port=8001)