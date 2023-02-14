import encrypt
import database

encrypted_key = database.get_latest_key()

print(f"The key is: {str(encrypt.decrypt_string(encrypted_key))[:8]}")