from app import db
from .models import Customer
from .exceptions import InvalidSSNId, InvalidCustomerId, InvalidName, InvalidAge, InvalidAddress


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
   # db.session.flush()


def delete_customer(form):
    '''
      Delete a customer when the entered Customer Id, Customer SSN ID is entered.
      Get the details of customer name, age and address.
      Upon clicking delete button it deletes the customer from the database
    '''
   # if customer_id == False or customer_ssn_id == False or customer_name == False or customer_age == False or customer_address == False:
     #   raise ValueError('One of the required field is missing')
    customer_ssn_id = form['customer_ssn_id']
    customer_id = form['customer_id']
    customer_name = form['customer_name']
    customer_age = form['customer_age']
    customer_address = form['customer_address']


    customer_ssn_id_exists = Customer.query.filter_by(
        customer_ssn_id=customer_ssn_id
    ).first()


    customer_id_exists = Customer.query.filter_by(
        customer_id=customer_id
    ).first()


    customer_name_exists = Customer.query.filter_by(
        customer_name=customer_name
    ).first()

    customer_age_exists = Customer.query.filter_by(
        customer_age=int(customer_age)
    ).first()

    customer_address_exists = Customer.query.filter_by(
        customer_address=customer_address
    ).first()

    if customer_ssn_id_exists is None:
        raise InvalidSSNId()

    if customer_id_exists is None:
        raise InvalidCustomerId()

    if customer_name_exists is None:
        raise InvalidName()

    if customer_age_exists is None:
        raise InvalidAge()

    if customer_address_exists is None:
        raise InvalidAddress()

    customer = Customer.query.filter_by(customer_id=customer_id).first()

    db.session.delete(customer)
    db.session.commit()





