import json
from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from flask_sqlalchemy import sqlalchemy
from .service import create_customer_account, get_all_accounts, delete_customer_account, get_all_account_status
from .exceptions import InvalidAccountType, NoSuchAccount, AccountAlreadyExists

bp_account = Blueprint(
    'account', __name__, template_folder='templates', static_folder='static'
)


@bp_account.route('/create', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        customer_id = request.form.get('customer_id', False)
        account_type = request.form.get('account_type', False)
        account_balance = request.form.get('account_balance', False)

        try:
            account = create_customer_account(
                customer_id, account_type, account_balance)
            flash('Account creation initiated successfully', 'success')
        except AccountAlreadyExists as account_already_exists:
            flash(account_already_exists.message, 'error')
        except InvalidAccountType as invalid_account_type:
            flash(invalid_account_type.message, 'error')
        except sqlalchemy.exc.IntegrityError as integrity_error:
            flash('Customer with ID {customer_id} does not exist'.format(
                customer_id=customer_id), 'error')
        except ValueError as value_error:
            flash(str(value_error), 'error')

    return render_template('create_account.html')


@bp_account.route('/delete', methods=['GET', 'POST'])
def delete_account():
    all_accounts = get_all_accounts()
    if request.method == 'POST':
        account_id = request.form.get('account_id', False)
        account_type = request.form.get('account_type', False)
        try:
            delete_customer_account(account_id, account_type)
            flash('Account deleted successfully', 'success')
        except NoSuchAccount as no_such_account:
            flash(no_such_account.message, 'error')
        except ValueError as value_error:
            flash(str(value_error), 'error')

    return render_template('delete_account.html', account_pair=all_accounts, account_pair_json=json.dumps(all_accounts))


@bp_account.route('/show', methods=['GET'])
def show_status():
    all_statuses = get_all_account_status()
    print(all_statuses)
    return render_template('account_status.html', all_statuses=all_statuses)