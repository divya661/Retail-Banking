class InvalidSSNId(Exception):
    '''
    Exception raised when the SSN ID is invalid
    '''

    def __init__(self):
        self.message = 'Invalid SSN ID. Either in use or less than 9 digits'
        super().__init__(self.message)


class CustomerDoesNotExist(Exception):
    '''
    Exception raised when customer with provided ssn id and id does not exist
    '''

    def __init__(self, customer_ssn_id, customer_id):
        self.customer_ssn_id = customer_ssn_id
        self.customer_id = customer_id
        self.message = 'customer with SSN ID {ssn} and ID {id} does not exist'.format(ssn=self.customer_ssn_id, id=self.customer_id)
        super().__init__(self.message)