key = {"\n": "\n", "0": "~", " ": " ", "1": "`", "2": "!", "3": "@", "4": "#", "5": "$", "6": "%", "7": "^", "8": "&",
       "9": "*", ".": "(", "#": ")", "$": "-", "a": "_", "b": "=", "c": "+", "d": "A", "e": "B", "f": "C", "g": "D",
       "h": "E", "i": "F", "j": "G", "k": "H", "l": "I", "m": "J", "n": "K", "o": "L", "p": "M", "q": "N", "r": "O",
       "s": "P", "t": "Q", "u": "R", "v": "S", "w": "T", "x": "U", "y": "V", "z": "W", "A": "X", "B": "Y", "C": "Z",
       "D": "a", "E": "b", "F": "c", "G": "d", "H": "e", "I": "f", "J": "g", "K": "h", "L": "i", "M": "j", "N": "k",
       "O": "l", "P": "m", "Q": "n", "R": "o", "S": "p", "T": "q", "U": "r", "V": "s", "W": "t", "X": "u", "Y": "v",
       "Z": "w", "=": ";", "-": "}", ":": "{", "<": "<"}

dkey = {"w": "Z", "v": "Y", "u": "X", "t": "W", "s": "V", "r": "U", "q": "T", "p": "S", "o": "R", "n": "Q", "m": "P",
        "l": "O", "k": "N", "j": "M", "i": "L", "h": "K", "g": "J", "f": "I", "e": "H", "d": "G", "c": "F", "b": "E",
        "a": "D", "Z": "C", "Y": "B", "X": "A", "W": "z", "V": "y", "U": "x", "T": "w", "S": "v", "R": "u", "Q": "t",
        "P": "s", "O": "r", "N": "q", "M": "p", "L": "o", "K": "n", "J": "m", "I": "l", "H": "k", "G": "j", "F": "i",
        "E": "h", "D": "g", "C": "f", "B": "e", "A": "d", "+": "c", "=": "b", "_": "a", "-": "$", ")": "#", "(": ".",
        "*": "9", "&": "8", "^": "7", "%": "6", "$": "5", "#": "4", "@": "3", "!": "2", "`": "1", "~": "0", " ": " ",
        ";": "=", "}": "-", "{": ":", "\n": "\n", "<": "<"}


def decrypt_file(file_name):
    file = open(file_name, 'r')
    lines = file.read().split("\n")
    accounts = {}
    for i in lines:
        i = i.split(",")
        i = decrypt_list(i)
        if len(i) == 1:
            pass
        else:
            accounts[str(i[0])] = i[1:]
    return accounts


def encrypt_list(decrypted_list):
    encrypted_list = []
    for word in decrypted_list:
        encrypted_list += [encrypt_string(word)]
    return encrypted_list


def decrypt_list(encrypted_list):
    decrypted_list = []
    for word in encrypted_list:
        decrypted_list += [decrypt_string(word)]
    return decrypted_list


def encrypt_string(string):
    decrypted_string = ""
    for letter in str(string):
        decrypted_string += key.get(letter)
    return decrypted_string


def decrypt_string(string):
    encrypted_string = ""
    for letter in str(string):
        encrypted_string += dkey.get(letter)
    return encrypted_string
