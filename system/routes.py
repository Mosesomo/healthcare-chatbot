from system import app
from flask import render_template, url_for, redirect


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