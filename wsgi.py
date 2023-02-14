from flask import Flask, request, render_template, flash, session, redirect, url_for
import backEnd
import database
import encrypt
from app import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home', methods=['POST'])
def login_request():
    user_id_num = request.form['user_id_num']
    user_first_name = request.form['user_first_name']
    user_last_name = request.form['user_last_name']
    user_password = str(request.form['user_password'])
    test, data = backEnd.sign_in(user_id_num, user_first_name, user_last_name, user_password)
    if test:
        session['user_first_name'] = data[0]
        session['user_last_name'] = data[1]
        session['user_password'] = data[2]
        session['balance'] = data[3]
        session['user_id_num'] = user_id_num
        if session['user_id_num'] == "1":
            return render_template('confirmCentralBank.html')
        else:
            return render_template('home.html', fName=session['user_first_name'], lName=session['user_last_name'],
                                   balance=f"{float(session['balance']):13,.2f}")
    else:
        flash("Invalid User, please try again!")
        return render_template('index.html')


@app.route('/transaction', methods=['POST'])
def home_page():
    transaction_type = request.form['tran_type']
    if transaction_type == "T":
        return render_template('trade.html', fName=session['user_first_name'], lName=session['user_last_name'],
                               balance=f"{float(session['balance']):13,.2f}")
    elif transaction_type == "V":
        return run_view_page()
    elif transaction_type == "A":
        return render_template('auditDocType.html')
    elif transaction_type == "D":
        return render_template('addFunds.html')


@app.route('/trade', methods=['POST'])
def trade_request():  # add flash saying the trade went through with details
    session['recip_id_num'] = request.form['recip_id_num']
    recip_first_name = request.form['recip_first_name']
    recip_last_name = request.form['recip_last_name']
    if backEnd.verify_recipient(session['recip_id_num'], recip_first_name, recip_last_name):
        return render_template('confirmTrade.html', balance=f"{float(session['balance']):13,.2f}")
    else:
        flash(f"No user found with the information {recip_id_num} {recip_first_name} {recip_last_name}")
        return render_template('trade.html', fName=session['user_first_name'], lName=session['user_last_name'],
                               balance=f"{float(session['balance']):13,.2f}")


@app.route('/sendTrade', methods=['POST', 'GET'])
def confirm_trade():
    try:
        amount = float(request.form['tradeAmount'])
    except (ValueError, TypeError):
        flash('Invalid input, please enter a number!')
        return render_template('confirmTrade.html')
    if amount <= float(session['balance']):
        backEnd.transaction(session['user_id_num'], amount, "Credit")
        backEnd.transaction(session['recip_id_num'], amount, "Debit")
        backEnd.log_transaction(session['user_id_num'], session['recip_id_num'], amount)
        test, data = backEnd.sign_in(session['user_id_num'], session['user_first_name'], session['user_last_name'],
                                     session['user_password'])
        session['balance'] = data[3]
        return redirect(url_for('go_home', fName=session['user_first_name'], lName=session['user_last_name'],
                                balance=f"{float(session['balance']):13,.2f}"))
    else:
        flash('The amount you entered was outside of your balance!')
        return render_template('confirmTrade.html')


@app.route('/exitView', methods=['POST'])
def exit_view():
    return render_template('home.html', fName=session['user_first_name'], lName=session['user_last_name'],
                           balance=f"{float(session['balance']):13,.2f}")


@app.route('/confirmCB', methods=['POST'])
def confirm_central_bank():
    user_key = request.form['key']
    previous_key = encrypt.decrypt_string(database.get_latest_key())
    if user_key == previous_key[0:8]:
        return render_template('centralBankHome.html')
    else:
        flash("Incorrect Key, please try again!")
        return render_template('confirmCentralBank.html')


@app.route('/centralTransaction', methods=['POST'])
def central_transaction():
    user_request = request.form['central_tran_type']
    if user_request == "Z":
        return render_template('createAccount.html')
    elif user_request == "A":
        return render_template('auditDocType.html')
    elif user_request == "V":
        return run_view_page()
    elif user_request == "D":
        return render_template('decryption.html')


@app.route('/docType', methods=['POST'])
def doc_type():  # rework - database.read_rows(doc_request) to a for loop - decrypting [1:] adding [0] then added
    doc_request = request.form['doc_type']
    data = ["Error"]
    display_data = []
    if doc_request == "account":
        data = database.read_rows('AccountChain')
    elif doc_request == "transaction":
        data = database.read_rows('TransactionChain')
    elif doc_request == "deposit":
        data = database.read_rows('DepositChain')
    elif doc_request == "key":
        data = [encrypt.decrypt_string(database.get_latest_key())]
        return render_template('showDecryption.html', output=data)
    for i in data:
        row_id = i[0]
        row_data = encrypt.decrypt_list(i[1:])
        display_data += [row_id] + row_data
    return render_template('showDecryption.html', output=display_data)


@app.route('/createAccount', methods=['POST'])
def create_account():
    new_user_first_name = request.form['new_user_first_name']
    new_user_last_name = request.form['new_user_last_name']
    new_user_password = request.form['new_user_password']
    new_user_confirm_password = request.form['new_user_confirm_password']
    if new_user_password == new_user_confirm_password:
        new_user_id_num = str(backEnd.add_account(new_user_first_name, new_user_last_name, new_user_password))
        message = f"Account Made for {new_user_first_name} {new_user_last_name}, ID number {new_user_id_num}"
        flash(message)
        return render_template('index.html')


@app.route('/addFunds', methods=['POST', 'GET'])
def add_funds():
    try:
        amount = float(request.form['accountAmount'])
    except (ValueError, TypeError):
        flash('Invalid input, please enter a number!')
        return render_template('addFunds.html')
    backEnd.transaction("1", amount, "Credit")
    backEnd.transaction(session['user_id_num'], amount, "Debit")
    backEnd.log_transaction("1", session['user_id_num'], amount)
    backEnd.log_deposit(session['user_id_num'], amount)
    account_info = database.get_account(session['user_id_num'])  # here
    session['balance'] = float(encrypt.decrypt_string(account_info[-1]))
    return redirect(url_for('go_home', fName=session['user_first_name'], lName=session['user_last_name'],
                            balance=session['balance']))


def run_view_page():
    list1, list2, list3, list4 = backEnd.view_transactions(int(session['user_id_num']))
    return render_template('view.html', fName=session['user_first_name'], lName=session['user_last_name'],
                           balance=f"{float(session['balance']):13,.2f}",
                           list1=list1[::-1], list2=list2[::-1], list3=list3[::-1], list4=list4[::-1])


@app.route('/auditDocType', methods=['POST'])
def audit_doc_type():
    audit_request = request.form['audit_doc_type']
    output = ""
    if audit_request == "balances":
        output = backEnd.audit_balances()
    elif audit_request == "transactions":
        output = backEnd.audit_transactions()
    return render_template('audit.html', output=output)


@app.route('/home_page', methods=['POST', 'GET'])
def go_home():
    # first_name = request.args.get('fName')
    # last_name = request.args.get('lName')
    # session['balance'] = request.args.get('balance')
    return render_template('home.html', fName=session['user_first_name'], lName=session['user_last_name'],
                           balance=session['balance'])


@app.route('/newUser', methods=['GET'])
def new_user_request():
    return render_template('createAccount.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
