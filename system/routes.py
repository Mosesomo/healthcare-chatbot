import re
from system import app, db, bcrypt, serial, photos, docs, scheduler
from system.form import AppointmentForm, LoginForm, RegistrationForm, DoctorRegistration
from flask import flash, render_template, url_for, redirect, send_from_directory, make_response, send_file
from system.model import User, Doctor, Testimonial, Appointment
from system.send_mails import (send_approval_email, send_confirmation_email,
                               send_doctor_notification_email,
                               send_patient_confirmation_email, send_doctor_cancellation_email,
                               send_patient_cancellation_email, send_reminder_email,
                               send_approval_cancellation_mail)
from flask_login import current_user, login_required, logout_user, login_user
from itsdangerous import SignatureExpired
from datetime import datetime, date, timedelta
from sqlalchemy import desc
from system.generate_report import generate_report
from io import BytesIO



@app.route('/')
@app.route('/home')
def home():
    testimonials = Testimonial.query.all()
    doctors = Doctor.query.all()
    return render_template('index.html',
                           doctors=doctors,
                           testimonials=testimonials)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/services')
def services():
    return render_template('service.html')

@app.route('/testimonial')
def testimonials():
    testimonials = Testimonial.query.all()
    return render_template('testimonial.html', testimonials=testimonials)

@app.route('/404')
def not_found():
    return render_template('404.html')


@app.route('/chatbot')
@login_required
def chatbot():
    return render_template('chatbot.html')


@app.route('/appointment')
@login_required
def appointment():
    doctor = Doctor.query.filter_by(department="Counselling").first()
    return render_template('appointment.html', doctor=doctor)

