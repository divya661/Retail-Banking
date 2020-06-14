from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from .exceptions import InvalidSSNId
from .forms import CustomerForm
from .models import Customer
from .service import create_customer, get_all_customers, get_customer_by_id

bp_customer = Blueprint(
    'customer', __name__, template_folder='templates', static_folder='static'
)


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
