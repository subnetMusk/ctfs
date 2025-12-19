from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
from .models import User
from . import db

bp = Blueprint('main', __name__)

def login_required(view_func):
    def wrapped(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login'))
        return view_func(*args, **kwargs)
    wrapped.__name__ = view_func.__name__
    return wrapped

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=session.get('username'))

@bp.route('/api/ping')
def api_ping():
    return jsonify({'ok': True, 'message': 'pong', 'user': session.get('username')})

@bp.route('/api/demo-data')
def api_demo_data():
    return jsonify({'items': [1, 2, 3], 'info': 'network-demo', 'user': session.get('username')})

@bp.route('/api/get-pref')
@login_required
def get_pref():
    user = User.query.get(session.get('user_id'))
    return jsonify({'favoriteColor': user.favorite_color if user else None})

@bp.route('/api/save-pref', methods=['POST'])
@login_required
def save_pref():
    data = request.get_json(silent=True) or {}
    fav = (data.get('favoriteColor') or '').strip() or None
    user = User.query.get(session.get('user_id'))
    if user:
        user.favorite_color = fav
        db.session.commit()
    return jsonify({'saved': True, 'data': {'favoriteColor': fav}})