@app.route('/appointment/<doctor_id>')
@login_required
def doc_appointment(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    if doctor and doctor.department == "Counselling":
        return render_template('appointment.html', doctor=doctor)
    else:
        return redirect(url_for('not_found'))


@app.route('/dashboard')
@login_required
def dashboard():
    patients = User.query.all()
    patient_count = len(patients)
    doctors = Doctor.query.all()
    approved_doc = Doctor.query.filter_by(approved=True).all()
    count = len(approved_doc)
    non_approved = Doctor.query.filter_by(approved=False).all()
    pending = len(non_approved)
    
    appointments = Appointment.query.all()
    count_appointments = len(appointments)

    if isinstance(current_user, User) and not current_user.is_admin:
        return redirect(url_for('my_appointments'))
    elif isinstance(current_user, Doctor):
        return redirect(url_for('appointments'))
    
    return render_template('dashboard.html',
                           patients=patients,
                           doctors=doctors,
                           count=count,
                           patient_count=patient_count,
                           pending=pending,
                           count_appointments=count_appointments)

@app.route('/approve_doctor/<doctor_id>', methods=['GET', 'POST'])
@login_required
def approve_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    
    if doctor:
        doctor.approved = True
        db.session.commit()
            
        send_approval_email(doctor)
        flash('Approval successfull', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Doctor not found', 'error')
        return redirect(url_for('dashboard'))

    
@app.route('/dashbord/patients')
@login_required
def patients():
    patients = User.query.all()
    return render_template('patient.html', patients=patients)

@app.route('/dashboard/doctors')
@login_required
def doctors():
    doctors = Doctor.query.filter_by(approved=True).all()
    count = len(doctors)
    
    return render_template('doctors.html',
                           doctors=doctors,
                           count=count)

@app.route('/appointments')
@login_required
def appointments():
    appointments = Appointment.query.order_by(desc(Appointment.appointment_date)).all()
    return render_template('appointments.html', appointments=appointments)

@app.route('/my_appointments')
@login_required
def my_appointments():
    appointments = Appointment.query.order_by(desc(Appointment.appointment_date)).all()
    return render_template('patient_appointments.html', appointments=appointments)

@app.route('/account/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.email_confirmed:
            login_user(user)
            if user.is_admin:
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('home'))  # Redirect regular users to home page
        else:
            flash('Login unsuccessful, please check your email or password!', 'danger')
    return render_template('login.html', form=form)

@app.route('/account/login/doctor', methods=['GET', 'POST'])
def login_doctor():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        doctor = Doctor.query.filter_by(email=form.email.data).first()
        if doctor and bcrypt.check_password_hash(doctor.password, form.password.data) and doctor.email_confirmed:
            login_user(doctor)
            if doctor.approved:
                return redirect(url_for('appointments'))
            else:
                flash('Your account is pending for approval. Check your email within 30 mins', 'warning')
                return redirect(url_for('home'))  # Redirect to home or another appropriate page
        else:
            flash('Login unsuccessful, please check your email or password!', 'danger')
    return render_template('login_doctor.html', form=form)

@app.route('/account/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            first_name=form.firstName.data,
            last_name=form.lastName.data,
            email=form.email.data,
            phone=form.phone.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        
        flash(f"Welcome {user.first_name}, your account has been registered successfully,\
            and a confirmation link has been sent to your email, please confirm your email to proceed to login",
            'success')
        
        # send confirmation email
        token = serial.dumps(('user', user.email), salt='email-confirm')

        confirm_url = url_for('confirm_email', token=token, _external=True)
        entity_type = 'user'
        send_confirmation_email(user.email, confirm_url, entity_type)
        
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        entity_type, email = serial.loads(token, salt='email-confirm', max_age=3600)
        if entity_type == 'user':
            user = User.query.filter_by(email=email).first()
            if user:
                user.email_confirmed = True
                db.session.commit()
                flash('Your email has been confirmed successfully! Now you can login.', 'success')
                return redirect(url_for('login'))
        elif entity_type == 'doctor':
            doctor = Doctor.query.filter_by(email=email).first()
            if doctor:
                doctor.email_confirmed = True
                db.session.commit()
                flash('Your email has been confirmed successfully! Now you can login.', 'success')
                return redirect(url_for('login_doctor'))
        flash('Invalid token or user/doctor not found.', 'danger')
        return redirect(url_for('register'))
    except SignatureExpired:
        flash('The confirmation link has expired. Please register again.', 'danger')
        return redirect(url_for('register_doc'))
    except:
        flash('The confirmation link is invalid.', 'danger')
        return redirect(url_for('register'))



@app.route('/account/register_doctor', methods=['GET', 'POST'])
def register_doc():
    if current_user.is_authenticated:
        return redirect(url_for('appointment'))
    form = DoctorRegistration()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        # Handle the upload of qualifications file (document)
        qualifications_filename = docs.save(form.qualifications.data)
        qualifications_url = url_for('uploaded_document', filename=qualifications_filename)
        
        # Handle the upload of picture file (image)
        picture_filename = photos.save(form.picture.data)
        picture_url = url_for('uploaded_photo', filename=picture_filename)

        # Convert start_time and end_time to datetime objects
        start_time_str = form.start_time.data.strip()
        end_time_str = form.end_time.data.strip()

        # Define a regex pattern to match the time format
        time_pattern = re.compile(r'^\d{1,2}:\d{2} [AP]M$')

        if not time_pattern.match(start_time_str) or not time_pattern.match(end_time_str):
            flash('Invalid time format. Please use HH:MM AM/PM format.', 'error')
            return redirect(url_for('register_doc'))

        start_time = datetime.strptime(start_time_str, '%I:%M %p').time()
        end_time = datetime.strptime(end_time_str, '%I:%M %p').time()

        # Define a common date for start and end times
        common_date = date.today()
        
        selected_days = ",".join(form.availability.data)
        
        doctor = Doctor(
            name=form.name.data,
            phone=form.phone.data,
            email=form.email.data,
            department=form.department.data,
            lincense=form.license.data,
            fee=form.fee.data,
            availability=selected_days,
            start_time=datetime.combine(common_date, start_time),
            end_time=datetime.combine(common_date, end_time),
            qualifications=qualifications_url,
            picture=picture_url,
            password=hashed_password
        )
        db.session.add(doctor)
        db.session.commit()
        flash(f"Welcome Dr.{doctor.name}, your account has been registered successfully,\
            and a confirmation link has been sent to your email, please confirm your email to proceed to login",
            'success')
        
        token = serial.dumps(('doctor', doctor.email), salt='email-confirm')
        confirm = url_for('confirm_email', token=token, _external=True)
        entity_type = 'doctor'
        send_confirmation_email(doctor.email, confirm, entity_type)
        
        return redirect(url_for('login_doctor'))
    
    return render_template('register_doctor.html', form=form)

@app.route('/uploads/photos/<filename>')
def uploaded_photo(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

@app.route('/uploads/documents/<filename>')
def uploaded_document(filename):
    return send_from_directory(app.config['UPLOADED_DOCUMENTS_DEST'], filename)

@app.route('/account/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/patient-doctor-appointment', methods=['GET', 'POST'])
@login_required
def patient_doc_appointment():
    form = AppointmentForm()
    
    if not (isinstance(current_user, User) and not current_user.is_admin):
        return redirect(url_for('not_found'))
    
    
    if form.validate_on_submit():
        doctor_id = form.doctor.data
        appointment_time = form.appointment_time.data
        appointment_date = form.appointment_date.data
        
        # No need to combine appointment_date and appointment_time here
        # appointment_datetime = datetime.combine(appointment_date, appointment_time)
        
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            flash('Invalid doctor selected!', 'error')
            return redirect(url_for('patient_doc_appointment'))
        
        # Check if appointment date falls within doctor's available days
        if appointment_date.strftime('%A').lower() not in doctor.availability.split(','):
            flash('Doctor is not available on the selected date', 'warning')
            return redirect(url_for('patient_doc_appointment'))

        # Check if appointment time falls within doctor's available hours
        if not doctor.is_doctor_available(appointment_time):
            flash('Doctor is not available at the selected time', 'warning')
            return redirect(url_for('patient_doc_appointment'))
        
        user_id = current_user.id
        # Check for existing appointments at the selected date and time
        existing_appointment = Appointment.query.filter_by(doctor_id=doctor_id, appointment_date=appointment_date, appointment_time=appointment_time).first()
        if existing_appointment:
            flash('Appointment time is already booked', 'warning')
            return redirect(url_for('patient_doc_appointment'))
        
        # Create the appointment without setting appointment_datetime directly
        appointment = Appointment(
            doctor_id=doctor_id,
            user_id=user_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            location=form.location.data,
            description=form.description.data
        )
        db.session.add(appointment)
        db.session.commit()
        
        send_patient_confirmation_email(current_user.email, doctor.name, appointment_date, appointment_time,
                                        form.location.data, form.description.data)

        # Send notification email to doctor
        send_doctor_notification_email(doctor.email, current_user.first_name + ' ' + current_user.last_name,
                                       appointment_date, appointment_time, form.location.data,
                                       form.description.data)


        flash('Appointment scheduled successfully', 'success')
        return redirect(url_for('my_appointments'))
        
    return render_template('appointment.html', form=form)


@app.route('/patient-doctor-appointment/cancel-appointment/<appointment_id>', methods=['GET', 'POST'])
@login_required
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment:
        if current_user == appointment.user:
            send_doctor_cancellation_email(appointment.doctor.email, appointment.user.first_name,
                                           appointment.appointment_date, appointment.appointment_time,
                                           appointment.location, appointment.description)
            flash('Appointment cancelled', 'success')
            appointment.status = True
            db.session.commit()
            return redirect(url_for('my_appointments'))
        elif current_user == appointment.doctor:
            send_patient_cancellation_email(appointment.user.email, appointment.doctor.name,
                                            appointment.appointment_date, appointment.appointment_time,
                                            appointment.location, appointment.description)
            flash('Appointment cancelled', 'success')
            appointment.status = True
            db.session.commit()
            return redirect(url_for('appointments'))
        
    flash('Appointment not found or unauthorized', 'error')
    return redirect(url_for('patient_doc_appointment'))


@app.route('/delete-appointment/<appointment_id>', methods=['GET', 'POST'])
@login_required
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment:
        db.session.delete(appointment)
        db.session.commit()
        flash("Appointment deleted successfully", 'success')
        return redirect(url_for('appointments'))
    else:
        flash("Appointment not found", 'danger')
        return redirect(url_for('appointments'))


@app.route('/dashboard/cancel-approval/<doc_id>', methods=['GET', 'POST'])
def cancel_approval(doc_id):
    doctor = Doctor.query.get_or_404(doc_id)
    if doctor:
        db.session.delete(doctor)
        db.session.commit()
        send_approval_cancellation_mail(doctor)
        flash('Approval cancelled succesfully', 'success')
        
        return redirect(url_for('dashboard'))
    flash('Doctor not found', 'warning')
    return redirect(url_for('dashboard'))


@app.route('/reschdule-appointment', methods=['GET', 'POST'])
@login_required
def reschedule():
    form = AppointmentForm()

    # Check if the user is a regular user and not an admin
    if not (isinstance(current_user, User) and not current_user.is_admin):
        return redirect(url_for('not_found'))

    if form.validate_on_submit():
        doctor_id = form.doctor.data
        appointment_time = form.appointment_time.data
        appointment_date = form.appointment_date.data

        # Retrieve the existing appointment if any
        existing_appointment = Appointment.query.filter_by(doctor_id=doctor_id,
                                                            appointment_date=appointment_date,
                                                            appointment_time=appointment_time).first()

        if existing_appointment:
            # Delete the existing appointment
            db.session.delete(existing_appointment)
            db.session.commit()

        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            flash('Invalid doctor selected!', 'error')
            return redirect(url_for('patient_doc_appointment'))

        # Check if appointment date falls within doctor's available days
        if appointment_date.strftime('%A').lower() not in doctor.availability.split(','):
            flash('Doctor is not available on the selected date', 'warning')
            return redirect(url_for('patient_doc_appointment'))

        # Check if appointment time falls within doctor's available hours
        if not doctor.is_doctor_available(appointment_time):
            flash('Doctor is not available at the selected time', 'warning')
            return redirect(url_for('patient_doc_appointment'))

        user_id = current_user.id

        # Create the new appointment
        appointment = Appointment(
            doctor_id=doctor_id,
            user_id=user_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            location=form.location.data,
            description=form.description.data
        )
        db.session.add(appointment)
        db.session.commit()

        # Send notification emails
        send_patient_confirmation_email(current_user.email, doctor.name, appointment_date, appointment_time,
                                        form.location.data, form.description.data)

        send_doctor_notification_email(doctor.email, current_user.first_name + ' ' + current_user.last_name,
                                       appointment_date, appointment_time, form.location.data,
                                       form.description.data)

        flash('Appointment rescheduled successfully', 'success')
        return redirect(url_for('my_appointments'))

    return render_template('reschedule.html', form=form)


@app.route('/dashboard/appointment-report', methods=['GET', 'POST'])
def report():
    appointments = Appointment.query.order_by(desc(Appointment.appointment_date)).all()
    count = len(appointments)
    return render_template('report.html',
                           appointments=appointments,
                           count=count)

def send_reminder_emails():
    # Calculate the date for the next day
    tomorrow = datetime.now() + timedelta(days=1)
    
    # Query for appointments scheduled for the next day
    appointments_tomorrow = Appointment.query.filter_by(appointment_date=tomorrow.date()).all()
    
    for appointment in appointments_tomorrow:
        send_reminder_email(appointment)
        
scheduler.add_job(send_reminder_emails, 'cron', day_of_week='mon-sun', hour=0, minute=0)  # Run daily at midnight
scheduler.start()


@app.route('/download_report')
def download_report():
    report_data = generate_report()
    return send_file(BytesIO(report_data), mimetype="text/csv", as_attachment=True, download_name='report.csv')
