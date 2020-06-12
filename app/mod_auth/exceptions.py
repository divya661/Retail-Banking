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