import uuid
from system import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String(55), default=str(uuid.uuid4), primary_key=True)
    first_name = db.Column(db.String(35), nullable=False)
    last_name = db.Column(db.String(35), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(60), unique=True, nullable=False)
    email_confirmed = db.Column(db.Boolean, default=False)
    
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())
    
    def __repr__(self):
        return (f"(<User id:{self.id}, FirstName:{self.first_name}, LastName:{self.last_name}, Email:{self.email}, Password:{self.password}>, Email_confirmed: {self.email_confirmed})")


class Doctor(db.Model):
    id = db.Column(db.String(35), default=str(uuid.uuid4), primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    department = db.Column(db.String(67), nullable=False)
    picture = db.Column(db.String(255), nullable=False, default='profile.jpg')

    def __init__(self, **kwargs):
        super(Doctor, self).__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

    def __repr__(self):
        return (f"<Doctor ID:{self.id}, Name:{self.name}, Phone:{self.phone}, Department:{self.department}, Profile:{self.picture}>")

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
