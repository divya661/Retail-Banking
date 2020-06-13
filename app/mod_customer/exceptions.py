class InvalidSSNId(Exception):
    '''
    Exception raised when the SSN ID is invalid
    '''

    def __init__(self):
        self.message = 'Invalid SSN ID. Either in use or less than 9 digits'
        super().__init__(self.message)
