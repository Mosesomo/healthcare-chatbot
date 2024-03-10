from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField,
                     PasswordField,
                     BooleanField, EmailField)
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators= [DataRequired(), Length(min=8)])
    remember = BooleanField('Remember')
    submit = SubmitField("sign In")
    
    

class RegistrationForm(FlaskForm):
    firstName = StringField("First Name", validators=[DataRequired()])
    lastName = StringField("Last Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirmPassword = PasswordField("Confirm Password",
                                    validators=[DataRequired(),
                                                Length(min=8),
                                                EqualTo('password')])
    submit = SubmitField("sign Up")
    
    def validate_email(self, email):
        pass
    