from cryptography.fernet import Fernet

key = b'x3cBd0n8proNaQlMjRADy6ZhVR46ulsxQg3TbuZ645s='
crypt = Fernet(key)

def encrypted(text):
    ciphertext = crypt.encrypt(text.encode())
    return str(ciphertext)[2:-1]

def decrypted(text):
    plaintext = crypt.decrypt(text.encode())
    return str(plaintext)[2:-1]