from flask_wtf import FlaskForm
from sqlalchemy import Float
from wtforms import (StringField, SubmitField,
                     PasswordField, FloatField,
                     BooleanField, EmailField,
                     TimeField, SelectMultipleField,
                     DateField, TextAreaField,
                     SelectField, RadioField)
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, Regexp
from system.model import User, Doctor
from flask_wtf.file import FileField, FileAllowed, FileRequired
from system import photos, docs


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
    email = EmailField("Email", validators=[DataRequired(),
                                            Regexp(r'^[\w\.-]+@[\w\.-]+\.\w+$', message='Invalid email address')],
                       render_kw={"email": "example@gmail.com"})
    phone = StringField('Phone Number', validators=[DataRequired(),
                                                    Regexp('^\\+254[0-9]{9}$',
                                                           message='Invalid phone number.\
                                                               Must start with +254 followed by 9 digits.')],
                        render_kw={"placeholder": "+254xxxxxxxxx"})
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=16)],
                             render_kw={"Password": "Password"})
    confirmPassword = PasswordField("Confirm Password",
                                    validators=[DataRequired(),
                                                Length(min=8),
                                                EqualTo('password')],
                                    render_kw={"placeholder": "Confirm paswword"})
    submit = SubmitField("sign Up")
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already exist')
        
    
    def validate_password(self, password_field):
        password = password_field.data
        # Check if password contains at least one uppercase letter, one lowercase letter, and one digit
        if (not any(c.isupper() for c in password)
            or not any(c.islower() for c in password)
            or not any(c.isdigit() for c in password)):
            raise ValidationError('Password must contain at least one uppercase letter,\
                one lowercase letter, and one digit.')
        
class DoctorRegistration(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(),
                                            Regexp(r'^[\w\.-]+@[\w\.-]+\.\w+$', message='Invalid email address')],
                       render_kw={"placeholder": "example@gmail.com"})
    phone = StringField('Phone Number', validators=[DataRequired(),
                                                    Regexp('^\\+254[0-9]{9}$',
                                                           message='Invalid phone number.\
                                                               Must start with +254 followed by 9 digits.')],
                        render_kw={"placeholder": "+254xxxxxxxxx"})
    license = StringField('Doctor License Number',
                                 validators=[DataRequired(),
                                             Regexp(r'^MP-\d{6}$|^DE-\d{6}$', message='Invalid license number format')])
    department = StringField("Department", validators=[DataRequired()])
    fee = FloatField('Consultation Fee')
    availability = SelectMultipleField('Available Days', choices=[
                                                                ('monday', 'Monday'),
                                                                ('tuesday', 'Tuesday'),
                                                                ('wednesday', 'Wednesday'),
                                                                ('thursday', 'Thursday'),
                                                                ('friday', 'Friday')
                                                            ], validators=[DataRequired()])      
    start_time = StringField('From', validators=[DataRequired()],
                           render_kw={'placeholder': 'HH:MM AM/PM'})
    end_time = StringField('To', validators=[DataRequired()],
                           render_kw={'placeholder': 'HH:MM AM/PM'})
    qualifications = FileField("Upload your Certificate",
                               validators=[FileRequired(),
                                           FileAllowed(docs, 'Only pdf and docx are allowed')])
    picture = FileField('Upload Your Picture', validators=[FileRequired(),
                                                           FileAllowed(photos, 'Only images are allowed')])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=16)],
                             render_kw={"Password": "Password"})
    confirmPassword = PasswordField("Confirm Password",
                                    validators=[DataRequired(),
                                                Length(min=8),
                                                EqualTo('password')],
                                    render_kw={"placeholder": "Confirm paswword"})
    submit = SubmitField("sign Up")
    
    
    def validate_email(self, email):
        email = Doctor.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already exist')
        
    def validate_password(self, password_field):
        password = password_field.data
        # Check if password contains at least one uppercase letter, one lowercase letter, and one digit
        if (not any(c.isupper() for c in password)
            or not any(c.islower() for c in password)
            or not any(c.isdigit() for c in password)):
            raise ValidationError('Password must contain at least\
                one uppercase letter, one lowercase letter, and one digit.')
        
    


class AppointmentForm(FlaskForm):
    doctor = SelectField('Select Doctor', coerce=str, validators=[DataRequired()])
    appointment_date = DateField('Appointment Date', format='%Y-%m-%d', validators=[DataRequired()])
    appointment_time = TimeField('Appointment Time', format='%H:%M', validators=[DataRequired()])
    location = RadioField('Appointment Location', choices=[('google_meet', 'Google Meet'), ('hospital', 'Hospital')],
                          default='google_meet', validators=[DataRequired()])
    description = TextAreaField('Description', render_kw={"placeholder": "Please share something to prepare for our meeting"})
    submit = SubmitField('Schedule Appointment')
    
    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        # Query doctors and populate doctor choices
        self.doctor.choices = [(doctor.id, doctor.name) for doctor in Doctor.query.filter_by(approved=True).all()]