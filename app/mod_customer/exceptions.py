class InvalidSSNId(Exception):
    '''
    Exception raised when the SSN ID is invalid
    '''

    def __init__(self):
        self.message = 'Invalid SSN ID. '
        super().__init__(self.message)

class InvalidCustomerId(Exception):
    '''
    Exception raised when customer ID entered is invalid
    '''
    def __init__(self):
        self.message = "Invalid Customer ID. Either the customer with this ID doesn't exist or it is less than 9 digits"
        super().__init__(self.message)


class InvalidAge(Exception):
    '''
    Exception raised when customer ID entered is invalid
    '''

    def __init__(self):
        self.message = "Invalid Age. It should be an interger value."
        super().__init__(self.message)

class InvalidAddress(Exception):
    '''
    Exception raised when customer ID entered is invalid
    '''

    def __init__(self):
        self.message = "Customer doesn't exists or invalid Address"
        super().__init__(self.message)

class InvalidName(Exception):
    '''
    Exception raised when customer ID entered is invalid
    '''

    def __init__(self):
        self.message = "Invalid Name"
        super().__init__(self.message)