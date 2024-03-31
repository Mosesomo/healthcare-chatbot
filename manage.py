"""This script is for managing our database, all the insertion of data
    and also deletion of data is being done in this script
"""
from system import app, db
from system.model import User, Doctor, Appointment, Testimonial


with app.app_context():
    db.create_all()
    
    """"doctor = Doctor(
        name="Moses Omondi",
        phone="+254758171116",
        department="Surgery",
        picture='img/doc2.jpg'
    )
    
    db.session.add(doctor)
    
    doctor1 = Doctor(
        name="Charity Akello",
        phone="+254758171116",
        department="Counselling",
        picture='img/doc2.jpg'
    )
    db.session.add(doctor1)
    
    doctor2 = Doctor(
        name="Main Johnson",
        phone="+254758171116",
        department="Surgery",
        picture='img/doc5.jpg'
    )
    
    db.session.add(doctor2)
    
    doctor3 = Doctor(
        name="Davis Doe",
        phone="+254758171116",
        department="Counselling",
        picture='img/doc6.jpg'
    )
    
    
    db.session.add(doctor3)"""
    
    """testimonial1 = Testimonial(
        name="Nicholus Mbuki",
        text="I had a fantastic experience with the healthcare team\
            at your clinic. They were very professional and made me feel at\
        ease. The treatment was effective, and I've noticed a significant improvement in my health.",
        picture='img/boy6.jpeg'
    )
    
    db.session.add(testimonial1)
    
    testimonial2 = Testimonial(
        name="Maryanne Ayuma",
        text="The care I received was top-notch. The staff was attentive and made sure\
            I understood everything. I feel much better now and am looking forward\
                to continued support from your team.",
        picture='img/lady5.jpeg'
    )
    
    db.session.add(testimonial2)
    
    testimonial3 = Testimonial(
        name="Duncan Peter",
        text="My experience at your clinic was incredibly positive.\
            The staff was caring and knowledgeable, and I felt well-informed\
                about my treatment options. I'm grateful for the support and care I received.",
        picture='img/boy5.jpeg'
    )
    
    db.session.add(testimonial3)"""
    
    """user_id = 'cb5c3bc8-f8db-4e8a-8fc6-1c7b8affb8a9'
    user = User.query.get(user_id)
    user.is_admin = True"""
    
    
    # doc_id = 'f845c425-2bcc-40b2-9617-ce4b35ef9cad'
    # doc = Doctor.query.get(doc_id)
    # doc.email_confirmed = True
    
    """doctor_id = 'edf84aac-e868-4d84-96e3-136af439d4cd'
    doctor = Doctor.query.get(doctor_id)
    if doctor:
        db.session.delete(doctor)"""
    
    """appointments = Appointment.query.all()
        for appointment in appointments:
        db.session.delete(appointments)"""
        
    db.session.commit()
    
        
    doctors = Doctor.query.all()
    for doctor in doctors:
        print(doctor)
        
    users = User.query.all()
    for user in users:
        print(f"\n{users}")
    