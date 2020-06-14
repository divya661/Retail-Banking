import random
import string
from datetime import datetime
from app import db


def random_nine_digit_id():
    charset = string.digits
    return ''.join(
        [
            random.choice(charset) for _ in range(9)
        ]
    )


class Customer(db.Model):
    __tablename__ = 'customer'

    customer_id = db.Column(
        db.String(20), primary_key=True, default=random_nine_digit_id
    )

    customer_ssn_id = db.Column(
        db.String(10),  nullable=False, unique=True
    )

    customer_name = db.Column(
        db.String(30), nullable=False
    )

    customer_age = db.Column(
        db.Integer(), nullable=False
    )

    customer_address = db.Column(
        db.String(500), nullable=False
    )

    customer_state = db.Column(
        db.String(30), nullable=False
    )

    customer_city = db.Column(
        db.String(30), nullable=False
    )

    customer_last_updated = db.Column(
        db.DateTime(), nullable=False
    )
    customer_status = db.Column(
        db.String(30), nullable=False
    )
    customer_message = db.Column(
        db.String(30), nullable=True
    )

    def __init__(self, customer_ssn_id, customer_name, customer_age, customer_address, customer_state, customer_city, customer_status, customer_message):
        self.customer_ssn_id = customer_ssn_id
        self.customer_name = customer_name
        self.customer_age = customer_age
        self.customer_address = customer_address
        self.customer_state = customer_state
        self.customer_city = customer_city
        self.customer_status = customer_status
        self.customer_message = customer_message
        self.update_timestamp()

    def update_timestamp(self):
        self.customer_last_updated = datetime.utcnow()

    def __repr__(self):
        return "Customer('{cust_ssn}','{cust_name}','{cust_age}','{cust_addr}','{cust_state}','{cust_city}')".format(cust_ssn=self.customer_ssn_id, cust_name=self.customer_name, cust_age=self.customer_age, cust_addr=self.customer_address, cust_state=self.customer_state, cust_city=self.customer_city)
