from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from .exceptions import Invalid_SSN_Id
from .form import CustomerForm
from .models import Customer
from app import db

bp_customer = Blueprint(
    'customer', __name__, template_folder='templates', static_folder='static'
)


@bp_customer.route('/signup', methods=['POST','GET'])
def signup():
    if session.get('customer_id'):
        return redirect(url_for('site_root'))
    form = CustomerForm()
    if request.method == 'POST':
        customer_ssn_id = form.customer_ssn_id.data
        customer_name = form.customer_name.data
        customer_age = form.customer_age.data
        customer_address = form.customer_address.data
        customer_state = form.customer_state.data
        customer_city = form.customer_city.data

        customer = Customer(customer_ssn_id=customer_ssn_id, customer_name=customer_name, customer_age=customer_age,
                        customer_address=customer_address, customer_state=customer_state, customer_city=customer_city)
        db.session.add(customer)
        db.session.commit()
        flash("You are successfully registered!", "success")
        return redirect(url_for('auth.login'))
    return render_template("create_customer.html", title="Create Customer Account", form=form)

