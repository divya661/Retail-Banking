import random
import string
from random import randint

from app import db


def generate_customer_id():
    '''
    Generates a 9 digit customer id
    '''
    range_start = 10**(10-1)
    range_end = 10**10-1
    return randint(range_start,range_end)


class Customer(db.Model):
    __tablename__ = 'customer'


    customer_ssn_id = db.Column(
        db.BigInteger(),  nullable=False, primary_key=True
    )
    customer_name = db.Column(
        db.String(30), nullable=False
    )
    customer_age = db.Column(
        db.BigInteger(), nullable=False
    )
    customer_address =  db.Column(
        db.String(500), nullable=False
    )
    customer_state = db.Column(
        db.String(30), nullable=False
    )
    customer_city = db.Column(
        db.String(30), nullable=False
    )

    def __init__(self, customer_ssn_id, customer_name, customer_age, customer_address, customer_state, customer_city):
        self.customer_ssn_id = customer_ssn_id
        self.customer_name = customer_name
        self.customer_age = customer_age
        self.customer_address = customer_address
        self.customer_state = customer_state
        self.customer_city = customer_city


  #  def __repr__(self):
   #     return '<%d %d %s %d %s %s %s>'%(customer_id = self.customer_id, customer_ssn_id = self.customer_ssn_id, customer_name = self.customer_name, customer_age = self.customer_age, customer_address = self.customer_address, customer_state = self.customer_state, customer_city = self.customer_city )

    def __repr__(self):
        return f"Customer('{self.customer_ssn_id}','{self.customer_name}','{self.customer_age}','{self.customer_address}','{self.customer_state}','{self.customer_city}')"
