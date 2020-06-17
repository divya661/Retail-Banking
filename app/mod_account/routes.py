import json
from flask import Blueprint, render_template, request, flash, session, url_for, redirect, Response
from flask_sqlalchemy import sqlalchemy
from .service import create_customer_account, get_all_accounts, delete_customer_account, get_all_account_status, withdraw_from_account, get_account_by_id, deposit_to_account, transfer_from_account, get_account_balance_pair, get_transactions, get_date_transactions, search_accounts, get_statement_detail_of_account
from .exceptions import InvalidAccountType, NoSuchAccount, AccountAlreadyExists, CustomerDoesNotExist, InsufficientBalance
import os, xlwt, io, sys
from fpdf import FPDF

bp_account = Blueprint(
    'account', __name__, template_folder='templates', static_folder='static'
)


@bp_account.route('/create', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        customer_id = request.form.get('customer_id', False)
        account_type = request.form.get('account_type', False)
        account_balance = request.form.get('account_balance', False)

        try:
            account = create_customer_account(
                customer_id, account_type, account_balance)
            flash('Account creation initiated successfully', 'success')
        except CustomerDoesNotExist as customer_does_not_exist:
            flash(customer_does_not_exist.message, 'error')
        except AccountAlreadyExists as account_already_exists:
            flash(account_already_exists.message, 'error')
        except InvalidAccountType as invalid_account_type:
            flash(invalid_account_type.message, 'error')
        except sqlalchemy.exc.IntegrityError as integrity_error:
            flash('Customer with ID {customer_id} does not exist'.format(
                customer_id=customer_id), 'error')
        except ValueError as value_error:
            flash(str(value_error), 'error')

    return render_template('create_account.html')


@bp_account.route('/delete', methods=['GET', 'POST'])
def delete_account():
    if request.method == 'POST':
        account_id = request.form.get('account_id', False)
        account_type = request.form.get('account_type', False)
        try:
            delete_customer_account(account_id, account_type)
            flash('Account deleted successfully', 'success')
        except NoSuchAccount as no_such_account:
            flash(no_such_account.message, 'error')
        except ValueError as value_error:
            flash(str(value_error), 'error')

    all_accounts = get_all_accounts()
    return render_template('delete_account.html', account_pair=all_accounts, account_pair_json=json.dumps(all_accounts))


@bp_account.route('/show', methods=['GET'])
def show_status():
    all_statuses = get_all_account_status()
    print(all_statuses)
    return render_template('account_status.html', all_statuses=all_statuses)


@bp_account.route('/withdraw/<account_id>', methods=['GET', 'POST'])
def withdraw(account_id):
    if request.method == 'POST':
        withdraw_amount = int(request.form.get('withdraw_amount', 0))
        try:
            withdraw_from_account(account_id, withdraw_amount)
            flash('Amount withdrawn successfully', 'success')
        except NoSuchAccount as no_such_account:
            flash(no_such_account.message, 'error')
        except InsufficientBalance as insufficient_balance:
            flash(insufficient_balance.message, 'error')
        except ValueError as value_error:
            flash(str(value_error), 'error')

    account_details = get_account_by_id(account_id)
    return render_template('withdraw_account.html', account_details=account_details)


@bp_account.route('/deposit/<account_id>', methods=['GET', 'POST'])
def deposit(account_id):
    if request.method == 'POST':
        deposit_amount = int(request.form.get('deposit_amount', 0))
        try:
            deposit_to_account(account_id, deposit_amount)
            flash('Amount deposited successfully', 'success')
        except NoSuchAccount as no_such_account:
            flash(no_such_account.message, 'error')
        except ValueError as value_error:
            flash(str(value_error), 'error')

    account_details = get_account_by_id(account_id)
    return render_template('deposit_account.html', account_details=account_details)


@bp_account.route('/transfer/<account_id>', methods=['GET', 'POST'])
def transfer(account_id):
    if request.method == 'POST':
        dest_account = request.form.get('dest_account')
        transfer_amount = int(request.form.get('transfer_amount', 0))
        try:
            transfer_from_account(account_id, dest_account, transfer_amount)
            flash('Amount transferred successfully', 'success')
        except NoSuchAccount as no_such_account:
            flash(no_such_account.message, 'error')
        except InsufficientBalance as insufficient_balance:
            flash(insufficient_balance.message, 'error')
        except ValueError as value_error:
            flash(str(value_error), 'error')

    account_balance_pairs = get_account_balance_pair()
    return render_template('transfer_account.html', source_account=account_id, account_balance_pairs=account_balance_pairs, account_balance_pairs_json=json.dumps(account_balance_pairs))


@bp_account.route('/statement/ntrans/<acc_id>', methods=['GET'])
def statement_ntrans(acc_id):
    ntrans = int(request.args.get('ntrans', 4))
    page = int(request.args.get('page', 0))

    if page < 0:
        page = 0

    transactions = get_transactions(acc_id, ntrans, page)
    return render_template('statement_ntrans.html', ntrans=ntrans, page=page, acc_id=acc_id, transactions=transactions)

@bp_account.route('/statement/dates/<acc_id>', methods=['GET'])
def statement_dates(acc_id):
    ntrans = int(request.args.get('ntrans', 4))
    page = int(request.args.get('page', 0))
    start = request.args.get('start', None)
    end = request.args.get('end', None)
    transactions = None

    if page < 0:
        page = 0

    if start is not None and end is not None:
        transactions = get_date_transactions(acc_id, start, end, ntrans, page)

    return render_template('statement_dates.html', ntrans=ntrans, page=page, acc_id=acc_id, transactions=transactions, start=start, end=end)



@bp_account.route('/statement', methods=['GET', 'POSt'])
def statement():
    if request.method == 'POST':
        account_id = request.form['account_id']
        show = request.form['show']
        number_transactions = request.form['number_transactions']

        if show == 'last_n_trans':
            redirect_to = '/account/statement/ntrans/{acc_id}?ntrans={trans}'.format(
                acc_id=account_id, trans=number_transactions)
        else:
            redirect_to = '/account/statement/dates/{acc_id}?ntrans={trans}'.format(
                acc_id=account_id, trans=number_transactions)

        return redirect(redirect_to)

    account_balance_pairs = get_account_balance_pair()
    return render_template('account_statement.html', accounts=account_balance_pairs.keys())


@bp_account.route('/details', methods=['GET', 'POST'])
def account_details():
    if request.method == 'POST':
        search = request.form.get('search', None)
        search_type = request.form.get('type', None)
        try:
            accounts = search_accounts(search, search_type)
            return render_template('account_details.html', accounts=accounts)
        except ValueError as value_error:
            flash(str(value_error), 'error')

    return render_template('account_details.html')


@bp_account.route('/statement/ntrans/download/report/pdf/<string:acc_id>/<int:ntrans>/<int:page>')
def download_report_as_pdf(acc_id,ntrans,page):
    try:
        transactions = get_transactions(acc_id, ntrans, page)

        pdf = FPDF()
        pdf.add_page()

        page_width = pdf.w - 2 * pdf.l_margin

        pdf.set_font('Times', 'B', 20.0)
        pdf.cell(page_width, 0.0, 'Account Statement', align='C')
        pdf.ln(10)

        pdf.set_font('Courier', '', 12)

        col_width = page_width / 4
        pdf.ln(1)
        th = pdf.font_size

        pdf.cell(col_width+2,th,'Transaction Id',border=1)
        pdf.cell(col_width+2,th,'Transaction Type',border=1)
        pdf.cell(col_width+2,th,'Date',border=1)
        pdf.cell(col_width+2,th,'Amount',border=1)

        for row in transactions:
            pdf.ln(4.5)
            pdf.cell(col_width + 2, th, row.transaction_id, border=1)
            pdf.cell(col_width + 2, th, row.transaction_type, border=1)
            pdf.cell(col_width + 2, th, str(row.date), border=1)
            pdf.cell(col_width + 2, th, str(row.amount), border=1)
        pdf.ln(10)

        pdf.set_font('Times', '', 10.0)
        pdf.cell(page_width, 0.0, '- end of report -', align='C')


        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',
                        headers={'Content-Disposition': 'attachment;filename=account-statement.pdf'})
    except Exception as e:
        print(e)
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',
                        headers={'Content-Disposition': 'attachment;filename=account-statement.pdf'})

