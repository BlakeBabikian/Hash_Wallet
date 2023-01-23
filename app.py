from flask import Flask, request, render_template, flash, session, redirect, url_for
import backEnd
import encrypt
import os

app = Flask(__name__)
app.secret_key = "BentleyBondBait"
port = int(os.environ.get('PORT', 5000))

global user_id_num, user_first_name, user_last_name, user_password, balance,\
    recip_id_num, recip_first_name, recip_last_name


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home', methods=['POST'])
def login_request():
    global user_id_num, user_first_name, user_last_name, user_password, balance
    user_id_num = request.form['user_id_num']
    user_first_name = request.form['user_first_name']
    user_last_name = request.form['user_last_name']
    user_password = str(request.form['user_password'])
    test, data = backEnd.sign_in(user_id_num, user_first_name, user_last_name, user_password)
    if test:
        user_first_name = data[0]
        user_last_name = data[1]
        balance = data[3]
        if user_id_num == "0":
            return render_template('confirmCentralBank.html')
        else:
            return render_template('home.html', fName=user_first_name, lName=user_last_name,
                                   balance=f"{float(balance):13,.2f}")
    else:
        flash("Invalid User, please try again!")
        return render_template('index.html')


@app.route('/transaction', methods=['POST'])
def home_page():
    global user_id_num, user_first_name, user_last_name, user_password, balance
    transaction_type = request.form['tran_type']
    if transaction_type == "T":
        return render_template('trade.html', fName=user_first_name, lName=user_last_name,
                               balance=f"{float(balance):13,.2f}")
    elif transaction_type == "V":
        return run_view_page()
    elif transaction_type == "A":
        return render_template('auditDocType.html')
    elif transaction_type == "D":
        return render_template('addFunds.html')


@app.route('/trade', methods=['POST'])
def trade_request():
    global recip_id_num, recip_first_name, recip_last_name
    recip_id_num = request.form['recip_id_num']
    recip_first_name = request.form['recip_first_name']
    recip_last_name = request.form['recip_last_name']
    if backEnd.verify_recipient(recip_id_num, recip_first_name, recip_last_name):
        return render_template('confirmTrade.html')
    else:
        flash(f"No user found with the information {recip_id_num} {recip_first_name} {recip_last_name}")
        return render_template('trade.html', fName=user_first_name, lName=user_last_name,
                               balance=f"{float(balance):13,.2f}")


@app.route('/sendTrade', methods=['POST', 'GET'])
def confirm_trade():
    global user_id_num, user_first_name, user_last_name, user_password, recip_id_num, balance
    try:
        amount = float(request.form['tradeAmount'])
    except (ValueError, TypeError):
        flash('Invalid input, please enter a number!')
        return render_template('confirmTrade.html')
    if amount <= float(balance):
        backEnd.transaction(user_id_num, amount, "Credit")
        backEnd.transaction(recip_id_num, amount, "Debit")
        backEnd.log_transaction(user_id_num, recip_id_num, amount)
        test, data = backEnd.sign_in(user_id_num, user_first_name, user_last_name, user_password)
        balance = data[3]
        return redirect(url_for('go_home', fName=user_first_name, lName=user_last_name,
                               balance=f"{float(balance):13,.2f}"))
    else:
        flash('The amount you entered was outside of your balance!')
        return render_template('confirmTrade.html')


@app.route('/exitView', methods=['POST'])
def exit_view():
    return render_template('home.html', fName=user_first_name, lName=user_last_name,
                           balance=f"{float(balance):13,.2f}")


@app.route('/confirmCB', methods=['POST'])
def confirm_central_bank():
    user_key = request.form['key']
    with open('key.txt', 'r', encoding='utf-8') as file:
        previous_key = encrypt.decrypt_string(file.read())
    file.close()
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
def doc_type():
    doc_request = request.form['doc_type']
    data = ["Error"]
    if doc_request == "account":
        data = encrypt.decrypt_file('AccountChain.csv')
    elif doc_request == "transaction":
        data = encrypt.decrypt_file('TransactionChain.csv')
    elif doc_request == "deposit":
        data = encrypt.decrypt_file('DepositChain.csv')
    elif doc_request == "key":
        with open('key.txt', 'r') as file:
            data = [encrypt.decrypt_string(file.read())]
        return render_template('showDecryption.html', output=data)
    data = [(key, value) for key, value in data.items()]
    return render_template('showDecryption.html', output=data)


@app.route('/createAccount', methods=['POST'])
def create_account():
    global recip_id_num
    new_f_name = request.form['new_user_first_name']
    new_l_name = request.form['new_user_last_name']
    new_password = request.form['new_user_password']
    new_confirm_password = request.form['new_user_confirm_password']
    if new_password == new_confirm_password:
        new_id_num = str(backEnd.add_account(new_f_name, new_l_name, new_password))
        recip_id_num = new_id_num
        message = f"Account Made for {new_f_name} {new_l_name}, ID number {new_id_num}"
        flash(message)
        return render_template('index.html')


@app.route('/addFunds', methods=['POST', 'GET'])
def add_funds():
    global user_id_num, user_first_name, user_last_name, balance
    try:
        amount = float(request.form['accountAmount'])
    except (ValueError, TypeError):
        flash('Invalid input, please enter a number!')
        return render_template('addFunds.html')
    backEnd.transaction("0", amount, "Credit")
    backEnd.transaction(user_id_num, amount, "Debit")
    backEnd.log_transaction("0", user_id_num, amount)
    backEnd.log_deposit(user_id_num, amount)
    account_info = backEnd.load_account(user_id_num)
    balance = float(account_info[-1])
    return redirect(url_for('go_home', fName=user_first_name, lName=user_last_name, balance=balance))


def run_view_page():
    global user_last_name, user_last_name
    list1, list2, list3, list4 = backEnd.view_transactions(user_id_num)
    return render_template('view.html', fName=user_first_name, lName=user_last_name,
                           balance=f"{float(balance):13,.2f}",
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
    first_name = request.args.get('fName')
    last_name = request.args.get('lName')
    user_balance = request.args.get('balance')
    return render_template('home.html', fName=first_name, lName=last_name, balance=user_balance)


@app.route('/newUser', methods=['GET'])
def new_user_request():
    return render_template('createAccount.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
