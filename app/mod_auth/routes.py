from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from .service import login_user, signup_user
from .exceptions import UserNotFound, InvalidPassword, UserAlreadyExists, PasswordDoNotMatch

bp_auth = Blueprint(
    'auth', __name__, template_folder='templates', static_folder='static'
)

def already_logged_in():
    if 'employee_id' in session and 'username' in session:
        return True
    return False

@bp_auth.route('/', methods=['GET', 'POST'])
def login():
    if already_logged_in():
        return redirect(url_for('site_root'))
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
        except ValueError as value_error:
            flash(value_error.message, 'error')
    return render_template('login.html')

@bp_auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if already_logged_in():
        return redirect(url_for('site_root'))
    if request.method == 'POST':
        username = request.form.get('username', False)
        password = request.form.get('password', False)
        confirm_password = request.form.get('confirmPassword', False)
        try:
            employee_id, username = signup_user(username, password, confirm_password)
            session['employee_id'] = employee_id
            session['username'] = username
            return redirect(url_for('site_root'))
        except UserAlreadyExists as user_already_exists:
            flash(user_already_exists.message, 'error')
        except PasswordDoNotMatch as password_do_not_match:
            flash(password_do_not_match.message, 'error')
        except ValueError as value_error:
            flash(value_error.message, 'error')
    return render_template('signup.html')

@bp_auth.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('site_root'))
