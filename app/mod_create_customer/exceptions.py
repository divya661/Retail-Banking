

class Invalid_SSN_Id(Exception):
    '''
    Exception raised when the password is invalid
    '''

    def __init__(self):
        super().__init__('Invalid SSN ID. Either in use or less than 9 digits')

