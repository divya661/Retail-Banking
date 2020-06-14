from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from .exceptions import InvalidSSNId, InvalidCustomerId, InvalidAddress, InvalidAge, InvalidName
from .forms import CustomerForm, DeleteForm
from .models import Customer
from .service import create_customer, delete_customer
from app import db

bp_customer = Blueprint(
    'customer', __name__, template_folder='templates', static_folder='static'
)


@bp_customer.route('/signup', methods=['POST','GET'])
def signup():
    form = CustomerForm()
    if form.validate_on_submit():
        try:
            customer = create_customer(request.form)
            flash("Customer successfully registered!", "success")
        except InvalidSSNId as invalid_ssn_id:
            flash(invalid_ssn_id.message, "error")
        except InvalidAge as invalid_age:
            flash(invalid_age.message, "error")

        return redirect(url_for("customer.signup"))

    return render_template("create_customer.html", title="Create Customer Account", form=form)

@bp_customer.route('/delete',methods=['POST','GET'])
def delete():
    form = DeleteForm()
    if form.validate_on_submit():

        try:
            delete_customer(request.form)
            flash("Customer deletion initiated successfully", "success")
        except InvalidCustomerId as invalid_customer_id:
            flash(invalid_customer_id.message, "error")
        except InvalidSSNId as invalid_ssn_id:
            flash(invalid_ssn_id.message, "error")
        except InvalidAge as invalid_age:
            flash(invalid_age.message, "error")
        except InvalidName as invalid_name:
            flash(invalid_name.message, "error")
        except InvalidAddress as invalid_address:
            flash(invalid_address.message, "error")
        return redirect(url_for("customer.delete"))
    return render_template("delete_customer.html", title="Delete Customer",form=form)