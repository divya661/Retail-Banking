from app import db
from app.mod_customer import Customer
from .models import Account, AccountStatus, Transaction
from .exceptions import NoSuchAccount, AccountAlreadyExists, CustomerDoesNotExist, InsufficientBalance
import sys

STATUS_PENDING = 'pending'
STATUS_ACTIVE = 'active'
STATUS_DELETED = 'deleted'

MESSAGES = {
    'ACC_CREATION_COMPLETE': 'Account creation complete',
    'ACC_ALREADY_EXISTS': 'Customer already has account of specified type',
    'ACC_DELETED': 'Account deleted',
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


def get_account_by_id(account_id):
    return Account.query.filter_by(
        account_id=account_id).first()


def withdraw_from_account(account_id, amount):
    if amount < 0:
        raise ValueError('Withdraw amount cannot be less than zero')

    account_exists = Account.query.filter_by(
        account_id=account_id).first()

    if account_exists is None:
        raise NoSuchAccount(account_id, None)

    if account_exists.account_balance < amount:
        raise InsufficientBalance(account_id)

    account_exists.account_balance -= amount
    transaction = Transaction(account_id, 'withdraw', amount)

    db.session.add(transaction)
    db.session.commit()
    db.session.flush()

    update_account_status(account_id, account_exists.customer_id,
                          account_exists.account_type, STATUS_ACTIVE, 'Amount withdrawn successfully')


def deposit_to_account(account_id, amount):
    if amount < 0:
        raise ValueError('Deposit amount cannot be less than zero')

    account_exists = Account.query.filter_by(
        account_id=account_id).first()

    if account_exists is None:
        raise NoSuchAccount(account_id, None)

    account_exists.account_balance += amount
    transaction = Transaction(account_id, 'deposit', amount)

    db.session.add(transaction)
    db.session.commit()
    db.session.flush()

    update_account_status(account_id, account_exists.customer_id,
                          account_exists.account_type, STATUS_ACTIVE, 'Amount deposited successfully')


def get_account_balance_pair():
    accounts = db.session.query(Account).all()
    pairs = {}
    for account in accounts:
        pairs[account.account_id] = account.account_balance
    return pairs


def transfer_from_account(from_account_id, to_account_id, amount):
    if amount < 0:
        raise ValueError('Deposit amount cannot be less than zero')
    if from_account_id == to_account_id:
        raise ValueError('Cannot transer money to self')

    from_account = Account.query.filter_by(
        account_id=from_account_id
    ).first()
    to_account = Account.query.filter_by(
        account_id=to_account_id
    ).first()

    if from_account is None:
        raise NoSuchAccount(from_account_id, None)
    if to_account is None:
        raise NoSuchAccount(to_account_id, None)

    if amount > from_account.account_balance:
        raise InsufficientBalance(from_account_id)

    from_account.account_balance -= amount
    to_account.account_balance += amount

    transaction_from = Transaction(from_account_id, 'transfer', amount)
    transaction_to = Transaction(to_account_id, 'transfer', amount)

    db.session.add(transaction_from)
    db.session.add(transaction_to)
    db.session.commit()
    db.session.flush()

    update_account_status(from_account_id, from_account.customer_id,
                          from_account.account_type, STATUS_ACTIVE, 'Amount transferred successfully')

    update_account_status(to_account_id, to_account.customer_id,
                          to_account.account_type, STATUS_ACTIVE, 'Amount received successfully')


def get_transactions(acc_id, ntrans, page):
    query = Transaction.query.filter_by(account_id=acc_id).order_by(
        Transaction.date.desc()).limit(ntrans).offset(page * ntrans)

    return query



def get_date_transactions(acc_id, start, end, ntrans, page):
    query = Transaction.query.filter_by(account_id=acc_id).filter(Transaction.date.between(start, end)).order_by(
        Transaction.date.desc()).limit(ntrans).offset(page * ntrans)
    print(query[0])
    return query


def search_by_account_id(account_id):
    if account_id is None or account_id == '':
        raise ValueError('Account ID can not be None')

    return [get_account_by_id(account_id)]


def search_by_customer_id(customer_id):
    if customer_id is None or customer_id == '':
        raise ValueError('Customer ID cannot be None')

    return Account.query.filter_by(
        customer_id=customer_id)


def search_by_ssn_id(ssn_id):
    if ssn_id is None or ssn_id == '':
        raise ValueError('SSN ID cannot be None')

    customer = Customer.query.filter_by(customer_ssn_id=ssn_id).first()
    return search_by_customer_id(customer.customer_id)


def search_all_accounts(param):
    return db.session.query(Account).all()


def search_accounts(search, search_type):
    search_types = {
        'account_id': search_by_account_id,
        'customer_id': search_by_customer_id,
        'ssn_id': search_by_ssn_id,
        'all': search_all_accounts,
    }

    return search_types[search_type](search)

def get_statement_detail_of_account(account_id,start_date,end_date):
    transaction = Transaction.query.filter(Transaction.date.between(start_date,end_date), Transaction.account_id==account_id ).all()
    transaction_obj = []
    for trans in transaction:
        trans_obj = {"transaction_id":trans.transaction_id,"transaction_type":trans.transaction_type,"date":trans.date,"amount":trans.amount}
        transaction_obj.append(trans_obj)

    print(transaction_obj)
    return transaction_obj
