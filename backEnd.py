import encrypt
import hashlib
import datetime
import database

money_supply = 1000000000000.0


def audit_transactions():
    transactions = database.read_rows('TransactionChain')
    audited_transactions = []
    for i in range(len(transactions)-1):
        previous_trans = list(transactions[i])
        previous_trans_id = str(previous_trans[0])
        previous_trans_data = encrypt.decrypt_list(previous_trans[1:])
        previous_trans = [previous_trans_id] + previous_trans_data
        next_trans = list(transactions[i+1])
        next_trans_id = str(next_trans[0])
        next_trans_data = encrypt.decrypt_list(next_trans[1:])
        next_trans = [next_trans_id] + next_trans_data
        hash_from_data = hashlib.sha256(f"{previous_trans[1]} {previous_trans[2]} {previous_trans[3]} "
                                        f"{previous_trans[4]} {previous_trans[5]} {previous_trans[7]}"
                                        .encode('utf-8')).hexdigest()
        if hash_from_data == previous_trans[6] and hash_from_data == next_trans[7]:
            audited_transactions += [f"Valid {previous_trans[0]} {hash_from_data[2:9]} {next_trans[7][2:9]}"]
        else:
            audited_transactions = [f"Invalid {previous_trans[0]} {hash_from_data[2:9]} {next_trans[7][2:9]}"]
            break
    return audited_transactions


def audit_balances():
    accounts = sorted(database.get_user_ids())
    audited_balances = []
    population_balance = 0.0
    for account in accounts:
        test_balance = float(encrypt.decrypt_string(database.get_account(account)[-1]))
        chain_balance = float(balance_through_chain(account))
        if account == 1:
            total_deposits = database.get_total_deposits()
            taken_from_system = (chain_balance * -1)
            true_balance = test_balance + taken_from_system
            if true_balance == float(money_supply) and total_deposits == taken_from_system:
                audited_balances += [
                    f"All money is accounted for, True money in circulation = {taken_from_system:13,.2f}, deposits = "
                    f"{total_deposits:13,.2f}."]
            elif true_balance >= float(money_supply):
                audited_balances += [f"Money seems to have entered the system"]
            else:
                audited_balances += [f"Money seems to have left the system"]
        elif test_balance == chain_balance:
            audited_balances += [
                f"Checks out! Balance: ${test_balance:13,.2f}   Chain Balance: ${chain_balance:13,.2f}"]
            population_balance += chain_balance
        else:
            audited_balances += [
                f"Doesn't check out! Balance: ${test_balance:13,.2f}   Chain Balance: ${chain_balance:13,.2f}"]
    return audited_balances


def balance_through_chain(account_num):
    data = database.get_transactions(encrypt.encrypt_string(account_num))
    chain_balance = 0.0
    for transactions in data:
        transaction_data = encrypt.decrypt_list(transactions[1:])
        if transaction_data[1] == str(account_num):
            chain_balance += float(transaction_data[2])
        elif transaction_data[0] == str(account_num):
            chain_balance -= float(transaction_data[2])
    return chain_balance


def sign_in(account_num, account_f_name, account_l_name, account_password):
    account_info = list(database.get_account(int(account_num)))[1:]
    account_info = encrypt.decrypt_list(account_info)
    if account_info[0] == account_f_name and account_info[1] == account_l_name and account_info[2] == account_password:
        date, time = get_time()
        session_data = [None, account_num, date, time]
        database.add_row('SessionChain', session_data)
        return True, account_info
    else:
        return False, None


def verify_recipient(recipient_num, recipient_f_name, recipient_l_name):
    account_info = list(database.get_account(int(recipient_num)))[1:3]
    account_info = encrypt.decrypt_list(account_info)
    if account_info[0] == recipient_f_name and account_info[1] == recipient_l_name:
        return True
    else:
        return False


def transaction(account_num, amount, transaction_type):
    account_info = database.get_account(int(account_num))
    balance = float(encrypt.decrypt_string(account_info[4]))
    if transaction_type == "Debit":
        balance += float(amount)
    elif transaction_type == "Credit":
        balance -= float(amount)
    balance = encrypt.encrypt_string(balance)
    database.change_balance(account_num, balance)


def view_transactions(account_num):
    transactions = database.get_transactions(encrypt.encrypt_string(account_num))
    dates, times, other_accounts, amounts = [], [], [], []
    for i in transactions:
        i = encrypt.decrypt_list(i[1:])
        dates += [str(i[3])]
        times += [i[4].split('.')[0]]
        if i[0] == str(account_num):
            other_accounts += [i[1]]
            amounts += [f"-{float(i[2]):13,.2f}"]
        else:
            other_accounts += [i[0]]
            amounts += [f"+{float(i[2]):13,.2f}"]
    return dates, times, other_accounts, amounts


def add_account(first_name, last_name, password):
    encrypted_list = encrypt.encrypt_list([first_name, last_name, password, '0.0'])
    data = [None] + encrypted_list
    number = database.add_row('AccountChain', data)
    return number


def log_transaction(sender_id, recipient_id, amount):
    previous_hash = encrypt.decrypt_string(database.get_latest_key())
    date, time = get_time()
    string = f"{str(sender_id)} {str(recipient_id)} {str(amount)} {str(date)} {str(time)} {previous_hash}"
    new_hash = hashlib.sha256(string.encode('utf-8')).hexdigest()
    encrypted_list = encrypt.encrypt_list([sender_id, recipient_id, amount, date, time, new_hash, previous_hash])
    new_transaction = [None] + encrypted_list
    database.add_row('TransactionChain', new_transaction)


def log_deposit(account_num, amount):
    date, time = get_time()
    string = f"{str(account_num)} {str(amount)} {str(date)} {str(time)}"
    deposit_hash = hashlib.sha256(string.encode('utf-8')).hexdigest()
    encrypted_list = encrypt.encrypt_list([account_num, amount, date, time, deposit_hash])
    new_deposit = [None] + encrypted_list
    database.add_row('DepositChain', new_deposit)


def get_time():
    date_time = str(datetime.datetime.now()).split(" ")
    date = date_time[0]
    time = date_time[1]
    return date, time