@bp_account.route('/statement/date/download/report/pdf/<string:acc_id>/<int:ntrans>/<start>/<end>/<int:page>')
def download_report_as_pdf_by_date(acc_id,ntrans,start,end,page):
    try:
        transactions = get_date_transactions(acc_id,start, end, ntrans, page)

        pdf = FPDF()
        pdf.add_page()

        page_width = pdf.w - 2 * pdf.l_margin

        pdf.set_font('Times', 'B', 20.0)
        pdf.cell(page_width, 0.0, 'Account Statement', align='C')
        pdf.ln(10)

        pdf.set_font('Courier', '', 12)

        col_width = page_width / 4
        pdf.ln(1)
        th = pdf.font_size

        pdf.cell(col_width+2,th,'Transaction Id',border=1)
        pdf.cell(col_width+2,th,'Transaction Type',border=1)
        pdf.cell(col_width+2,th,'Date',border=1)
        pdf.cell(col_width+2,th,'Amount',border=1)

        for row in transactions:
            pdf.ln(4.5)
            pdf.cell(col_width + 2, th, row.transaction_id, border=1)
            pdf.cell(col_width + 2, th, row.transaction_type, border=1)
            pdf.cell(col_width + 2, th, str(row.date), border=1)
            pdf.cell(col_width + 2, th, str(row.amount), border=1)
        pdf.ln(10)

        pdf.set_font('Times', '', 10.0)
        pdf.cell(page_width, 0.0, '- end of report -', align='C')


        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',
                        headers={'Content-Disposition': 'attachment;filename=account-statement.pdf'})
    except Exception as e:
        print(e)
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',
                        headers={'Content-Disposition': 'attachment;filename=account-statement.pdf'})


