# Authentication routes for user registration, login, and logout
# Flask, Flask-Login, Flask-Bcrypt, re

import re
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db, bcrypt
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from urllib.parse import urlparse

bp = Blueprint('auth', __name__)

def is_safe_url(target):
    if not target:
        return False
    ref_url = urlparse(request.host_url)
    test_url = urlparse(target)
    return test_url.scheme in ('', 'http', 'https') and ref_url.netloc == test_url.netloc

def validate_username(username):
    if not username or len(username) < 3 or len(username) > 30:
        return False, "Username must be 3-30 characters long."
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores."
    return True, None

def validate_password(password):
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, None

def validate_email(email):
    if not email or '@' not in email or '.' not in email:
        return False, "Please enter a valid email address."
    if len(email) > 120:
        return False, "Email address is too long."
    return True, None

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        valid, error = validate_username(username)
        if not valid:
            flash(error, 'danger')
            return redirect(url_for('auth.register'))
        
        valid, error = validate_email(email)
        if not valid:
            flash(error, 'danger')
            return redirect(url_for('auth.register'))
        
        valid, error = validate_password(password)
        if not valid:
            flash(error, 'danger')
            return redirect(url_for('auth.register'))
        
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        
        if existing_user:
            flash('Username already exists. Please choose another.', 'danger')
            return redirect(url_for('auth.register'))
        if existing_email:
            flash('Email already registered. Please login.', 'danger')
            return redirect(url_for('auth.login'))
            
        new_user = User(username=username, email=email, balance=1000)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html', title='Register')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
            
    return render_template('auth/login.html', title='Login')

@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
