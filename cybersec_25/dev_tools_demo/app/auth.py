from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import User

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful! Welcome, {}.'.format(user.username), 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'success')
    return redirect(url_for('main.index'))
