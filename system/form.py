from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField,
                     PasswordField,
                     BooleanField, EmailField)
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from system.model import User


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()],
                       render_kw={"email": "example@gmail.com"})
    password = PasswordField("Password", validators= [DataRequired(), Length(min=8)],
                             render_kw={"Password": "Password"})
    remember = BooleanField('Remember')
    submit = SubmitField("sign In")
    
    

class RegistrationForm(FlaskForm):
    firstName = StringField("First Name", validators=[DataRequired()])
    lastName = StringField("Last Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()],
                       render_kw={"email": "example@gmail.com"})
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)],
                             render_kw={"Password": "Password"})
    confirmPassword = PasswordField("Confirm Password",
                                    validators=[DataRequired(),
                                                Length(min=8),
                                                EqualTo('password')],
                                    render_kw={"Confirm password": "Confirm paswword"})
    submit = SubmitField("sign Up")
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already exist')
        
    