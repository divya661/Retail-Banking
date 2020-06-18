import json
from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from .exceptions import InvalidSSNId, CustomerDoesNotExist
from .forms import CustomerForm
from .models import Customer
from .service import create_customer, get_all_customers, get_customer_by_id, delete_customer, get_all_active_accounts, get_all_active_inactive_accounts, edit_customer

bp_customer = Blueprint(
    'customer', __name__, template_folder='templates', static_folder='static'
)

@bp_customer.before_request
def authenticate():
    employee_id = session.get('employee_id', False)
    username = session.get('username', False)

    if employee_id == False or username == False:
        return redirect(url_for('auth.login'))

@bp_customer.route('/signup', methods=['POST', 'GET'])
def signup():
    form = CustomerForm()
    if request.method == 'POST':
        try:
            create_customer(request.form)
            flash("Customer successfully registered!", "success")
        except InvalidSSNId as invalid_ssn_id:
            flash("Customer already exists or invalid SSN ID", "error")
        return redirect(url_for("customer.signup"))
    return render_template("create_customer.html", title="Create Customer Account", form=form)


@bp_customer.route('/status')
def status():
    return render_template("customer_status.html", entries=get_all_customers())


@bp_customer.route('customer/status/<string:customer_id>', methods=['GET'])
def details(customer_id):
    return render_template("customer_details.html", detail=get_customer_by_id(customer_id))


@bp_customer.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        try:
            delete_customer(request.form)
            flash('Customer account deactivated successfully', 'success')
        except CustomerDoesNotExist as customer_does_not_exist:
            flash(customer_does_not_exist.message, 'error')

    customers_mappings = get_all_active_accounts()
    return render_template('delete_customer.html', customers=customers_mappings, json_customers=json.dumps(customers_mappings))

@bp_customer.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        try:
            edit_customer(request.form)
            flash('Customer account updated successfully', 'success')
        except CustomerDoesNotExist as customer_does_not_exist:
            flash(customer_does_not_exist.message, 'error')
    customers_mappings = get_all_active_inactive_accounts()
    return render_template('edit_customer.html', customers=customers_mappings, json_customers=json.dumps(customers_mappings))