@bp_account.route('/statement/ntrans/download/report/excel/<string:acc_id>/<int:ntrans>/<int:page>')
def download_report_as_excel(acc_id,ntrans,page):
    try:
        transactions = get_transactions(acc_id, ntrans, page)


        # output in bytes
        output = io.BytesIO()
        # create WorkBook object
        workbook = xlwt.Workbook()
        # add a sheet
        sh = workbook.add_sheet('Account Statement Report')

        # add headers
        sh.write(0, 0, 'Transaction Id')
        sh.write(0, 1, 'Transaction Type')
        sh.write(0, 2, 'Date')
        sh.write(0, 3, 'Amount')

        idx = 1
        for row in transactions:
            sh.write(idx, 0, str(row.transaction_id))
            sh.write(idx, 1, str(row.transaction_type))
            sh.write(idx, 2, str(row.date))
            sh.write(idx, 3, str(row.amount))
            idx +=1


        workbook.save(output)
        output.seek(0)

        return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition": "attachment;filename=account_statement.xls"})
    except Exception as e:
        print(e)
    return Response(output, mimetype="application/ms-excel",
                    headers={"Content-Disposition": "attachment;filename=account_statement.xls"})


@bp_account.route('/statement/date/download/report/excel/<string:acc_id>/<int:ntrans>/<start>/<end>/<int:page>')
def download_report_as_excel_by_date(acc_id,ntrans,start,end,page):
    try:
        transactions = get_date_transactions(acc_id,start, end, ntrans, page)
        # output in bytes
        output = io.BytesIO()
        # create WorkBook object
        workbook = xlwt.Workbook()
        # add a sheet
        sh = workbook.add_sheet('Account Statement Report')

        # add headers
        sh.write(0, 0, 'Transaction Id')
        sh.write(0, 1, 'Transaction Type')
        sh.write(0, 2, 'Date')
        sh.write(0, 3, 'Amount')

        idx = 1
        for row in transactions:
            sh.write(idx, 0, str(row.transaction_id))
            sh.write(idx, 1, str(row.transaction_type))
            sh.write(idx, 2, str(row.date))
            sh.write(idx, 3, str(row.amount))
            idx +=1


        workbook.save(output)
        output.seek(0)

        return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition": "attachment;filename=account_statement.xls"})
    except Exception as e:
        print(e)
    return Response(output, mimetype="application/ms-excel",
                    headers={"Content-Disposition": "attachment;filename=account_statement.xls"})

