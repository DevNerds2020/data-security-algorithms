from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def aes_encryption(data):
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    nonce = cipher.nonce
    return key, cipher, ciphertext, tag, nonce

def aes_decryption(key, nonce, ciphertext, tag):
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    return data


userinput = input()
data = bytes(userinput, 'utf-8')

key, cipher, ciphertext, tag, nonce = aes_encryption(data)

print("key =>", key)
print("cipher =>", cipher)
print("ciphertext (encrypted data) =>", ciphertext)
print("tag =>", tag)
print("nonce =>", nonce)

originaldata = aes_decryption(key, nonce, ciphertext, tag)
print("original_data =>", originaldata)
