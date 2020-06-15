class InvalidAccountType(Exception):
    '''
    Thrown when account type is not savings or current
    '''

    def __init__(self, input_account_type):
        self.input_account_type = input_account_type
        self.message = 'Invalid account type: {account_type}'.format(
            self.input_account_type
        )
        super().__init__(self.message)


class NoSuchAccount(Exception):
    '''
    Thrown when no such account exists
    '''

    def __init__(self, account_id, account_type):
        self.account_id = account_id
        self.account_type = account_type
        if self.account_type is not None:
            self.message = 'Account with ID {account_id} and type {account_type} does not exist'.format(
                account_id=self.account_id, account_type=self.account_type)
        else:
            self.message = 'Account with ID {account_id} does not exist'.format(
                account_id=self.account_id)
        super().__init__(self.message)


class AccountAlreadyExists(Exception):
    '''
    Raised when account of same type already exists
    '''

    def __init__(self, account_id, account_type):
        self.account_id = account_id
        self.account_type = account_type
        self.message = 'Account {account_id} of type {account_type} already exists'.format(
            account_id=account_id, account_type=account_type)
        super().__init__(self.message)


class CustomerDoesNotExist(Exception):
    '''
    Exception raised when customer with provided ssn id and id does not exist
    '''

    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.message = 'customer with ID {id} does not exist'.format(
            id=self.customer_id)
        super().__init__(self.message)


class InsufficientBalance(Exception):
    '''
    Exception raised when there is insufficient balance in specified acc
    '''

    def __init__(self, account_id):
        self.message = 'Insufficient balance in account {account_id}'.format(
            account_id=account_id)
        super().__init__(self.message)
