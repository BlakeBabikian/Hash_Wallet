import encrypt
import encrypt
import hashlib
import datetime


money_supply = 1000000000000


def load_account(account_num):
    accounts = encrypt.decrypt_file('chain.csv')
    account = accounts.get(account_num)
    return account


def load_transactions(account_num):
    transactions = encrypt.decrypt_file('TransactionChain.csv')
    account_transactions = []
    for link in transactions.values():
        if link[0] == account_num or link[1] == account_num:
            account_transactions += [link]
    return account_transactions


def audit_transactions():
    transactions = encrypt.decrypt_file('TransactionChain.csv')
    audited_transactions = []
    keys = list(transactions.keys())
    for i in range(len(keys)-1):
        previous_trans = transactions.get(keys[i])
        next_trans = transactions.get(keys[i+1])
        hash_from_data = hashlib.sha256(f"{previous_trans[0]} {previous_trans[1]} {previous_trans[2]} "
                                        f"{previous_trans[3]} {previous_trans[4]} {previous_trans[6]}"
                                        .encode('utf-8')).hexdigest()
        if hash_from_data == previous_trans[5] and hash_from_data == next_trans[6]:
            audited_transactions += [f"Valid {hash_from_data[5:9]} {next_trans[6][5:9]}"]
        else:
            audited_transactions += [f"Invalid {hash_from_data[5:9]} {next_trans[6][5:9]}"]
    return audited_transactions


def audit_balances():
    accounts = encrypt.decrypt_file('chain.csv')
    audited_balances = []
    population_balance = 0.0
    for account_id, account in accounts.items():
        test_balance = float(account[-1])
        chain_balance = float(balance_through_chain(account_id))
        if account_id == "0":
            taken_from_system = (chain_balance * -1)
            true_balance = test_balance + taken_from_system
            if true_balance == float(money_supply):
                audited_balances += [f"All money is accounted for, True money in circulation = {chain_balance * -1:13,.2f}"]
            elif true_balance >= float(money_supply):
                audited_balances += [f"Money seems to have entered the system"]
            else:
                audited_balances += [f"Money seems to have left the system"]
        elif test_balance == chain_balance:
            audited_balances += [f"Checks out! Balance: ${test_balance:13,.2f}   Chain Balance: ${chain_balance:13,.2f}"]
            population_balance += chain_balance
        else:
            audited_balances += [f"Doesn't check out! Balance: ${test_balance:13,.2f}   Chain Balance: ${chain_balance:13,.2f}"]
    return audited_balances


def balance_through_chain(account_num):
    transactions = encrypt.decrypt_file('TransactionChain.csv')
    chain_balance = 0.0
    for link in transactions.values():
        if link[1] == str(account_num):
            chain_balance += float(link[2])
        elif link[0] == str(account_num):
            chain_balance -= float(link[2])
    return chain_balance


def sign_in(account_num, account_f_name, account_l_name, account_password):
    account_info = load_account(account_num)
    if account_info[0] == account_f_name and account_info[1] == account_l_name and account_info[2] == account_password:
        return True, account_info
    else:
        return False, None


def verify_recipient(recipient_num, recipient_f_name, recipient_l_name):
    account_info = load_account(recipient_num)
    if account_info[0] == recipient_f_name and account_info[1] == recipient_l_name:
        return True
    else:
        return False


def transaction(account_num, amount, transaction_type):
    account_info = load_account(account_num)
    balance = float(account_info[3])
    if transaction_type == "Debit":
        balance += float(amount)
    elif transaction_type == "Credit":
        balance -= float(amount)
    account_info[3] = str(balance)
    update_balance(account_info, account_num)


def view_transactions(account_num):
    transactions = load_transactions(account_num)
    dates, times, other_accounts, amounts = [], [], [], []
    for i in transactions:
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
    accounts = encrypt.decrypt_file('chain.csv')
    number = str(len(accounts))
    chain = open('chain.csv', 'a')
    encrypted_list = encrypt.encrypt_list([number, first_name, last_name, password, '0.0'])
    chain.write(f'{encrypted_list[0]},{encrypted_list[1]},{encrypted_list[2]},{encrypted_list[3]},{encrypted_list[4]}\n') #here
    chain.close()
    return number


def log_transaction(sender_id, recipient_id, amount):
    read_key = open('key.txt', 'r')
    previous_key = encrypt.decrypt_string(read_key.read()) # here
    date_time = str(datetime.datetime.now()).split(" ")
    date = date_time[0]
    time = date_time[1]
    string = f"{str(sender_id)} {str(recipient_id)} {str(amount)} {str(date)} {str(time)} {previous_key}"
    new_key = hashlib.sha256(string.encode('utf-8')).hexdigest()
    transactions = encrypt.decrypt_file('TransactionChain.csv')
    number = str(len(transactions))
    transaction_writer = open('TransactionChain.csv', 'a')
    encrypted_list = encrypt.encrypt_list([number, sender_id, recipient_id, amount, date, time, new_key, previous_key])
    transaction_writer.write(f"{encrypted_list[0]},{encrypted_list[1]},{encrypted_list[2]},{encrypted_list[3]},"
                             f"{encrypted_list[4]},{encrypted_list[5]},{encrypted_list[6]},{encrypted_list[7]}\n") # here
    transaction_writer.close()
    write_key = open('key.txt', 'w')
    write_key.write(encrypt.encrypt_string(new_key)) # here
    write_key.close()


def update_balance(account_info, account_num):
    accounts = encrypt.decrypt_file('chain.csv')
    accounts[account_num] = [account_info[0], account_info[1], account_info[2], account_info[3]]
    write_account = open('chain.csv', 'w')
    for account_id, account in accounts.items():
        encrypted_list = encrypt.encrypt_list([account_id, account[0], account[1], account[2], account[3]])
        write_account.writelines(f"{encrypted_list[0]},{encrypted_list[1]},{encrypted_list[2]},{encrypted_list[3]},"
                                 f"{encrypted_list[4]}\n") # here


"""add_account("Blake","Babikian","4Amigos4")

transaction("0", "100.0", "Credit")
transaction("1", "100.0", "Debit")
log_transaction("0","1","100.0")"""


"""add_account("Jack","McDiarmid","444")

transaction("0", "50.0", "Credit")
transaction("2", "50.0", "Debit")
log_transaction("0","2","50.0")"""

"""add_account("Angie","Grabmeier","Volleyball")

transaction("0", "150.0", "Credit")
transaction("3", "150.0", "Debit")
log_transaction("0","3","150.0")"""

'''print(sign_in("1","Blake","Babikian","4Amigos4"))
print(sign_in("2","Jack","McDiarmid","444"))
print(audit_transactions())'''