from email.policy import default
import uuid
from datetime import datetime
from flask_login import UserMixin
from system import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    # Check if the user_id belongs to a regular user (Patient)
    user = User.query.get(user_id)
    if user:
        return user
    
    # If the user_id doesn't belong to a regular user, try loading a doctor
    doctor = Doctor.query.get(user_id)
    return doctor


class User(db.Model, UserMixin):
    id = db.Column(db.String(55), primary_key=True)
    first_name = db.Column(db.String(35), nullable=False)
    last_name = db.Column(db.String(35), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(34), nullable=True)
    password = db.Column(db.String(60), nullable=False)
    email_confirmed = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    # Define relationships
    appointments = db.relationship('Appointment', back_populates='user', lazy=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

    def __repr__(self):
        return f"<User id:{self.id}, FirstName:{self.first_name}, LastName:{self.last_name}, Email:{self.email}, Email_confirmed: {self.email_confirmed}, is_admin: {self.is_admin}>"

class Doctor(db.Model, UserMixin):
    id = db.Column(db.String(35), primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    lincense = db.Column(db.String(25), nullable=False)
    department = db.Column(db.String(67), nullable=False)
    picture = db.Column(db.String(255), nullable=False, default='profile.jpg')
    approved = db.Column(db.Boolean, default=False)  # Approval status
    email_confirmed = db.Column(db.Boolean, default=False)
    qualifications = db.Column(db.Text, nullable=True)  # Qualifications or certifications
    fee = db.Column(db.Float, nullable=True)                     # Fee per appointment
    availability = db.Column(db.String(255), nullable=True)
    start_time = db.Column(db.DateTime())
    end_time = db.Column(db.DateTime())
    password = db.Column(db.String(50), nullable=False)
    # Define relationships
    appointments = db.relationship('Appointment', back_populates='doctor', lazy=True)

    def __init__(self, **kwargs):
        super(Doctor, self).__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

    
    def is_doctor_available(self, appointment_time):
        """
        Check if the doctor is available at the given appointment_time.

        :param appointment_time: Time of the appointment
        :type appointment_time: datetime.time
        :return: True if the doctor is available, False otherwise
        :rtype: bool
        """
        if self.availability:
            # Parse the availability string to get the start and end times
            start_time = self.start_time.time()
            end_time = self.end_time.time()

            # Check if the appointment time falls within the doctor's available hours
            return start_time <= appointment_time <= end_time
        else:
            return False
        
        
    def __repr__(self):
        return f"<Doctor ID:{self.id}, Name:{self.name}, Email:{self.email}, Phone:{self.phone}, Department:{self.department}, Profile:{self.picture}, ConsultationFee: {self.fee}>"


class Appointment(db.Model):
    id = db.Column(db.String(35), primary_key=True)
    doctor_id = db.Column(db.String(35), db.ForeignKey('doctor.id'), nullable=False)
    user_id = db.Column(db.String(55), db.ForeignKey('user.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(100), nullable=False)  # Virtual or Hospital
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.Boolean, default=False) # cancelled or confirmed
    # Define relationships
    doctor = db.relationship('Doctor', back_populates='appointments')
    user = db.relationship('User', back_populates='appointments')

    def __init__(self, **kwargs):
        super(Appointment, self).__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

    @property
    def appointment_datetime(self):
        """
        Get the appointment datetime by combining the date and time.

        :return: Appointment datetime
        :rtype: datetime.datetime
        """
        return datetime.combine(self.appointment_date, self.appointment_time)

    def __repr__(self):
        return f"<Appointment ID:{self.id}, Doctor:{self.doctor_id}, User:{self.user_id}, Date:{self.appointment_date}, Time:{self.appointment_time} Location:{self.location}>"

class Testimonial(db.Model):
    id = db.Column(db.String(35), default=str(uuid.uuid4), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    picture = db.Column(db.String(255), nullable=False, default='profile.jpg')
    
    def __init__(self, **kwargs):
        super(Testimonial, self).__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())
    
    def __repr__(self):
        return (f"<Testimonial ID:{self.id}, Name:{self.name}, Picture:{self.picture}, Text:{self.text}>")