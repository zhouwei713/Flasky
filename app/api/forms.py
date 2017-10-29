'''
Created on 20171029

@author: zhou
'''

from wtforms import StringField, SubmitField, validators, PasswordField, TextAreaField,BooleanField, SelectField, FileField
from wtforms.validators import Required, EqualTo, Length, Regexp, Email, DataRequired
from flask_wtf import Form
from werkzeug.routing import ValidationError
from ..models import Role, User
from flask_pagedown.fields import PageDownField

class QueryIPForm(Form):
    search = StringField('Search for IP', validators=[DataRequired()])
    submit = SubmitField('Go To Google Map')
    #submit2 = SubmitField('Check IP Detail')