import json
from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from flask_sqlalchemy import sqlalchemy
from .service import create_customer_account, get_all_accounts, delete_customer_account, get_all_account_status, withdraw_from_account, get_account_by_id, deposit_to_account
from .exceptions import InvalidAccountType, NoSuchAccount, AccountAlreadyExists, CustomerDoesNotExist, InsufficientBalance

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
        except CustomerDoesNotExist as customer_does_not_exist:
            flash(customer_does_not_exist.message, 'error')
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

    all_accounts = get_all_accounts()
    return render_template('delete_account.html', account_pair=all_accounts, account_pair_json=json.dumps(all_accounts))


@bp_account.route('/show', methods=['GET'])
def show_status():
    all_statuses = get_all_account_status()
    print(all_statuses)
    return render_template('account_status.html', all_statuses=all_statuses)


@bp_account.route('/withdraw/<account_id>', methods=['GET', 'POST'])
def withdraw(account_id):
    if request.method == 'POST':
        withdraw_amount = int(request.form.get('withdraw_amount', 0))
        try:
            withdraw_from_account(account_id, withdraw_amount)
            flash('Amount withdrawn successfully', 'success')
        except NoSuchAccount as no_such_account:
            flash(no_such_account.message, 'error')
        except InsufficientBalance as insufficient_balance:
            flash(insufficient_balance.message, 'error')
        except ValueError as value_error:
            flash(str(value_error), 'error')

    account_details = get_account_by_id(account_id)
    return render_template('withdraw_account.html', account_details=account_details)


@bp_account.route('/deposit/<account_id>', methods=['GET', 'POST'])
def deposit(account_id):
    if request.method == 'POST':
        deposit_amount = int(request.form.get('deposit_amount', 0))
        try:
            deposit_to_account(account_id, deposit_amount)
            flash('Amount deposited successfully', 'success')
        except NoSuchAccount as no_such_account:
            flash(no_such_account.message, 'error')
        except InsufficientBalance as insufficient_balance:
            flash(insufficient_balance.message, 'error')
        except ValueError as value_error:
            flash(str(value_error), 'error')

    account_details = get_account_by_id(account_id)
    return render_template('deposit_account.html', account_details=account_details)
