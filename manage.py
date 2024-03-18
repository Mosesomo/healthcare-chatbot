from system import app, db
from system.model import User, Doctor, Testimonial


with app.app_context():
    db.create_all()
    
    """doctor = Doctor(
        name="Moses Omondi",
        phone="+254758171116",
        department="Surgery"
    )
    
    db.session.add(doctor)
    
    doctor1 = Doctor(
        name="Davis Doe",
        phone="+254758171116",
        department="Counselling"
    )
    
    db.session.add(doctor1)
    
    db.session.commit()"""
    
    doctors = Doctor.query.all()
    for doctor in doctors:
        print(doctor)
        
    users = User.query.all()
    for user in users:
        print(user)