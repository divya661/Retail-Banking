from app import db
from .models import Customer
from .exceptions import InvalidSSNId


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
                        customer_address=customer_address, customer_state=customer_state, customer_city=customer_city)

    db.session.add(customer)
    db.session.commit()
    db.session.flush()
    return customer
