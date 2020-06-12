import random
import string
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


def generate_employee_id():
    '''
    Generates a six digit alpha numeric employee id
    '''
    charset = string.ascii_uppercase + \
        string.digits   # Alpha numeric charset - upper case letters and digits

    return ''.join([
        random.choice(charset) for _ in range(6)
    ])


class Employee(db.Model):
    __tablename__ = 'employee'

    employee_id = db.Column(
        db.String(10), primary_key=True, default=generate_employee_id
    )
    username = db.Column(
        db.String(20), unique=True, nullable=False
    )
    password = db.Column(
        db.String(128), nullable=False
    )

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def generate_password_hash(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '{employee_id} -> {username}'.format(employee_id=self.employee_id, username=self.username)
