from app import db
from .models import Employee
from .exceptions import UserNotFound, InvalidPassword, UserAlreadyExists, PasswordDoNotMatch


def login_user(username, password):
    '''
    Verifies username and password

    Parameters:
        username: string or False
        password: string or False

    returns:
        employee_id: string
        username: string
    '''
    if username == False or password == False:
        raise ValueError('Username or password not provided')

    employee = Employee.query.filter_by(username=username).first()

    if employee is None:
        raise UserNotFound(username, 'Username not found')

    if employee.check_password(password) is False:
        raise InvalidPassword

    return employee.employee_id, employee.username


def signup_user(username, password, confirm_password):
    '''
    Verifies username, password and confirm_password
    and creates a new employee account

    Parameters:
        username: string or False
        password: string or False
        confirm_password: string or False

    returns:
        employee_id: string
        username: string
    '''

    if username == False or password == False or confirm_password == False:
        raise ValueError('One of the required field is missing')
    if password != confirm_password:
        raise PasswordDoNotMatch()

    employee_exists = Employee.query.filter_by(username=username).first()

    if employee_exists is not None:
        raise UserAlreadyExists(username)

    new_employee = Employee(username, password)
    db.session.add(new_employee)
    db.session.commit()
    db.session.flush()

    return new_employee.employee_id, new_employee.username
    
