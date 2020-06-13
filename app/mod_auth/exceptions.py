class UserNotFound(Exception):
    '''
    Exception raised when user is not found

    Attributes:
        username: username that is not found
    '''

    def __init__(self, username, message):
        self.username = username
        self.message = message
        super().__init__(self.message)


class InvalidPassword(Exception):
    '''
    Exception raised when the password is invalid
    '''

    def __init__(self):
        super().__init__('Invalid username or password')


class UserAlreadyExists(Exception):
    '''
    Exception raised when trying to sign up and a user with the same username already exists

    Attributes:
        username: username that already exists
    '''

    def __init__(self, username):
        self.message = 'A user with the username {username} already exists'.format(
            username=username)
        super().__init__(self.message)


class PasswordDoNotMatch(Exception):
    '''
    Exception raised when password and confirm password do not match
    '''

    def __init__(self):
        self.message = 'Password and confirm password do not match'
        super().__init__(self.message)
