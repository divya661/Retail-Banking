import string
import random
from datetime import datetime
from app import db
from .exceptions import InvalidAccountType


def random_nine_digit_id():
    charset = string.digits
    return ''.join(
        [
            random.choice(charset) for _ in range(9)
        ]
    )


class Account(db.Model):
    __tablename__ = 'account'
    account_id = db.Column(
        db.String(20),
        primary_key=True,
        default=random_nine_digit_id,
    )
    customer_id = db.Column(
        db.String(20),
        db.ForeignKey('customer.customer_id'),
        nullable=False,
    )
    account_type = db.Column(
        db.String(20),
        nullable=False,
    )
    account_balance = db.Column(
        db.BigInteger,
        nullable=False,
    )

    def __init__(self, customer_id, account_type, account_balance):
        if account_type != 'savings' and account_type != 'current':
            raise InvalidAccountType(account_type)
        self.customer_id = customer_id
        self.account_type = account_type
        self.account_balance = int(account_balance)


class AccountStatus(db.Model):
    __tablename__ = 'account_status'

    account_id = db.Column(
        db.String(20),
        primary_key=True,
        nullable=False,
    )
    customer_id = db.Column(
        db.String(20),
        db.ForeignKey('customer.customer_id'),
        nullable=False,
    )
    account_type = db.Column(
        db.String(20),
        nullable=False,
    )
    status = db.Column(
        db.String(20),
        nullable=False
    )
    message = db.Column(
        db.String(123),
    )
    last_updated = db.Column(
        db.DateTime(),
        nullable=False,
    )

    def __init__(self, account_id, customer_id, account_type, status, message):
        self.account_id = account_id
        self.customer_id = customer_id
        self.account_type = account_type
        self.status = status
        self.message = message
        self.update_timestamp()

    def update_timestamp(self):
        self.last_updated = datetime.utcnow()


class Transaction(db.Model):
    __tablename__ = 'transaction'

    account_id = db.Column(
        db.String(20),
        db.ForeignKey('account.account_id'),
        nullable=False
    )
    transaction_id = db.Column(
        db.String(20),
        primary_key=True,
        default=random_nine_digit_id,
    )
    transaction_type = db.Column(
        db.String(20),
        nullable=False,
    )
    date = db.Column(
        db.DateTime(),
        nullable=False,
        default=datetime.utcnow,
    )
    amount = db.Column(
        db.BigInteger,
        nullable=False,
    )

    def __init__(self, account_id, transaction_type, amount):
        self.account_id = account_id
        self.transaction_type = transaction_type
        self.amount = amount
