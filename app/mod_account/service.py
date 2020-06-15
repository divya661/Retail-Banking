from app import db
from app.mod_customer import Customer
from .models import Account, AccountStatus
from .exceptions import NoSuchAccount, AccountAlreadyExists, CustomerDoesNotExist

STATUS_PENDING = 'pending'
STATUS_ACTIVE = 'active'
STATUS_DELETED = 'deleted'

MESSAGES = {
    'ACC_CREATION_COMPLETE': '“Account creation initiated successfully',
    'ACC_ALREADY_EXISTS': 'Customer already has account of specified type',
    'ACC_DELETED': 'Account deletion initiated successfully',
}


def update_account_status(account_id, customer_id, account_type, status, message):
    status_exists = AccountStatus.query.filter_by(
        account_id=account_id,
        customer_id=customer_id,
    ).first()

    if status_exists is not None:
        if status is not None:
            status_exists.status = status
        status_exists.message = message
        status_exists.update_timestamp()
    else:
        if status is None:
            raise ValueError('Inconsistent database state! Status None for account ID {} and customer ID {}'.format(
                account_id, customer_id)
            )
        status = AccountStatus(account_id, customer_id,
                               account_type, status, message)
        db.session.add(status)

    db.session.commit()
    db.session.flush()


def create_customer_account(customer_id, account_type, account_balance):
    '''
    Service function to create an account
    '''
    message = MESSAGES['ACC_CREATION_COMPLETE']
    if customer_id == False or account_type == False or account_balance == False:
        raise ValueError('Value not provided for one of the required fields')

    customer_exists = Customer.query.filter_by(
        customer_id=customer_id,
        archived=False,
    ).first()

    if customer_exists is None:
        raise CustomerDoesNotExist(customer_id)

    account_exists = Account.query.filter_by(
        customer_id=customer_id,
        account_type=account_type,
    ).first()

    if account_exists is not None:
        # Account already exists
        # then update account status to reflect creation attempt
        # and raise an error
        message = MESSAGES['ACC_ALREADY_EXISTS']
        update_account_status(account_exists.account_id,
                              customer_id, account_exists.account_type, None, message)
        raise AccountAlreadyExists(
            account_exists.account_id, account_exists.account_type)
    else:
        # Account does not exist - create new one
        new_account = Account(customer_id, account_type, account_balance)
        db.session.add(new_account)

    db.session.commit()
    db.session.flush()

    if new_account:
        update_account_status(new_account.account_id,
                              customer_id, new_account.account_type, STATUS_PENDING, message)

    return new_account


def get_all_accounts():
    '''
    Returns all account and type pairs
    '''
    accounts = db.session.query(Account).all()
    account_id_type_pair = {}
    for account in accounts:
        account_id_type_pair[account.account_id] = account.account_type
    return account_id_type_pair


def delete_customer_account(account_id, account_type):
    '''
    Service function to delete a customers' account
    '''
    message = MESSAGES['ACC_DELETED']
    if account_id == False or account_type == False:
        raise ValueError('Value not provided for one of the required fields')

    account_exists = Account.query.filter_by(
        account_id=account_id, account_type=account_type).first()

    if account_exists is None:
        raise NoSuchAccount(account_id, account_type)

    update_account_status(
        account_exists.account_id,
        account_exists.customer_id,
        account_exists.account_type,
        STATUS_DELETED,
        message,
    )

    db.session.delete(account_exists)
    db.session.commit()
    db.session.flush()


def get_all_account_status():
    '''
    Returns all account statuses
    '''
    account_statuses = db.session.query(AccountStatus).all()
    status_array = []
    for status in account_statuses:
        status_array.append(
            (
                status.customer_id,
                status.account_id,
                status.account_type,
                status.status,
                status.message,
                status.last_updated.strftime("%Y-%M-%d %H:%M:%S")
            )
        )
    return status_array
