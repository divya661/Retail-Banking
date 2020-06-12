from .models import Employee
from .exceptions import UserNotFound, InvalidPassword


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
