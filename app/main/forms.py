'''
Created on 2017415

@author: zhou
'''
from wtforms import StringField, SubmitField, validators, PasswordField, TextAreaField,BooleanField, SelectField, FileField
from wtforms.validators import Required, EqualTo, Length, Regexp, Email, DataRequired
from flask_wtf import Form
from werkzeug.routing import ValidationError
from ..models import Role, User
from flask_pagedown.fields import PageDownField

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')
    
class ChangePw(Form):
    oldpassword = PasswordField('Enter Your Old Password', validators=[Required()])
    newpassword = PasswordField('Enter Your New Password', validators=[Required(), EqualTo('newpassword2',message='Passwords must match')])
    newpassword2 = PasswordField('Confirm Password', validators=[Required()])
    submit = SubmitField('Go')
    
class EditProfileForm(Form):
    #avatar = FileField('Profile Picture')
    name = StringField('Real Name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0,64)])
    about_me = TextAreaField('About ma')
    submit = SubmitField('Submit')
    
class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(),Length(1, 64), Email()])
    username = StringField('Username', validators=[Required(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0 ,'Username must have only letters, numbers, dots or underscores')]
                           )
    confirmed =BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real Name', validators=[Length(0,64)])
    location = StringField('Location', validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')
    
    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user
        
    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
    
    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('User already in use.')
        
class PostForm(Form):
    postname = StringField("Post Name", validators=[DataRequired()])
    body = PageDownField("Post Content", validators=[DataRequired()])
    #picture = FileField("Upload Your Picture")
    original = StringField("Original Author")
    submit = SubmitField('Submit')
    
class CommentForm(Form):
    body = TextAreaField('',validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class SearchForm(Form):
    search = StringField('Search for IP', validators=[DataRequired()])
    submit = SubmitField('Search')
    
    
    
        
    