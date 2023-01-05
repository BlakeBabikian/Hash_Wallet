from Wallet import encrypt

file = open('key.txt', 'r')
encrypted_key = file.read()

print(f"The key is: {str(encrypt.decrypt_string(encrypted_key))[:8]}")