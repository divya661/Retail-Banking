from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from .service import login_user
from .exceptions import UserNotFound, InvalidPassword

bp_auth = Blueprint(
    'auth', __name__, template_folder='templates', static_folder='static'
)


@bp_auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', False)
        password = request.form.get('password', False)
        try:
            employee_id, username = login_user(username, password)
            session['employee_id'] = employee_id
            session['username'] = username
            return redirect(url_for('site_root'))
        except UserNotFound as user_not_found:
            flash('Invalid username or password', 'error')
        except InvalidPassword as invalid_password:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

