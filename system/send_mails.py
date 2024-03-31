"""This module handle email sending"""
from system import mail, serial
from flask_mail import Message
from flask import render_template
from system.model import Appointment


def send_patient_confirmation_email(patient_email, doctor_name,
                                    appointment_date, appointment_time,
                                    location, description):
    msg = Message('Appointment Confirmation',
                  sender='medibridgenoreply@mosesomo.tech',
                  recipients=[patient_email])
    msg.html = render_template('patient_confirmation_email.html',
                               doctor_name=doctor_name,
                               appointment_date=appointment_date,
                               appointment_time=appointment_time, location=location,
                               description=description)
    mail.send(msg)


def send_doctor_notification_email(doctor_email, patient_name, 
                                   appointment_date, appointment_time, 
                                   location, description):
    msg = Message('New Appointment Notification', 
                  sender='medibridgenoreply@mosesomo.tech', 
                  recipients=[doctor_email])
    msg.html = render_template('doctor_notification_email.html', 
                               patient_name=patient_name, 
                               appointment_date=appointment_date, 
                               appointment_time=appointment_time, location=location, 
                               description=description)
    mail.send(msg)
    

def send_confirmation_email(email, confirm_url, entity_type):
    msg = Message('Confirm Your Email', sender='noreply@mosesomo.tech', recipients=[email])
    msg.body = f'Please click the following link to confirm your email: {confirm_url}'
    mail.send(msg)

    # Modify the token generation to include the entity type
    token = serial.dumps((entity_type, email), salt='email-confirm')
    return token

def send_approval_email(doctor):
    msg = Message('Doctor Approval Notification', sender='medibrigenoreply@mosesomo.tech', recipients=[doctor.email])
    msg.body = f'Hello Dr. {doctor.name},\n\nYour registration as a doctor has been approved. You can now login to your account.\n\nRegards,\n MediBridge Hospital'
    mail.send(msg)


def send_patient_cancellation_email(patient_email, doctor_name, appointment_date, appointment_time, location, description):
    msg = Message('Appointment Cancellation Notification', sender='medibridgenoreply@mosesomo.tech', recipients=[patient_email])
    msg.html = render_template('patient_cancellation_email.html', doctor_name=doctor_name, appointment_date=appointment_date, appointment_time=appointment_time, location=location, description=description)
    mail.send(msg)

def send_doctor_cancellation_email(doctor_email, patient_name, appointment_date, appointment_time, location, description):
    msg = Message('Appointment Cancellation Notification', sender='medibridgenoreply@mosesomo.tech', recipients=[doctor_email])
    msg.html = render_template('doctor_cancellation_email.html', patient_name=patient_name, appointment_date=appointment_date, appointment_time=appointment_time, location=location, description=description)
    mail.send(msg)
    

def send_reminder_email(appointment):
    # Send reminder email to user
    send_email(appointment.user.email, "Appointment Reminder", f"Your appointment with Dr. {appointment.doctor.name} is tomorrow at {appointment.appointment_time}. Don't forget!")

    # Send reminder email to doctor
    send_email(appointment.doctor.email, "Appointment Reminder", f"You have an appointment with {appointment.user.first_name} {appointment.user.last_name} tomorrow at {appointment.appointment_time}.")

def send_email(recipient, subject, body):
    msg = Message(subject, sender="your_email@example.com", recipients=[recipient])
    msg.body = body
    mail.send(msg)
    
def send_approval_cancellation_mail(doctor):
    msg = Message('Doctor Approval cancellation Notification', sender='medibrigenoreply@mosesomo.tech', recipients=[doctor.email])
    msg.body = f'Hello Dr. {doctor.name},\n\nYour registration as a doctor has been cancelled. Please check on your details and sign up again.\n\nRegards,\n MediBridge Hospital'
    mail.send(msg)
