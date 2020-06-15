from app import db
from .models import Customer
from .exceptions import InvalidSSNId, CustomerDoesNotExist
from datetime import datetime

STATUS_ACTIVE = 'active'
STATUS_ARCHIVED = 'archived'

MESSAGES = {
    'CUST_CREATED': 'customer created successfully',
    'CUST_UPDATED': 'customer updated successfully',
    'CUST_DELETED': 'customer account deactivated',
    'CUST_REACTIVATE': 'customer account reactivated',
}


def create_customer(form):
    '''
    Creates a customer provided the flask form object
    '''
    customer_ssn_id = str(form['customer_ssn_id'])
    customer_name = form['customer_name']
    customer_age = form['customer_age']
    customer_address = form['customer_address']
    customer_state = form['customer_state']
    customer_city = form['customer_city']

    customer_exists = Customer.query.filter_by(
        customer_ssn_id=customer_ssn_id
    ).first()
    if customer_exists is not None:
        raise InvalidSSNId()

    customer = Customer(customer_ssn_id=customer_ssn_id, customer_name=customer_name, customer_age=customer_age,
                        customer_address=customer_address, customer_state=customer_state, customer_city=customer_city,
                        customer_status=STATUS_ACTIVE, customer_message=MESSAGES['CUST_CREATED'])

    db.session.add(customer)
    db.session.commit()
    db.session.flush()
    return customer


def get_all_customers():
    return Customer.query.filter_by().all()

def get_all_active_accounts():
    acc_mappings = {}
    for customer in Customer.query.filter_by(archived=False).all():
        acc_mappings[customer.customer_ssn_id] = {
            'customer_id': customer.customer_id,
            'customer_name': customer.customer_name,
            'customer_age': customer.customer_age,
            'customer_address': customer.customer_address,
            'customer_state': customer.customer_state,
            'customer_city': customer.customer_city,
        }

    return acc_mappings

def get_customer_by_id(customer_id):
    return Customer.query.filter_by(customer_id=customer_id).first()


def delete_customer(form):
    '''
      Delete a customer when the entered Customer Id, Customer SSN ID is entered.
      Get the details of customer name, age and address.
      Upon clicking delete button it deletes the customer from the database
    '''
   # if customer_id == False or customer_ssn_id == False or customer_name == False or customer_age == False or customer_address == False:
    #   raise ValueError('One of the required field is missing')
    customer_ssn_id = form.get('customer_ssn_id', '')
    customer_id = form.get('customer_id', '')

    customer_exists = Customer.query.filter_by(
        customer_ssn_id=customer_ssn_id,
        customer_id=customer_id,
    ).first()

    if customer_exists is None:
        raise CustomerDoesNotExist(customer_ssn_id, customer_id)

    customer_exists.customer_status = STATUS_ARCHIVED
    customer_exists.customer_message = MESSAGES['CUST_DELETED']
    customer_exists.archive_customer()

    db.session.commit()
    db.session.flush()
