from system import app, db, bcrypt, mail, serial
from system.form import LoginForm, RegistrationForm
from flask import flash, render_template, url_for, redirect
from system.model import User, Doctor
from flask_login import current_user, login_required, logout_user, login_user
from flask_mail import Message


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

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
    return render_template('testimonial.html')

@app.route('/404')
def not_found():
    return render_template('404.html')

@app.route('/account/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.email_confirmed:
            login_user(user)
            flash('Login successfull', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful, please check your email or password!', 'danger')
    
    return render_template('login.html', form=form)

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
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        
        flash(f"Welcome {user.first_name}, your account has been registered successfully,\
            and a confirmation link has been sent to your email, please confirm your email to proceed to login",
            'success')
        
        # send confirmation email
        token = serial.dumps(user.email, salt='email-confirm')
        confirm_url = url_for('confirm_email', token=token, _external=True)
        send_confirmation_email(user.email, confirm_url)
        
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

def send_confirmation_email(email, confirm_url):
    msg = Message('Confirm Your Email', sender='noreply@mosesomo.tech', recipients=[email])
    msg.body = f'Please click the following link to confirm your email: {confirm_url}'
    mail.send(msg)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = serial.loads(token, salt='email-confirm', max_age=3600)
        user = User.query.filter_by(email=email).first()
        if user:
            user.email_confirmed = True
            db.session.commit()
            flash('Your email has been confirmed successfully! Now you can login..', 'success')
        else:
            flash('Invalid token or user not found.', 'danger')
    except:
        flash('The confirmation link is invalid or expired.', 'danger')
        return redirect(url_for('register'))
    return redirect(url_for('login'))


@app.route('/account/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))